"""
Basit Dosya Göndericisi
    - Sunucuya (localhost:5001) TCP soketiyle bağlanır.
    - `buyuk_dosya.txt` dosyasını 1 KiB’lik parçalar hâlinde gönderir.
    - Sunucu tarafında temel `server.py` dinleyicisi yeterlidir.

Kullanım
    python3 client.py
"""

import socket
import os

HOST = "127.0.0.1"
PORT = 5001
BUFSIZE = 1024
FILENAME = "buyuk_dosya.txt"

sock = socket.socket()
try:
    sock.connect((HOST, PORT))
except ConnectionRefusedError:
    print("⛔ Sunucuya bağlanılamadı − server.py çalışıyor mu?")
    exit(1)

if not os.path.isfile(FILENAME):
    print(f"⛔ Gönderilecek dosya bulunamadı: {FILENAME}")
    sock.close()
    exit(1)

with open(FILENAME, "rb") as f:
    while True:
        chunk = f.read(BUFSIZE)
        if not chunk:
            break
        try:
            sock.sendall(chunk)
        except BrokenPipeError:
            print("⛔ Bağlantı kesildi: Sunucu dosya almayı durdurdu.")
            break

print("✅ Dosya başarıyla gönderildi.")
sock.close()
