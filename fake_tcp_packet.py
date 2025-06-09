from scapy.all import IP, TCP, send

ip = IP(dst="127.0.0.1")  # hedef IP (localhost)
tcp = TCP(sport=44444, dport=5001, flags="S", seq=12345)

packet = ip / tcp
send(packet)
print("⚠️ Sahte TCP SYN paketi gönderildi (enjeksiyon testi).")
