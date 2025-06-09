"""
İşlev
    - İstemci bağlandığında ilk paket olarak parola (PASSWORD) bekler.
    - Doğru parolayı doğrularsa 'OK' gönderir, yanlışsa 'ERROR' ve bağlantıyı kapatır.
    - Kimlik doğrulama başarılıysa gelen veriyi `gelen_dosya.txt` dosyasına kaydeder.

Gereksinim
    - İstemci tarafında parola ➝ dosya gönderen script (client_auth.py)
    - Port 5001’in başka süreç tarafından kullanılmıyor olması.

Kullanım
    python3 server_auth.py
"""

import socket

# ============================================================================
# Sabitler
# ============================================================================
PASSWORD    = "network2024"
HOST, PORT  = "0.0.0.0", 5001
OUTFILE     = "gelen_dosya.txt"
BUFSIZE     = 1024   #1 KiB

# ============================================================================
# Sunucuyu Kur
# ============================================================================
srv = socket.socket()
srv.bind((HOST, PORT))
srv.listen(1)
print(f"🌐 Sunucu dinleniyor... ({HOST}:{PORT})")

try:
    cli, addr = srv.accept()
    print(f"🔗 {addr} bağlandı.")

    # 1) Parola Al & Doğrula ────────────────────────────────────────────
    received_pwd = cli.recv(BUFSIZE).decode().strip()

    if received_pwd != PASSWORD:
        cli.send(b"ERROR")
        print("❌ Hatalı şifre! Bağlantı sonlandırıldı.")
        cli.close()
        srv.close()
        exit(1)

    cli.send(b"OK")
    print("✅ Kimlik doğrulama başarılı. Dosya alınıyor...")

    # 2) Dosyayı Kaydet ────────────────────────────────────────────────
    with open(OUTFILE, "wb") as f:
        while True:
            data = cli.recv(BUFSIZE)
            if not data:
                break
            f.write(data)

    print("📄 Dosya başarıyla alındı →", OUTFILE)

except Exception as exc:
    print("⛔ Sunucu hatası:", exc)

finally:
    cli.close()
    srv.close()
