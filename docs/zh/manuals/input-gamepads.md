---
title: 游戏手柄输入在Defold中
brief: 本手册解释了游戏手柄输入的工作原理。
---

::: sidenote
建议您先熟悉Defold中输入的一般工作方式，如何接收输入以及输入在脚本文件中的接收顺序。有关输入系统的更多信息，请参阅[输入系统概述手册](/manuals/input)。
:::

# Gamepads
游戏手柄触发器允许您将标准游戏手柄输入绑定到游戏功能。游戏手柄输入提供以下绑定：

- 左右摇杆（方向和点击）
- 左右数字板。右数字板通常对应Xbox控制器上的"A"、"B"、"X"和"Y"按钮，以及PlayStation控制器上的"方块"、"圆圈"、"三角"和"十字"按钮。
- 左右扳机键
- 左右肩键
- 开始、返回和指南按钮

![](images/input/gamepad_bindings.png)

::: important
下面的示例使用了上图中显示的操作。与所有输入一样，您可以自由命名输入操作。
:::

## 数字按钮
数字按钮生成按下、释放和重复事件。以下示例显示如何检测数字按钮的输入（按下或释放）：

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- 向左移动
        elseif action.released then
            -- 停止移动
        end
    end
end
```

## 模拟摇杆
当摇杆移动到手柄设置文件中定义的死区之外时，模拟摇杆会生成连续的输入事件（见下文）。以下示例显示如何检测模拟摇杆的输入：

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- 左摇杆向下拨动
        print(action.value) -- 取值范围 0.0 到 -1.0
    end
end
```

模拟摇杆在移动到超过特定阈值的主要方向时也会生成按下和释放事件。这使得将模拟摇杆也用作数字方向输入变得容易：

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- 左摇杆向下拨动到头
    end
end
```

## 多个游戏手柄
Defold通过主机操作系统支持多个游戏手柄，操作会将操作表的`gamepad`字段设置为输入来源的游戏手柄编号：

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- 手柄0号玩家申请加入游戏
        end
    end
end
```

## 连接和断开
游戏手柄输入绑定还提供两个名为`Connected`和`Disconnected`的独立绑定，用于检测游戏手柄何时连接（包括从一开始就连接的手柄）或断开。

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- 手柄0号已连接
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- 手柄0号已断开
        end
    end
end
```

## 原始游戏手柄
(自Defold 1.2.183起)

游戏手柄输入绑定还提供一个名为`Raw`的独立绑定，用于提供任何连接的游戏手柄的未过滤（未应用死区）的按钮、轴和方向键输入。

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## 游戏手柄设置文件
游戏手柄输入设置为每种硬件游戏手柄类型使用单独的映射文件。特定硬件游戏手柄的游戏手柄映射在*gamepads*文件中设置。Defold附带了一个内置的游戏手柄文件，其中包含常见游戏手柄的设置：

![Gamepad settings](images/input/gamepads.png)

如果您需要创建新的游戏手柄设置文件，我们有一个简单的工具可以帮助您：

[Click to download gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

这个工具包含 Windows, Linux 和 macOS 的可运行文件. 命令行启动方法:

```sh
./gdc
```

该工具将要求您按下连接控制器上的不同按钮。然后，它将输出一个新的游戏手柄文件，其中包含您控制器的正确映射。保存新文件，或将其与现有的游戏手柄文件合并，然后在*game.project*中更新设置：

![Gamepad settings](images/input/gamepad_setting.png)

### 未识别的游戏手柄
(自Defold 1.2.186起)

当游戏手柄连接且没有该游戏手柄的映射时，游戏手柄将只生成"connected"、"disconnected"和"raw"操作。在这种情况下，您需要在游戏中手动将原始游戏手柄数据映射到操作。

(自Defold 1.4.8起)

可以通过从操作中读取`gamepad_unknown`值来检查游戏手柄的输入操作是否来自未知游戏手柄：

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
``` 

## HTML5中的游戏手柄
HTML5构建中支持游戏手柄，并生成与其他平台相同的输入事件。游戏手柄的支持基于[游戏手柄API](https://www.w3.org/TR/gamepad/)，大多数浏览器都支持此API（[参考此支持图表](https://caniuse.com/?search=gamepad)）。如果浏览器不支持游戏手柄API，Defold将静默忽略项目中的任何游戏手柄触发器。您可以通过检查`navigator`对象上是否存在`getGamepads`函数来检查浏览器是否支持游戏手柄API：

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end
if supports_gamepads() then
    print("Platform supports gamepads")
end
```

如果您的游戏在`iframe`内运行，您还必须确保`iframe`已添加`gamepad`权限：

```html
<iframe allow="gamepad"></iframe>
```


### 标准游戏手柄
(自Defold 1.4.1起)

如果连接的游戏手柄被浏览器识别为标准游戏手柄，它将使用[游戏手柄设置文件](/manuals/input-gamepads/#gamepads-settings-file)中的"Standard Gamepad"映射（在`/builtins`中的`default.gamepads`文件中包含标准游戏手柄映射）。标准游戏手柄定义为具有16个按钮和2个模拟摇杆，按钮布局类似于PlayStation或Xbox控制器（有关更多信息，请参阅[W3C定义和按钮布局](https://w3c.github.io/gamepad/#dfn-standard-gamepad)）。如果连接的游戏手柄未被识别为标准游戏手柄，Defold将在游戏手柄设置文件中查找与硬件游戏手柄类型匹配的映射。

## Windows上的游戏手柄
在Windows上，目前只支持XBox 360控制器。要将360控制器连接到Windows机器，[请确保正确设置](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows)。
## Android上的游戏手柄
(自Defold 1.2.183起)

Android构建中支持游戏手柄，并生成与其他平台相同的输入事件。游戏手柄的支持基于[Android按键和运动事件输入系统](https://developer.android.com/training/game-controllers/controller-input)。Android输入事件将使用上述相同的*gamepad*文件转换为Defold游戏手柄事件。

在Android上添加额外的游戏手柄绑定时，您可以使用以下查找表将Android输入事件转换为*gamepad*文件值：

| 按键事件到按钮索引   | 索引 | 版本 |
|-----------------------------|-------|---------|
| AKEYCODE_BUTTON_A           | 0     | 1.2.183 |
| AKEYCODE_BUTTON_B           | 1     | 1.2.183 |
| AKEYCODE_BUTTON_C           | 2     | 1.2.183 |
| AKEYCODE_BUTTON_X           | 3     | 1.2.183 |
| AKEYCODE_BUTTON_L1          | 4     | 1.2.183 |
| AKEYCODE_BUTTON_R1          | 5     | 1.2.183 |
| AKEYCODE_BUTTON_Y           | 6     | 1.2.183 |
| AKEYCODE_BUTTON_Z           | 7     | 1.2.183 |
| AKEYCODE_BUTTON_L2          | 8     | 1.2.183 |
| AKEYCODE_BUTTON_R2          | 9     | 1.2.183 |
| AKEYCODE_DPAD_CENTER        | 10    | 1.2.183 |
| AKEYCODE_DPAD_DOWN          | 11    | 1.2.183 |
| AKEYCODE_DPAD_LEFT          | 12    | 1.2.183 |
| AKEYCODE_DPAD_RIGHT         | 13    | 1.2.183 |
| AKEYCODE_DPAD_UP            | 14    | 1.2.183 |
| AKEYCODE_BUTTON_START       | 15    | 1.2.183 |
| AKEYCODE_BUTTON_SELECT      | 16    | 1.2.183 |
| AKEYCODE_BUTTON_THUMBL      | 17    | 1.2.183 |
| AKEYCODE_BUTTON_THUMBR      | 18    | 1.2.183 |
| AKEYCODE_BUTTON_MODE        | 19    | 1.2.183 |
| AKEYCODE_BUTTON_1           | 20    | 1.2.186 |
| AKEYCODE_BUTTON_2           | 21    | 1.2.186 |
| AKEYCODE_BUTTON_3           | 22    | 1.2.186 |
| AKEYCODE_BUTTON_4           | 23    | 1.2.186 |
| AKEYCODE_BUTTON_5           | 24    | 1.2.186 |
| AKEYCODE_BUTTON_6           | 25    | 1.2.186 |
| AKEYCODE_BUTTON_7           | 26    | 1.2.186 |
| AKEYCODE_BUTTON_8           | 27    | 1.2.186 |
| AKEYCODE_BUTTON_9           | 28    | 1.2.186 |
| AKEYCODE_BUTTON_10          | 29    | 1.2.186 |
| AKEYCODE_BUTTON_11          | 30    | 1.2.186 |
| AKEYCODE_BUTTON_12          | 31    | 1.2.186 |
| AKEYCODE_BUTTON_13          | 32    | 1.2.186 |
| AKEYCODE_BUTTON_14          | 33    | 1.2.186 |
| AKEYCODE_BUTTON_15          | 34    | 1.2.186 |
| AKEYCODE_BUTTON_16          | 35    | 1.2.186 |

([Android `KeyEvent` 定义](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| 运动事件到轴索引  | 索引 |
|-----------------------------|-------|
| AMOTION_EVENT_AXIS_X        | 0     |
| AMOTION_EVENT_AXIS_Y        | 1     |
| AMOTION_EVENT_AXIS_Z        | 2     |
| AMOTION_EVENT_AXIS_RZ       | 3     |
| AMOTION_EVENT_AXIS_LTRIGGER | 4     |
| AMOTION_EVENT_AXIS_RTRIGGER | 5     |
| AMOTION_EVENT_AXIS_HAT_X    | 6     |
| AMOTION_EVENT_AXIS_HAT_Y    | 7     |

([Android `MotionEvent` 定义](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

将此查找表与Google Play商店中的游戏手柄测试应用程序结合使用，以确定您游戏手柄上的每个按钮映射到哪个按键事件。
