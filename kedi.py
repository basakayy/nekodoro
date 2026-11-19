import math

P = 4

RENKLER = {
    "K": "#1c1a21",
    "B": "#3d424b",
    "O": "#585f6a",
    "o": "#eceef2",
    "R": "#ff5a3c",
    "r": "#ff9a85",
    "D": "#c9361f",
    "G": "#3fae4a",
    "P": "#ffadb5",
    "N": "#f07c8c",
    "S": "#ffffff",
    "U": "#5aa9f0",
    "u": "#bfe1ff",
}

ARKA_PLAN = "#f3f7fc"
DAMA_RENKLERI = ["#ffffff", "#d3e3f6"]
DAMA_BOYUTU = 4 * P
CIZGI_RENGI = RENKLER["K"]
SAPKA_RENGI = RENKLER["R"]
PIKSEL_FONT = "Consolas"
CIMEN = ["#7cc96b", "#6bb85b"]
TOPRAK = ["#c98e5a", "#b97d4b"]

KAFA = [
    ".......GG.......",
    "..G...GGGG...G..",
    "...GGKGGGGKGG...",
    "..KRGGRGGRGGRK..",
    ".KRrRRRRRRRRRRK.",
    "KRrRRRRRRRRRRRRK",
    "KRrRRKKKKKKRRRRK",
    "KRRKOOOOOOOOKRRK",
    "KRKOOOOOOOOOOKRK",
    "KRKOOKSOOKSOOKRK",
    "KRKOOKKooKKOOKRK",
    "KRKOPooNNooPOKRK",
    "KRRKOoKooKoOKRRK",
    ".KRRKOoKKoOKRRK.",
    ".KDRRKooooKRRDK.",
    "OOKDDRKKKKRDDK..",
    "OOOKKKKKKKKKK...",
]

KAFA_GOZ_KAPALI = KAFA[:9] + ["KRKOOOOOOOOOOKRK"] + KAFA[10:]

GOVDE_SOL = [
    "............",
    "............",
    "............",
    ".K..........",
    "KBK.........",
    "KOK.........",
    "KOK.........",
    "KOK.........",
    "KOK.........",
    "KOK.........",
    "KOKKKKKKKKKK",
    "KOOOOOOOOOOO",
    ".KOOOOOOOOOO",
    ".KOOOOOOOOOO",
    ".KOOOOOOOOOO",
    ".KOOOOOOOOOO",
    ".KOOOOOOOOOO",
]

GOVDE_ALT = [
    ".KOOOOOOOOOOOOOOOK..........",
    "..KBBOOOOOOOOOOBBK..........",
    "...KOOKOOKKKKOOKOOK.........",
]

BACAKLAR_1 = [
    "...KOOKOOK..KOOKOOK.........",
    "...KooKooK..KooKooK.........",
    "...KKKKKKK..KKKKKKK.........",
]

BACAKLAR_2 = [
    "...KOOKOOK..KOOKOOK.........",
    "...KKKKooK..KKKKooK.........",
    "......KKKK.....KKKK.........",
]

UYKU_GOVDE_1 = [
    "..............",
    "..............",
    "..............",
    "..............",
    "..............",
    "..............",
    "..............",
    "..............",
    "....KKKKKKKKKK",
    "..KKOOOOOOOOOO",
    ".KOOOOOOOOOOOO",
    "KOOOOOOOOOOOOO",
    "KOOOOOOOOOOOOO",
    "KBOOOOOOOOOOOO",
    "KBBKKKKKKKOOOO",
    "KBKOOOOOOOKOOO",
    ".KKKKKKKKKKKKK",
]

UYKU_GOVDE_2 = UYKU_GOVDE_1[:8] + [
    "..KKKKKKKKKKKK",
    ".KOOOOOOOOOOOO",
] + UYKU_GOVDE_1[10:]

UYKU_KAFA = KAFA_GOZ_KAPALI[:16] + ["KKKKKKKKKKKKK..."]


def yan_yana(sol, sag):
    return [sol_satir + sag_satir for sol_satir, sag_satir in zip(sol, sag)]


AYAKTA = yan_yana(GOVDE_SOL, KAFA) + GOVDE_ALT + BACAKLAR_1
YURUME_2 = yan_yana(GOVDE_SOL, KAFA) + GOVDE_ALT + BACAKLAR_2
GOZ_KIRPMA = yan_yana(GOVDE_SOL, KAFA_GOZ_KAPALI) + GOVDE_ALT + BACAKLAR_1
UYKU_1 = yan_yana(UYKU_GOVDE_1, UYKU_KAFA)
UYKU_2 = yan_yana(UYKU_GOVDE_2, UYKU_KAFA)

Z_HARFI = [
    "KKKK",
    "..K.",
    ".K..",
    "KKKK",
]

SU_BARDAGI = [
    "K....K",
    "KSSSSK",
    "KUUUUK",
    "KUuUUK",
    "KUuUUK",
    ".KUUK.",
    ".KKKK.",
]

SU_METNI = "Su içme zamanı! Bir bardak su iç, ben de içiyorum."

BALON_KUYRUGU = [
    "KSSK",
    "KSK.",
    "KK..",
]

HAREKETLI = "hareketli"


class Kedi:
    def __init__(self, tuval, genislik, yukseklik, balon_y=10):
        self.tuval = tuval
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.balon_y = balon_y

        self.durum = "bekle"
        self.x = genislik / 2
        self.zemin_y = yukseklik - 4 * P
        self.yon = 1
        self.kare = 0
        self.balon_metni = None
        self.su_kalan_kare = 0

        self._arka_plan_ciz()
        self._animasyon_dongusu()

    def durum_degistir(self, yeni_durum):
        self.durum = yeni_durum
        if yeni_durum != "mola":
            self.x = self.genislik / 2
            self.yon = 1

    def konus(self, metin):
        self.balon_metni = metin

    def sus(self):
        self.balon_metni = None

    def su_hatirlat(self, saniye=15):
        self.su_kalan_kare = saniye * 20

    def _animasyon_dongusu(self):
        self.kare += 1
        self.tuval.delete(HAREKETLI)

        if self.durum == "uyku":
            self._uyuyan_kedi()
        elif self.durum == "mola":
            self._mola_hareketi()
        else:
            sprite = GOZ_KIRPMA if self.kare % 80 < 3 else AYAKTA
            self._sprite_ciz(sprite, self.x, self.zemin_y)

        if self.su_kalan_kare > 0:
            self.su_kalan_kare -= 1
            self._su_bardagi_ciz()
            self._balon_ciz(SU_METNI)
        elif self.balon_metni:
            self._balon_ciz(self.balon_metni)

        self._cerceve_ciz()
        self.tuval.after(50, self._animasyon_dongusu)

    def _mola_hareketi(self):
        self.x += P / 2 * self.yon
        kenar = 16 * P
        if self.x > self.genislik - kenar:
            self.yon = -1
        elif self.x < kenar:
            self.yon = 1

        zipliyor = (self.kare // 60) % 2 == 1
        yukseklik = 0
        if zipliyor:
            yukseklik = abs(math.sin(self.kare * 0.2)) * 6 * P

        if zipliyor and yukseklik > 5:
            sprite = YURUME_2
        elif (self.kare // 4) % 2 == 0:
            sprite = AYAKTA
        else:
            sprite = YURUME_2

        self._golge_ciz(self.x)
        self._sprite_ciz(sprite, self.x, self.zemin_y - yukseklik)

    def _uyuyan_kedi(self):
        sprite = UYKU_1 if (self.kare // 30) % 2 == 0 else UYKU_2
        self._sprite_ciz(sprite, self.x, self.zemin_y)

        for i in range(3):
            ilerleme = ((self.kare + i * 25) % 75) / 75
            zx = self.x + 15 * P + ilerleme * 4 * P
            zy = self.zemin_y - 17 * P - ilerleme * 10 * P
            boyut = 2 if ilerleme < 0.5 else 3
            self._sprite_ciz(Z_HARFI, zx, zy, piksel=boyut, ortala=False)

    def _sprite_ciz(self, sprite, orta_x, alt_y, piksel=P, ortala=True):
        genislik = len(sprite[0]) * piksel
        yukseklik = len(sprite) * piksel
        if ortala:
            x0, y0 = orta_x - genislik / 2, alt_y - yukseklik
        else:
            x0, y0 = orta_x, alt_y
        x0 = int(x0 // piksel) * piksel
        y0 = int(y0 // piksel) * piksel

        for satir_no, satir in enumerate(sprite):
            if self.yon == -1 and ortala:
                satir = satir[::-1]
            y = y0 + satir_no * piksel

            # Aynı renkteki ardışık pikseller tek dikdörtgen olarak çiziliyor
            sutun = 0
            while sutun < len(satir):
                harf = satir[sutun]
                bitis = sutun
                while bitis < len(satir) and satir[bitis] == harf:
                    bitis += 1
                if harf != ".":
                    self.tuval.create_rectangle(
                        x0 + sutun * piksel, y,
                        x0 + bitis * piksel, y + piksel,
                        fill=RENKLER[harf], outline="", tags=HAREKETLI)
                sutun = bitis

    def _arka_plan_ciz(self):
        for satir, y in enumerate(range(0, self.zemin_y, DAMA_BOYUTU)):
            for sutun, x in enumerate(range(0, self.genislik, DAMA_BOYUTU)):
                renk = DAMA_RENKLERI[(satir + sutun) % 2]
                self.tuval.create_rectangle(x, y, x + DAMA_BOYUTU, y + DAMA_BOYUTU,
                                            fill=renk, outline="")

        satir_sayisi = (self.yukseklik - self.zemin_y) // P + 1
        for satir in range(satir_sayisi):
            renkler = CIMEN if satir < 2 else TOPRAK
            y = self.zemin_y + satir * P
            for sutun in range(self.genislik // P + 1):
                renk = renkler[(sutun + satir) % 2]
                x = sutun * P
                self.tuval.create_rectangle(x, y, x + P, y + P, fill=renk, outline="")

    def _cerceve_ciz(self):
        self.tuval.create_rectangle(2, 2, self.genislik - 2, self.yukseklik - 2,
                                    outline=RENKLER["K"], width=4, tags=HAREKETLI)

    def _su_bardagi_ciz(self):
        ziplama = P if (self.kare // 10) % 2 == 0 else 0
        eski_yon = self.yon
        self.yon = 1
        self._sprite_ciz(SU_BARDAGI, 10 * P, self.zemin_y - ziplama)
        self.yon = eski_yon

    def _golge_ciz(self, orta_x):
        x0 = int((orta_x - 10 * P) // P) * P
        self.tuval.create_rectangle(x0, self.zemin_y, x0 + 20 * P, self.zemin_y + P,
                                    fill="#4f9a42", outline="", tags=HAREKETLI)

    def _balon_ciz(self, metin):
        sol, sag = 10, self.genislik - 10
        ust = self.balon_y
        alt = ust + 46
        k = RENKLER["K"]
        e = {"outline": "", "tags": HAREKETLI}

        self.tuval.create_rectangle(sol + P, ust, sag - P, alt, fill=k, **e)
        self.tuval.create_rectangle(sol, ust + P, sag, alt - P, fill=k, **e)
        self.tuval.create_rectangle(sol + P, ust + P, sag - P, alt - P, fill="white", **e)

        kuyruk_x = max(sol + 3 * P, min(sag - 6 * P, self.x + 7 * P * self.yon))
        eski_yon = self.yon
        self.yon = 1
        self._sprite_ciz(BALON_KUYRUGU, kuyruk_x, alt - P, ortala=False)
        self.yon = eski_yon

        self.tuval.create_text((sol + sag) / 2, (ust + alt) / 2, text=metin,
                               fill=k, font=(PIKSEL_FONT, -13, "bold"),
                               width=sag - sol - 24, justify="center", tags=HAREKETLI)
