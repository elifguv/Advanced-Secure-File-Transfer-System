"""
PySimpleGUI tabanlı “Secure File Sender” arayüzü
     1. Kullanıcı bir dosya seçer (FileBrowse)
     2. “Gönder” düğmesine tıklandığında send_file(filepath) fonksiyonu çağrılır
        – Bu fonksiyon fragment_sender_hash.send_file() olup,
            • parola ➝ hash ➝ dosya parçaları gönderir
            • (True, msg) veya sadece True/False döndürür
     3. İşlem durumu log penceresinde gösterilir.

Gereksinim
    pip install PySimpleGUI
    fragment_sender_hash.send_file() fonksiyonunun import edilebilir olması.

Kullanım
    python3 ui_client.py
"""

import PySimpleGUI as sg
from auth.fragment_sender_hash import send_file  #send_file(path) -> bool | (bool, str)

# ─────────────────────────────────────────────────────────────
# 1) Tema & Layout
# ─────────────────────────────────────────────────────────────
sg.theme("DarkBlue3")

layout = [
    [sg.Text("Seçilecek dosya:"), sg.Input(key="-FILE-", expand_x=True), sg.FileBrowse("Gözat")],
    [sg.Button("Gönder", key="-SEND-")],
    [sg.Multiline(size=(60, 10), key="-LOG-", disabled=True, autoscroll=True)],
]

window = sg.Window("Secure File Sender", layout, finalize=True)

# ─────────────────────────────────────────────────────────────
# 2) Event Loop
# ─────────────────────────────────────────────────────────────
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    #Dosya gönderim işlemi
    if event == "-SEND-":
        filepath = values["-FILE-"]
        if not filepath:
            sg.popup_error("Önce bir dosya seç!")
            continue

        window["-LOG-"].print(f"📤 Gönderim başladı: {filepath}")
        try:
            ok, *msg = send_file(filepath) if isinstance(send_file(filepath), tuple) else (send_file(filepath),)
            msg_text = msg[0] if msg else ("Tamamlandı" if ok else "Hata")
            window["-LOG-"].print(("✅ " if ok else "❌ ") + msg_text + "\n")
        except Exception as exc:
            window["-LOG-"].print(f"❌ Hata: {exc}\n")

window.close()
