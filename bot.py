from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
    PleaseWaitFewMinutes,
    ClientError,
)
import json
import os
import time
import config
from ui import basari, hata, uyari, bilgi, islem, guvenli_bekleme, ilerleme_cubugu


def challenge_kod_iste(username, choice):
    """Instagram challenge doğrulama kodu istediğinde çağrılır."""
    yontem = "SMS" if choice == 0 else "E-posta"
    uyari(f"Instagram şüpheli giriş doğrulaması istiyor! ({yontem})")
    kod = input(f"  📱 {yontem} ile gelen doğrulama kodunu gir: ").strip()
    return kod


class InstaBot:
    """Instagram bot ana sınıfı."""

    # Güncel Instagram uygulama sürümü ve cihaz bilgileri
    # Instagram bu değerleri kontrol edip eski sürümleri reddediyor
    DEVICE_SETTINGS = {
        "app_version": "357.0.0.0.60",
        "android_version": 34,
        "android_release": "14",
        "dpi": "480dpi",
        "resolution": "1080x2400",
        "manufacturer": "Samsung",
        "device": "SM-S926B",
        "model": "samsung",
        "cpu": "qcom",
        "version_code": "604247942",
    }

    USER_AGENT = (
        "Instagram 357.0.0.0.60 Android (34/14; 480dpi; 1080x2400; "
        "samsung; SM-S926B; e2s; qcom; tr_TR; 604247942)"
    )

    def __init__(self):
        self.cl = self._yeni_client()
        self.takip_sayaci = 0
        self.atlanan_sayaci = 0
        self.hata_sayaci = 0
        self.takip_edilenler = set()

    # ─────────────────────────────────────
    #  GİRİŞ İŞLEMLERİ
    # ─────────────────────────────────────

    def _yeni_client(self):
        """Temiz bir Client oluşturur ve güncel cihaz bilgilerini ayarlar."""
        cl = Client()
        cl.delay_range = [1, 3]
        cl.challenge_code_handler = challenge_kod_iste

        # Güncel cihaz bilgilerini ayarla
        cl.set_device(self.DEVICE_SETTINGS)
        cl.set_user_agent(self.USER_AGENT)

        return cl

    def giris_yap(self, kullanici_adi, sifre):
        """Instagram'a giriş yapar. Oturum dosyası varsa onu kullanır."""
        oturum_yolu = config.OTURUM_DOSYASI

        try:
            # Kayıtlı oturum varsa yükle
            if os.path.exists(oturum_yolu):
                bilgi("Kayıtlı oturum bulundu, yükleniyor...")
                self.cl.load_settings(oturum_yolu)
                self.cl.login(kullanici_adi, sifre)
                try:
                    self.cl.account_info()
                    basari("Kayıtlı oturum ile giriş başarılı!")
                    return True
                except LoginRequired:
                    bilgi("Oturum süresi dolmuş, yeniden giriş yapılıyor...")
                    self.cl = self._yeni_client()

            # Yeni giriş yap
            islem("Instagram'a giriş yapılıyor...")
            self.cl.login(kullanici_adi, sifre)
            self.cl.dump_settings(oturum_yolu)
            basari("Giriş başarılı! Oturum kaydedildi.")
            return True

        except (TwoFactorRequired, ChallengeRequired):
            # Normal giriş başarısız - Session ID yöntemine yönlendir
            print()
            uyari("━" * 54)
            uyari("  Instagram ek doğrulama istiyor.")
            uyari("  Session ID ile giriş yapılacak.")
            uyari("━" * 54)
            return self._session_id_ile_giris(oturum_yolu)

        except PleaseWaitFewMinutes:
            hata("Instagram geçici olarak engelledi! Birkaç dakika bekleyip tekrar dene.")
            return False

        except Exception as e:
            if "bloks" in str(e).lower() or "caa" in str(e).lower():
                print()
                uyari("Instagram yeni güvenlik sistemi devrede.")
                uyari("Session ID ile giriş yapılacak.")
                return self._session_id_ile_giris(oturum_yolu)
            hata(f"Giriş hatası: {e}")
            return False

    def _session_id_ile_giris(self, oturum_yolu):
        """Tarayıcıdan alınan Session ID ile giriş yapar."""
        print()
        bilgi("━" * 54)
        bilgi("  SESSION ID NASIL ALINIR?")
        bilgi("━" * 54)
        print()
        bilgi("  1. Bilgisayarından tarayıcıyı aç (Chrome/Edge/Firefox)")
        bilgi("  2. instagram.com adresine git ve hesabına giriş yap")
        bilgi("  3. Giriş yaptıktan sonra F12 tuşuna bas (Geliştirici Araçları)")
        bilgi("  4. Üst menüden 'Application' (Chrome) veya")
        bilgi("     'Storage' (Firefox) sekmesine tıkla")
        bilgi("  5. Sol menüde 'Cookies' → 'https://www.instagram.com' tıkla")
        bilgi("  6. Listede 'sessionid' satırını bul")
        bilgi("  7. 'Value' sütunundaki değeri kopyala")
        print()
        bilgi("  ⚡ KISA YOL: Adres çubuğuna şunu yaz ve Enter'a bas:")
        print()
        bilgi('     javascript:void(prompt("Session ID:",document.cookie.match(/sessionid=([^;]+)/)?.[1]))')
        print()

        session_id = input("  🔑 Session ID'yi yapıştır: ").strip()

        if not session_id:
            hata("Session ID boş bırakılamaz!")
            return False

        # Olası tırnak/boşluk temizliği
        session_id = session_id.strip("'\"").strip()

        try:
            self.cl = self._yeni_client()
            islem("Session ID ile giriş yapılıyor...")
            self.cl.login_by_sessionid(session_id)

            # Giriş doğrulama
            hesap = self.cl.account_info()
            self.cl.dump_settings(oturum_yolu)
            basari(f"Giriş başarılı! Hoş geldin @{hesap.username}")
            return True

        except Exception as e:
            hata(f"Session ID ile giriş başarısız: {e}")
            uyari("Session ID'nin doğru kopyalandığından emin ol.")
            uyari("Tarayıcıda Instagram'a giriş yapmış olmalısın.")
            return False

    def session_giris(self, session_id):
        """Tarayıcıdan alınan Session ID ile giriş yapar."""
        oturum_yolu = config.OTURUM_DOSYASI

        try:
            self.cl = self._yeni_client()
            islem("Session ID ile giriş yapılıyor...")
            self.cl.login_by_sessionid(session_id)

            # Giriş doğrulama
            hesap = self.cl.account_info()
            self.cl.dump_settings(oturum_yolu)
            basari(f"Giriş başarılı! Hoş geldin @{hesap.username}")
            return True

        except Exception as e:
            hata(f"Session ID ile giriş başarısız: {e}")
            uyari("Session ID'nin doğru kopyalandığından emin ol.")
            uyari("Tarayıcıda Instagram'a giriş yapmış olmalısın.")
            return False

    # ─────────────────────────────────────
    #  TAKİP İŞLEMLERİ
    # ─────────────────────────────────────

    def _kullanici_takip_et(self, user_pk, username, kaynak):
        """Tek bir kullanıcıyı takip eder (tekrar kontrolü ile)."""
        if user_pk in self.takip_edilenler:
            uyari(f"{username} zaten bu oturumda takip edildi, atlanıyor.")
            self.atlanan_sayaci += 1
            return False

        try:
            self.cl.user_follow(user_pk)
            self.takip_edilenler.add(user_pk)
            self.takip_sayaci += 1
            basari(f"{username} ({kaynak}) takip edildi. [Toplam: {self.takip_sayaci}]")
            guvenli_bekleme(config.MIN_BEKLEME, config.MAX_BEKLEME)
            return True

        except PleaseWaitFewMinutes:
            hata("Instagram geçici engel koydu! 5 dakika bekleniyor...")
            import time
            time.sleep(300)
            self.hata_sayaci += 1
            return False

        except ClientError as e:
            if "feedback_required" in str(e).lower():
                hata("Instagram aksiyon limiti! 10 dakika bekleniyor...")
                import time
                time.sleep(600)
            else:
                hata(f"{username} takip edilemedi: {e}")
            self.hata_sayaci += 1
            return False

        except Exception as e:
            hata(f"{username} takip edilemedi: {e}")
            self.hata_sayaci += 1
            return False

    # ─────────────────────────────────────
    #  HASHTAG TARAMA
    # ─────────────────────────────────────

    def hashtag_tara(self, hashtag_listesi):
        """Hashtag'lerdeki gönderilerin beğenen ve yorum yapanlarını takip eder."""
        toplam_hashtag = len(hashtag_listesi)

        for idx, ht in enumerate(hashtag_listesi, 1):
            print()
            bilgi(f"[{idx}/{toplam_hashtag}] #{ht} hashtag'i taranıyor...")
            print()

            try:
                gonderiler = self.cl.hashtag_medias_recent(ht, amount=config.HASHTAG_GONDERI_SAYISI)
            except Exception as e:
                hata(f"#{ht} hashtag'i taranamadı: {e}")
                continue

            if not gonderiler:
                uyari(f"#{ht} için gönderi bulunamadı.")
                continue

            bilgi(f"{len(gonderiler)} gönderi bulundu.")

            for g_idx, gonderi in enumerate(gonderiler, 1):
                gonderi_sahibi_pk = gonderi.user.pk

                islem(f"Gönderi {g_idx}/{len(gonderiler)} işleniyor...")

                # ── BEĞENENLERİ TAKİP ET ──
                try:
                    begenenler = self.cl.media_likers(gonderi.id)
                    # Gönderi sahibini filtrele
                    begenenler = [u for u in begenenler if u.pk != gonderi_sahibi_pk]
                    secilen = begenenler[:config.BEGENEN_LIMIT]

                    if secilen:
                        bilgi(f"  Beğenenler ({len(secilen)} kişi):")
                        for user in secilen:
                            self._kullanici_takip_et(user.pk, user.username, "beğenen")
                    else:
                        uyari("  Bu gönderide uygun beğenen bulunamadı.")

                except Exception as e:
                    hata(f"  Beğenenler alınamadı: {e}")

                # ── YORUM YAPANLARI TAKİP ET ──
                try:
                    yorumlar = self.cl.media_comments(gonderi.id, amount=config.YORUM_LIMIT)
                    # Gönderi sahibinin kendi yorumlarını filtrele
                    yorumlar = [y for y in yorumlar if y.user.pk != gonderi_sahibi_pk]

                    if yorumlar:
                        bilgi(f"  Yorum yapanlar ({len(yorumlar)} kişi):")
                        for yorum in yorumlar:
                            self._kullanici_takip_et(yorum.user.pk, yorum.user.username, "yorum yapan")
                    else:
                        uyari("  Bu gönderide uygun yorum yapan bulunamadı.")

                except Exception as e:
                    hata(f"  Yorumlar alınamadı: {e}")

            ilerleme_cubugu(idx, toplam_hashtag, "Hashtag İlerlemesi")

    # ─────────────────────────────────────
    #  ÖNERİLEN HESAPLAR
    # ─────────────────────────────────────

    def onerilenleri_takip_et(self):
        """Instagram'ın önerdiği hesapları takip eder."""
        bilgi("Önerilen hesaplar alınıyor...")

        try:
            onerilenler = self.cl.user_suggested(self.cl.user_id, amount=config.ONERILEN_HESAP_SAYISI)
        except Exception as e:
            hata(f"Önerilen hesaplar alınamadı: {e}")
            return

        if not onerilenler:
            uyari("Önerilen hesap bulunamadı.")
            return

        bilgi(f"{len(onerilenler)} önerilen hesap bulundu.")
        print()

        for idx, kullanici in enumerate(onerilenler, 1):
            self._kullanici_takip_et(kullanici.pk, kullanici.username, "önerilen")
            ilerleme_cubugu(idx, len(onerilenler), "Önerilen Hesaplar")

    # ─────────────────────────────────────
    #  İSTATİSTİKLER
    # ─────────────────────────────────────

    def istatistikleri_al(self):
        """Bot çalışma istatistiklerini döndürür."""
        return [
            ("Takip Edilen", self.takip_sayaci),
            ("Atlanan (tekrar)", self.atlanan_sayaci),
            ("Hata", self.hata_sayaci),
            ("Toplam İşlem", self.takip_sayaci + self.atlanan_sayaci + self.hata_sayaci),
        ]
