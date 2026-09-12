---
title: Windows platformu için Defold geliştirme
brief: Bu kılavuz, Windows'ta Defold uygulamalarının nasıl derlenip çalıştırılacağını açıklar
---

# Windows için geliştirme

Windows platformu için Defold uygulamaları geliştirmek, dikkat edilmesi gereken çok az noktanın bulunduğu basit bir süreçtir.

## Proje ayarları

Windows'a özgü uygulama yapılandırması, *game.project* ayarlar dosyasının [Windows bölümünden](/manuals/project-settings/#windows) yapılır.

## Uygulama simgesi

Bir Windows oyununda kullanılan uygulama simgesinin .ico biçiminde olması gerekir. [ICOConvert](https://www.icoconverter.com/) veya [AConvert](https://www.aconvert.com/icon/png-to-ico/) gibi bir çevrimiçi araç kullanarak .png dosyasından kolayca .ico dosyası oluşturabilirsiniz. Bir görüntü yükleyin ve en azından şu simge boyutlarını kullanın: 16x16, 24x24, 32x32, 48x48, 256x256.

Kaynak: [Microsoft - Windows uygulama simgesi oluşturma](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### ImageMagick yazılım paketiyle yerel olarak .ico dosyası oluşturma.
[ImageMagick](https://www.imagemagick.org/), dijital görüntüleri düzenlemek ve işlemek için kullanılan ücretsiz, açık kaynaklı bir yazılım paketidir.

1. ImageMagick kurun
  * Linux: `apt` kullanarak kurun
```
sudo apt install imagemagick
```
  * Windows: [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows) adresinden indirin:
  * macOS: `brew` kullanarak kurun:
```
brew install imagemagick
```

2. PNG simgenizi hazırlayın.
3. [convert](https://www.imagemagick.org/script/convert.php) aracını kullanarak PNG dosyasını ICO biçimine dönüştürün:
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## Sık sorulan sorular
:[Windows FAQ](../shared/windows-faq.md)
