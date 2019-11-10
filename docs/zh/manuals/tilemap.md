---
title: Defold 瓷砖地图手册
brief: 本教程介绍了 Defold 对于瓷砖地图的支持.
---

# Tile map （瓷砖地图）

*瓷砖地图* 是一个可以借由瓷砖图集装配，绘制成一个大网格地图的组件. 瓷砖地图一般用来作为游戏关卡环境. 你可以在地图上使用瓷砖图集里设置的 *碰撞形状* 来进行碰撞检测或者模拟物理效果.

创建瓷砖地图之前要先创建好瓷砖图集. 关于如何创建瓷砖图集，详情请见 [瓷砖图集手册](/manuals/tilesource).

## 创建瓷砖地图

创建瓷砖地图的步骤:

- 在 *Assets* 浏览器中<kbd>右键点击</kbd>，然后选择 <kbd>New... ▸ Tile Map</kbd>).
- 新的瓷砖地图会在瓷砖地图编辑器中打开.
- 给新文件命名.

  ![新瓷砖地图](images/tilemap/tilemap.png){srcset="images/tilemap/tilemap@2x.png 2x"}

- 用事先准备好的瓷砖图集设置 *Tile Source* 属性.

在瓷砖地图上绘制瓷砖的方法:

1. 在 *Outline* 视图中选择或者创建一个 *Layer* 用于绘制瓷砖.
2. 选取一个瓷砖当作笔刷 (按 <kbd>空格</kbd> 键显示瓷砖表)

   ![Palette](images/tilemap/palette.png){srcset="images/tilemap/palette@2x.png 2x"}

3. 用选取的笔刷铺设瓷砖. 要清除一个瓷砖, 可以选择一个空白瓷砖当笔刷覆盖掉它, 也可以使用橡皮擦工具 (<kbd>Edit ▸ Select Eraser</kbd>).

   ![铺瓷砖](images/tilemap/paint_tiles.png){srcset="images/tilemap/paint_tiles@2x.png 2x"}

你可以直接从层里选择一块瓷砖当作笔刷. 按住 <kbd>Shift</kbd> 键点击瓷砖即可把它用作当前笔刷. 按住 <kbd>Shift</kbd> 键并拖动还可以选择一片瓷砖作为大笔刷.

![选取瓷砖](images/tilemap/pick_tiles.png){srcset="images/tilemap/pick_tiles@2x.png 2x"}

## 把瓷砖地图加入到游戏中

把瓷砖地图加入游戏的步骤:

1. 建立一个游戏对象用以承载瓷砖地图组件. 这个游戏对象可以来自文件或者直接在集合里创建.
2. 右键点击游戏对象根节点选择 <kbd>Add Component File</kbd>.
3. 选取瓷砖地图文件.

![使用瓷砖地图](images/tilemap/use_tilemap.png){srcset="images/tilemap/use_tilemap@2x.png 2x"}

## 用脚本更改瓷砖

游戏运行时可以使用脚本动态读写瓷砖地图的内容. 通过调用 [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) 和 [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile) 方法:

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Replace grass-tile (2) with dangerous hole tile (number 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```
