---
title: Defold 场景编辑器
brief: 场景编辑器用于编辑集合、游戏对象、GUI、粒子效果和其他可视资源。本手册说明选择、工具，以及如何在 2D 和 3D 中导航场景视图，包括自由摄像机模式和摄像机设置。
---

# Defold 场景编辑器

**Scene Editor** 是用于构建和编辑场景的可视化编辑器，例如集合、游戏对象和其他可视资源。

默认情况下，许多可视场景会以 **2D 正交**视图打开。进行 3D 工作时，您可以切换到面向 3D 的布局，启用 3D 网格平面，并使用**透视**摄像机。

## 打开场景编辑器

在 *Assets* 面板中双击可视资源即可打开 Scene Editor，例如：

- **场景结构** — 集合（`.collection`）、游戏对象（`.go`）
- **2D 资源** — 图集（`.atlas`）、瓦片地图（`.tilemap`）、精灵（`.sprite`）、瓦片源（`.tilesource`）
- **3D 资源** — 模型（`.model`、`.glb`、`.gltf`）
- **UI** — GUI 场景（`.gui`）
- **效果** — 粒子效果（`.particlefx`）
- 以及其他资源

## 场景视图导航（摄像机控制）

Scene Editor 摄像机可以通过鼠标和键盘控制。可用控制取决于您使用的是标准摄像机导航还是 **Free Camera Mode**。

### 标准导航（所有可视编辑器）

这些控制在可视编辑器中可用：

- **平移**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **缩放**
  - <kbd>Mouse Wheel</kbd>，或
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **围绕选择旋转/环绕（3D）**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

您也可以使用 **Frame Selection**（<kbd>F</kbd>）将摄像机聚焦到当前选择。

## 2D 和 3D 场景方向 {#2d-and-3d-scene-orientation}

场景视图可用于 2D 和 3D 工作流：

- 在 **2D** 中，通常使用带有 2D 网格的正交视图。
- 在 **3D** 中，通常会：
  - 将视图重新对齐到 3D 方向，
  - 使用**透视**摄像机，
  - 选择合适的网格平面（通常用 **Y** 表示“地面”）。

您可以通过工具栏和 **View** 菜单访问这些功能。

![Scene Editor 3D](images/editor/3d_scene.png)

## 工具栏概览

场景视图右上角有一个工具栏，包含常用工具和视图选项（从左到右）：

- **移动工具**（<kbd>W</kbd>）
- **旋转工具**（<kbd>E</kbd>）
- **缩放工具**（<kbd>R</kbd>）
- **网格设置**（`▦`）
- **对齐/重新对齐 2D/3D 摄像机**（`2D`）— 在 2D 和 3D 方向之间切换（快捷键 <kbd>.</kbd>）
- **摄像机透视/正交**
- **可见性过滤器**（`👁`）

![Toolbar](images/editor/toolbar.png)

## 选择和操作对象 {#manipulating-objects}

### 选择对象

在主窗口中的对象上 <kbd>Left Mouse Click</kbd> 可选择它们。编辑器视图中围绕对象的矩形（或长方体）会以青色高亮，表示当前选择的项目。所选对象也会像上图一样在 `Outline` 视图中高亮。

  您也可以通过以下方式选择对象：

- <kbd>Left Mouse Click</kbd> 并 <kbd>Drag</kbd>，选择选择区域内的所有对象。
- 在 `Outline` 中 <kbd>Left Mouse Click</kbd> 对象，按住 <kbd>⇧ Shift</kbd> 可以扩展选择，按住 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> 可以选择或取消选择点击的对象。

#### 移动工具

![Move tool](images/editor/icon_move.png){.left}

要移动对象，请使用 *Move Tool*。您可以在场景编辑器右上角的工具栏中找到它，也可以按 <kbd>W</kbd> 键。

![Move object](images/editor/move.png){.inline}![Move object 3D](images/editor/move_3d.png){.inline}

gizmo 会变化并显示一组操纵器 - 方块和箭头（选中的操纵器会变为橙色），您可以 <kbd>Drag</kbd> 来移动：

- 一个位于中心的青色方块手柄，仅在屏幕空间中移动对象，
- 3 个沿各轴的红、绿、蓝箭头，仅沿给定的 X、Y 或 Z 轴移动对象。
- 3 个红、绿、蓝方块手柄（透明填充轮廓），仅在给定平面上移动对象，例如 X-Y（蓝色），以及（在 3D 中旋转摄像机时可见的）X-Z（绿色）和 Y-Z（红色）平面。

#### 旋转工具

![Rotate tool](images/editor/icon_rotate.png){.left}

要旋转对象，请在工具栏中选择 *Rotate Tool*，或按 <kbd>E</kbd> 键。

![Rotate object](images/editor/rotate.png){.inline}![Rotate object 3D](images/editor/rotate_3d.png){.inline}

此工具由四个圆形操纵器组成（选中的操纵器会变为橙色），您可以 <kbd>Drag</kbd> 来旋转：

- 一个青色（外侧、最大的圆）操纵器，用于在屏幕空间中旋转对象
- 3 个较小的红、绿、蓝圆形操纵器，分别允许围绕 X、Y 和 Z 轴旋转。对于 2D 正交视图，其中两个与 X 轴和 Y 轴垂直，因此圆只会显示为穿过对象的两条线。

#### 缩放工具

![Scale tool](images/editor/icon_scale.png){.left}

要缩放对象，请在工具栏中选择 *Scale Tool*，或按 <kbd>R</kbd> 键。

![Scale object](images/editor/scale.png){.inline}![Scale object 3D](images/editor/scale_3d.png){.inline}

此工具由一组方形/立方体操纵器组成（选中的操纵器会变为橙色），您可以 <kbd>Drag</kbd> 来缩放：

- 中心的一个青色立方体会在所有轴上等比缩放对象（包括 Z）。
- 3 个红、蓝、绿立方体操纵器分别沿 X、Y 和 Z 轴缩放对象。
- 3 个红、绿、蓝方形操纵器（透明填充轮廓）分别在 X-Y、X-Z 或 Y-Z 平面上缩放对象。

### 可见性过滤器 {#visibility-filters}

单击工具栏中的**可见性眼睛图标**（`👁`），可以切换各种组件类型以及边界框和辅助线（`Component Guides`，快捷键 <kbd>Ctrl</kbd> + <kbd>H</kbd>（Win/Linux）或 <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>（Mac））的可见性。

![Visibility filters](images/editor/visibilityfilters.png)

## 网格设置 {#grid-settings}

可以自定义网格以适配您的工作流（在 3D 中尤其有用）。单击 **Grid Settings** 按钮（`▦`）打开网格设置弹窗。

![Grid Settings](images/editor/grid_popup.png)

设置包括：

- **网格大小（X/Y/Z）**
  设置每个轴上网格线之间的间距。小数值适合精确放置小对象，大数值适合获得更宽的概览。
- **活动平面（X/Y/Z）**
  选择绘制网格的平面。在 2D 工作流中，这通常是 **Z**（默认 X-Y 平面）。在 3D 工作流中，**Y** 通常用于表示地面/地板平面。
- **网格颜色**
  设置网格线颜色。用于在不同场景背景下获得更好的对比。
- **网格不透明度**
  控制网格线的透明程度。较低的值会让网格不那么干扰视图，同时仍提供参考。
- 一个 **Reset to Defaults** 按钮
  将所有网格设置恢复为原始值。

## 摄像机类型：透视与正交

Scene Editor 支持两种摄像机：

- **正交**摄像机（常用于 2D 工作流）
- **透视**摄像机（常用于 3D 工作流）

使用工具栏中的摄像机切换按钮进行切换。在 3D 场景中，透视导航通常更自然。

## 自由摄像机模式 {#free-camera-mode}

为了快速进行 3D 导航，Scene Editor 提供 **Free Camera Mode**，即第一人称 / “FPS 风格”的摄像机。

### 激活自由摄像机模式

- 按住 <kbd>Right Mouse Button</kbd> — 只要按住按钮，Free Camera Mode 就保持激活
- <kbd>Shift</kbd> + <kbd>`</kbd>（反引号）— 切换开启 Free Camera Mode，松开后仍保持激活

::: sidenote
在某些键盘布局（例如瑞典语）上，反引号键是死键，可能无法按预期触发快捷键。您
可以在 `File ▸ Preferences ▸ Keys` 中重新绑定此快捷键，并为 `Scene -> Free Camera -> Activate` 输入新的快捷键
:::

当 Free Camera Mode 激活时，Scene View 边缘会显示一圈高亮线。

### 退出自由摄像机模式

- 松开 <kbd>Right Mouse Button</kbd>（通过按住激活时），或
- <kbd>Left Mouse Button</kbd>、<kbd>Right Mouse Button</kbd>（按下并松开），或在 Free Camera Mode 通过切换激活时按 <kbd>Esc</kbd>。

### 环顾四周（鼠标视角）

Free Camera Mode 激活时，这些按键会控制摄像机移动（而不是编辑器工具）：

- 移动鼠标控制 **yaw**（左/右）和 **pitch**（上/下）
- Pitch 会被限制，以避免摄像机翻转

您也可以选择反转 Y 轴（见下方 **Free camera settings**）。

### 移动

Free Camera Mode 激活时：

- <kbd>W</kbd> — 前进
- <kbd>S</kbd> — 后退
- <kbd>A</kbd> — 左移
- <kbd>D</kbd> — 右移
- <kbd>E</kbd> — 上移
- <kbd>Q</kbd> — 下移

::: sidenote
所有移动按键都可以在 `File ▸ Preferences ▸ Keys` 中重新绑定。然后搜索 `Scene -> Free Camera`
:::

速度修饰键：

- 按住 <kbd>Shift</kbd> — 更快移动
- 按住 <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> — 更慢/更精确地移动

### 行走模式（可选）

Free Camera Mode 支持 **Walking Mode**。

启用后：
- 上/下移动会被约束，使其更像在地面平面上的第一人称行走。
- 当您探索关卡并希望保持一致的“贴地”移动时，这很有用。

## 摄像机设置弹窗

工具栏中的透视摄像机按钮带有一个摄像机相关偏好的设置弹窗。

![Perspective Camera Settings](images/editor/camera_popup.png)

弹窗包含：

- **移动速度**
  调整自由摄像机移动速度。

- **视角灵敏度**
  调整摄像机响应鼠标移动旋转的速度。

- **反转 Y**
  反转垂直鼠标视角。

- **行走模式**
  约束移动，以便进行类似地面的导航。

- **Reset to Defaults**
  恢复默认摄像机设置。
