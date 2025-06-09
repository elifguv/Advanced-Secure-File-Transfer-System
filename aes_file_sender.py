"""
Amaç
    - Önceden AES-EAX ile şifrelenmiş `encrypted.bin` dosyasını
      TCP soketi üzerinden sunucuya (127.0.0.1:5001) göndermek.

Gereksinim
    - Sunucu tarafında 5001 portunda dinleyen bir alıcı
    - encrypted.bin dosyası bu dizinde mevcut olmalı.

Kullanım
    python3 aes_file_sender.py
"""

import socket

#sunucu adresi ve portu
HOST = "127.0.0.1"
PORT = 5001
BUFSIZE = 1024          #1 KiB parça boyutu

#1) Soketi oluştur ve bağlan
client_socket = socket.socket()
client_socket.connect((HOST, PORT))

#2) Şifreli dosyayı parça parça oku & gönder
with open("encrypted.bin", "rb") as f:
    while chunk := f.read(BUFSIZE):
        client_socket.sendall(chunk)

print("✅  Şifreli dosya gönderildi.")

#3) Bağlantıyı kapat
client_socket.close()
