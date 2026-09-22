---
title: Defold-Entwicklung für die Windows-Plattform
brief: Dieses Handbuch beschreibt, wie du unter Windows Builds von Defold-Anwendungen erstellst und diese ausführst
---

# Entwicklung für Windows {#windows-development}

Die Entwicklung von Defold-Anwendungen für die Windows-Plattform ist unkompliziert und erfordert nur wenige besondere Überlegungen.

## Projekteinstellungen {#project-settings}

Die Windows-spezifische Konfiguration der Anwendung erfolgt im [Windows-Abschnitt](/manuals/project-settings/#windows) der Einstellungsdatei *game.project*.

## Anwendungssymbol {#application-icon}

Das Anwendungssymbol für ein Windows-Spiel muss im .ico-Format vorliegen. Du kannst mit einem Online-Werkzeug wie [ICOConvert](https://www.icoconverter.com/) oder [AConvert](https://www.aconvert.com/icon/png-to-ico/) ganz einfach eine .ico-Datei aus einer .png-Datei erstellen. Lade ein Bild hoch und verwende mindestens die folgenden Symbolgrößen: 16x16, 24x24, 32x32, 48x48, 256x256.

Quelle: [Microsoft - Erstellen von Windows-Anwendungssymbolen](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Eine .ico-Datei lokal mit der Softwaresammlung ImageMagick erstellen. {#creating-ico-file-locally-using-imagemagick-software-suite}
[ImageMagick](https://www.imagemagick.org/) ist eine kostenlose Open-Source-Softwaresammlung zum Bearbeiten und Verändern digitaler Bilder.

1. Installiere ImageMagick
  * Linux: Installiere es mit `apt`
```
sudo apt install imagemagick
```
  * Windows: Lade es von [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows) herunter:
  * macOS: Installiere es mit `brew`:
```
brew install imagemagick
```

2. Bereite dein PNG-Symbol vor.
3. Wandle die PNG-Datei mit dem Werkzeug [convert](https://www.imagemagick.org/script/convert.php) in eine ICO-Datei um:
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## FAQ
:[Windows FAQ](../shared/windows-faq.md)
