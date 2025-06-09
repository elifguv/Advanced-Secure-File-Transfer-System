"""
İşlev
    1. TCP üzerinden gelen istemciden parola (PASSWORD) kabul eder
       – doğruysa 'OK', yanlışsa 'ER' yanıtı verir.
    2. İkinci adımda istemciden SHA-256 hash değeri alır ve yine 'OK' yanıtlar.
    3. Ardından dosya parçalarını alıp `gelen_dosya.txt` dosyasına yazar.
    4. Dosya bittiğinde kendi hesapladığı hash ile beklenen hash'i karşılaştırır.

Gereksinim
    - İstemci tarafında aynı sırayla: parola ➝ hash ➝ dosya parçası gönderen
      script (örn. fragment_sender_hash.py)

Kullanım
    python3 server_auth_hash.py
"""

import socket
import hashlib
from typing import Tuple

# ============================================================================
# Sabitler
# ============================================================================
PASSWORD   = "network2025"
HOST, PORT = "0.0.0.0", 5001
OUTFILE    = "gelen_dosya.txt"
BUF_SIZE   = 256 * 1024         #256 KiB

# ============================================================================
# Yardımcı fonksiyon: SHA-256
# ============================================================================
def sha256_hash(fp: str) -> str:
    """Dosya içeriğinin SHA-256 (hex) özetini döndürür."""
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

# ============================================================================
# Sunucuyu başlat
# ============================================================================
srv = socket.socket()
srv.bind((HOST, PORT))
srv.listen(1)
print(f"🌐 Sunucu dinleniyor... ({HOST}:{PORT})")

try:
    cli, addr = srv.accept()
    print(f"🔗 {addr} bağlandı.")

    # 1) Parola kontrolü ────────────────────────────────────────────────
    pwd = cli.recv(64).decode().strip()
    if pwd != PASSWORD:
        cli.send(b"ER")
        print("❌ Hatalı şifre! Bağlantı kapatıldı.")
        cli.close(); srv.close(); exit()

    cli.send(b"OK")   #parola onay
    print("✅ Parola doğrulandı.")

    # 2) Hash al ───────────────────────────────────────────────────────
    expected_hash = cli.recv(64).decode()
    cli.send(b"OK")
    print("✅ Hash alındı → dosya bekleniyor...")

    # 3) Dosya parçalarını kaydet ─────────────────────────────────────
    with open(OUTFILE, "wb") as f:
        while True:
            data = cli.recv(BUF_SIZE)
            if not data:
                break
            f.write(data)

    print("📄 Dosya alındı, SHA-256 kontrol ediliyor…")
    real_hash = sha256_hash(OUTFILE)

    # 4) Hash karşılaştırma ───────────────────────────────────────────
    if real_hash == expected_hash:
        print("✅ SHA-256 doğrulaması BAŞARILI!")
    else:
        print("❌ SHA-256 doğrulaması BAŞARISIZ!")

except Exception as exc:
    print("⛔ Sunucu hatası:", exc)

finally:
    cli.close()
    srv.close()
