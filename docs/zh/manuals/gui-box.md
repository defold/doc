---
title: Defold 中的 GUI 方块节点
brief: 本教程介绍了如何使用 GUI 方块节点.
---

# GUI 方块节点

方块节点是一个可以填充颜色, 纹理或者动画的矩形.

## 添加方块节点

添加方块节点可以在 *Outline* 中 <kbd>右键点击</kbd> 然后选择 <kbd>Add ▸ Box</kbd>, 或者按 <kbd>A</kbd> 然后选择 <kbd>Box</kbd>.

你可以使用图集或者瓷砖图源里的图片或者动画添加到GUI上去. 要添加纹理 <kbd>右键点击</kbd>  *Outline* 中的 *Textures* 文件夹图标, 选择 <kbd>Add ▸ Textures...</kbd>. 然后设置方块节点的 *Texture* 属性:

![纹理](images/gui-box/create.png)

注意方块节点的图像可以染色. 使用 color 加成到图片上面, 也就是说如果设置 color 为白色 (默认值) 则没有染色.

![染色纹理](images/gui-box/tinted.png)

即使没有纹理设置, 方块节点也会被渲染, 或者不论把 alpha 设置成 `0`, 还是把 sized 设置成 `0, 0, 0`. 方块节点应该设置纹理以便渲染器合批而减少 draw call.

## 播放动画

Box 节点可以由其图集或者瓷砖图源内容来播放动画. 详情请见 [逐帧动画教程](/manuals/flipbook-animation).

:[Slice-9](../shared/slice-9-texturing.md)