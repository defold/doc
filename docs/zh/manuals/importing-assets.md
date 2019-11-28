---
title: 导入和编辑资源
brief: 本教程介绍了在 Defold 中如何使用外部编辑器编辑资源文件.
---

# 导入和编辑资源导入和编辑资源

一个游戏项目通常包含了大量其他程序生成的资源文件, 比如图像, 3D 模型, 音乐文件, 动画之类的. Defold 工作流就包括使用第三方工具创建资源然后导入Defold中使用. 当这些资源导入之后就可以被Defold的各种组件使用, 比如 逐帧动画, 瓷砖地图, 粒子特效之类的:

* 图片用于创建 [图集](/manuals/atlas) 瓷砖图源可以用于 [sprite](/manuals/sprite), [瓷砖地图](/manuals/tilemap) 和 [粒子特效](/manuals/particlefx). 详情请见 [图像教程](/manuals/graphics/#importing-image-files).
* 声音文件可以用 [声音组件](/manuals/sound)来播放.
* Spine 动画数据可以用于 [Spine 组件](/manuals/spinemodel) 来显示.
* 字体文件 可以用于 [Label 组件](/manuals/label) 和GUI中的 [text 节点](/manuals/gui-text).
* Collada 模型可以用于 [Model 组件](/manuals/model) 来显示3D模型和动画.


## 第三方工具

Defold 并不提供图片, 声音, 模型 或者 动画文件的创建功能. 这些文件应该由 Defold 以外的工具创建好之后再导入到 Defold 里使用. Defold 自动检测资源文件的改动然后自动刷新到编辑器里.

目前内置编译器不提供自定义编译流程, 但是我们提供了另一个编译工具 (详见 [Bob编译器](/manuals/bob)) 方便加入任何编译流程.

Defold 编辑器自己生成的资源都是纯文本格式的以方便合并.甚至可以使用代码来修改 参见 [这个帖子](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210). 注意我们没有发布固定的资源文本格式, 因为格式可能随着升级不断变化.

另外要注意一点就是如果使用外部编辑器破坏了资源文本的话, 再回到 Defold 可能就无法打开这个文件了.
