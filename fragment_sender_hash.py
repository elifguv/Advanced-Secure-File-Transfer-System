import socket
import hashlib
import os, sys

def sha256_hash(filepath):
    """Verilen dosyanın SHA-256 özetini döndürür (hex)."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def split_file(filename, chunk_size=256 * 1024):
    """Dosyayı bellek yerine liste-liste parçalamaz, parça parça yield eder."""
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# ──────────────────────────────────────────────────────────────
#  ANA FONKSİYON:  GUI'den çağırmak için send_file(path, …)
# ──────────────────────────────────────────────────────────────
PASSWORD = "network2025"          #sunucudaki PASSWORD ile bire bir aynı olmalı

def send_file(
    filepath: str,
    host: str = "127.0.0.1",
    port: int = 5001,
    chunk: int = 256 * 1024,
) -> bool:
    # ------------------------------------------------------------
    if not os.path.isfile(filepath):
        print("⛔ Dosya bulunamadı:", filepath)
        return False

    try:
        sock = socket.socket()
        sock.connect((host, port))

        # 1) PAROLA GÖNDER  ────────────────────────────────
        sock.send(PASSWORD.encode())     #parola yolla
        ack = sock.recv(2)               #'OK' bekle
        if ack != b"OK":
            print("⛔ Sunucu şifreyi reddetti!")
            sock.close()
            return False

        # 2) SHA-256 HASH GÖNDER  ─────────────────────────
        file_hash = sha256_hash(filepath)
        sock.send(file_hash.encode())
        ack = sock.recv(2)               #yine 'OK' bekle
        if ack != b"OK":
            print("⛔ Sunucu hash'i reddetti!")
            sock.close()
            return False

        # 3) DOSYA PARÇALARINI GÖNDER  ────────────────────
        total_parts = (os.path.getsize(filepath) + chunk - 1) // chunk
        for idx, part in enumerate(split_file(filepath, chunk)):
            percent = (idx + 1) / total_parts * 100          # % ilerleme
            print(f"🟢 Parça {idx+1}/{total_parts}  ({percent:5.1f} %)") 
            sock.sendall(part)

        sock.shutdown(socket.SHUT_WR)
        sock.close()
        return True, "Hash onaylandı, dosya gönderildi."

    except Exception as exc:
        print("⛔ Gönderim hatası:", exc)
        return False, f"Gönderim hatası: {exc}"
# ————————————————————————————————————————————
# terminalden doğrudan çalıştırmak için
# ————————————————————————————————————————————
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 fragment_sender_hash.py <dosya_yolu>")
        sys.exit(1)

    ok = send_file(sys.argv[1])
    print("✅ Tamamlandı" if ok else "❌ Başarısız")
