"""
╔══════════════════════════════════════════╗
║   INSTAGRAM TAKİP BOTU - ANA DOSYA      ║
║   Konsol üzerinden çalışan Instagram     ║
║   hashtag tabanlı takip botu.            ║
╚══════════════════════════════════════════╝

Kullanım:
    python main.py

Gereksinimler:
    pip install -r requirements.txt
"""

import sys
import getpass
from colorama import Fore, Style

from ui import ekrani_temizle, banner, cizgi, bilgi, basari, hata, uyari, islem, ozet_tablosu
from bot import InstaBot
import config


def hashtag_al():
    """Kullanıcıdan hashtag'leri alır."""
    print()
    cizgi()
    print(Fore.CYAN + Style.BRIGHT + "  📝 HASHTAG GİRİŞİ")
    cizgi()

    while True:
        try:
            sayi = int(input(Fore.WHITE + "\n  Kaç adet hashtag gireceksin?: " + Fore.GREEN))
            if sayi < 1:
                uyari("En az 1 hashtag girmelisin!")
                continue
            break
        except ValueError:
            hata("Lütfen geçerli bir sayı gir!")

    hashtags = []
    print()
    for i in range(sayi):
        while True:
            ht = input(Fore.WHITE + f"  {i+1}. Hashtag (# olmadan): " + Fore.GREEN).strip()
            if ht:
                # Başında # varsa kaldır
                ht = ht.lstrip("#").strip()
                if ht:
                    hashtags.append(ht)
                    break
            hata("Boş hashtag giremezsin!")

    return hashtags


def ayarlari_goster():
    """Mevcut ayarları gösterir."""
    ozet_tablosu("MEVCUT AYARLAR", [
        ("Min Bekleme", f"{config.MIN_BEKLEME} saniye"),
        ("Max Bekleme", f"{config.MAX_BEKLEME} saniye"),
        ("Hashtag Başına Gönderi", config.HASHTAG_GONDERI_SAYISI),
        ("Gönderi Başına Beğenen Limiti", config.BEGENEN_LIMIT),
        ("Gönderi Başına Yorum Limiti", config.YORUM_LIMIT),
        ("Önerilen Hesap Sayısı", config.ONERILEN_HESAP_SAYISI),
    ])


def ana_menu():
    """Ana menüyü gösterir ve seçim alır."""
    print()
    cizgi("═")
    print(Fore.CYAN + Style.BRIGHT + "  📋 ANA MENÜ")
    cizgi("═")
    print(Fore.WHITE + "  [1] 🚀 Botu Başlat (Hashtag Tarama + Önerilen Hesaplar)")
    print(Fore.WHITE + "  [2] 🔍 Sadece Hashtag Tarama")
    print(Fore.WHITE + "  [3] 👥 Sadece Önerilen Hesapları Takip Et")
    print(Fore.WHITE + "  [4] ⚙️  Ayarları Görüntüle")
    print(Fore.WHITE + "  [5] ❌ Çıkış")
    cizgi("═")

    while True:
        secim = input(Fore.WHITE + "\n  Seçimin (1-5): " + Fore.GREEN).strip()
        if secim in ["1", "2", "3", "4", "5"]:
            return secim
        hata("Geçersiz seçim! 1-5 arası bir sayı gir.")


def main():
    ekrani_temizle()
    banner()

    # ── GİRİŞ YÖNTEMİ SEÇİMİ ──
    cizgi()
    print(Fore.CYAN + Style.BRIGHT + "  🔐 GİRİŞ YÖNTEMİ")
    cizgi()
    print(Fore.WHITE + "  [1] 🔑 Session ID ile giriş (Önerilen)")
    print(Fore.WHITE + "  [2] 👤 Kullanıcı adı + Şifre ile giriş")
    cizgi()

    while True:
        giris_secim = input(Fore.WHITE + "\n  Seçimin (1-2): " + Fore.GREEN).strip()
        if giris_secim in ["1", "2"]:
            break
        hata("Geçersiz seçim!")

    # ── BOT BAŞLAT ──
    bot = InstaBot()

    if giris_secim == "1":
        # Session ID ile giriş
        print()
        bilgi("━" * 54)
        bilgi("  SESSION ID NASIL ALINIR?")
        bilgi("━" * 54)
        print()
        bilgi("  1. Tarayıcıdan instagram.com'a giriş yap")
        bilgi("  2. F12 tuşuna bas (Geliştirici Araçları)")
        bilgi("  3. 'Application' sekmesi → 'Cookies' →")
        bilgi("     'https://www.instagram.com' tıkla")
        bilgi("  4. 'sessionid' satırının 'Value' değerini kopyala")
        print()
        session_id = input(Fore.WHITE + "  🔑 Session ID: " + Fore.GREEN).strip().strip("'\"")
        print(Style.RESET_ALL, end="")

        if not session_id:
            hata("Session ID boş bırakılamaz!")
            sys.exit(1)

        if not bot.session_giris(session_id):
            hata("Giriş başarısız! Program sonlandırılıyor.")
            sys.exit(1)
    else:
        # Kullanıcı adı + şifre ile giriş
        kullanici_adi = input(Fore.WHITE + "\n  Kullanıcı Adı: " + Fore.GREEN).strip()
        sifre = getpass.getpass(Fore.WHITE + "  Şifre (gizli): " + Fore.GREEN)
        print(Style.RESET_ALL, end="")

        if not kullanici_adi or not sifre:
            hata("Kullanıcı adı ve şifre boş bırakılamaz!")
            sys.exit(1)

        if not bot.giris_yap(kullanici_adi, sifre):
            hata("Giriş başarısız! Program sonlandırılıyor.")
            sys.exit(1)

    # ── ANA DÖNGÜ ──
    while True:
        secim = ana_menu()

        if secim == "1":
            hashtags = hashtag_al()
            ozet_tablosu("TARAMA ÖZETİ", [
                ("Hashtag Sayısı", len(hashtags)),
                ("Hashtag'ler", ", ".join(f"#{h}" for h in hashtags)),
                ("Önerilen Hesaplar", "Evet"),
            ])

            onay = input(Fore.YELLOW + "  Başlatılsın mı? (e/h): " + Fore.GREEN).strip().lower()
            if onay != "e":
                uyari("İşlem iptal edildi.")
                continue

            print()
            cizgi("═")
            print(Fore.GREEN + Style.BRIGHT + "  🚀 BOT BAŞLATILIYOR...")
            cizgi("═")

            # Hashtag tarama
            bot.hashtag_tara(hashtags)

            # Önerilen hesaplar
            print()
            cizgi()
            print(Fore.CYAN + Style.BRIGHT + "  👥 ÖNERİLEN HESAPLAR")
            cizgi()
            bot.onerilenleri_takip_et()

            # Sonuç
            ozet_tablosu("SONUÇ RAPORU", bot.istatistikleri_al())

        elif secim == "2":
            hashtags = hashtag_al()
            ozet_tablosu("TARAMA ÖZETİ", [
                ("Hashtag Sayısı", len(hashtags)),
                ("Hashtag'ler", ", ".join(f"#{h}" for h in hashtags)),
            ])

            onay = input(Fore.YELLOW + "  Başlatılsın mı? (e/h): " + Fore.GREEN).strip().lower()
            if onay != "e":
                uyari("İşlem iptal edildi.")
                continue

            bot.hashtag_tara(hashtags)
            ozet_tablosu("SONUÇ RAPORU", bot.istatistikleri_al())

        elif secim == "3":
            print()
            cizgi()
            print(Fore.CYAN + Style.BRIGHT + "  👥 ÖNERİLEN HESAPLAR")
            cizgi()
            bot.onerilenleri_takip_et()
            ozet_tablosu("SONUÇ RAPORU", bot.istatistikleri_al())

        elif secim == "4":
            ayarlari_goster()

        elif secim == "5":
            print()
            basari("Görüşmek üzere! 👋")
            print()
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        uyari("Program kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        hata(f"Beklenmeyen hata: {e}")
        sys.exit(1)
