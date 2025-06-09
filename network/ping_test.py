"""
Amaç
    - Belirtilen bir host'a ICMP Ping göndermek (`ping -c N`)
    - Komut satırı çıktısından ortalama RTT (Round-Trip Time) değerini çekmek (macOS formatı)
    - Tam ping çıktısını da ekrana basmak

Gereksinim
    - Sistem `ping` komutuna ICMP erişimine izin vermeli
    - Windows'ta `-n <count>` ve farklı regex gerekir (burada macOS/Linux odaklı)

Kullanım
    python3 ping_test.py           # varsayılan 4 paket  → 8.8.8.8
    python3 ping_test.py 1.1.1.1 6 # host=1.1.1.1, count=6
"""

import subprocess
import re
import sys

# ─────────────────────────────────────────────────────────────
#  1) Ping Fonksiyonu
# ─────────────────────────────────────────────────────────────
def ping(host: str, count: int = 4) -> None:
    """
    host  : ICMP ping atılacak domain/IP
    count : Gönderilecek paket sayısı
    """
    try:
        #ping çıktısı: byte decode UTF-8
        output = subprocess.check_output(
            ["ping", "-c", str(count), host],
            stderr=subprocess.STDOUT,
        ).decode()
    except subprocess.CalledProcessError as exc:
        print("⛔ Ping komutu hata verdi:\n", exc.output.decode())
        return

    #macOS/Linux formatı:  round-trip min/avg/max/stddev = 22.3/35.3/67.6/18.7 ms
    rtt_match = re.search(
        r"round-trip [^=]+= ([\d\.]+/[\d\.]+/[\d\.]+/[\d\.]+) ms",
        output,
    )

    if rtt_match:
        min_, avg, max_, stddev = rtt_match.group(1).split("/")
        print(f"✅ Ortalama RTT: {avg} ms")
    else:
        print("❌ Ortalama RTT alınamadı (regex eşleşmedi).")

    #tam ping çıktısını da göster
    print("\n— Ping Çıktısı —")
    print(output)

# ─────────────────────────────────────────────────────────────
#  2) Komut Satırından Çalıştırıldığında
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    #terminal argümanları → host, count
    host  = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    ping(host, count)
