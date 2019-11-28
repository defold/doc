---
title: Defold 中的 Spine 骨骼动画
brief: 本教程介绍了如何通过 _Spine_ 或者 _Dragon Bone_ 把骨骼动画带入 Defold.
---

# Spine 动画

_Spine_ 是由 Esoteric Software 开发的第三方动画工具, 可以让你使用 _骨骼_ 绑定的技术创建动画. 这对于角色或者动物动画非常方便, 对制作其他动画也很有帮助, 比如绳子, 车辆或者树叶.

Defold 实现了 [Spine JSON 格式](http://esotericsoftware.com/spine-json-format) 的运行时和动画表达.

Defold 支持了主要的 Spine 动画功能, 包括反向运动鞋 (IK).

::: 注意
目前, Defold 不支持翻转 X 或者 Y 轴的动画关键帧. Defold 只支持骨骼驱动的网格动画, 不支持单个三角形顶点动画. 一定要做的话就用骨骼 100% 绑定一个三角形来做骨骼动画.
:::

::: 注意
Defold 支持 Spine runtime 2.x 功能. 少量支持 Spine 3.x 功能. 为了保证兼容性请只使用 Spine 2.x 功能!
:::

## 概念

*Spine JSON 数据文件*
: 此数据文件包含骨架, 所有图片插槽名, 皮肤和动画数据. 虽然图片文件并不嵌入在这个文件里. Spine 和 Dragon Bones 都可以生成这个文件, 喜欢用哪个就用哪个.

*Spine scene*
: 把 Spine JSON 数据文件和 Defold 图集文件做捆绑以便在骨骼插槽上显示图片内容.

*Spine model*
: _SpineModel_ 组件是最终游戏对象里用的用于显示动画的组件. 此组件包含骨骼游戏对象树状关系, 要播放的动画, 要使用的皮肤以及渲染时要使用的材质. 详情请见 [SpineModel 教程](/manuals/spinemodel).

*Spine Node*
: 在 GUI 场景播放 Spine 动画用的组件, 相当于游戏场景的 Spine model 组件. 详情请见 [GUI spine 教程](/manuals/gui-spine).

## 动画工具

Defold 支持的 Spine JSON 数据文件可以用 Esoteric Software 的 _Spine_ 软件, 或者 _Dragon Bones_ 软件输出.

_Spine_ 软件主页 http://esotericsoftware.com

![Spine](images/spine/spine.png)

_Dragon Bones_ 软件主页 http://dragonbones.com

![Dragon Bones](images/spine/dragonbones.png)

::: 注意
_Dragon Bones_ 输出的 Spine JSON 数据文件应该能正常使用. 如果发现 _Dragon Bones_ 输出文件在 Defold 中显示不正确, 我们推荐先用官方 [Spine Skeleton Viewer](http://esotericsoftware.com/spine-skeleton-viewer) 检查数据是否能正确读出. Spine Skeleton Viewer 能够指出数据文件问题所在, 比如实例或者数据项缺失.
:::


## 导入 Spine 角色和动画

在 Spine 创建好模型和动画之后, 可以方便地导入到 Defold 中:

- 把动画输出为 Spine JSON 版本文件.
- 把输出的 JSON 文件放入项目目录中.
- 把所需所有碎图放入项目目录中.
- 把所有碎图建立 _图集_. (建立图集相关内容请参考 [2D 图像教程](/manuals/2dgraphics) 以及下面列举的一些注意事项)

![Export JSON from Spine](images/spine/spine_json_export.png)

如果使用 _Dragon Bones_, 选择 *Spine* 作为输出类型. 选择 *Images* 作为图片类型. 这样可以把 *.json* 及其所需图片输出到一个文件夹中. 如上所属导入 Defold 即可.

![Export JSON from Dragon Bones](images/spine/dragonbones_json_export.png)

数据存入 Defold 后, 就可以创建 _Spine scene_ 资源文件了:

- 新建 _Spine scene_ 资源文件 (从主菜单选择 <kbd>New ▸ Spine Scene File</kbd>)
- 双击文件打开 spine scene 编辑器.
- 设置 *Properties*.

![Setup the Spine Scene](images/spine/spinescene.png){srcset="images/spine/spinescene@2x.png 2x"}

Spine Json
: Spine JSON 数据文件.

Atlas
: Spine 动画需要的图集.

## 创建 SpineModel 组件

创建并配置好 _Spine scene_ 之后, 就可以创建 SpineModel 组件了. 详情请见 [SpineModel 教程](/manuals/spinemodel).

## 创建 Spine GUI nodes

在 GUI 场景也可以使用 Spine 动画. 详情请见 [GUI spine 教程](/manuals/gui-spine).

## 播放 Spine 动画

Defold 通过 Lua 接口实现了全方位控制 Spine 动画播放的运行环境. 详情请见 [动画教程](/manuals/animation).

## 图集相关注意事项

动画通过去掉图片文件后缀的方法识别引用图片. 在 Spine 软件里图片文件位于 *Images* 目录下:

![Spine images hierarchy](images/spine/spine_images.png)

上图中图片没有嵌套关系. 但是通常, 图片会被分组放入子目录下, 其引用就包含了子目录前缀. 比如, 骨骼插槽对文件 *head_parts/eyes.png* 的引用就是 *head_parts/eyes*. 输出的 JSON 文件图片引用也是这个所以 Defold 图集中图片名要与之相匹配.

在 Defold 里 <kbd>Add Images</kbd> 时, 图片会以文件名去掉后缀的方法命名. 所以对于 *eyes.png* 自动命名就是 "eyes". 这样正好但是这是不带路径的情况.

对于带路径的 "head_parts/eyes" 该怎么办? 最简单的办法就是建立动画组 (图集 *Outline* 视图根节点右键选择 *Add Animation Group*). 然后手动命名为 "head_parts/eyes" (名字里的 `/` 字符合法) 再把 "eyes.png" 放入这个动画组.

![Atlas path names](images/spine/atlas_names.png){srcset="images/spine/atlas_names@2x.png 2x"}

关于 Spine 动画控制详情请见 [动画教程](/manuals/animation).
