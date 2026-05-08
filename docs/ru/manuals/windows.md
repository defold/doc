---
title: Разработка под платформу Windows в Defold
brief: В этом руководстве описано, как собирать и запускать приложения Defold на платформе Windows
---

# Разработка под Windows

Разработка приложений Defold для платформы Windows является довольно простым процессом и требует учёта лишь нескольких нюансов.

## Настройки проекта

Специфичная для Windows конфигурация приложения выполняется в разделе [Windows](/manuals/project-settings/#windows) файла настроек *game.project*.

## Иконка приложения

Иконка приложения для игры под Windows должна быть в формате .ico. Вы можете легко создать файл .ico из файла .png с помощью онлайн-инструментов, таких как [ICOConvert](https://www.icoconverter.com/) или [AConvert](https://www.aconvert.com/icon/png-to-ico/). Загрузите изображение и используйте как минимум следующие размеры иконок: 16x16, 24x24, 32x32, 48x48, 256x256.

Источник: [Microsoft - Windows app icon construction](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Создание .ico-файла локально с помощью набора программ ImageMagick.

[ImageMagick](https://www.imagemagick.org/) — это бесплатный пакет программ с открытым исходным кодом, используемый для редактирования и обработки цифровых изображений.

1. Установите ImageMagick
  * Linux: установите с помощью `apt`
```
sudo apt install imagemagick
```
  * Windows: загрузите с [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows)
  * macOS: установите с помощью `brew`
```
brew install imagemagick
```

2. Подготовьте ваш PNG-файл иконки.
3. Преобразуйте PNG в ICO с помощью инструмента [convert](https://www.imagemagick.org/script/convert.php):
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```

## FAQ
:[Windows FAQ](../shared/windows-faq.md)
