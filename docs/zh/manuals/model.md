---
title: Defold 中的3D模型
brief: 此手册介绍了如何将3D模型，骨骼和动画带入你的游戏之中.
---

# Model 组件

Defold 核心是3D的. 就算只有2D材质的话渲染也是3D的, 只不过是映射到平面屏幕上而已.  Defold 允许在集合中使用 3D 资源, 或者称作 _模型_ . 你可以用Defold制作全3D的, 或者2D和3D混合的游戏.

## 创建模型

来看一个示例. 我们已经用 _Blender_ 做好了一个带骨骼和动画的模型.

Blender 是一个著名的3D软件. 它可以运行在 Windows, Mac OS X and Linux 系统上并且可以在 http://www.blender.org 免费下载.

现在我们把它来导入 Defold.

![Model in Blender](images/model/blender.png){srcset="images/model/blender@2x.png 2x"}

首先需要使用 Blender Collada 导出器输出 *.dae* 格式的文件. 导出的文件包含模型的所有点，线和面, 还包含 _UV 坐标_ (模型与贴图的部分与部分的映射). 如果做了，还包含骨骼和动画数据.

关于多边形网格详见 http://en.wikipedia.org/wiki/Polygon_mesh. 关于 UV 坐标与 UV 映射详见 http://en.wikipedia.org/wiki/UV_mapping.

现在要导入模型, 简单的拖拽 *.dae* 文件及其相应的纹理图到 *Project 浏览器* 的某个位置.

![Imported model assets](images/model/assets.png){srcset="images/model/assets@2x.png 2x"}

## 创建 model 组件

Model 组件和其他游戏对象组件一样，两种创建办法:

- *Assets* 浏览器里 <kbd>右键点击</kbd> 选择 <kbd>New... ▸ Model</kbd> 创建 *Model 文件*.
- 直接在 *Outline* 视图的游戏对象上 <kbd>右键点击</kbd> 然后选择 <kbd>Add Component ▸ Model</kbd>.

![Model in game object](images/model/model.png)

模型组件需要设置一些属性:

*Mesh*
: 这个属性指定 Collada *.dae* 文件的模型网格. 如果文件包含多组网格, 只读取第一个.

*Material*
: 添加合适的材质. 一开始可以使用默认的 *model.material* 材质.

*Texture*
: 指定适当的纹理.

*Skeleton*
: 指定 Collada *.dae* 文件里的骨骼. 注意Defold只支持一个骨骼树.

*Animations*
: 指定模型的 *动画集文件*.

*Default Animation*
: 指定自动播放的默认动画 (从动画集之中) .


有了模型组件就可以使用随意使用组件功能同时可以使用 *Scene Editor* 工具移动，旋转和缩放模型游戏对象了.

![Wiggler ingame](images/model/ingame.png){srcset="images/model/ingame@2x.png 2x"}


