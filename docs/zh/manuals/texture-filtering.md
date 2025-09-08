---
title: 纹理过滤
brief: 本手册介绍了渲染图形时纹理过滤的可用选项。
---

# 纹理过滤和采样

纹理过滤决定了当一个 _texel_（纹理中的像素）与屏幕像素不是完美对齐时的视觉效果。当您移动包含纹理的图形元素小于一个像素的距离时，就会发生这种情况。以下过滤方法可用：

Nearest
: 将选择最近的 texel（图素）来为屏幕像素着色。如果您想要实现从纹理到屏幕的完美一对一像素映射，应选择这种采样方法。使用最近邻过滤时，所有内容在移动时都会从一个像素跳到另一个像素。如果精灵移动缓慢，这可能会看起来闪烁。

Linear
: 在为屏幕像素着色之前，texel（图素）将与其相邻像素进行平均。这为缓慢、连续的运动产生平滑的外观，因为精灵会在完全着色之前渗入像素中——因此可以将精灵移动小于一个完整像素的距离。

使用哪种过滤的设置存储在[项目设置](/manuals/project-settings/#graphics)文件中。有两个设置：

default_texture_min_filter
: 缩小过滤适用于 texel（图素）小于屏幕像素的情况。

default_texture_mag_filter
: 放大过滤适用于 texel（图素）大于屏幕像素的情况。

两个设置都接受值 `linear`、`nearest`、`nearest_mipmap_nearest`、`nearest_mipmap_linear`、`linear_mipmap_nearest` 或 `linear_mipmap_linear`。例如：

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

如果您不指定任何内容，默认情况下两者都设置为 `linear`。

请注意，*game.project* 中的设置由默认采样器使用。如果您在自定义材质中指定采样器，可以专门为每个采样器设置过滤方法。有关详细信息，请参阅[材质手册](/manuals/material/)。
