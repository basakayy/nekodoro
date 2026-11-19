import threading
import time
import winsound

NOTALAR = {
    "DO": 523,
    "RE": 587,
    "MI": 659,
    "FA": 698,
    "SOL": 784,
    "LA": 880,
    "SI": 988,
    "DO2": 1047,
}

CALISMA_BITTI = [
    ("DO", 120), ("MI", 120), ("SOL", 120), ("DO2", 250),
    ("SUS", 80), ("SOL", 120), ("DO2", 350),
]

MOLA_BITTI = [
    ("SOL", 180), ("MI", 180), ("DO", 180), ("SUS", 80), ("RE", 150), ("DO", 350),
]

SU_ZAMANI = [
    ("SOL", 70), ("DO2", 70), ("SUS", 60), ("SOL", 70), ("DO2", 120),
]

MELODILER = {
    "calisma_bitti": CALISMA_BITTI,
    "mola_bitti": MOLA_BITTI,
    "su": SU_ZAMANI,
}

SES_SECENEKLERI = ["Melodi", "Zil", "Sessiz"]


def _melodi_cal(melodi):
    for nota, sure in melodi:
        if nota == "SUS":
            time.sleep(sure / 1000)
        else:
            winsound.Beep(NOTALAR[nota], sure)


def cal_sesi(secim, olay):
    if secim == "Sessiz":
        return
    if secim == "Zil":
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        return

    # Beep bloklayıcı olduğu için arayüz donmasın diye ayrı thread'de çalınıyor
    threading.Thread(target=_melodi_cal, args=(MELODILER[olay],), daemon=True).start()
