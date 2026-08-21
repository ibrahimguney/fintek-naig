from __future__ import annotations

from functools import reduce
import argparse
import io
import time

import pandas as pd
import requests

from common import RAW

YEAR = 2021
API_BASE = "https://api.worldbank.org/v2/country/all/indicator"

WDI = {
    "NY.GDP.PCAP.PP.KD": "gdp_per_capita_ppp_2021",
    "IT.NET.USER.ZS": "internet_users_2021",
    "FS.AST.PRVT.GD.ZS": "domestic_credit_private_2021",
    "FP.CPI.TOTL.ZG": "inflation_2021",
    "SP.URB.TOTL.IN.ZS": "urban_population_2021",
    "BX.KLT.DINV.WD.GD.ZS": "fdi_net_inflows_2021",
}

WGI = {
    "VA.EST": "wgi_voice_accountability_2021",
    "PV.EST": "wgi_political_stability_2021",
    "GE.EST": "wgi_government_effectiveness_2021",
    "RQ.EST": "wgi_regulatory_quality_2021",
    "RL.EST": "wgi_rule_of_law_2021",
    "CC.EST": "wgi_control_corruption_2021",
}

WGI_SHEETS = {
    "va": "wgi_voice_accountability_2021",
    "pv": "wgi_political_stability_2021",
    "ge": "wgi_government_effectiveness_2021",
    "rq": "wgi_regulatory_quality_2021",
    "rl": "wgi_rule_of_law_2021",
    "cc": "wgi_control_corruption_2021",
}

WGI_XLSX_URL = (
    "https://www.worldbank.org/content/dam/sites/govindicators/doc/"
    "wgidataset_with_sourcedata-2025.xlsx"
)


def _request_json(indicator: str, source: int | None = None) -> list[dict]:
    params = {"date": YEAR, "format": "json", "per_page": 1000}
    if source is not None:
        params["source"] = source
    url = f"{API_BASE}/{indicator}"
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.get(url, params=params, timeout=45)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
                raise RuntimeError(f"Unexpected World Bank API response for {indicator}")
            return payload[1]
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"World Bank API failed for {indicator}: {last_error}")


def _indicator_frame(indicator: str, out_name: str, source: int | None = None) -> pd.DataFrame:
    rows = _request_json(indicator, source=source)
    out = []
    for row in rows:
        country = row.get("country") or {}
        iso2 = country.get("id")
        iso3 = row.get("countryiso3code")
        value = row.get("value")
        if not iso2 or len(str(iso2)) != 2:
            continue
        out.append({
            "ISO2": str(iso2).upper(),
            "ISO3": iso3,
            "country_wb": country.get("value"),
            out_name: value,
        })
    df = pd.DataFrame(out)
    if not df.empty:
        df[out_name] = pd.to_numeric(df[out_name], errors="coerce")
        df = df.drop_duplicates(subset=["ISO2"], keep="last")
    return df


def fetch_wdi() -> pd.DataFrame:
    frames = [_indicator_frame(code, name, source=2) for code, name in WDI.items()]
    base = frames[0]
    for frame in frames[1:]:
        base = base.merge(
            frame.drop(columns=[c for c in ["ISO3", "country_wb"] if c in frame.columns]),
            on="ISO2",
            how="outer",
        )
    base = base.sort_values("ISO2")
    base.to_csv(RAW / "wdi_2021.csv", index=False)
    return base


def fetch_wgi_api() -> pd.DataFrame:
    frames = [_indicator_frame(code, name, source=3) for code, name in WGI.items()]
    if any(frame.empty for frame in frames):
        raise RuntimeError("One or more WGI API series returned no rows")
    base = frames[0]
    for frame in frames[1:]:
        base = base.merge(
            frame.drop(columns=[c for c in ["ISO3", "country_wb"] if c in frame.columns]),
            on="ISO2",
            how="outer",
        )
    return base.sort_values("ISO2")


def _normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        pd.Index(df.columns)
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def fetch_wgi_excel() -> pd.DataFrame:
    response = requests.get(WGI_XLSX_URL, timeout=90)
    response.raise_for_status()
    xlsx_path = RAW / "wgidataset_with_sourcedata-2025.xlsx"
    xlsx_path.write_bytes(response.content)

    frames = []
    for sheet, out_name in WGI_SHEETS.items():
        d = pd.read_excel(io.BytesIO(response.content), sheet_name=sheet)
        d = _normalise_columns(d)
        required = {"economy_code", "year", "governance_estimate_approx_2_5_to_2_5"}
        missing = required.difference(d.columns)
        if missing:
            raise RuntimeError(f"WGI sheet {sheet} missing columns: {sorted(missing)}")
        d = d.loc[pd.to_numeric(d["year"], errors="coerce") == YEAR].copy()
        d = d.rename(columns={
            "economy_code": "ISO3",
            "economy_name": "country_wb",
            "governance_estimate_approx_2_5_to_2_5": out_name,
        })
        keep = [c for c in ["ISO3", "country_wb", out_name] if c in d.columns]
        frames.append(d[keep].drop_duplicates(subset=["ISO3"], keep="last"))

    wgi = reduce(lambda left, right: left.merge(right, on="ISO3", how="outer"), frames)

    countries = requests.get(
        "https://api.worldbank.org/v2/country",
        params={"format": "json", "per_page": 400},
        timeout=45,
    )
    countries.raise_for_status()
    country_rows = countries.json()[1]
    crosswalk = pd.DataFrame([
        {"ISO2": x.get("iso2Code"), "ISO3": x.get("id"), "region_id": (x.get("region") or {}).get("id")}
        for x in country_rows
    ])
    crosswalk = crosswalk[crosswalk["region_id"].astype(str).str.len() > 0]
    crosswalk = crosswalk.drop(columns="region_id").drop_duplicates("ISO3")
    wgi = crosswalk.merge(wgi, on="ISO3", how="inner")
    return wgi.sort_values("ISO2")


def fetch_wgi() -> pd.DataFrame:
    try:
        wgi = fetch_wgi_api()
        method = "World Bank Indicators API, source=3"
    except Exception as api_error:
        print(f"WGI API fallback activated: {api_error}")
        wgi = fetch_wgi_excel()
        method = "WGI 2025 revision Excel fallback"
    wgi.to_csv(RAW / "wgi_2021.csv", index=False)
    print(f"WGI source: {method}")
    return wgi


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch/cached 2021 WDI and WGI controls.")
    parser.add_argument("--force", action="store_true", help="Refresh cached snapshots from World Bank.")
    args = parser.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    wdi_path = RAW / "wdi_2021.csv"
    wgi_path = RAW / "wgi_2021.csv"
    if wdi_path.exists() and wgi_path.exists() and not args.force:
        print(f"Using cached WDI snapshot -> {wdi_path}")
        print(f"Using cached WGI snapshot -> {wgi_path}")
        return

    wdi = fetch_wdi()
    wgi = fetch_wgi()
    print(f"Saved WDI 2021 snapshot: {len(wdi)} rows -> {wdi_path}")
    print(f"Saved WGI 2021 snapshot: {len(wgi)} rows -> {wgi_path}")


if __name__ == "__main__":
    main()
