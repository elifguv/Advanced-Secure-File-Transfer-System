"""
Amaç
    - Gönderen istemci, sunucuya (127.0.0.1:5001) bağlanırken
      önce sabit bir parola (PASSWORD) ile kimlik doğrulaması yapar.
    - Sunucu "OK" derse `buyuk_dosya.txt` dosyasını TCP üzerinden gönderir.

Gereksinim
    - Sunucu tarafında parola kontrolü yapan bir socket dinleyicisi
      (örn. server_auth.py veya server_auth_hash.py)

Kullanım
    python3 client_auth.py
"""

import socket
import os

PASSWORD = "network2025"   #sunucudaki PASSWORD ile bire bir aynı olmalı
HOST, PORT = "127.0.0.1", 5001
BUFSIZE = 1024             #1 KiB parça boyutu
FILENAME = "buyuk_dosya.txt"

# ------------------------------------------------------------
#  1) TCP soketi oluştur ve sunucuya bağlan
# ------------------------------------------------------------
sock = socket.socket()
try:
    sock.connect((HOST, PORT))
except ConnectionRefusedError:
    print("⛔ Sunucuya bağlanılamadı − server çalışıyor mu?")
    exit(1)

# ------------------------------------------------------------
#  2) Parola gönder (kimlik doğrulama)
# ------------------------------------------------------------
sock.send(PASSWORD.encode())        #parola yolla
response = sock.recv(1024).decode() #sunucudan cevap bekle

if response != "OK":
    print("❌ Kimlik doğrulama başarısız.")
    sock.close()
    exit(1)

print("✅ Kimlik doğrulama başarılı. Dosya gönderiliyor...")

# ------------------------------------------------------------
#  3) Dosya parçalarını gönder
# ------------------------------------------------------------
if not os.path.isfile(FILENAME):
    print("⛔ Gönderilecek dosya bulunamadı:", FILENAME)
    sock.close()
    exit(1)

with open(FILENAME, "rb") as f:
    while chunk := f.read(BUFSIZE):
        sock.sendall(chunk)

print("✅ Dosya başarıyla gönderildi.")

# ------------------------------------------------------------
#  4) Bağlantıyı kapat
# ------------------------------------------------------------
sock.close()
