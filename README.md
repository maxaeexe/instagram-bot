# 📸 Instagram Takip Botu

Hashtag tabanlı otomatik takip botu. Instagram'da belirli hashtag'lerdeki gönderilerin beğenenlerini, yorum yapanlarını ve önerilen hesapları takip eder.

## 🚀 Kurulum

```bash
pip install -r requirements.txt
```

## 📋 Kullanım

```bash
python main.py
```

### Giriş Yöntemleri
- **Session ID** (Önerilen): Tarayıcıdan alınan session cookie ile giriş
- **Kullanıcı Adı + Şifre**: Doğrudan kimlik bilgileri ile giriş

### Özellikler
- 🔍 Hashtag tabanlı kullanıcı tarama
- 👥 Önerilen hesapları takip etme
- ⏱️ Akıllı bekleme sistemi (ban koruması)
- 📊 Detaylı istatistik raporu
- 🎨 Renkli konsol arayüzü

## ⚙️ Yapılandırma

`config.py` dosyasından bot ayarlarını düzenleyebilirsin:

| Ayar | Varsayılan | Açıklama |
|------|-----------|----------|
| `MIN_BEKLEME` | 15 sn | Minimum bekleme süresi |
| `MAX_BEKLEME` | 35 sn | Maksimum bekleme süresi |
| `HASHTAG_GONDERI_SAYISI` | 3 | Her hashtag'den çekilecek gönderi |
| `BEGENEN_LIMIT` | 3 | Gönderi başına takip edilecek beğenen |
| `YORUM_LIMIT` | 3 | Gönderi başına çekilecek yorum |
| `ONERILEN_HESAP_SAYISI` | 5 | Takip edilecek önerilen hesap |

## ⚠️ Uyarı

Bu bot eğitim amaçlıdır. Instagram'ın kullanım koşullarına aykırı kullanımlardan kullanıcı sorumludur.
