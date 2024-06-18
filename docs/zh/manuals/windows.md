---
title: Windows 平台下的 Defold 开发
brief: 本教程介绍了在 Windows 平台下如何编译和运行 Defold 应用 
---

# Windows 开发

为Windows平台开发开发Defold应用是一件轻车熟路的事.

## 项目设置

Windows 相关设置位于*game.project* 文件的 [Windows部分](/manuals/project-settings/#Windows)  .

## 应用图标

Windows游戏的图标要使用 .ico 格式. 你可以拿一个 .png 文件, 使用[ICOConvert](https://www.icoconverter.com/) 或者  [AConvert](https://www.aconvert.com/icon/png-to-ico/) 之类的在线工具生成 .ico 图标. 上传图片最小使用这些尺寸: 16x16, 24x24, 32x32, 48x48, 256x256.

原文: [Microsoft - Windows 应用图标建设](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction#icon-sizes-win32)

### 使用 ImageMagick 系列工具在本地生成 .ico 图标.
例如在 Linux 上:
1. 安装 [ImageMagick](https://www.imagemagick.org/):
```
sudo apt install imagemagick
```
2. 准备好你的 PNG 图标.
3. 使用 [convert](https://www.imagemagick.org/script/convert.php) 工具从 PNG 转换到 ICO:
```bash
convert icon_256x256px.png -compress None -define icon:auto-resize=256,128,96,64,48,32,24,16 favicon.ico
```

## 问答
:[Windows 问答](../shared/windows-faq.md)
