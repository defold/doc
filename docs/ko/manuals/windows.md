---
title: Windows 플랫폼용 Defold 개발
brief: 이 매뉴얼은 Windows에서 Defold 어플리케이션을 빌드하고 실행하는 방법을 설명합니다
---

# Windows 개발

Windows 플랫폼용 Defold 어플리케이션 개발은 고려할 사항이 매우 적은 간단한 과정입니다.

## 프로젝트 설정

Windows 전용 어플리케이션 구성은 *game.project* 설정 파일의 [Windows 섹션](/manuals/project-settings/#windows)에서 수행합니다.

## 어플리케이션 아이콘

Windows 게임에 사용되는 어플리케이션 아이콘은 .ico 포멧이어야 합니다. [ICOConvert](https://www.icoconverter.com/) 또는 [AConvert](https://www.aconvert.com/icon/png-to-ico/) 같은 온라인 도구를 사용하면 .png 파일에서 .ico 파일을 쉽게 만들 수 있습니다. 이미지를 업로드하고 최소한 다음 아이콘 크기를 사용하세요: 16x16, 24x24, 32x32, 48x48, 256x256.

출처: [Microsoft - Windows 앱 아이콘 구성](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### ImageMagick 소프트웨어 모음을 사용해 로컬에서 .ico 파일 생성하기.
[ImageMagick](https://www.imagemagick.org/)은 디지털 이미지를 편집하고 조작하는 데 사용하는 무료 오픈 소스 소프트웨어 모음입니다.

1. ImageMagick을 설치합니다
  * Linux: `apt`를 사용해 설치합니다
```
sudo apt install imagemagick
```
  * Windows: [https://imagemagick.org/script/download.php#windows](https://imagemagick.org/script/download.php#windows)에서 다운로드합니다:
  * macOS: `brew`를 사용해 설치합니다:
```
brew install imagemagick
```

2. PNG 아이콘을 준비합니다.
3. [convert](https://www.imagemagick.org/script/convert.php) 도구를 사용해 PNG를 ICO로 변환합니다:
```bash
magick icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```



## FAQ
:[Windows FAQ](../shared/windows-faq.md)
