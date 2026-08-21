# fintek-naig — CBDC ve Programlanabilir Ödemeler Ampirik Araştırma Projesi

Bu depo, **CBDC gelişim aşamalarını finansal kapsayıcılık, dijital ödeme, makroekonomik yapı ve yönetişim göstergeleriyle analiz eden** makalenin yeniden üretilebilir veri, kod ve analiz altyapısını içerir.

## Araştırma sorusu
Ülkelerde CBDC çalışmalarının daha ileri aşamaya ulaşması; finansal kapsayıcılık, dijital ödeme kullanımı, ekonomik gelişmişlik, dijital altyapı, finansal derinlik, makroekonomik istikrar ve yönetişim kalitesi ile ilişkili midir?

## Veri katmanları
- **BIS CBDC Projects Database — March 2024**: CBDC proje aşamaları. `data/raw/bis_cbdc_mar2024.csv`.
- **World Bank Global Findex Database 2025 — 2021 wave**: finansal kapsayıcılık ve dijital ödeme göstergeleri. `data/raw/findex_selected_2021.csv`.
- **World Development Indicators (WDI) — 2021**: GDP per capita PPP, internet kullanımı, özel sektöre kredi, enflasyon, kentleşme ve FDI kontrolleri. İlk çalıştırmada `data/raw/wdi_2021.csv` üretilir ve önbelleğe alınır.
- **Worldwide Governance Indicators (WGI), 2025 Revision — 2021 slice**: Voice & Accountability, Political Stability, Government Effectiveness, Regulatory Quality, Rule of Law ve Control of Corruption. İlk çalıştırmada `data/raw/wgi_2021.csv` üretilir ve önbelleğe alınır.

Resmî veri bağlantıları ve sürüm notları: `data/source_manifest.csv`.
Değişken tanımları: `data/documentation/phase2_variable_dictionary.csv`.

## Faz 1 analizleri
1. Veri doğrulama ve BIS + Findex birleştirme
2. Tanımlayıcı istatistikler ve korelasyonlar
3. Ordered Probit
4. Ordered Logit sağlamlık kontrolü
5. Binary Logistic Regression
6. Random Forest + repeated stratified cross-validation
7. Permutation feature importance
8. Makale grafikleri
9. Türkiye ampirik profili

## Faz 2 analizleri
10. WDI + WGI gerçek verilerinin indirilmesi ve yerel snapshot olarak saklanması
11. BIS + Findex + WDI + WGI genişletilmiş veri seti
12. İç içe ekonometrik modeller:
   - `M1_digital`: dijital finans + ülke ölçeği
   - `M2_macro`: M1 + ekonomik/dijital/makro kontroller
   - `M3_governance`: M2 + WGI bileşik yönetişim endeksi
13. Ordered Probit ve Ordered Logit
14. Binary Logit — HC3 sağlam standart hatalar
15. VIF çoklu doğrusal bağlantı kontrolü
16. Altı WGI boyutunun tek tek sağlamlık analizi
17. **XGBoost** — 5-fold × 3 tekrar çapraz doğrulama
18. **SHAP** — değişken önem ve yorumlanabilirlik
19. Otomatik makale sonuç özeti: `outputs/phase2_results_summary.md`

## Neden 2021?
Global Findex göstergeleri 2021 dalgasından geldiği için WDI ve WGI kontrolleri de 2021'e sabitlenmiştir. Böylece açıklayıcı değişkenler aynı referans yılından gelir. CBDC proje aşaması BIS March 2024 snapshot'ından alınır; bu nedenle çalışma kesitsel ve ilişkisel olarak yorumlanmalı, nedensellik iddiası yapılmamalıdır.

## WGI metodolojik notu
WGI için **2025 Revision** kullanılır. Bu sürüm tarihsel tahminleri yeni yöntemle 1996'ya kadar geriye dönük yeniden hesaplar. Ana modelde altı WGI boyutunun ortalamasından oluşturulan `wgi_governance_index_2021` kullanılır; yüksek korelasyon nedeniyle altı boyut aynı regresyona birlikte konulmaz. Boyutlar ayrıca tek tek sağlamlık testlerinde incelenir.

## Windows'ta ilk kurulum
Proje klasöründe:

```text
setup_windows.bat
```

Ardından bütün Faz 1 + Faz 2 analizlerini çalıştırmak için:

```text
run_all.bat
```

veya terminalden:

```bash
python run_all.py
```

### World Bank verilerini yeniden indirmek
İlk `run_all.py` çalıştırması WDI/WGI snapshot'larını otomatik indirir. Sonraki çalıştırmalarda yerel CSV'ler kullanılır. Verileri daha sonra güncellemek için:

```text
refresh_world_bank_data.bat
```

veya:

```bash
python analysis/08_fetch_wdi_wgi.py --force
```

## Klasör yapısı

```text
fintek-naig/
├── analysis/
│   ├── 00_validate_inputs.py
│   ├── 01_prepare_dataset.py
│   ├── ...
│   ├── 08_fetch_wdi_wgi.py
│   ├── 09_prepare_extended_dataset.py
│   ├── 10_extended_econometric.py
│   ├── 11_xgboost_shap.py
│   └── 12_results_summary.py
├── data/
│   ├── raw/                  # BIS, Findex ve indirilen WDI/WGI snapshot'ları
│   ├── processed/            # Faz 1 ve Faz 2 analize hazır veri setleri
│   └── documentation/        # Veri/değişken sözlükleri
├── outputs/
│   ├── tables/
│   ├── figures/
│   ├── phase2_results_summary.md
│   └── phase2_xgboost_summary.json
├── .github/workflows/
├── requirements.txt
├── run_all.py
├── setup_windows.bat
├── run_all.bat
└── refresh_world_bank_data.bat
```

## Beklenen Faz 2 çıktıları
- `data/raw/wdi_2021.csv`
- `data/raw/wgi_2021.csv`
- `data/processed/cbdc_extended_2021.csv`
- `outputs/tables/phase2_data_coverage.csv`
- `outputs/tables/phase2_ordered_models.csv`
- `outputs/tables/phase2_binary_logit_HC3.csv`
- `outputs/tables/phase2_model_fit.csv`
- `outputs/tables/phase2_vif.csv`
- `outputs/tables/phase2_wgi_dimension_robustness.csv`
- `outputs/tables/phase2_xgboost_cv_metrics.csv`
- `outputs/tables/phase2_xgboost_shap_importance.csv`
- `outputs/figures/phase2_xgboost_shap_importance.png`
- `outputs/phase2_results_summary.md`

## Yeniden üretilebilirlik
Faz 1 ham verileri depoda bulunur. Faz 2 WDI/WGI verileri ilk çalıştırmada resmî World Bank kaynaklarından indirilip yerel CSV snapshot'larına dönüştürülür; bundan sonra analizler önbellekten tekrar çalıştırılabilir. GitHub Actions aynı pipeline'ı çalıştırır ve Faz 2 veri/çıktılarını `phase2-reproducibility` artifact'ı olarak saklar.

## Kavramsal not
Makale, **programlanabilir para** ile **programlanabilir/koşullu ödeme** ayrımını korur. TCMB vaka kısmı, uluslararası ülke karşılaştırmalı ampirik analizden ayrı fakat tamamlayıcı bir bölüm olarak ele alınır.

## Public repository notu
Bu depo public olduğu için yayımlanmamış Word makale taslağı depoya dahil edilmez. Veri, kod ve yeniden üretilebilir analiz bileşenleri burada tutulur.
