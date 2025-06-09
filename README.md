# 📥 Gelişmiş Dosya Transfer Sistemi  
Bilgisayar Ağları dersi dönem projesi – 2024-2025  

 **Amaç:**  
 
Dosya transferi sırasında gizlilik, bütünlük ve erişim kontrolü sağlamak; aynı zamanda düşük seviye IP başlık manipülasyonlarını ve ağ performans testlerini deneyimlemek.   

---

## İçerik & Özellikler
| Modül | Açıklama |
|-------|----------|
| **core/** | `client.py` & `server.py` – temel TCP dosya gönderimi |
| **encryption/** | `aes_encrypt.py`, `aes_file_sender.py` – AES-EAX ile şifreleme ve şifreli dosya iletimi :contentReference[oaicite:1]{index=1} |
| **auth/** | `client_auth.py`, `server_auth.py` – parola tabanlı kimlik doğrulama; `fragment_sender_hash.py`, `server_auth_hash.py` – SHA-256 bütünlük kontrolü 
| **fragmentation/** | `fragment_sender.py` – 256 KB parçalama; sunucuda dosya birleştirme|
| **network/** | `df_flag_packet.py`, `ttl_manipulation.py`, `checksum.py`, `ping_test.py`, `fake_tcp_packet.py` – DF bayrağı, TTL & checksum hesaplama, sahte paket üretimi  |
| **ui/** | `ui_client.py` (PySimpleGUI) – tek tıkla gönderim, canlı log; `ui_server.py` – basit sunucu konsolu |
| **data/** | Örnek dosyalar (`buyuk_dosya.txt`, `encrypted.bin`, vb.) |

Ek olarak:  
* **Wireshark** filtreleri ile trafik analizi ve **tc/netem** ile %10–20 paket kaybı senaryoları 
* **MITM** tehdit modellemesi (pasif) ve geliştirme alanları listesi  

---

## Gereksinimler
| Yazılım / Kütüphane |
|--------------------|
| Python ≥ 3.11 |
| `pycryptodome` |
| `scapy` |
| `pysimplegui` |
| `iproute2` (tc için, yalnızca Linux) |
| `Wireshark` (opsiyonel, analiz için) |

> **Not:** Windows’ta Scapy ham soket kısıtlamaları nedeniyle bazı ağ testleri çalışmayabilir.

---

## Kurulum
```bash
# 1) Depoyu klonlayın

# 2) Sanal ortam oluşturun
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate

# 3) Gereksinimleri yükleyin
pip install -r requirements.txt     # yoksa manuel: pip install pycryptodome scapy pysimplegui
```
## Çalıştırma

1. **Sunucuyu başlatın**
   ```bash
   python core/server.py           # Konsol sürümü
   # veya
   python ui/ui_server.py          # GUI sürümü
   ```

2. **(İsteğe bağlı) Şifreli dosya oluşturun**

   ```bash
   python encryption/aes_encrypt.py data/sifreleme.txt
   ```

3. **İstemciyi çalıştırın**
   ```bash
    # Düz metin dosyası gönderimi
    python core/client.py data/buyuk_dosya.txt
   
    # Şifreli dosya gönderimi
    python encryption/aes_file_sender.py data/encrypted.bin

    # veya GUI istemci
    python ui/ui_client.py
    ``` 

> İstemci ve sunucu aynı makinede ise varsayılan localhost:5001 kullanılır.
Farklı bir IP/port gerekiyorsa ilgili dosyalardaki HOST / PORT değişkenlerini güncelleyin.

## Test Senaryoları

| Senaryo               | Nasıl?                                                                                                   | Beklenen Sonuç                                         |
|-----------------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| **Kimlik doğrulama**  | Yanlış parola girin                                                                                      | Sunucu bağlantıyı kapatır                              |
| **Bütünlük**          | Gönderim sonrası SHA-256 eşleşmesini kontrol edin                                                        | Hash değerleri aynıdır                                 |
| **DF bayrağı**        | `python network/df_flag_packet.py`                                                                       | Wireshark filtresi `ip.flags.df==1` paketi gösterir    |
| **TTL sınırı**        | `python network/ttl_manipulation.py` ile `TTL=2`                                                         | Paket hedefe ulaşmadan düşer                           |
| **%10 paket kaybı**   | `sudo tc qdisc add dev <iface> root netem loss 10%`                                                      | Transfer yeniden denemelerle tamamlanır                |
| **%20 paket kaybı**   | `sudo tc qdisc add dev <iface> root netem loss 20%`                                                      | SHA-256 doğrulaması **başarısız** olur                 |
