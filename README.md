# fintek-naig — CBDC ve Programlanabilir Ödemeler Ampirik Araştırma Projesi

Bu depo, **CBDC gelişim aşamalarını finansal kapsayıcılık ve dijital ödeme göstergeleriyle analiz eden** makalenin veri, kod, tablo, grafik ve taslak metinlerini birlikte tutar.

## Araştırma sorusu
Ülkelerde CBDC çalışmalarının daha ileri aşamaya ulaşması; finansal kapsayıcılık, dijital ödeme kullanımı ve ülke ölçeği ile ilişkili midir?

## Veri
- **BIS CBDC Projects Database — March 2024**: CBDC proje aşamaları.
- **World Bank Global Findex Database 2025 — 2021 wave**: finansal kapsayıcılık ve dijital ödeme göstergeleri.
- `data/raw/` altında kullanılan kaynak veri/kompakt araştırma özeti depoda tutulur.
- `data/processed/` altındaki 112 ülkelik temizlenmiş veri, analiz için hazır dosyadır.

Resmî veri bağlantıları: `data/source_manifest.csv`.

## Analizler
1. Veri doğrulama ve yeniden birleştirme
2. Tanımlayıcı istatistikler ve korelasyonlar
3. Ordered Probit
4. Ordered Logit sağlamlık kontrolü
5. Binary Logistic Regression
6. Random Forest + tekrar eden stratified cross-validation
7. Permutation feature importance
8. Makale grafikleri
9. Türkiye ampirik profili

## Windows'ta ilk kurulum
Proje klasöründe çift tıklayın:

```text
setup_windows.bat
```

Bu komut `.venv` oluşturur ve gerekli Python paketlerini yükler.

## Tüm analizleri tek komutla çalıştırma

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
│   ├── raw/                  # Kaynak/kompakt ham veri
│   ├── processed/            # Analize hazır veri
│   └── documentation/        # Veri sözlüğü
├── outputs/
│   ├── tables/               # Makale tabloları
│   └── figures/              # Makale grafikleri
├── manuscript/               # Makale Word taslağı
├── notebooks/                # İleri EDA/ML notebook alanı
├── .github/workflows/        # GitHub Actions yeniden üretilebilirlik testi
├── requirements.txt
├── run_all.py
├── setup_windows.bat
├── run_all.bat
└── github_first_push.bat
```

## GitHub'a ilk yükleme
1. GitHub'da boş bir `fintek-naig` deposu oluşturun.
2. `github_first_push.bat` dosyasındaki iki `REM git ...` satırında repo URL'sini düzenleyin.
3. Satırların başındaki `REM` ifadesini kaldırın.
4. Dosyayı çalıştırın.

Alternatif terminal komutları:

```bash
git init
git add .
git commit -m "Initial CBDC empirical research project"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADI/fintek-naig.git
git push -u origin main
```

## Yeniden üretilebilirlik notu
Analizin çalışması için büyük Global Findex Excel dosyasını her seferinde indirmek gerekmez. Bu araştırmada kullanılan 2021 ülke düzeyi değişkenleri `data/raw/findex_selected_2021.csv` içinde tutulmuştur. Böylece mevcut sonuçlar internet bağlantısı olmadan yeniden üretilebilir.

## Kavramsal not
Makale, **programlanabilir para** ile **programlanabilir/koşullu ödeme** ayrımını korumalıdır. TCMB vaka kısmı, uluslararası ülke karşılaştırmalı ampirik analizden ayrı fakat tamamlayıcı bir bölüm olarak ele alınır.
