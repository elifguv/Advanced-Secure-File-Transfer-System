from scapy.all import IP, ICMP, send

# DF (Don't Fragment) bayrağı set edilmiş bir ICMP paketi oluştur
ip = IP(dst="8.8.8.8", flags="DF") 
icmp = ICMP()
packet = ip / icmp

send(packet)
print("✅ DF flag'li ICMP paketi gönderildi.")
