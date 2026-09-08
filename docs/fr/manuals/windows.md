---
title: Développement avec Defold pour la plateforme Windows
brief: Ce manuel décrit comment compiler et exécuter des applications Defold sous Windows
---

# Développement pour Windows {#windows-development}

Développer des applications Defold pour la plateforme Windows est un processus simple qui nécessite très peu de précautions particulières.

## Paramètres du projet {#project-settings}

La configuration de l'application propre à Windows s'effectue dans la [section Windows](/manuals/project-settings/#windows) du fichier de paramètres *game.project*.

## Icône de l'application {#application-icon}

L'icône de l'application utilisée pour un jeu Windows doit être au format .ico. Vous pouvez facilement créer un fichier .ico à partir d'un fichier .png à l'aide d'un outil en ligne comme [ICOConvert](https://www.icoconverter.com/) ou [AConvert](https://www.aconvert.com/icon/png-to-ico/). Téléversez une image et utilisez au moins les tailles d'icône suivantes : 16x16, 24x24, 32x32, 48x48, 256x256.

Source : [Microsoft - Création d'une icône d'application Windows](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Création locale d'un fichier .ico à l'aide de la suite logicielle ImageMagick. {#creating-ico-file-locally-using-imagemagick-software-suite}
[ImageMagick](https://www.imagemagick.org/) est une suite logicielle gratuite et open source qui permet de modifier et de manipuler des images numériques.

1. Installez ImageMagick
  * Linux : installez-le à l'aide de `apt`
```
sudo apt install imagemagick
```
  * Windows : téléchargez-le depuis [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows) :
  * macOS : installez-le à l'aide de `brew` :
```
brew install imagemagick
```

2. Préparez votre icône PNG.
3. Convertissez le fichier PNG en ICO à l'aide de l'outil [convert](https://www.imagemagick.org/script/convert.php) :
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## Foire aux questions {#faq}
:[Windows FAQ](../shared/windows-faq.md)
