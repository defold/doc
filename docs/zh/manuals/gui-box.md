---
title: Defold中的GUI方块节点
brief: 本手册介绍了如何使用GUI方块节点。
---

# GUI 方块节点

方块节点是一个填充了颜色、纹理或动画的矩形。

## 添加方块节点

添加方块节点可以在 *Outline* 中 <kbd>右键点击</kbd> 然后选择 <kbd>Add ▸ Box</kbd>, 或者按 <kbd>A</kbd> 然后选择 <kbd>Box</kbd>.

你可以使用已添加到GUI中的图集或瓦片图源的图像和动画。通过<kbd>右键点击</kbd>*Outline*中的*Textures*文件夹图标并选择<kbd>Add ▸ Textures...</kbd>来添加纹理。然后设置方块节点的*Texture*属性：

![纹理](images/gui-box/create.png)

注意方块节点的颜色会对图形进行染色。染色颜色会与图像数据相乘，这意味着如果将颜色设置为白色（默认值），则不会应用染色效果。

![染色纹理](images/gui-box/tinted.png)

即使没有分配纹理，或者将alpha设置为`0`，或者将大小设置为`0, 0, 0`，方块节点也始终会被渲染。方块节点应该始终分配纹理，以便渲染器能够正确地进行批处理并减少绘制调用次数。

## 播放动画

方块节点可以播放图集或瓦片图源中的动画。有关详细信息，请参阅[逐帧动画手册](/manuals/flipbook-animation)。

:[Slice-9](../shared/slice-9-texturing.md)