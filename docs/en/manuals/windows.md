---
title: Defold development for the Windows platform
brief: This manual describes how to build and run Defold applications on Windows
---

# Windows development

Developing Defold applications for the Windows platform is a straight forward process with very few considerations to make.

## Project settings

Windows specific application configuration is done from the [Windows section](/manuals/project-settings/#windows) of the *game.project* settings file.

## Application icon

The application icon used for a Windows game must be in the .ico format. You can easily create a .ico file from a .png file using an online tool such as [ICOConvert](https://www.icoconverter.com/) or [AConvert](https://www.aconvert.com/icon/png-to-ico/). Upload an image and use at least the following icon sizes: 16x16, 24x24, 32x32, 48x48, 256x256.

Source: [Microsoft - Windows app icon construction](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Creating .ico file locally using [ImageMagick](https://www.imagemagick.org/) software suite.
Example for Linux:
1. Instal ImageMagick:
```
sudo apt install imagemagick
```
3. Prepare your PNG icon.
4. Convert PNG to ICO using [convert](https://www.imagemagick.org/script/convert.php) tool:
```bash
convert icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```

## FAQ
:[Windows FAQ](../shared/windows-faq.md)
