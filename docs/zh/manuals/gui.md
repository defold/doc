---
title: Defold中的GUI场景
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

*Outline*列出了所有GUI的内容：它的节点列表和任何依赖项（见下文）。

中央编辑区域显示GUI。编辑区域右上角的工具栏包含*移动*、*旋转*和*缩放*工具，以及一个[布局](/manuals/gui-layouts)选择器。

![toolbar](images/gui/toolbar.png)

白色矩形显示当前选定布局的边界，即项目设置中设置的默认显示宽度和高度。

## Gui属性

在*Outline*中选择根"Gui"节点会显示GUI组件的*Properties*：

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

Defold游戏中的资源树是静态的，因此您需要为GUI节点添加的任何依赖项都必须添加到组件中。*Outline*按类型将所有依赖项分组在"文件夹"下：

![dependencies](images/gui/dependencies.png)

要添加新的依赖项，将其从*Asset*窗格拖放到编辑器视图中。

或者，<kbd>右键点击</kbd>*Outline*中的"Gui"根节点，然后从弹出上下文菜单中选择<kbd>Add ▸ [type]</kbd>。

您也可以<kbd>右键点击</kbd>要添加类型的文件夹图标，然后选择<kbd>Add ▸ [type]</kbd>。

## 节点类型

GUI组件由一组节点构建而成。节点是简单的元素。它们可以被平移（移动、缩放和旋转），并在编辑器中或通过脚本在运行时按父子层次结构排序。存在以下节点类型：

Box node
: ![box node](images/icons/gui-box-node.png){.left}
  具有单一颜色、纹理或翻书动画的矩形节点。详情请参见[Box节点文档](/manuals/gui-box)。

<div style="clear: both;"></div>

Text node
: ![text node](images/icons/gui-text-node.png){.left}
  显示文本。详情请参见[Text节点文档](/manuals/gui-text)。

<div style="clear: both;"></div>

Pie node
: ![pie node](images/icons/gui-pie-node.png){.left}
  可以部分填充或反转的圆形或椭圆节点。详情请参见[Pie节点文档](/manuals/gui-pie)。

<div style="clear: both;"></div>

Template node
: ![template node](images/icons/gui.png){.left}
  模板用于基于其他GUI场景文件创建实例。详情请参见[Template节点文档](/manuals/gui-template)。

<div style="clear: both;"></div>

ParticleFX node
: ![particlefx node](images/icons/particlefx.png){.left}
  播放粒子效果。详情请参见[ParticleFX节点文档](/manuals/gui-particlefx)。

<div style="clear: both;"></div>

通过右键点击*Nodes*文件夹并选择<kbd>Add ▸</kbd>，然后选择<kbd>Box</kbd>、<kbd>Text</kbd>、<kbd>Pie</kbd>、<kbd>Template</kbd>或<kbd>ParticleFx</kbd>来添加节点。

![Add nodes](images/gui/add_node.png)

您也可以按<kbd>A</kbd>并选择要添加到GUI的类型。

## 节点属性

每个节点都有一组广泛的属性来控制其外观：

Id
: 节点的标识。此名称在GUI场景中必须是唯一的。

Position, Rotation and Scale
: 控制节点的位置、方向和拉伸。您可以使用*移动*、*旋转*和*缩放*工具更改这些值。这些值可以从脚本中动画化（[了解更多](/manuals/property-animation)）。

Size (box, text和pie节点)
: 节点的大小默认为自动，但通过将*Size Mode*设置为`Manual`，您可以更改该值。大小定义了节点的边界，并在进行输入选择时使用。此值可以从脚本中动画化（[了解更多](/manuals/property-animation)）。

Size Mode (box和pie节点)
: 如果设置为`Automatic`，编辑器将为节点设置大小。如果设置为`Manual`，您可以自己设置大小。

Enabled
: 如果未选中，节点不会被渲染，不会被动画化，也不能使用`gui.pick_node()`进行选择。使用`gui.set_enabled()`和`gui.is_enabled()`以编程方式更改和检查此属性。

Visible
: 如果未选中，节点不会被渲染，但仍然可以被动画化，并且可以使用`gui.pick_node()`进行选择。使用`gui.set_visible()`和`gui.get_visible()`以编程方式更改和检查此属性。

Text (text节点)
: 要在节点上显示的文本。

Line Break (text节点)
: 设置文本根据节点的宽度进行换行。

Font (text节点)
: 渲染文本时要使用的字体。

Texture (box和pie节点)
: 要在节点上绘制的纹理。这是对图集或瓷砖图源中的图像或动画的引用。

Material (box, pie节点, text和particlefx节点)
: 绘制节点时要使用的材质。这可以是添加到大纲的Materials部分的材质，或者留空以使用分配给GUI组件的默认材质。

Slice 9 (box节点)
: 设置当节点调整大小时保留节点纹理边缘周围的像素大小。详情请参见[Box节点文档](/manuals/gui-box)。

Inner Radius (pie节点)
: 节点的内半径，沿X轴表示。详情请参见[Pie节点文档](/manuals/gui-pie)。

Outer Bounds (pie节点)
: 控制外边界的行为。详情请参见[Pie节点文档](/manuals/gui-pie)。

Perimeter Vertices (pie节点)
: 将用于构建形状的段数。详情请参见[Pie节点文档](/manuals/gui-pie)。

Pie Fill Angle (pie节点)
: 饼图应该填充多少。详情请参见[Pie节点文档](/manuals/gui-pie)。

Template (template节点)
: 用作节点模板的GUI场景文件。详情请参见[Template节点文档](/manuals/gui-template)。

ParticleFX (particlefx节点)
: 在此节点上使用的粒子效果。详情请参见[ParticleFX节点文档](/manuals/gui-particlefx)。

Color
: 节点的颜色。如果节点有纹理，颜色会着色纹理。颜色可以从脚本中动画化（[了解更多](/manuals/property-animation)）。

Alpha
: 节点的半透明性。alpha值可以从脚本中动画化（[了解更多](/manuals/property-animation)）。

Inherit Alpha
: 设置此复选框使节点继承父节点的alpha值。然后节点的alpha值将与父节点的alpha值相乘。

Leading (text节点)
: 行间距的缩放数字。值为`0`表示没有行间距。`1`（默认值）是正常行间距。

Tracking (text节点)
: 字母间距的缩放数字。默认为0。

Layer
: 为节点分配层会覆盖正常的绘制顺序，而是遵循层顺序。详情请参见下文。

Blend mode
: 控制节点图形与背景图形的混合方式：
  - `Alpha` 将节点的像素值与背景进行alpha混合。这对应于图形软件中的"正常"混合模式。
  - `Add` 将节点的像素值与背景相加。这对应于某些图形软件中的"线性减淡"。
  - `Multiply` 将节点的像素值与背景相乘。
  - `Screen` 将节点的像素值与背景成反比相乘。这对应于图形软件中的"屏幕"混合模式。

Pivot
: 设置节点的枢轴点。这可以看作是节点的"中心点"。任何旋转、缩放或大小更改都将围绕此点发生。

  可能的值是`Center`、`North`、`South`、`East`、`West`、`North West`、`North East`、`South West`或`South East`。

  ![pivot point](images/gui/pivot.png)

  如果您更改节点的pivot，节点将移动，使新pivot位于节点的位置。文本节点对齐方式设置为`Center`表示文本居中对齐，`West`表示文本左对齐，`East`表示文本右对齐。

X Anchor, Y Anchor
: 锚点控制当场景边界或父节点边界被拉伸以适应物理屏幕大小时节点的垂直和水平位置如何改变。

  ![Anchor unadjusted](images/gui/anchoring_unadjusted.png)

  以下锚点模式可用：

  - `None`（对于*X Anchor*和*Y Anchor*）保持节点相对于父节点或场景中心的位置，相对于其*调整后*的大小。
  - `Left`或`Right`（*X Anchor*）缩放节点的水平位置，使其与父节点或场景的左边缘和右边缘保持相同的百分比距离。
  - `Top`或`Bottom`（*Y Anchor*）缩放节点的垂直位置，使其与父节点或场景的顶部和底部边缘保持相同的百分比距离。

  ![Anchoring](images/gui/anchoring.png)

Adjust Mode
: 设置节点的调整模式。调整模式设置控制当场景边界或父节点边界被调整以适应物理屏幕大小时节点会发生什么。

  在为典型横向分辨率创建的场景中创建的节点：

  ![Unadjusted](images/gui/unadjusted.png)

  使场景适应纵向屏幕会导致场景被拉伸。每个节点的边界框同样被拉伸。但是，通过设置调整模式，可以保持节点内容的纵横比不变。以下模式可用：

  - `Fit` 缩放节点内容，使其等于拉伸的边界框宽度或高度，以较小者为准。换句话说，内容将适合拉伸的节点边界框内。
  - `Zoom` 缩放节点内容，使其等于拉伸的边界框宽度或高度，以较大者为准。换句话说，内容将完全覆盖拉伸的节点边界框。
  - `Stretch` 拉伸节点内容，使其填充拉伸的节点边界框。

  ![Adjust modes](images/gui/adjusted.png)

  如果GUI场景属性*Adjust Reference*设置为`Disabled`，此设置将被忽略。

Clipping Mode (box和pie节点)
: 设置节点上的裁剪模式：

  - `None` 正常渲染节点。
  - `Stencil` 使节点边界定义用于裁剪节点子节点的模板蒙版。

  详情请参见[GUI裁剪手册](/manuals/gui-clipping)。

Clipping Visible (box和pie节点)
: 设置为在模板区域中渲染节点内容。详情请参见[GUI裁剪手册](/manuals/gui-clipping)。

Clipping Inverted (box和pie节点)
: 反转模板蒙版。详情请参见[GUI裁剪手册](/manuals/gui-clipping)。


## 枢轴、锚点和调整模式

枢轴、锚点和调整模式属性的组合允许非常灵活的GUI设计，但如果不看具体示例，可能很难理解它们是如何工作的。让我们以这个为640x1136屏幕创建的GUI模型为例：

![](images/gui/adjustmode_example_original.png)

界面是使用X和Y锚点设置为None创建的，每个节点的调整模式保留为默认值Fit。顶部面板的pivot是North，底部面板的pivot是South，顶部面板中的条的pivot设置为West。其余节点的pivot都设置为Center。如果我们将窗口调整得更宽，会发生以下情况：

![](images/gui/adjustmode_example_resized.png)

现在，如果我们希望顶部和底部条始终与屏幕一样宽怎么办？我们可以将顶部和底部的灰色背景面板的调整模式更改为Stretch：

![](images/gui/adjustmode_example_resized_stretch.png)

这样更好。灰色背景面板现在将始终拉伸到窗口的宽度，但顶部面板中的条以及底部的两个框位置不正确。如果我们希望将顶部的条保持在左侧对齐，我们需要将X锚点从None更改为Left：

![](images/gui/adjustmode_example_top_anchor_left.png)

这正是我们想要的顶部面板。顶部面板中的条已经将其枢轴点设置为West，这意味着它们将很好地定位，条的左/西边缘（枢轴）锚定到父面板的左边缘（X锚点）。

现在，如果我们将左侧框的X锚点设置为Left，右侧框的X锚点设置为Right，我们得到以下结果：

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

这还不是预期的结果。两个框应该像顶部面板中的两个条一样保持靠近左右边缘。原因是pivot错误：

![](images/gui/adjustmode_example_bottom_pivot_center.png)

两个框的pivot都设置为Center。这意味着当屏幕变宽时，框的中心点（pivot）将保持与边缘相同的相对距离。对于左侧框，在原始的640x1136窗口中，它距离左边缘17%：

![](images/gui/adjustmode_example_original_ratio.png)

当屏幕调整大小时，左侧框的中心点保持与左边缘相同的17%距离：

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

如果我们将左侧框的pivot从Center更改为West，右侧框更改为East，并重新定位框，即使屏幕调整大小，我们也能得到我们想要的结果：

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

通过将一个节点拖放到您希望成为其父节点的节点上，使该节点成为另一个节点的子节点。具有父节点的节点继承应用于父节点的变换（位置、旋转和缩放），并相对于父节点pivot。

![Parent child](images/gui/parent_child.png)

父节点在其子节点之前绘制。使用层来更改父节点和子节点的绘制顺序并优化节点的渲染（见下文）。


## 层和绘制调用

层提供了对节点绘制方式的精细控制，可用于减少引擎绘制GUI场景必须创建的绘制调用次数。当引擎即将绘制GUI场景的节点时，它根据以下条件将节点分组到绘制调用批次中：

- 节点必须使用相同的类型。
- 节点必须使用相同的图集或瓷砖图源。
- 节点必须使用相同的混合模式渲染。
- 它们必须使用相同的字体。

如果其中任何一个条件不满足，就会破坏合批并产生另一个绘制调用。蒙版和被蒙版节点必然会破坏合批并产生绘制调用。

树形结构对于节点管理非常方便。但是混合不同类型的节点一定会破坏合批渲染：

![Breaking batch hierarchy](images/gui/break_batch.png)

渲染管线被迫为不同类型的节点建立不同的渲染批次。这三个按钮就会产生6次绘制调用。

如果使用层，可以重塑节点的绘制顺序，渲染管线就能更好地进行合批并减少绘制调用。第一步是创建新层。在*大纲*的"Layers"文件夹上<kbd>右键点击</kbd>，然后选择<kbd>Add ▸ Layer</kbd>。在*Properties*视图中填写*Name*属性为层命名。

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
