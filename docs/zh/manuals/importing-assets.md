---
title: 导入和编辑资源
brief: 本教程介绍了导入, 编辑资源的方法.
---

# 导入和编辑资源导入和编辑资源

一个游戏项目通常包含了大量其他程序生成的资源文件, 比如图像, 3D 模型, 音乐文件, 动画之类的. Defold 工作流就包括使用第三方工具创建资源然后导入Defold中使用. 当这些资源导入之后就可以被Defold的各种组件使用, 比如 逐帧动画, 瓷砖地图, 粒子特效之类的:


## 导入资源

Defold 要求其所用资源全部位于项目文件夹内. 先导入后使用. 导入方法很简单, 从文件系统任意位置拖动任意文件放入 Defold 编辑器 _资源面板_ 里即可.

![Importing files](images/graphics/import.png){srcset="images/graphics/import@2x.png 2x"}

::: 注意
Defold 支持 PNG 和 JPEG 图片格式. 其中 PNG 图片必须是 32 位 RGBA 格式的. 其他格式要先转换成支持格式后再使用.
:::

## 使用资源

当资源文件导入 Defold 之后就可以使用各种组件来创造逐帧动画, 瓷砖地图, 粒子特效等各种内容:

* 图片可以用来实现2D游戏常见的各种可视内容. 详情请见 [如何导入和使用2D图像](/manuals/importing-graphics).
* 声音文件可以用 [声音组件](/manuals/sound)来播放.
* Spine 动画数据可以用于 [Spine 组件](/manuals/spinemodel) 来显示.
* 字体文件 可以用于 [Label 组件](/manuals/label) 和GUI中的 [text 节点](/manuals/gui-text).
* Collada 模型可以用于 [Model 组件](/manuals/model) 来显示3D模型和动画. [关于3D模型导入详见这里](/manuals/importing-models).


## 编辑外部资源

Defold 并不提供图片, 声音, 模型 或者 动画文件的创建功能. 这些文件应该由 Defold 以外的工具创建好之后再导入到 Defold 里使用. Defold 自动检测资源文件的改动然后自动刷新到编辑器里. 之后 Defold 会自动进行资源文件的更新.


## 编辑 Defold 资源

Defold 编辑器自己生成的资源都是纯文本格式的以方便合并.甚至可以使用代码来修改 参见 [这个帖子](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210).

注意我们没有发布固定的资源文本格式, 因为格式可能随着升级不断变化. 你也可以使用 [编辑器脚本](/manuals/editor-scripts/) 在编辑器特定的生命周期中运行脚本来生成或者修改资源.

另外要注意一点就是如果使用外部编辑器破坏了资源文本的话, 再回到 Defold 可能就无法打开这个文件了.

某些第三方工具 [比如 Tiled](/assets/tiled/) 也可以用来自动生成 Defold 资源.
