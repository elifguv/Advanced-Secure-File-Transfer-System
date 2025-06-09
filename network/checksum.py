"""
IPv4 başlıkları için 16-bit İnternet Checksum hesaplaması.

Algoritma:
    1. Veriyi 16-bit (2 byte) bloklar hâlinde topla
    2. Taşan 16-bitleri alta ekle (carry wrap-around)
    3. Sonucu bire tamamla  (one’s complement)

Referans: RFC 1071 – Computing the Internet Checksum
"""

from typing import ByteString

def checksum(data: ByteString) -> int:
    """
    IPv4 / TCP / UDP başlıklarında kullanılan 16-bit checksum döndürür.

    Parameters
    ----------
    data : bytes or bytearray
        Kontrol toplamı hesaplanacak ham bayt dizisi

    Returns
    -------
    int
        0–0xFFFF arası 16-bit checksum (Big-Endian)
    """
    total = 0

    #1) 16-bit bloklar hâlinde topla
    for i in range(0, len(data), 2):
        hi = data[i]            << 8    # üst byte
        lo = data[i + 1] if i + 1 < len(data) else 0
        total += hi + lo

    #2) Carry wrap-around (16 bit üzerinde taşanlar eklenir)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    #3) One’s complement: bit-wise NOT & 0xFFFF
    return (~total) & 0xFFFF


# ───────────────────────────────────────────────────────────
#  Demo / Hızlı Test
# ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    #örnek IPv4 başlığı (20 byte) – 0x0000 checksum alanı dahil
    sample = (
        b"\x45\x00\x00\x28"    #Version/IHL, DSCP/ECN, Total Length
        b"\x1c\x46\x40\x00"    #Identification, Flags/Fragment
        b"\x40\x06\x00\x00"    #TTL, Protocol (TCP), Checksum=0x0000
        b"\xc0\xa8\x00\x68"    #Source IP: 192.168.0.104
        b"\xc0\xa8\x00\x01"    #Dest   IP: 192.168.0.1
    )

    print(f"Checksum: 0x{checksum(sample):04X}")
