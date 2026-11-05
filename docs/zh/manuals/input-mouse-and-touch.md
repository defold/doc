---
title: Defold鼠标和触摸输入
brief: 本手册解释了鼠标和触摸输入的工作原理。
---

::: sidenote
建议您熟悉Defold中输入的一般工作方式，如何接收输入以及在脚本文件中接收输入的顺序。有关输入系统的更多信息，请参阅[输入系统概述手册](/manuals/input)。
:::

# 鼠标触发器 {#mouse-triggers}
鼠标触发器允许您将鼠标按钮和滚轮输入绑定到游戏操作。

![](images/input/mouse_bindings.png)

::: sidenote
鼠标按键输入 `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` 和 `MOUSE_BUTTON_MIDDLE` 等同于 `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` 和 `MOUSE_BUTTON_3`.
:::

::: important
下面的示例使用了上图中显示的操作。与所有输入一样，您可以自由命名输入操作。
:::

## 鼠标按钮 {#mouse-buttons}
鼠标按钮会生成`pressed`、`released`和`repeated`事件。以下示例显示如何检测鼠标左键的输入（按下或释放）：

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- 鼠标左键按下
        elseif action.released then
            -- 鼠标左键释放
        end
    end
end
```

::: important
`MOUSE_BUTTON_LEFT`（或`MOUSE_BUTTON_1`）输入操作也会为单点触摸输入发送。
:::

### 区分鼠标点击与触摸 {#distinguishing-mouse-clicks-from-touch}

`action.source` 可以区分物理鼠标按下与触摸模拟的点击，包括首次按下。将 `MOUSE_BUTTON_LEFT` 绑定到 `mouse_button_left`，并在脚本或 GUI 脚本中使用以下代码：

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") and action.pressed then
        if action.source == hash("mouse") then
            print("Mouse pressed at:", action.x, action.y)
        elseif action.source == hash("touch") then
            print("Touch pressed at:", action.x, action.y)
        end
    end
end
```

即使没有单独的 Touch Trigger，模拟为鼠标点击的触摸也会报告 `hash("touch")`。识别点击不需要 `action.touch` 表或之前的移动事件。全部来源值，以及多个绑定共用动作名称时的来源规则，请参阅[输入设备来源](/manuals/input/#input-device-source)。

在 iOS 上，自定义 `Info.plist` 必须启用 `UIApplicationSupportsIndirectInputEvents`，才能进行这种区分。内置清单已启用此项。

## 鼠标滚轮 {#mouse-wheel}
鼠标滚轮输入检测滚动操作。如果滚轮滚动，`action.value`字段为`1`，否则为`0`。（滚动操作被视为按钮按下处理。Defold目前不支持触摸板上的精细滚动输入。）

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- 鼠标滚轮向上滚动
        end
    end
end
```

## 鼠标移动 {#mouse-movement}
鼠标移动是单独处理的。除非在输入绑定中设置了至少一个鼠标触发器，否则不会接收到鼠标移动事件。

指针移动不绑定到动作名称：`action_id` 为 `nil`，`action` 表包含指针位置和移动增量。物理鼠标的来源为 `hash("mouse")`，由触摸模拟的移动来源为 `hash("touch")`。加速度计采样也使用 `action_id == nil`，因此请检查来源进行区分，具体见[输入设备来源](/manuals/input/#input-device-source)。

```lua
function on_input(self, action_id, action)
    if action_id == nil and
        (action.source == hash("mouse") or action.source == hash("touch")) then
        -- 让游戏对象跟随鼠标/触摸移动
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# 触摸触发器 {#touch-triggers}
单点和多点触摸类型触发器在iOS和Android设备上的原生应用程序和HTML5包中可用。

![](images/input/touch_bindings.png)

## 单点触摸 {#single-touch}
单点触摸类型触发器不是从输入绑定的触摸触发器部分设置的。相反，**当您为`MOUSE_BUTTON_LEFT`或`MOUSE_BUTTON_1`设置了鼠标按钮输入时，单点触摸触发器会自动设置**。

## 多点触摸 {#multi-touch}
多点触摸类型触发器在操作表中填充一个名为`touch`的表。表中的元素是用数字`1`--`N`进行整数索引的，其中`N`是触摸点的数量。表的每个元素包含输入数据的字段：

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- 在每个触摸点生成
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
多点触摸不能分配与`MOUSE_BUTTON_LEFT`或`MOUSE_BUTTON_1`的鼠标按钮输入相同的操作。分配相同的操作将有效地覆盖单点触摸，并阻止您接收任何单点触摸事件。
:::

::: sidenote
[Defold-Input资源](https://defold.com/assets/defoldinput/)可用于轻松设置虚拟屏幕控件，如按钮和支持多点触摸的模拟摇杆。
:::


## 检测对象上的点击或触摸 {#detecting-click-or-tap-on-objects}
检测用户何时点击或触摸视觉组件是许多游戏中需要的非常常见的操作。可能是用户与按钮或其他UI元素的交互，或者与游戏对象的交互，如策略游戏中的玩家控制单位、地牢爬行游戏中关卡上的宝藏或RPG中的任务给予者。使用的方法取决于视觉组件的类型。

### 检测与GUI节点的交互 {#detecting-interaction-with-gui-nodes}
对于UI元素，有一个`gui.pick_node(node, x, y)`函数，它将根据指定坐标是否在GUI节点的边界内返回`true`或`false`。请参阅[API文档](/ref/gui/#gui.pick_node:node-x-y)、[指针悬停示例](/examples/gui/pointer_over/)或[按钮示例](/examples/gui/button/)了解更多信息。

### 检测与游戏对象的交互 {#detecting-interaction-with-game-objects}
对于游戏对象，检测交互更加复杂，因为诸如摄像机平移和渲染脚本投影等因素将影响所需的计算。检测与游戏对象的交互有两种通用方法：

  1. 跟踪用户可以与之交互的游戏对象的位置和大小，并检查鼠标或触摸坐标是否在任何对象的边界内。
  2. 将碰撞对象附加到用户可以与之交互的游戏对象上，并附加一个跟随鼠标或手指的碰撞对象，并检查它们之间的碰撞。

::: sidenote
可以在[Defold-Input资源](https://defold.com/assets/defoldinput/)中找到使用碰撞对象检测用户输入的现成解决方案，支持拖动和点击。
:::

在这两种情况下，都需要从鼠标或触摸事件的屏幕空间坐标和游戏对象的世界空间坐标进行转换。这可以通过几种不同的方式完成：

  * 手动跟踪渲染脚本使用的视图和投影，并使用它在世界空间之间进行转换。有关此示例，请参阅[摄像机手册](/manuals/camera/#converting-mouse-to-world-coordinates)。
  * 使用[第三方摄像机解决方案](/manuals/camera/#third-party-camera-solutions)并利用提供的屏幕到世界转换函数。
