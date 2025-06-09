"""
Amaç
    - Büyük bir dosyayı (varsayılan: buyuk_dosya.txt) 256 KiB'lik parçalar hâlinde TCP üzerinden sunucuya göndermek.

Gereksinim
    - Sunucu tarafında parçaları kabul eden dinleyici (server.py)
    - buyuk_dosya.txt aynı dizinde mevcut olmalı.

Parametreler
    HOST, PORT   : Sunucu adresi
    CHUNK_SIZE   : Gönderim başına okunan bayt miktarı (256 KiB)
"""

import socket
import os
from typing import Generator

#sunucu bilgileri
HOST = "127.0.0.1"
PORT = 5001
CHUNK_SIZE = 256 * 1024      # 256 KiB
FILENAME   = "buyuk_dosya.txt"

# ─────────────────────────────────────────────────────────────
#  1) Yardımcı Fonksiyon: Dosyayı parça parça üret
# ─────────────────────────────────────────────────────────────
def iter_file(filepath: str, chunk_size: int = CHUNK_SIZE) -> Generator[bytes, None, None]:
    """
    Dosyayı bellek yerine stream olarak parça parça döndürür.
    Bellek dostudur.
    """
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

# ─────────────────────────────────────────────────────────────
#  2) Soketi oluştur ve sunucuya bağlan
# ─────────────────────────────────────────────────────────────
sock = socket.socket()
try:
    sock.connect((HOST, PORT))
except ConnectionRefusedError:
    print("⛔ Sunucuya bağlanılamadı — server.py çalışıyor mu?")
    exit(1)

# ─────────────────────────────────────────────────────────────
#  3) Dosya var mı kontrolü
# ─────────────────────────────────────────────────────────────
if not os.path.isfile(FILENAME):
    print(f"⛔ Gönderilecek dosya bulunamadı: {FILENAME}")
    sock.close()
    exit(1)

file_size   = os.path.getsize(FILENAME)
total_parts = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE

# ─────────────────────────────────────────────────────────────
#  4) Dosyayı parça parça gönder
# ─────────────────────────────────────────────────────────────
for idx, part in enumerate(iter_file(FILENAME), start=1):
    percent = idx / total_parts * 100
    print(f"🟢 Parça {idx}/{total_parts}  ({percent:5.1f} %)")
    sock.sendall(part)

print("✅ Dosya gönderimi tamamlandı.")

# ─────────────────────────────────────────────────────────────
#  5) Bağlantıyı kapat
# ─────────────────────────────────────────────────────────────
sock.shutdown(socket.SHUT_WR)
sock.close()
