"""
Amaç
    - AES‐EAX modu kullanarak dosya içeriklerini şifrelemek (encrypt_file)
    - Aynı anahtarla dosyayı geri çözmek (decrypt_file)

Gereksinimler
    pip install pycryptodome

Kullanım
    python3 aes_encrypt.py           # sifreleme.txt -> encrypted.bin -> ekran çıktısı
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ──────────────────────────────────────────────────────────
# 1) Dosya Şifreleme
# ──────────────────────────────────────────────────────────
def encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    input_path  : Şifrelenecek dosyanın yolu
    output_path : Şifrelenmiş veriyi (nonce|tag|ciphertext) tutacak dosya
    key         : 16-byte (128-bit) AES anahtarı
    """
    cipher = AES.new(key, AES.MODE_EAX)       #EAX = CTR + authentication
    with open(input_path, "rb") as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # dosyaya sırasıyla Nonce | Tag | Ciphertext yaz
    with open(output_path, "wb") as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

    print(f"🔒 {input_path} dosyası şifrelendi → {output_path}")

# ──────────────────────────────────────────────────────────
# 2) Dosya Çözme (verify + decrypt)
# ──────────────────────────────────────────────────────────
def decrypt_file(input_path: str, key: bytes) -> None:
    """
    input_path : İçinde Nonce|Tag|Ciphertext bulunan dosya
    key        : Aynı 16-byte AES anahtarı
    """
    with open(input_path, "rb") as f:
        nonce = f.read(16)          #16-byte nonce
        tag   = f.read(16)          #16-byte auth tag
        ciphertext = f.read()       #kalan hepsi şifreli veri

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    print("🔓 Çözülen içerik:\n" + plaintext.decode())

# ──────────────────────────────────────────────────────────
# 3) Komut satırından doğrudan çalıştırıldığında demo yap
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    key = get_random_bytes(16)                          #128-bit rastgele anahtar
    encrypt_file("sifreleme.txt", "encrypted.bin", key) #demo şifreleme
    decrypt_file("encrypted.bin", key)                  #demo çözme
