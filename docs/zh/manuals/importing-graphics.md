---
title: 2D图形导入和使用在Defold中
brief: 本手册介绍了如何导入和使用2D图形.
---

# 导入2D图形

Defold支持2D游戏中常用的多种视觉组件。您可以使用Defold创建静态和动画精灵、UI组件、粒子效果、瓦片地图和位图字体。在创建任何这些视觉组件之前，您需要导入包含您希望使用的图形的图像文件。要导入图像文件，只需将文件从计算机的文件系统中拖出，然后放到Defold编辑器的*资源面板*中的适当位置。

![Importing files](images/graphics/import.png)

::: sidenote
Defold支持PNG和JPEG图像格式。其他图像格式需要先转换才能使用。
:::


## 创建Defold资源

当图像导入到Defold后，它们可以用来创建Defold特定的资源：

![atlas](images/icons/atlas.png){.icon} 图集
: 图集包含单独图像文件的列表，这些文件会自动组合成更大的纹理图像。图集可以包含静态图像和*动画组*，即组成翻页动画的图像集。

  ![atlas](images/graphics/atlas.png)

在[图集手册](/manuals/atlas)中了解更多关于图集资源的信息。

![tile source](images/icons/tilesource.png){.icon} 瓦片源
: 瓦片源引用一个图像文件，该文件已经被设计成由在统一网格上排序的较小子图像组成。这种复合图像常用的另一个术语是_精灵表_。瓦片源可以包含翻页动画，由动画的第一帧和最后一帧定义。还可以使用图像自动为瓦片附加碰撞形状。

  ![tile source](images/graphics/tilesource.png)

在[瓦片源手册](/manuals/tilesource)中了解更多关于瓦片源资源的信息。

![bitmap font](images/icons/font.png){.icon} 位图字体
: 位图字体将其字形包含在PNG字体表中。这些类型的字体与从TrueType或OpenType字体文件生成的字体相比没有性能改进，但可以在图像中直接包含任意图形、颜色和阴影。

在[字体手册](/manuals/font/#位图-bmfonts)中了解更多关于位图字体的信息。

  ![BMfont](images/font/bm_font.png)


## 使用Defold资源

当您将图像转换为图集和瓦片源文件后，您可以使用这些文件创建多种不同类型的视觉组件：

![sprite](images/icons/sprite.png){.icon}
: 精灵是显示在屏幕上的静态图像或翻页动画。

  ![sprite](images/graphics/sprite.png)

在[精灵手册](/manuals/sprite)中了解更多关于精灵的信息。

![tile map](images/icons/tilemap.png){.icon} 瓦片地图
: 瓦片地图组件将来自瓦片源的瓦片（图像和碰撞形状）拼凑成地图。瓦片地图不能使用图集源。

  ![tilemap](images/graphics/tilemap.png)

在[瓦片地图手册](/manuals/tilemap)中了解更多关于瓦片地图的信息。

![particle effect](images/icons/particlefx.png){.icon} 粒子特效
: 从粒子发射器生成的粒子由来自图集或瓦片源的静态图像或翻页动画组成。

  ![particles](images/graphics/particles.png)

在[粒子特效手册](/manuals/particlefx)中了解更多关于粒子特效的信息。

![gui](images/icons/gui.png){.icon} GUI
: GUI方块节点和饼图节点可以使用来自图集和瓦片源的静态图像和翻页动画。

  ![gui](images/graphics/gui.png)

在[GUI手册](/manuals/gui)中了解更多关于GUI的信息。
