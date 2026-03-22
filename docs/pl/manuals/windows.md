---
title: Tworzenie aplikacji Defold na platformie Windows
brief: Ta instrukcja opisuje, jak budować i uruchamiać aplikacje Defold w systemie Windows
---

# Tworzenie dla platformy Windows

Tworzenie aplikacji Defold na platformę Windows jest prostym procesem i wymaga bardzo niewielu dodatkowych uwag.

## Ustawienia projektu

Konfigurację aplikacji specyficzną dla Windows ustawiasz w sekcji [Windows](/manuals/project-settings/#windows) pliku ustawień *game.project*.

## Ikona aplikacji

Ikona aplikacji używana w grze przeznaczonej na Windows musi mieć format `.ico`. Plik `.ico` można łatwo utworzyć z pliku `.png` za pomocą narzędzia online, takiego jak [ICOConvert](https://www.icoconverter.com/) lub [AConvert](https://www.aconvert.com/icon/png-to-ico/). Prześlij obraz i użyj co najmniej następujących rozmiarów ikony: 16x16, 24x24, 32x32, 48x48, 256x256.

Źródło: [Microsoft - budowa ikon aplikacji Windows](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Tworzenie lokalnego pliku `.ico` za pomocą pakietu ImageMagick
[ImageMagick](https://www.imagemagick.org/) to darmowy, otwartoźródłowy zestaw narzędzi używany do edycji i przetwarzania obrazów cyfrowych.

1. Zainstaluj ImageMagick
  * Linux: Zainstaluj za pomocą `apt`
```
sudo apt install imagemagick
```
  * Windows: Pobierz z [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows):
  * macOS: Zainstaluj za pomocą `brew`:
```
brew install imagemagick
```

2. Przygotuj ikonę PNG.
3. Przekonwertuj PNG do ICO za pomocą narzędzia [convert](https://www.imagemagick.org/script/convert.php):
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## FAQ
:[FAQ dotyczące Windows](../shared/windows-faq.md)
