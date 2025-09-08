---
title: GUI场景在Defold中
brief: 本手册介绍了Defold GUI编辑器、各种类型的GUI节点和GUI脚本。
---

# GUI

Defold为您提供了自定义的GUI编辑器和强大的脚本功能，这些功能专门用于构建和实现用户界面。

Defold中的图形用户界面是一个组件，您可以构建它并将其附加到游戏对象上，然后放置在集合中。该组件具有以下特性：

* 它具有简单但强大的布局功能，允许您的用户界面进行独立于分辨率和纵横比的渲染。
* 它可以通过*GUI脚本*附加逻辑行为。
* 它（默认情况下）在其他内容之上渲染，与摄像机视图无关，因此即使您有移动的摄像机，您的GUI元素也会保持在屏幕上的位置。渲染行为可以更改。

GUI组件独立于游戏视图渲染。因此，它不会放置在集合编辑器中的特定位置，也不会在集合编辑器中具有视觉表示。但是，GUI组件必须驻留在位于集合中的游戏对象中。更改该位置不会对GUI产生影响。

## 创建GUI组件

GUI组件是从GUI场景原型文件（在其他引擎中也称为"prefabs"或"blueprints"）创建的。要创建新的GUI组件，在*Assets*浏览器中<kbd>右键点击</kbd>一个位置，然后选择<kbd>New ▸ Gui</kbd>。为新GUI文件键入一个名称，然后按<kbd>Ok</kbd>。

![New gui file](images/gui/new_gui_file.png)

Defold现在会自动在GUI场景编辑器中打开该文件。

![New gui](images/gui/new_gui.png)

*大纲*列出了所有GUI的内容：它的节点列表和任何依赖项（见下文）。

中央编辑区域显示GUI。编辑区域右上角的工具栏包含*移动*、*旋转*和*缩放*工具，以及一个[布局](/manuals/gui-layouts)选择器。

![toolbar](images/gui/toolbar.png)

白色矩形显示当前选定布局的边界，即项目设置中设置的默认显示宽度和高度。

## GUI属性

在*大纲*中选择根"Gui"节点会显示GUI组件的*属性*：

*Script*
: 绑定到此GUI组件的GUI脚本。

*Material*
: 渲染此GUI时使用的材质。请注意，也可以从大纲面板向GUI添加多个材质，并将这些材质分配给各个节点。

*Adjust Reference*
: 控制如何计算每个节点的*Adjust Mode*：

  - `Per Node` 根据父节点调整后的大小或调整后的屏幕大小调整每个节点。
  - `Disable` 关闭节点调整模式。这将强制所有节点保持其设置的大小。

*Current Nodes*
: 此GUI中当前使用的节点数。

*Max Nodes*
: 此GUI的最大节点数。

*Max Dynamic Textures*
: 可以使用[`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip)创建的最大纹理数。

## 运行时操作

您可以使用`go.get()`和`go.set()`从脚本组件在运行时操作GUI属性：

字体
: 获取或设置GUI中使用的字体。

![get_set_font](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- 获取当前分配给id为'default'的字体的字体文件
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- 将id为'default'的字体设置为分配给资源属性'mybigfont'的字体文件
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- 获取分配给id为'default'的新字体文件
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

材质
: 获取或设置GUI中使用的材质。

![get_set_material](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- 获取当前分配给id为'effect'的材质文件
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- 将id为'effect'的材质设置为分配给资源属性'myeffect'的材质文件
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- 获取分配给id为'effect'的新材质文件
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

纹理
: 获取或设置GUI中使用的纹理（图集）。

![get_set_texture](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- 获取当前分配给id为'theme'的纹理文件
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- 将id为'theme'的纹理设置为分配给资源属性'mytheme'的纹理文件
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- 获取分配给id为'theme'的新纹理文件
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## 依赖项

Defold游戏中的资源树是静态的，因此您需要为GUI节点添加的任何依赖项都必须添加到组件中。*大纲*按类型将所有依赖项分组在"文件夹"下：

![dependencies](images/gui/dependencies.png)

要添加新的依赖项，将其从*Asset*窗格拖放到编辑器视图中。

或者，<kbd>右键点击</kbd>*大纲*中的"Gui"根节点，然后从弹出上下文菜单中选择<kbd>Add ▸ [type]</kbd>。

您也可以<kbd>右键点击</kbd>要添加类型的文件夹图标，然后选择<kbd>Add ▸ [type]</kbd>。

## 节点类型

界面有节点组成. 节点是一种类似游戏对象的元素. 可以进行位移 (移动, 旋转和缩放) 并且以父子树形结构排列. 有以下几种节点类型:

Box node
: ![box node](images/icons/gui-box-node.png){.left}
  显示为纯色, 纹理或者逐帧动画的矩形. 详情请见 [方块节点教程](/manuals/gui-box).

<div style="clear: both;"></div>

Text node
: ![text node](images/icons/gui-text-node.png){.left}
  显示文字. 详情请见 [文本节点教程](/manuals/gui-text).

<div style="clear: both;"></div>

Pie node
: ![pie node](images/icons/gui-pie-node.png){.left}
  圆形或椭圆饼图. 详情请见 [饼图节点教程](/manuals/gui-pie).

<div style="clear: both;"></div>

Template node
: ![template node](images/icons/gui.png){.left}
  模板用来基于其他界面文件创建节点实例. 详情请见 [模板节点教程](/manuals/gui-template).

<div style="clear: both;"></div>

ParticleFX node
: ![particlefx node](images/icons/particlefx.png){.left}
  显示粒子特效. 详情请见 [粒子特效节点教程](/manuals/gui-particlefx).

<div style="clear: both;"></div>

右键点击 *Nodes* 文件夹选择 <kbd>Add ▸</kbd> 然后点击 <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> 或 <kbd>ParticleFx</kbd> 即可创建节点.

![Add nodes](images/gui/add_node.png)

还可以用快捷键 <kbd>A</kbd> 来创建节点.

## 节点属性

节点有自身属性:

Id
: 节点id. 每个id是这个界面中的唯一值.

Position, Rotation and Scale
: 节点位移. 可以使用 *移动*, *旋转* 和 *缩放* 工具自由修改. 也可以用脚本动画形式控制这些值.

Size (box, text 和 pie 节点)
: 默认尺寸设置为自动, 如果需要手动设定尺寸可以设置 *Size Mode* 为 `Manual`. 节点尺寸决定了节点接收输入操作的范围. 此值也可使用脚本动画进行控制.

Size Mode (box 和 pie 节点)
: 如果设为 `Automatic` 则自动计算并设置节点尺寸. 如果设为 `Manual` 则需手动设置节点尺寸.

Enabled
: 如果未选中, 则节点不会被渲染, 不会被动画驱动且不能使用 `gui.pick_node()` 返回节点. 可以使用 `gui.set_enabled()` 和 `gui.is_enabled()` 函数手动打开或检查该属性.

Visible
: 如果未选中, 则节点不会被渲染, 但是可以被动画驱动且可以使用 `gui.pick_node()` 返回节点. 可以使用 `gui.set_visible()` 和 `gui.get_visible()` 函数手动打开或检查该属性.

Text (text 节点)
: 节点上显示的文字.

Line Break (text 节点)
: 文字基于节点宽度换行.

Font (text 节点)
: 文字字体.

Texture (box 和 pie 节点)
: 节点上显示的纹理. 可以使用图集和瓷砖图源的图片或动画.

Slice 9 (box 节点)
: 缩放九宫格. 详情请见 [box 节点教程](/manuals/gui-box).

Inner Radius (pie 节点)
: 节点内半径, 延 X 轴. 详情请见 [pie 节点教程](/manuals/gui-pie).

Outer Bounds (pie 节点)
: 节点外轮廓. 详情请见 [pie 节点教程](/manuals/gui-pie).

Perimeter Vertices (pie 节点)
: 图形的分段数, 就是360度一圈需要的顶点数. 详情请见 [Pie 节点教程](/manuals/gui-pie)

Pie Fill Angle (pie 节点)
: 饼状图的填充. 详情请见 [Pie 节点教程](/manuals/gui-pie)

Template (template 节点)
: 节点模板界面文件. 详情请见 [Template 节点教程](/manuals/gui-template)

ParticleFX (particlefx 节点)
: 节点上显示的粒子特效. 详情请见 [ParticleFX 节点教程](/manuals/gui-particlefx)

Color
: 节点颜色. 如果用纹理填充, 则对纹理进行染色. 颜色可由脚本动画控制.

Alpha
: 节点不透明度. 不透明度可由脚本动画控制.

Inherit Alpha
: 继承父节点不透明度. 最终结果是父节点与此节点不透明度的叠加.

Leading (text 节点)
: 每行开头空白. `0` 无空白. 默认值为 `1`.

Tracking (text 节点)
: 字符间距缩放值. 默认值为 0.

Layer
: 把此节点分配给层. 详情请见下文.

Blend mode
: 混合模式控制其与下层颜色混合后的结果:
  - `Alpha` 覆盖下层颜色. 有的软件将其称作 "普通" 混合模式.
  - `Add` 叠加下层颜色. 有的软件将其称作 "增强" 混合模式.
  - `Multiply` 与下层颜色相乘.
  - `Screen` 将节点的像素值与背景成反比. 这种混合模式在图形软件中称作 "Screen".

Pivot
: 设置节点的枢轴点。这可以看作是节点的"中心点"。任何旋转、缩放或大小更改都将围绕此点发生。

  可能的值是`Center`、`North`、`South`、`East`、`West`、`North West`、`North East`、`South West`或`South East`。

  ![pivot point](images/gui/pivot.png)

  如果您更改节点的枢轴点，节点将移动，使新枢轴点位于节点的位置。文本节点对齐方式设置为`Center`表示文本居中对齐，`West`表示文本左对齐，`East`表示文本右对齐。

X Anchor, Y Anchor
: 锚点控制着当窗体或者父节点拉伸时当前节点位置如何处理.

  ![Anchor unadjusted](images/gui/anchoring_unadjusted.png)

  可选值有:

  - `None` (*X轴* 和 *Y轴*) 相对于窗体或者父节点的中心, 保持自身位置.
  - `Left` 或 `Right` (*X轴*) 缩放水平方向位置以便保持其相对于窗体或者父节点宽度方向上的百分比位置不变.
  - `Top` 或 `Bottom` (*Y轴*) 缩放垂直方向位置以便保持其相对于窗体或者父节点高度方向上的百分比位置不变.

  ![Anchoring](images/gui/anchoring.png)

Adjust Mode
: 节点调整模式. 调整模式控制着当窗体或者父节点拉伸时当前节点尺寸如何处理.

  这里有一个节点放置在逻辑分辨率为横屏的场景中:

  ![Unadjusted](images/gui/unadjusted.png)

  当场景需要填充竖屏时. 每个节点都会被拉伸. 但是如果使用了适当的调整模式, 节点内容的长宽比可以保持不变. 可选值有:

  - `Fit` 缩放节点内容,使其等于拉伸的边界框宽度或高度, 以数值最小者为准. 换句话说, 内容将拉伸到父级的边界.
  - `Zoom` 缩放节点内容,使其等于拉伸的边界框宽度或高度, 以数值最大者为准. 换句话说, 内容将超越过父级的边界.
  - `Stretch` 拉伸节点内容, 使其填充父级的边界框.

  ![Adjust modes](images/gui/adjusted.png)

  如果场景的 *Adjust Reference* 设置为 `Disabled` 的话, 此设置被忽略.

Clipping Mode (box 和 pie 节点)
: 剔除模式:

  - `None` 正常渲染.
  - `Stencil` 以当前节点边框作为子节点蒙版.

  详情请见 [GUI 蒙版教程](/manuals/gui-clipping)

Clipping Visible (box 和 pie 节点)
: 蒙版可见. 详情请见 [GUI clipping manual](/manuals/gui-clipping)

Clipping Inverted (box 和 pie 节点)
: 反转蒙版. 详情请见 [GUI clipping manual](/manuals/gui-clipping)


## 枢轴、锚点和调整模式

枢轴、锚点和调整模式的组合允许非常灵活的GUI设计，但如果不看具体示例，可能很难理解它们是如何工作的。让我们以这个为640x1136屏幕创建的GUI模型为例：

![](images/gui/adjustmode_example_original.png)

界面是使用X和Y锚点设置为None创建的，每个节点的调整模式保留为默认值Fit。顶部面板的枢轴点是North，底部面板的枢轴是South，顶部面板中的条的枢轴点设置为West。其余节点的枢轴点都设置为Center。如果我们将窗口调整得更宽，会发生以下情况：

![](images/gui/adjustmode_example_resized.png)

现在，如果我们希望顶部和底部条始终与屏幕一样宽怎么办？我们可以将顶部和底部的灰色背景面板的调整模式更改为Stretch：

![](images/gui/adjustmode_example_resized_stretch.png)

这样更好。灰色背景面板现在将始终拉伸到窗口的宽度，但顶部面板中的条以及底部的两个框位置不正确。如果我们希望将顶部的条保持在左侧对齐，我们需要将X锚点从None更改为Left：

![](images/gui/adjustmode_example_top_anchor_left.png)

这正是我们想要的顶部面板。顶部面板中的条已经将其枢轴点设置为West，这意味着它们将很好地定位，条的左/西边缘（枢轴）锚定到父面板的左边缘（X锚点）。

现在，如果我们将左侧框的X锚点设置为Left，右侧框的X锚点设置为Right，我们得到以下结果：

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

这还不是预期的结果。两个框应该像顶部面板中的两个条一样保持靠近左右边缘。原因是枢轴点错误：

![](images/gui/adjustmode_example_bottom_pivot_center.png)

两个框的枢轴点都设置为Center。这意味着当屏幕变宽时，框的中心点（枢轴点）将保持与边缘相同的相对距离。对于左侧框，在原始的640x1136窗口中，它距离左边缘17%：

![](images/gui/adjustmode_example_original_ratio.png)

当屏幕调整大小时，左侧框的中心点保持与左边缘相同的17%距离：

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

如果我们将左侧框的枢轴点从Center更改为West，右侧框更改为East，并重新定位框，即使屏幕调整大小，我们也能得到我们想要的结果：

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## 绘制顺序

所有节点都按照它们在"Nodes"文件夹下列出的顺序进行渲染。列表顶部的节点首先绘制，因此将出现在所有其他节点的后面。列表中的最后一个节点最后绘制，意味着它将出现在所有其他节点的前面。更改节点上的Z值不会控制其绘制顺序；但是，如果您将Z值设置在渲染脚本的渲染范围之外，该节点将不再渲染到屏幕上。您可以使用层覆盖节点的索引顺序（见下文）。

![Draw order](images/gui/draw_order.png)

选择一个节点并按<kbd>Alt + Up/Down</kbd>向上或向下移动节点并更改其索引顺序。

绘制顺序可以在脚本中更改：

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## 父子层次结构

通过将一个节点拖放到您希望成为其父节点的节点上，使该节点成为另一个节点的子节点。具有父节点的节点继承应用于父节点的变换（位置、旋转和缩放），并相对于父节点枢轴点。

![Parent child](images/gui/parent_child.png)

父节点在其子节点之前绘制。使用层来更改父节点和子节点的绘制顺序并优化节点的渲染（见下文）。


## 层和绘制调用

层提供了对节点绘制方式的精细控制，可用于减少引擎绘制GUI场景必须创建的绘制调用次数。当引擎即将绘制GUI场景的节点时，它根据以下条件将节点分组到绘制调用批次中：

- 节点必须使用相同的类型。
- 节点必须使用相同的图集或瓷砖图源。
- 节点必须使用相同的混合模式渲染。

如果其中任何一个条件不满足，就会破坏合批并产生另一个绘制调用。蒙版和被蒙版节点必然会破坏合批并产生绘制调用。

树形结构对于节点管理非常方便。但是混合不同类型的节点一定会破坏合批渲染：

![Breaking batch hierarchy](images/gui/break_batch.png)

渲染管线被迫为不同类型的节点建立不同的渲染批次。这三个按钮就会产生6次绘制调用。

如果使用层，可以重塑节点的绘制顺序，渲染管线就能更好地进行合批并减少绘制调用。第一步是创建新层。在*大纲*的"Layers"文件夹上<kbd>右键点击</kbd>，然后选择<kbd>Add ▸ Layer</kbd>。在*属性*视图中填写*Name*属性为层命名。

![Layers](images/gui/layers.png)

现在为每个节点的*Layer*属性分配适当的层。层的绘制顺序优先级高于默认情况，所以将按钮背景都分配给"graphics"层，文本节点都分配给"text"层，那么界面绘制的顺序就是这样的：

* 首先绘制"graphics"层中的节点：

  1. "button-1"
  2. "button-2"
  3. "button-3"

* 然后绘制"text"层中的节点：

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

这样一来合批就形成了，不再需要那么多绘制调用！

注意，如果子节点没有设置分配层，默认会继承分配父节点所在的层。没有设置分配层的节点会被归为"null"层，这个层最先被绘制。
