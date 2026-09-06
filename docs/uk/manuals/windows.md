---
title: Розробка застосунків Defold для платформи Windows
brief: У цьому посібнику описано, як збирати й запускати застосунки Defold у Windows
---

# Розробка для Windows {#windows-development}

Розробка застосунків Defold для платформи Windows — простий процес, що потребує врахування лише кількох особливостей.

## Налаштування проєкту {#project-settings}

Специфічні для Windows налаштування застосунку задаються в [розділі Windows](/manuals/project-settings/#windows) файлу налаштувань *game.project*.

## Значок застосунку {#application-icon}

Значок застосунку для гри у Windows має бути у форматі .ico. Ви можете легко створити файл .ico з файлу .png за допомогою онлайн-інструмента, наприклад [ICOConvert](https://www.icoconverter.com/) або [AConvert](https://www.aconvert.com/icon/png-to-ico/). Завантажте зображення й використовуйте щонайменше такі розміри значків: 16x16, 24x24, 32x32, 48x48, 256x256.

Джерело: [Microsoft — створення значків застосунків Windows](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Локальне створення файлу .ico за допомогою пакета програм ImageMagick. {#creating-ico-file-locally-using-imagemagick-software-suite}
[ImageMagick](https://www.imagemagick.org/) — безкоштовний пакет програм із відкритим вихідним кодом для редагування й обробки цифрових зображень.

1. Установіть ImageMagick
  * Linux: установіть за допомогою `apt`
```
sudo apt install imagemagick
```
  * Windows: завантажте з [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows):
  * macOS: установіть за допомогою `brew`:
```
brew install imagemagick
```

2. Підготуйте значок у форматі PNG.
3. Перетворіть PNG на ICO за допомогою інструмента [convert](https://www.imagemagick.org/script/convert.php):
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## Поширені запитання {#faq}
:[Поширені запитання про Windows](../shared/windows-faq.md)
