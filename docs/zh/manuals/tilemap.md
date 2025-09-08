---
title: Defold 瓦片地图手册
brief: 本手册详细介绍了 Defold 对瓦片地图的支持。
---

# 瓦片地图

*瓦片地图*是一个组件，允许您将*瓦片图源*中的瓦片组装或绘制到大网格区域上。瓦片地图通常用于构建游戏关卡环境。您还可以在地图中使用瓦片图源中的*碰撞形状*进行碰撞检测和物理模拟（[示例](/examples/tilemap/collisions/)）。

在创建瓦片地图之前，您需要先创建瓦片图源。请参阅[瓦片图源手册](/manuals/tilesource)了解如何创建瓦片图源。

## 创建瓦片地图

要创建新的瓦片地图：

- 在*资源*浏览器中<kbd>右键点击</kbd>一个位置，然后选择<kbd>新建... ▸ 瓦片地图</kbd>）。
- 为文件命名。
- 新的瓦片地图会自动在瓦片地图编辑器中打开。

  ![新建瓦片地图](images/tilemap/tilemap.png)

- 将*瓦片图源*属性设置为您已准备好的瓦片图源文件。

要在瓦片地图上绘制瓦片：

1. 在*大纲*视图中选择或创建一个*图层*进行绘制。
2. 选择一个瓦片作为笔刷（按<kbd>空格键</kbd>显示瓦片调色板）或通过在调色板中点击并拖动选择几个瓦片来创建包含多个瓦片的矩形笔刷。

   ![调色板](images/tilemap/palette.png)

3. 使用选定的笔刷进行绘制。要擦除瓦片，可以选择一个空白瓦片作为笔刷使用，或选择橡皮擦（<kbd>编辑 ▸ 选择橡皮擦</kbd>）。

   ![绘制瓦片](images/tilemap/paint_tiles.png)

您可以直接从图层中拾取瓦片并将选择用作笔刷。按住<kbd>Shift</kbd>并点击瓦片可将其拾取为当前笔刷。按住<kbd>Shift</kbd>时，您还可以点击并拖动以选择一块瓦片作为更大的笔刷。此外，还可以通过按住<kbd>Shift+Ctrl</kbd>以类似方式剪切瓦片，或通过按住<kbd>Shift+Alt</kbd>擦除它们。

要顺时针旋转笔刷，请使用<kbd>Z</kbd>。使用<kbd>X</kbd>进行水平翻转，使用<kbd>Y</kbd>进行垂直翻转笔刷。

![拾取瓦片](images/tilemap/pick_tiles.png)

## 将瓦片地图添加到游戏中

要将瓦片地图添加到游戏中：

1. 创建一个游戏对象来容纳瓦片地图组件。游戏对象可以在文件中或直接在集合中创建。
2. 右键点击游戏对象的根节点，然后选择<kbd>添加组件文件</kbd>。
3. 选择瓦片地图文件。

![使用瓦片地图](images/tilemap/use_tilemap.png)

## 运行时操作

您可以通过多种不同的函数和属性在运行时操作瓦片地图（请参阅[API文档了解用法](/ref/tilemap/)）。

### 从脚本更改瓦片

您可以在游戏运行时动态读取和写入瓦片地图的内容。为此，请使用[`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile)和[`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile)函数：

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- 将草地瓦片（2）替换为危险的洞瓦片（编号4）。
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## 瓦片地图属性

除了*Id*、*Position*、*Rotation*和*Scale*属性外，还存在以下组件特定属性：

*瓦片图源*
: 用于瓦片地图的瓦片图源资源。

*材质*
: 用于渲染瓦片地图的材质。

*混合模式*
: 渲染瓦片地图时使用的混合模式。

### 混合模式
:[blend-modes](../shared/blend-modes.md)

### 更改属性

瓦片地图有许多不同的属性，可以使用`go.get()`和`go.set()`进行操作：

`tile_source`
: 瓦片地图的瓦片图源（`hash`）。您可以使用瓦片图源资源属性和`go.set()`更改此属性。请参阅[API参考中的示例](/ref/tilemap/#tile_source)。

`material`
: 瓦片地图的材质（`hash`）。您可以使用材质资源属性和`go.set()`更改此属性。请参阅[API参考中的示例](/ref/tilemap/#material)。

### 材质常量

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: 瓦片地图的颜色色调（`vector4`）。vector4用于表示色调，x、y、z和w分别对应红色、绿色、蓝色和alpha色调。

## 项目配置

*game.project*文件中有一些与瓦片地图相关的[项目设置](/manuals/project-settings#tilemap)。

## 外部工具

有一些外部地图/关卡编辑器可以直接导出到Defold瓦片地图：

### Tiled

[Tiled](https://www.mapeditor.org/)是一个知名且广泛使用的正交、等距和六边形地图编辑器。Tiled支持多种功能，可以[直接导出到Defold](https://doc.mapeditor.org/en/stable/manual/export-defold/)。在[Defold用户"goeshard"的这篇博客文章](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)中了解更多关于如何导出瓦片地图数据和附加元数据的信息。

### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold)可用于从简单的基础瓦片自动创建完整的瓦片集，它有一个地图编辑器，可以直接导出到Defold。
