# TO-DO APPLICATION WITH PYTHON

CustomTkinter ile gelistirilmis masaustu gorev takip uygulamasi. Kullanici girisi, gorev ekleme/silme, favori gorevler, tarih secimi, tekrar eden gorevler ve hatirlatici bildirimleri destekler.

GitHub: https://github.com/semihertan/TO-DO-APPLICATION-WITH-PYTHON

## Ozellikler

- Kullanici kayit ve giris ekrani
- SQLite tabanli yerel veri saklama
- Gorev ekleme, silme ve tamamlandi olarak isaretleme
- Favori gorev isaretleme
- Takvim ile son tarih secimi
- Gunluk ve haftalik tekrar eden gorevler
- Bildirim ve sesli basari geri bildirimi
- PyInstaller ile Windows exe paketleme

## Proje yapisi

```text
.
|-- assets/
|   |-- images/      # Ikonlar ve arka plan gorselleri
|   |-- sounds/      # Bildirim sesleri
|   `-- themes/      # CustomTkinter tema dosyalari
|-- data/            # Yerel SQLite veritabani dosyalari
|-- packaging/       # PyInstaller ayarlari
|-- src/             # Python kaynak kodlari
|   |-- database.py
|   `-- main.py
|-- .github/         # GitHub issue, PR ve CI ayarlari
|-- requirements.txt # Python bagimliliklari
`-- README.md
```

## Gereksinimler

- Python 3.11 veya uzeri
- Windows ortaminda test edilmistir

## Kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Calistirma

```powershell
python src/main.py
```

Uygulama veritabani `data/user_data.db` yolunda olusturulur. Bu dosya yerel kullanici verisi icerdigi icin GitHub'a gonderilmez.

## Paketleme

Windows icin exe uretmek:

```powershell
pyinstaller packaging/main.spec
```

Cikti dosyalari `dist/` klasorune yazilir. `build/` ve `dist/` klasorleri Git tarafinda yok sayilir.

## GitHub Yapilandirmasi

Bu proje GitHub'a yuklemeye hazir olacak sekilde yapilandirildi:

- `origin` remote adresi bu repo olarak ayarlandi.
- `.gitignore` ile sanal ortam, derleme ciktilari, cache dosyalari ve yerel veritabani dislandi.
- `.github/workflows/python-check.yml` ile push ve pull request icin Python syntax kontrolu eklendi.
- Issue ve pull request sablonlari eklendi.
- `.gitattributes` ile metin dosyalari icin satir sonu davranisi sabitlendi.

## Lisans

Bu proje MIT lisansi ile yayinlanir. Ayrintilar icin `LICENSE` dosyasina bakin.
