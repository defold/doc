---
title: Sviluppo con Defold per la piattaforma Windows
brief: Questo manuale descrive come creare build ed eseguire applicazioni Defold su Windows
---

# Sviluppo per Windows {#windows-development}

Sviluppare applicazioni Defold per la piattaforma Windows è un processo semplice che richiede pochi accorgimenti.

## Impostazioni del progetto {#project-settings}

La configurazione dell'applicazione specifica per Windows si effettua nella [sezione Windows](/manuals/project-settings/#windows) del file delle impostazioni *game.project*.

## Icona dell'applicazione {#application-icon}

L'icona dell'applicazione usata per un gioco Windows deve essere in formato .ico. Puoi creare facilmente un file .ico a partire da un file .png con uno strumento online come [ICOConvert](https://www.icoconverter.com/) o [AConvert](https://www.aconvert.com/icon/png-to-ico/). Carica un'immagine e usa almeno le seguenti dimensioni per l'icona: 16x16, 24x24, 32x32, 48x48, 256x256.

Fonte: [Microsoft - Creazione delle icone delle applicazioni Windows](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Creazione di un file .ico in locale con la suite software ImageMagick. {#creating-ico-file-locally-using-imagemagick-software-suite}
[ImageMagick](https://www.imagemagick.org/) è una suite software gratuita e open source per modificare ed elaborare immagini digitali.

1. Installa ImageMagick
  * Linux: installa tramite `apt`
```
sudo apt install imagemagick
```
  * Windows: scarica da [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows):
  * macOS: installa tramite `brew`:
```
brew install imagemagick
```

2. Prepara la tua icona PNG.
3. Converti il PNG in ICO con lo strumento [convert](https://www.imagemagick.org/script/convert.php):
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## FAQ
:[Windows FAQ](../shared/windows-faq.md)
