---
title: 纹理过滤
brief: 本教程介绍了渲染图像时纹理过滤的功能.
---

# 纹理过滤和采样

纹理过滤决定了当一个 _texel_ (图素, 纹理中的一个像素) 与屏幕像素不是完美对齐时的视觉效果. 当可视元素移动小于1个像素的时候就会发生这种现象. 可以选择以下的过滤方式:

Nearest
: 屏幕像素颜色选取自距离最近的图素. 这样就实现了从纹理到屏幕的像素对齐. 这种过滤模式使得像素移动类似于自动吸附. 要是Sprite移动很慢, 可能会感觉一跳一跳的.

Linear
: 屏幕像素颜色取决于图素及其旁边图素的颜色的平均值. 这样缓慢的移动能显得十分平滑, 因为渲染之前Sprite的颜色已经与周围进行了融合--所以移动小于一个像素距离也是可以的.

过滤设置保存在 [项目设置](/manuals/project-settings/#Graphics) 文件里. 一共有两项:

default_texture_min_filter
: 当图素小于屏幕像素大小, 要缩小时使用的过滤效果.

default_texture_mag_filter
: 当图素大于屏幕像素大小, 要放大时使用的过滤效果.

这两项取值都是 `linear` 或者 `nearest`. 比如:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

如果不赋值, 默认都是 `linear`.

注意 *game.project* 由默认采样器使用. 如果你在自定义材质里指定了特殊的采样器, 可以对每个采样器采用不同的过滤方法. 详情请见 [材质教程](/manuals/material/).
