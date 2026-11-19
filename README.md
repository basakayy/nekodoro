# Nekodoro 🍅🐈‍⬛

Ekranın köşesinde duran, domates başlıklı piksel bir kediyle Pomodoro sayacı.

<p align="center">
  <img src="gorseller/neko.png" alt="Nekodoro" width="288">
  <img src="gorseller/mola.png" alt="Yürüyüş molası" width="288">
  <img src="gorseller/su.png" alt="Su hatırlatması" width="288">
</p>

- **25 dakika odaklanma:** Neko uyur.
- **5 dakika mola:** Süre dolunca Neko uyanır, ses çalar ve seni kalkıp yürümeye çağırır. Molada o da yürür, zıplar.
- **Su hatırlatması:** Her 30 dakikalık çalışmada su içmeni hatırlatır.
- **Tur ve toplam süre:** Kaçıncı turda olduğunu ve toplam ne kadar çalıştığını gösterir.
- **Her zaman üstte:** Ekranın sağ alt köşesinde, görev çubuğunun hemen üstünde durur. Hangi programı kullanırsan kullan görünür kalır.
- **Sesler:** 8-bit melodi, sistem zili ya da sessiz.

> Yalnızca **Windows** üzerinde çalışır.

## İndir ve kullan

1. [Releases](../../releases) sayfasından `Nekodoro.exe` dosyasını indir.
2. Çift tıklayıp aç. Kurulum gerekmez.

Windows ilk açılışta **"Windows bilgisayarınızı korudu"** uyarısı gösterebilir. Uygulama imzalı olmadığı için bu uyarı çıkar. **Ek bilgi → Yine de çalıştır** ile açabilirsin.

### Kullanım

| | |
|---|---|
| **Başlat / Duraklat** | Sayacı başlatır ya da durdurur |
| **Sıfırla** | Mevcut turu baştan alır |
| **Ses menüsü** | Melodi, Zil veya Sessiz |
| **Taşımak** | Kedinin olduğu alanı tutup sürükle |
| **Kapatmak** | Sağ üstteki `x` |

## Kaynak koddan çalıştırma

Python 3 gerekir (Python 3.15 ile test edildi).

```
pip install -r requirements.txt
python main.py
```

Süreleri beklemeden denemek için test modu (10 sn çalışma, 10 sn mola, 15 sn'de su):

```
python main.py --test
```

## Exe oluşturma

```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name Nekodoro --icon nekodoro.ico --collect-data customtkinter main.py
```

Exe `dist/` klasörüne oluşur.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `main.py` | Pencere, sayaç ve düğmeler |
| `kedi.py` | Piksel kedi, animasyonlar ve konuşma balonu |
| `sesler.py` | Melodiler |
| `nekodoro.ico` | Uygulama simgesi |

## Lisans

[MIT](LICENSE)
