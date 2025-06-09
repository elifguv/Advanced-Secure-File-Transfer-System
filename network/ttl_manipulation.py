"""
Amaç
    - Scapy kullanarak özel TTL (Time-To-Live) değeri atanmış bir ICMP Echo (ping) paketi oluşturmak ve ağ üzerinden göndermek.
    - Gönderim sonrası kullanılan TTL’i konsola yazdırmak.

Gereksinim
    pip install scapy (macOS’ta: sudo python3 -m pip install scapy  &&  sudo python3 ttl_manipulation.py)

Not
    - Bu script yalnızca gönderir; yanıtı dinlemez.
    - root / sudo yetkisi gerekebilir (ham paket oluşturma nedeniyle).
"""

from scapy.all import IP, ICMP, send

# ============================================================================
# 1) IP + ICMP paketini oluştur
# ============================================================================
DST_IP = "8.8.8.8"      #hedef (Google DNS)
CUSTOM_TTL = 64         #TTL değeri (hop sayısı limiti)

ip_layer    = IP(dst=DST_IP, ttl=CUSTOM_TTL)  #IP başlığı + TTL
icmp_layer  = ICMP()                          #ICMP Echo Request

packet = ip_layer / icmp_layer                #katmanları birleştir

# ============================================================================
# 2) Paketi gönder
# ============================================================================
# send()  : Scapy ham paket gönderimi; verbose=0 sessiz mod için
send(packet, verbose=0)

print(f"✅ TTL değeri: {CUSTOM_TTL} — paket {DST_IP} adresine gönderildi.")
