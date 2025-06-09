"""
İşlev
    - İstemciden (client.py / fragment_sender.py) dosya almak.
    - İstemci ilk olarak gönderilen SHA-256 hash değerini iletir.
    - Sunucu 'OK' cevabı verdikten sonra dosya parçalarını kabul eder.
    - Dosya alındıktan sonra kendi hesapladığı özet ile beklenen özeti karşılaştırarak bütünlüğü doğrular.

Gereksinim
    - 5001 portu başka bir süreç tarafından kullanılmamalı.
    - İstemci aynı sırada: hash ➝ dosya gönderiyor olmalı.

Kullanım
    python3 server.py
"""
import socket

HOST = "0.0.0.0"
PORT = 5001
FILENAME = "gelen_dosya.txt"

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"🌐 Sunucu dinleniyor... ({HOST}:{PORT})")
client_socket, addr = server_socket.accept()
print(f"🔗 {addr} bağlandı.")

with open(FILENAME, "wb") as f:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        f.write(data)

print("✅ Dosya başarıyla alındı.")
client_socket.close()
server_socket.close()
