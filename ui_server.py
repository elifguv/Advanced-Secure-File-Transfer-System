import PySimpleGUI as sg
import threading, socket, os

def start_server(log, host="0.0.0.0", port=5001, outfile="gelen_dosya.txt"):
    try:
        srv = socket.socket()
        srv.bind((host, port))
        srv.listen(1)
        log.print("Sunucu dinleniyor…")
        cli, addr = srv.accept()
        log.print(f"{addr} bağlandı.")
        with open(outfile, "wb") as f:
            while data := cli.recv(1024):
                f.write(data)
        log.print("✅ Dosya kaydedildi.")
        cli.close()
        srv.close()
    except Exception as e:
        log.print("❌ Hata:", e)

sg.theme("DarkGreen4")
layout = [
    [sg.Button("Dinlemeyi Başlat", key="-START-")],
    [sg.Multiline(size=(60, 10), key="-LOG-", disabled=True)]
]
window = sg.Window("Secure File Receiver", layout)

while True:
    event, _ = window.read(timeout=100)
    if event == sg.WINDOW_CLOSED:
        break
    if event == "-START-":
        threading.Thread(target=start_server, args=(window["-LOG-"],), daemon=True).start()
        window["-START-"].update(disabled=True)

window.close()
