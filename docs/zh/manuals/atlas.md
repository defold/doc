---
title: 图集手册
brief: 本手册解释了 Defold 中图集资源的工作原理。
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

每个图集资源都有一组属性。当您在 *Outline* 视图中选择根项目时，这些属性会显示在 *Properties* 面板中。

Size
: 显示生成的纹理资源的计算总大小。宽度和高度设置为最接近的2的幂。请注意，如果启用纹理压缩，某些格式需要方形纹理。非方形纹理将被调整大小并用空白填充以使纹理变为方形。有关详细信息，请参阅[纹理配置文件手册](/manuals/texture-profiles/)。

Margin
: 应在每个图像之间添加的像素数。

Inner Padding
: 应在每个图像周围填充的空白像素数。

Extrude Borders
: 应在每个图像周围重复填充的边缘像素数。当片段着色器在图像边缘采样像素时，相邻图像（在同一图集纹理上）的像素可能会渗入。扩展边缘可以解决这个问题。

Max Page Size
: 多页图集中一页的最大尺寸。这可用于将图集拆分为同一图集的多个页面，以限制图集大小，同时仍仅使用单次绘制调用。此功能必须与位于 `/builtins/materials/*_paged_atlas.material` 中的启用多页图集的材料结合使用。

![Multi-page atlas](images/atlas/multipage_atlas.png)

Rename Patterns
: 以逗号（´,´）分隔的搜索和替换模式列表，其中每个模式的形式为 `search=replace`。
每个图像的原始名称（文件基本名称）将使用这些模式进行转换。（例如，模式 `hat=cat,_normal=`，将把名为 `hat_normal` 的图像重命名为 `cat`）。这在匹配图集之间的动画时很有用。

以下是不同属性设置的示例，其中四个64x64的正方形图像被添加到图集中。请注意，一旦图像无法适应128x128，图集如何跳转到256x256，导致大量浪费的纹理空间。

![Atlas properties](images/atlas/atlas_properties.png)

## 图像属性

图集中的每个图像都有一组属性：

Id
: 图像的ID（只读）。

Size
: 图像的宽度和高度（只读）。

Pivot
: 图像的轴心点（以单位为单位）。左上角是(0,0)，右下角是(1,1)。默认是(0.5, 0.5)。轴心点可以在0-1范围之外。轴心点是图像在精灵等中使用时将被居中的位置。您可以通过拖动编辑器视图上的轴心手柄来修改轴心点。只有当选择单个图像时，手柄才可见。拖动时按住 <kbd>Shift</kbd> 可以启用捕捉。

Sprite Trim Mode
: 精灵的渲染方式。默认是将精灵渲染为矩形（Sprite Trim Mode设置为Off）。如果精灵包含大量透明像素，使用4到8个顶点将精灵渲染为非矩形形状可能更有效。请注意，精灵修剪不与9宫格精灵一起工作。

Image
: 图像本身的路径。

![Image properties](images/atlas/image_properties.png)

## 动画属性

除了作为动画组一部分的图像列表外，还有一组可用属性：

Id
: 动画的名称。

Fps
: 动画的播放速度，以每秒帧数（FPS）表示。

Flip horizontal
: 水平翻转动画。

Flip vertical
: 垂直翻转动画。

Playback
: 指定动画应如何播放：

  - `None` 完全不播放，显示第一张图像。
  - `Once Forward` 从第一张到最后一张图像播放动画一次。
  - `Once Backward` 从最后一张到第一张图像播放动画一次。
  - `Once Ping Pong` 从第一张到最后一张图像播放动画一次，然后回到第一张图像。
  - `Loop Forward` 从第一张到最后一张图像重复播放动画。
  - `Loop Backward` 从最后一张到第一张图像重复播放动画。
  - `Loop Ping Pong` 从第一张到最后一张图像重复播放动画，然后回到第一张图像。

## 运行时纹理和图集创建

从 Defold 1.4.2 开始，可以在运行时创建纹理和图集。

### 在运行时创建纹理资源

使用 [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) 创建新的纹理资源：

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = resource.TEXTURE_TYPE_2D,
    format = resource.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

创建纹理后，您可以使用 [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) 设置纹理的像素：

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=resource.TEXTURE_TYPE_2D, format=resource.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
也可以使用 `resource.set_texture()` 通过使用小于纹理完整大小的缓冲区宽度和高度以及通过更改 `resource.set_texture()` 的 x 和 y 参数来更新纹理的子区域。
:::

纹理可以直接在[模型组件](/manuals/model/)上使用 `go.set()`：

```lua
  go.set("#model", "texture0", my_texture_id)
```

### 在运行时创建图集

如果纹理应该在[精灵组件](/manuals/sprite/)上使用，它首先需要被图集使用。使用 [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) 创建图集：

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frame_start = 1,
        frame_end   = 2,
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- assign the atlas to the 'sprite' component on the same go
  go.set("#sprite", "image", my_atlas_id)

  -- play the "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```