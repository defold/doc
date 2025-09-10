---
title: Defold中的GUI布局
brief: Defold支持GUI自动适应移动设备上的屏幕方向变化。本文档解释了此功能的工作原理。
---

# 布局

Defold支持GUI自动适应移动设备上的屏幕方向变化。通过使用此功能，您可以设计适应各种屏幕尺寸的方向和纵横比的GUI。还可以创建与特定设备型号匹配的布局。

## 创建显示配置文件

默认情况下，*game.project*设置指定使用内置的显示配置文件设置文件（"builtins/render/default.display_profiles"）。默认配置文件是"Landscape"（1280像素宽和720像素高）和"Portrait"（720像素宽和1280像素高）。配置文件上没有设置设备型号，因此它们将匹配任何设备。

要创建新的配置文件设置文件，可以复制"builtins"文件夹中的文件，或者在*Assets*视图中<kbd>右键点击</kbd>合适位置并选择<kbd>New... ▸ Display Profiles</kbd>。给新文件一个合适的名称，然后点击<kbd>Ok</kbd>。

编辑器现在会打开新文件进行编辑。通过点击*Profiles*列表中的<kbd>+</kbd>添加新的配置文件。对于每个配置文件，添加一组*限定符*：

Width
: 限定符的像素宽度。

Height
: 限定符的像素高度。

Device Models
: 以逗号分隔的设备型号列表。设备型号匹配设备型号名称的开头，例如`iPhone10`将匹配"iPhone10,*"型号。带有逗号的型号名称应该用引号括起来，即`"iPhone10,3", "iPhone10,6"`匹配iPhone X型号（参见[iPhone wiki](https://www.theiphonewiki.com/wiki/Models)）。请注意，调用`sys.get_sys_info()`时报告设备型号的唯一平台是Android和iOS。其他平台返回空字符串，因此永远不会选择具有设备型号限定符的显示配置文件。

![New display profiles](images/gui-layouts/new_profiles.png)

您还需要指定引擎应该使用您的新配置文件。打开*game.project*并在*display*下的*Display Profiles*设置中选择显示配置文件：

![Settings](images/gui-layouts/settings.png)

如果您希望引擎在设备旋转时自动在横屏和竖屏布局之间切换，请勾选*Dynamic Orientation*框。引擎将动态选择匹配的布局，并在设备改变方向时也更改选择。

## GUI布局

当前的显示配置文件集可用于创建GUI节点设置的布局变体。要向GUI场景添加新布局，请在*Outline*视图中右键点击*Layouts*图标并选择<kbd>Add ▸ Layout ▸ ...</kbd>：

![Add layout to scene](images/gui-layouts/add_layout.png)

编辑GUI场景时，所有节点都在特定布局上进行编辑。当前选定的布局在工具栏的GUI场景布局下拉框中指示。如果未选择布局，则在*Default*布局中编辑节点。

![Layouts toolbar](images/gui-layouts/toolbar.png)

![portrait edit](images/gui-layouts/portrait.png)

对节点属性所做的每个更改（在选择布局时）会_覆盖_*Default*布局中的属性。被覆盖的属性以蓝色标记。具有被覆盖属性的节点也以蓝色标记。您可以点击任何被覆盖属性旁边的重置按钮将其重置为原始值。

![landscape edit](images/gui-layouts/landscape.png)

布局不能删除或创建新节点，只能覆盖属性。如果需要从布局中移除节点，可以将其移出屏幕或使用脚本逻辑删除它。您还应注意当前选定的布局。如果向项目添加布局，新布局将根据当前选定的布局进行设置。此外，复制和粘贴节点时考虑当前选定的布局，在复制*和*粘贴时都是如此。

## 动态配置文件选择

动态布局匹配根据以下规则对每个显示配置文件限定符进行评分：

1. 如果没有设置设备型号，或者设备型号匹配，则为限定符计算分数（S）。

2. 分数（S）使用显示面积（A）、限定符的面积（A_Q）、显示的纵横比（R）和限定符的纵横比（R_Q）计算：

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. 如果限定符的方向（横屏或竖屏）与显示匹配，则选择得分最低的限定符的配置文件。

4. 如果找不到具有相同方向限定符的配置文件，则选择具有另一方向最佳得分限定符的配置文件。

5. 如果无法选择配置文件，则使用*Default*回退配置文件。

由于*Default*布局在运行时用作回退，如果没有更好的匹配布局，这意味着如果您添加"Landscape"布局，它将是*所有*方向的最佳匹配，直到您也添加"Portrait"布局。

## 布局更改消息

当引擎因设备旋转而切换布局时，会向受更改影响的GUI组件脚本发送`layout_changed`消息。消息包含布局的哈希ID，以便脚本可以根据选择的布局执行逻辑：

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- 转换为横屏布局
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- 转换为竖屏布局
  end
end
```

此外，每当窗口（游戏视图）更改时，当前渲染脚本都会收到消息，这包括方向更改。

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- 窗体尺寸变化. message.width 与 message.height 对应
    -- 改变后窗口的宽和高.
  end
end
```

当方向切换时，GUI布局管理器将根据您的布局和节点属性自动缩放和重新定位GUI节点。然而，游戏内容在单独的通道中渲染（默认情况下），使用拉伸适配投影到当前窗口。要更改此行为，要么提供自己修改的渲染脚本，要么使用相机[库](/assets/)。
