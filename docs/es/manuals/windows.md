---
title: Desarrollo de Defold para la plataforma Windows
brief: Este manual describe cómo crear y ejecutar aplicaciones Defold en Windows
---

# Desarrollo de Windows

Desarrollar aplicaciones de Defold para la plataforma Windows es un proceso sencillo que requiere muy pocas consideraciones.

## Configuraciones del Proyecto

La configuración de la aplicación específica para Windows se realiza desde la [Sección de Windows](/manuals/project-settings/#windows) del archivo de configuración *game.project*.

## Icono de la aplicación

El icono de la aplicación para un juego de Windows debe estar en formato .ico. Puedes crear fácilmente un archivo .ico a partir de un archivo .png usando una herramienta en línea como [ICOConvert](https://www.icoconverter.com/) o [AConvert](https://www.aconvert.com/icon/png-to-ico/). Sube una imagen y usa al menos uno de los siguientes tamaños de icono: 16x16, 24x24, 32x32, 48x48, 256x256.

Fuente: [Microsoft - Construcción de iconos de aplicaciones de Windows](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Creación de un archivo .ico localmente utilizando el paquete de software ImageMagick.
[ImageMagick](https://www.imagemagick.org/) es un paquete de software gratuito y de código abierto, utilizado para editar y manipular imágenes digitales.

1. Instalando ImageMagick
  * Linux: Instala usando `apt`
```
sudo apt install imagemagick
```
  * Windows: Descargar de [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows):
  * macOS: Instalar usando `brew`:
```
brew install imagemagick
```

2. Prepara tu icono PNG.
3. Convierte PNG a ICO usando la herramienta [convert](https://www.imagemagick.org/script/convert.php):
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## Preguntas frecuentes
:[Preguntas frecuentes de Windows](../shared/windows-faq.md)
