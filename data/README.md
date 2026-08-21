# Veri klasörü

Bu depo, makaledeki analizlerin internet olmadan yeniden üretilebilmesi için kullanılan küçük/orta boy araştırma verilerini içerir.

## raw/
- `bis_cbdc_mar2024.csv`: BIS'in Mart 2024 CBDC proje veri seti.
- `findex_selected_2021.csv`: World Bank Global Findex 2025 veritabanının 2021 dalgasından yalnızca bu çalışmada kullanılan değişkenlerin seçilmiş ülke düzeyi özeti.

## processed/
- `cbdc_findex_merged_2021.csv`: BIS ve Findex verilerinin ISO2 ülke kodu üzerinden birleştirilmiş analiz dosyası.

## Değişkenler
CBDC aşaması:
- 0 = bilinen çalışma yok
- 1 = araştırma
- 2 = pilot
- 3 = canlı CBDC

Temel açıklayıcı değişkenler:
- `account_ownership_2021`
- `digital_payment_2021`
- `online_bill_payment_2021`
- `digital_merchant_payment_2021`
- `borrowed_any_2021`
- `pop_adult`

Kaynak adresleri `source_manifest.csv` dosyasındadır.
