---
title: 图集手册
brief: 本手册介绍了 Defold 中图集资源是如何工作的。
---

# 图集

虽然单个图像通常用作精灵的源，但出于性能考虑，图像需要合并成更大的图像集，称为图集。将较小的图像集合并成图集在移动设备上尤其重要，因为与桌面计算机或专用游戏机相比，移动设备的内存和处理能力更为稀缺。

在 Defold 中，图集资源是一个单独图像文件的列表，这些文件会自动合并成一个更大的图像。

## 创建图集

在 *Assets* 浏览器中的上下文菜单中选择 <kbd>New... ▸ Atlas</kbd>。命名新的图集文件。编辑器现在将在图集编辑器中打开该文件。图集属性显示在
*Properties* 面板中，因此您可以编辑它们（详见下文）。

您需要先用图像或动画填充图集，然后才能将其用作精灵和粒子效果组件等对象组件的图形源。

确保您已将图像添加到项目中（将图像文件拖放到 *Assets* 浏览器中的正确位置）。

添加单个图像

: 从 *Asset* 面板将图像拖放到编辑器视图中。
  
  或者，在 *Outline* 面板中 <kbd>右键点击</kbd> 根 Atlas 条目。

  从弹出的上下文菜单中选择 <kbd>Add Images</kbd> 以添加单个图像。

  将打开一个对话框，您可以从中查找并选择要添加到 Atlas 的图像。请注意，您可以过滤图像文件并一次选择多个文件。

  ![Creating an atlas, adding images](images/atlas/add.png)

  添加的图像列在 *Outline* 中，完整的图集可以在中心编辑器视图中看到。您可能需要按 <kbd>F</kbd>（从菜单中选择 <kbd>View ▸ Frame Selection</kbd>）来框选选择。

  ![Images added](images/atlas/single_images.png)

添加翻书动画

: 在 *Outline* 面板中 <kbd>右键点击</kbd> 根 Atlas 条目。

  从弹出的上下文菜单中选择 <kbd>Add Animation Group</kbd> 以创建翻书动画组。

  一个新的、空的、具有默认名称（"New Animation"）的动画组被添加到图集中。

  从 *Asset* 面板将图像拖放到编辑器视图中，将它们添加到当前选定的组中。
  
  或者，<kbd>右键点击</kbd> 新组并从上下文菜单中选择 <kbd>Add Images</kbd>。

  将打开一个对话框，您可以从中查找并选择要添加到动画组的图像。

  ![Creating an atlas, adding images](images/atlas/add_animation.png)

  选定动画组后按 <kbd>空格键</kbd> 预览，按 <kbd>Ctrl/Cmd+T</kbd> 关闭预览。根据需要调整动画的 *Properties*（见下文）。

  ![Animation group](images/atlas/animation_group.png)

您可以通过选择图像并按 <kbd>Alt + Up/down</kbd> 来重新排列 Outline 中的图像。您还可以通过在 Outline 中复制和粘贴图像（从 <kbd>Edit</kbd> 菜单、右键上下文菜单或键盘快捷键）轻松创建副本。

## 图集属性

当您在 *Outline* 面板中选择图集根节点时，可以在 *Properties* 面板中编辑以下属性：

![Atlas properties](images/atlas/atlas_properties.png)

*Size*

: 图集输出图像的尺寸。图集构建器将尝试将所有图像打包到此尺寸的图像中。如果图像无法适应，将创建多个输出图像。默认尺寸为 2048x2048 像素。

*Margin*

: 添加到每个图像边缘的空白区域（以像素为单位）。这有助于防止图像在缩放时边缘像素被"污染"。默认值为 0。

*Inner Padding*

: 添加到每个图像内部的空白区域（以像素为单位）。这有助于防止图像在缩放时相邻像素被"污染"。默认值为 0。

*Extrude Borders*

: 如果启用，将复制每个图像的边缘像素并扩展图像。这有助于防止图像在缩放时边缘像素被"污染"。默认值为 false。

*Border Padding*

: 添加到整个图集边缘的空白区域（以像素为单位）。这有助于防止图集在缩放时边缘像素被"污染"。默认值为 0。

*Page Width/Height*

: 图集输出图像的尺寸。图集构建器将尝试将所有图像打包到此尺寸的图像中。如果图像无法适应，将创建多个输出图像。默认尺寸为 2048x2048 像素。

*Texture Compression*

: 用于图集输出图像的纹理压缩格式。默认值为 "None"。

*Output Format*

: 图集输出图像的格式。默认值为 "PNG"。

*Output Path*

: 图集输出图像的路径。默认值为 "atlas"。

## 图片属性

当您在 *Outline* 面板中选择单个图像时，可以在 *Properties* 面板中编辑以下属性：

![Image properties](images/atlas/image_properties.png)

*Image*

: 图像的路径。您可以通过点击此字段并从文件浏览器中选择新图像来更改图像。

*Trim Mode*

: 图像的修剪模式。默认值为 "None"。

*Trim Threshold*

: 图像的修剪阈值。默认值为 0。

*Trim Margin*

: 图像的修剪边距。默认值为 0。

*Pivot*

: 图像的轴心点。默认值为 "Center"。

*Extrude Borders*

: 如果启用，将复制图像的边缘像素并扩展图像。这有助于防止图像在缩放时边缘像素被"污染"。默认值为 false。

*Inner Padding*

: 添加到图像内部的空白区域（以像素为单位）。这有助于防止图像在缩放时相邻像素被"污染"。默认值为 0。

*Border Padding*

: 添加到图像边缘的空白区域（以像素为单位）。这有助于防止图像在缩放时边缘像素被"污染"。默认值为 0。

## 动画属性

当您在 *Outline* 面板中选择动画组时，可以在 *Properties* 面板中编辑以下属性：

![Animation properties](images/atlas/animation_properties.png)

*Id*

: 动画的标识符。您可以通过点击此字段并输入新名称来更改动画的名称。

*Fps*

: 动画的帧率。默认值为 30。

*Flip Horizontal*

: 如果启用，动画将水平翻转。默认值为 false。

*Flip Vertical*

: 如果启用，动画将垂直翻转。默认值为 false。

*Playback*

: 动画的播放模式。默认值为 "Once Forward"。

*Width*

: 动画组的宽度（以像素为单位）。默认值为 0。

*Height*

: 动画组的高度（以像素为单位）。默认值为 0。

*Origin X/Origin Y*

: 动画组的原点。默认值为 0。

## 运行时纹理及图集建立

Defold 支持在运行时动态创建纹理和图集。这对于动态加载资源、生成程序内容或实现动态纹理打包等功能非常有用。

### 运行时纹理

您可以使用 `resource.create_texture()` 函数在运行时创建纹理。此函数接受一个表格参数，其中包含纹理的宽度、高度、类型和格式等信息。

```lua
local texture_params = {
    width = 256,
    height = 256,
    type = resource.TEXTURE_TYPE_2D,
    format = resource.TEXTURE_FORMAT_RGBA,
}
local texture_id = resource.create_texture(texture_params)
```

创建纹理后，您可以使用 `resource.set_texture()` 函数更新纹理的内容。

```lua
local buffer = "..." -- 包含纹理数据的缓冲区
resource.set_texture(texture_id, buffer)
```

### 运行时图集

您可以使用 `resource.create_atlas()` 函数在运行时创建图集。此函数接受一个表格参数，其中包含图集的图像列表和动画列表等信息。

```lua
local atlas_params = {
    images = {
        { id = "image1", x = 0, y = 0, width = 64, height = 64 },
        { id = "image2", x = 64, y = 0, width = 64, height = 64 },
    },
    animations = {
        { id = "animation1", fps = 30, playback = resource.PLAYBACK_ONCE_FORWARD, frames = { "image1", "image2" } },
    },
}
local atlas_id = resource.create_atlas(atlas_params)
```

创建图集后，您可以使用 `resource.set_atlas()` 函数更新图集的内容。

```lua
local buffer = "..." -- 包含图集数据的缓冲区
resource.set_atlas(atlas_id, buffer)
```

## 相关手册

- [Sprite 手册](/manuals/sprite)
- [粒子效果手册](/manuals/particlefx)
- [Tile Source 手册](/manuals/tilesource)
- [材质手册](/manuals/material)
- [纹理配置文件手册](/manuals/texture-profiles)
- [资源手册](/manuals/resource)