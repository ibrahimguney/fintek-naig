# fintek-naig — CBDC ve Programlanabilir Ödemeler Ampirik Araştırma Projesi

Bu depo, **CBDC gelişim aşamalarını finansal kapsayıcılık ve dijital ödeme göstergeleriyle analiz eden** makalenin yeniden üretilebilir veri, kod ve analiz çıktılarını birlikte tutar.

## Araştırma sorusu
Ülkelerde CBDC çalışmalarının daha ileri aşamaya ulaşması; finansal kapsayıcılık, dijital ödeme kullanımı ve ülke ölçeği ile ilişkili midir?

## Veri
- **BIS CBDC Projects Database — March 2024**: CBDC proje aşamaları. Analizde kullanılan `Database` sayfası GitHub-dostu CSV anlık görüntüsü olarak `data/raw/bis_cbdc_mar2024.csv` içinde tutulur.
- **World Bank Global Findex Database 2025 — 2021 wave**: finansal kapsayıcılık ve dijital ödeme göstergeleri. Çalışmada kullanılan değişkenler `data/raw/findex_selected_2021.csv` içindedir.
- `analysis/01_prepare_dataset.py`, iki ham veri dosyasını ISO2 kodu üzerinden birleştirerek `data/processed/cbdc_findex_merged_2021.csv` dosyasını üretir.

Resmî veri bağlantıları: `data/source_manifest.csv`.

## Analizler
1. Veri doğrulama ve yeniden birleştirme
2. Tanımlayıcı istatistikler ve korelasyonlar
3. Ordered Probit
4. Ordered Logit sağlamlık kontrolü
5. Binary Logistic Regression
6. Random Forest + repeated stratified cross-validation
7. Permutation feature importance
8. Makale grafikleri
9. Türkiye ampirik profili

## Windows'ta ilk kurulum
Proje klasöründe:

```text
setup_windows.bat
```

Ardından bütün analizleri çalıştırmak için:

```text
run_all.bat
```

veya terminalden:

```bash
python run_all.py
```

## Klasör yapısı

```text
fintek-naig/
├── analysis/                 # Tüm analiz Python kodları
├── data/
│   ├── raw/                  # BIS ve Findex kaynak veri anlık görüntüleri
│   ├── processed/            # Kodla üretilen birleşik analiz verisi
│   └── documentation/        # Veri sözlüğü
├── outputs/
│   ├── tables/               # Makale tabloları
│   └── figures/              # Kodla üretilen grafikler
├── notebooks/                # İleri EDA / SHAP / ek ML çalışmaları
├── .github/workflows/        # Yeniden üretilebilirlik testi
├── requirements.txt
├── run_all.py
├── setup_windows.bat
└── run_all.bat
```

## Yeniden üretilebilirlik
Ham araştırma verileri depoda bulunduğu için mevcut analizler internet bağlantısı olmadan yeniden üretilebilir. GitHub Actions da `python run_all.py` komutuyla aynı analizi otomatik olarak test eder.

## Kavramsal not
Makale, **programlanabilir para** ile **programlanabilir/koşullu ödeme** ayrımını korur. TCMB vaka kısmı, uluslararası ülke karşılaştırmalı ampirik analizden ayrı fakat tamamlayıcı bir bölüm olarak ele alınır.

## Public repository notu
Bu depo public olduğu için yayımlanmamış Word makale taslağı depoya dahil edilmez. Veri, kod ve yeniden üretilebilir analiz bileşenleri burada tutulur; grafikler `run_all.py` ile yeniden üretilebilir.
