---
title: Desenvolvimento Defold para a plataforma Windows
brief: Este manual descreve como compilar e executar aplicações Defold no Windows
---

# Desenvolvimento para Windows

Desenvolver aplicações Defold para a plataforma Windows é um processo simples, com muito poucas considerações a fazer.

## Configurações do projeto

A configuração específica de aplicação Windows é feita na [seção Windows](/manuals/project-settings/#windows) do arquivo de configurações *game.project*.

## Ícone da aplicação

O ícone da aplicação usado para um jogo Windows deve estar no formato .ico. Você pode criar facilmente um arquivo .ico a partir de um arquivo .png usando uma ferramenta online como [ICOConvert](https://www.icoconverter.com/) ou [AConvert](https://www.aconvert.com/icon/png-to-ico/). Envie uma imagem e use pelo menos os seguintes tamanhos de ícone: 16x16, 24x24, 32x32, 48x48, 256x256.

Fonte: [Microsoft - Windows app icon construction](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### Criando arquivo .ico localmente usando a suíte ImageMagick.
[ImageMagick](https://www.imagemagick.org/) é uma suíte de software livre e de código aberto, usada para editar e manipular imagens digitais.

1. Instale o ImageMagick
  * Linux: instale usando `apt`
```
sudo apt install imagemagick
```
  * Windows: baixe de [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows):
  * macOS: instale usando `brew`:
```
brew install imagemagick
```

2. Prepare seu ícone PNG.
3. Converta PNG para ICO usando a ferramenta [convert](https://www.imagemagick.org/script/convert.php):
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## FAQ
:[Windows FAQ](../shared/windows-faq.md)
