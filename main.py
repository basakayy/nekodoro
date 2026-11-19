import ctypes
import sys
import tkinter as tk
from ctypes import wintypes

import customtkinter as ctk

from kedi import Kedi, ARKA_PLAN, CIZGI_RENGI, SAPKA_RENGI, PIKSEL_FONT
from sesler import cal_sesi, SES_SECENEKLERI

if "--test" in sys.argv:
    CALISMA_SURESI = 10
    MOLA_SURESI = 10
    SU_ARALIGI = 15
else:
    CALISMA_SURESI = 25 * 60
    MOLA_SURESI = 5 * 60
    SU_ARALIGI = 30 * 60

SAHNE_GENISLIK = 270
SAHNE_YUKSEKLIK = 210
BALON_Y = 48

DUGME_RENGI = SAPKA_RENGI
DUGME_UZERINDE = "#e5533a"
IKINCI_DUGME = "#d3e3f6"
IKINCI_DUGME_UZERINDE = "#b9d1ee"


def calisma_alani():
    # Görev çubuğu hariç ekran alanı: (sol, üst, sağ, alt)
    alan = wintypes.RECT()
    SPI_GETWORKAREA = 0x0030
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(alan), 0)
    return alan.left, alan.top, alan.right, alan.bottom


def sure_metni(toplam_saniye):
    saat, kalan = divmod(toplam_saniye, 3600)
    dakika = kalan // 60
    if saat > 0:
        return f"{saat} sa {dakika} dk"
    return f"{dakika} dk"


class NekodoroUygulamasi(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nekodoro")
        self.resizable(False, False)
        self.configure(fg_color=CIZGI_RENGI)
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.asama = "hazir"
        self.kalan_saniye = CALISMA_SURESI
        self.calisiyor_mu = False
        self.zamanlayici = None

        self.tur = 1
        self.toplam_calisma = 0
        self.su_sayaci = 0

        self.surukle_x = 0
        self.surukle_y = 0

        self._arayuzu_kur()
        self.kedi.konus("Merhaba, ben Neko! Hazır olunca Başlat'a bas.")
        self._ekrani_guncelle()
        self._sag_alt_koseye_yerles()

    def _arayuzu_kur(self):
        ic_kutu = ctk.CTkFrame(self, fg_color=ARKA_PLAN, corner_radius=0)
        ic_kutu.pack(padx=3, pady=3)

        self.tuval = tk.Canvas(
            ic_kutu,
            width=SAHNE_GENISLIK,
            height=SAHNE_YUKSEKLIK,
            bg=ARKA_PLAN,
            highlightthickness=0,
            cursor="fleur",
        )
        self.tuval.pack(padx=6, pady=(6, 5))
        self.kedi = Kedi(self.tuval, SAHNE_GENISLIK, SAHNE_YUKSEKLIK, balon_y=BALON_Y)

        self.tuval.bind("<ButtonPress-1>", self._surukleme_basladi)
        self.tuval.bind("<B1-Motion>", self._surukleniyor)

        self.sure_yazisi = self.tuval.create_text(
            12, 8, anchor="nw", text="25:00", fill=CIZGI_RENGI,
            font=(PIKSEL_FONT, -32, "bold"),
        )
        self.asama_yazisi = self.tuval.create_text(
            SAHNE_GENISLIK - 30, 12, anchor="ne", text="", fill=SAPKA_RENGI,
            font=(PIKSEL_FONT, -13, "bold"),
        )
        self.istatistik_yazisi = self.tuval.create_text(
            SAHNE_GENISLIK - 30, 30, anchor="ne", text="", fill=CIZGI_RENGI,
            font=(PIKSEL_FONT, -12),
        )

        kapat = self.tuval.create_text(
            SAHNE_GENISLIK - 12, 6, anchor="ne", text="x", fill=CIZGI_RENGI,
            font=(PIKSEL_FONT, -16, "bold"), tags="kapat",
        )
        self.tuval.tag_bind("kapat", "<Button-1>", lambda olay: self.destroy())
        self.tuval.tag_bind("kapat", "<Enter>",
                            lambda olay: self.tuval.itemconfigure(kapat, fill=SAPKA_RENGI))
        self.tuval.tag_bind("kapat", "<Leave>",
                            lambda olay: self.tuval.itemconfigure(kapat, fill=CIZGI_RENGI))

        dugmeler = ctk.CTkFrame(ic_kutu, fg_color="transparent")
        dugmeler.pack(pady=(0, 8))

        self.baslat_dugmesi = ctk.CTkButton(
            dugmeler,
            text="Başlat",
            width=72,
            height=28,
            corner_radius=0,
            border_width=2,
            border_color=CIZGI_RENGI,
            font=ctk.CTkFont(PIKSEL_FONT, 13, "bold"),
            fg_color=DUGME_RENGI,
            hover_color=DUGME_UZERINDE,
            command=self.baslat_duraklat,
        )
        self.baslat_dugmesi.pack(side="left", padx=3)

        sifirla_dugmesi = ctk.CTkButton(
            dugmeler,
            text="Sıfırla",
            width=60,
            height=28,
            corner_radius=0,
            border_width=2,
            border_color=CIZGI_RENGI,
            font=ctk.CTkFont(PIKSEL_FONT, 13, "bold"),
            fg_color=IKINCI_DUGME,
            hover_color=IKINCI_DUGME_UZERINDE,
            text_color=CIZGI_RENGI,
            command=self.sifirla,
        )
        sifirla_dugmesi.pack(side="left", padx=3)

        self.ses_secimi = ctk.StringVar(value="Melodi")
        ses_menusu = ctk.CTkOptionMenu(
            dugmeler,
            values=SES_SECENEKLERI,
            variable=self.ses_secimi,
            width=72,
            height=28,
            corner_radius=0,
            font=ctk.CTkFont(PIKSEL_FONT, 12),
            dropdown_font=ctk.CTkFont(PIKSEL_FONT, 12),
            fg_color=IKINCI_DUGME,
            button_color=IKINCI_DUGME_UZERINDE,
            button_hover_color="#a3c2e8",
            text_color=CIZGI_RENGI,
            command=self._ses_onizle,
        )
        ses_menusu.pack(side="left", padx=3)

    def _sag_alt_koseye_yerles(self):
        self.update_idletasks()
        _, _, sag, alt = calisma_alani()
        x = sag - self.winfo_reqwidth()
        y = alt - self.winfo_reqheight()
        self.geometry(f"+{x}+{y}")

    def _surukleme_basladi(self, olay):
        self.surukle_x = olay.x_root - self.winfo_x()
        self.surukle_y = olay.y_root - self.winfo_y()

    def _surukleniyor(self, olay):
        x = olay.x_root - self.surukle_x
        y = olay.y_root - self.surukle_y
        self.geometry(f"+{x}+{y}")

    def baslat_duraklat(self):
        if self.calisiyor_mu:
            self._durdur()
            self.kedi.durum_degistir("bekle")
            self.kedi.konus("Mola mı? Bekliyorum...")
        else:
            if self.asama == "hazir":
                self.asama = "calisma"
            self._kediyi_asamaya_gore_ayarla()
            self.calisiyor_mu = True
            self.zamanlayici = self.after(1000, self._tik)
        self._ekrani_guncelle()

    def _ses_onizle(self, secim):
        cal_sesi(secim, "calisma_bitti")

    def sifirla(self):
        self._durdur()
        self.asama = "hazir"
        self.kalan_saniye = CALISMA_SURESI
        self.kedi.durum_degistir("bekle")
        self.kedi.konus("Hazır olunca Başlat'a bas.")
        self._ekrani_guncelle()

    def _tik(self):
        if self.kalan_saniye <= 0:
            self._asama_bitti()
        else:
            self.kalan_saniye -= 1
            if self.asama == "calisma":
                self._su_kontrol()
        self._ekrani_guncelle()
        if self.calisiyor_mu:
            self.zamanlayici = self.after(1000, self._tik)

    def _su_kontrol(self):
        self.su_sayaci += 1
        if self.su_sayaci >= SU_ARALIGI:
            self.su_sayaci = 0
            self.kedi.su_hatirlat()
            cal_sesi(self.ses_secimi.get(), "su")

    def _durdur(self):
        self.calisiyor_mu = False
        if self.zamanlayici is not None:
            self.after_cancel(self.zamanlayici)
            self.zamanlayici = None

    def _asama_bitti(self):
        self._pencereyi_one_getir()

        if self.asama == "calisma":
            cal_sesi(self.ses_secimi.get(), "calisma_bitti")
            self.toplam_calisma += CALISMA_SURESI
            self.asama = "mola"
            self.kalan_saniye = MOLA_SURESI
            self._kediyi_asamaya_gore_ayarla()
        else:
            cal_sesi(self.ses_secimi.get(), "mola_bitti")
            self.tur += 1
            self.calisiyor_mu = False
            self.asama = "hazir"
            self.kalan_saniye = CALISMA_SURESI
            self.kedi.durum_degistir("bekle")
            self.kedi.konus("Mola bitti! Hazırsan yeni bir tur başlatalım.")

    def _kediyi_asamaya_gore_ayarla(self):
        if self.asama == "calisma":
            self.kedi.durum_degistir("uyku")
            self.kedi.sus()
        else:
            self.kedi.durum_degistir("mola")
            self.kedi.konus("Süre doldu! Hadi kalk, benimle 5 dakika yürü!")

    def _pencereyi_one_getir(self):
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)

    def _ekrani_guncelle(self):
        dakika, saniye = divmod(self.kalan_saniye, 60)
        self.tuval.itemconfigure(self.sure_yazisi, text=f"{dakika:02d}:{saniye:02d}")

        if self.asama != "hazir" and not self.calisiyor_mu:
            yazi = "Duraklatıldı"
        elif self.asama == "calisma":
            yazi = "Odaklanma zamanı"
        elif self.asama == "mola":
            yazi = "Yürüyüş molası!"
        else:
            yazi = "Hazır"
        self.tuval.itemconfigure(self.asama_yazisi, text=yazi)

        self.tuval.itemconfigure(
            self.istatistik_yazisi,
            text=f"Tur {self.tur} · {sure_metni(self.toplam_calisma)}",
        )

        if self.calisiyor_mu:
            self.baslat_dugmesi.configure(text="Duraklat")
        elif self.asama == "hazir":
            self.baslat_dugmesi.configure(text="Başlat")
        else:
            self.baslat_dugmesi.configure(text="Devam")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    uygulama = NekodoroUygulamasi()
    uygulama.mainloop()
