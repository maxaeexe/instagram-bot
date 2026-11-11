import os
import sys
import time
import random
from colorama import init, Fore, Style

# Colorama'yı başlat (Windows uyumu)
init(autoreset=True)

# ============================================
#   KONSOL ARAYÜZ FONKSİYONLARI
# ============================================

def ekrani_temizle():
    """Konsol ekranını temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    """Bot başlık bannerını gösterir."""
    print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ██╗███╗   ██╗███████╗████████╗ █████╗               ║
║     ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗              ║
║     ██║██╔██╗ ██║███████╗   ██║   ███████║              ║
║     ██║██║╚██╗██║╚════██║   ██║   ██╔══██║              ║
║     ██║██║ ╚████║███████║   ██║   ██║  ██║              ║
║     ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝              ║
║                                                          ║
║            ⚡ INSTAGRAM TAKİP BOTU ⚡                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")


def cizgi(karakter="─", uzunluk=58):
    """Ayırıcı çizgi çizer."""
    print(Fore.CYAN + karakter * uzunluk)


def bilgi(mesaj):
    """Bilgi mesajı yazdırır."""
    print(Fore.CYAN + "[ℹ] " + Style.RESET_ALL + mesaj)


def basari(mesaj):
    """Başarı mesajı yazdırır."""
    print(Fore.GREEN + "[✔] " + Style.RESET_ALL + mesaj)


def uyari(mesaj):
    """Uyarı mesajı yazdırır."""
    print(Fore.YELLOW + "[⚠] " + Style.RESET_ALL + mesaj)


def hata(mesaj):
    """Hata mesajı yazdırır."""
    print(Fore.RED + "[✖] " + Style.RESET_ALL + mesaj)


def islem(mesaj):
    """İşlem mesajı yazdırır."""
    print(Fore.MAGENTA + "[→] " + Style.RESET_ALL + mesaj)


def bekleme_goster(saniye):
    """Geri sayımlı bekleme gösterir."""
    for kalan in range(saniye, 0, -1):
        sys.stdout.write(Fore.YELLOW + f"\r    ⏳ Bekleniyor: {kalan} saniye (Ban Koruması)   ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 55 + "\r")
    sys.stdout.flush()


def guvenli_bekleme(min_sure, max_sure):
    """Rastgele süre bekler ve geri sayım gösterir."""
    bekleme = random.randint(min_sure, max_sure)
    bekleme_goster(bekleme)


def ozet_tablosu(baslik, veriler):
    """Özet tablosu gösterir.
    
    veriler: [(etiket, deger), ...] listesi
    """
    print()
    cizgi("═")
    print(Fore.CYAN + Style.BRIGHT + f"  📊 {baslik}")
    cizgi("═")
    for etiket, deger in veriler:
        print(Fore.WHITE + f"  ▸ {etiket}: " + Fore.GREEN + Style.BRIGHT + str(deger))
    cizgi("═")
    print()


def ilerleme_cubugu(mevcut, toplam, etiket="İlerleme"):
    """Basit bir ilerleme çubuğu gösterir."""
    genislik = 30
    dolu = int(genislik * mevcut / toplam) if toplam > 0 else 0
    bos = genislik - dolu
    yuzde = int(100 * mevcut / toplam) if toplam > 0 else 0
    cubuk = Fore.GREEN + "█" * dolu + Fore.WHITE + "░" * bos
    sys.stdout.write(f"\r  {etiket}: [{cubuk}{Style.RESET_ALL}] {yuzde}% ({mevcut}/{toplam})")
    sys.stdout.flush()
    if mevcut == toplam:
        print()
