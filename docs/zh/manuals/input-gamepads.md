---
title: Defold 游戏手柄输入教程
brief: 本教程介绍了游戏手柄输入的功能.
---

::: sidenote
建议首先熟练掌握 Defold 中常规输入的消息处理方式, 例如输入消息获取以及脚本间输入消息广播顺序等. 关于输入系统详情请见 [输入系统教程](/manuals/input).
:::

# Gamepads
游戏手柄触发器可以绑定标准手柄输入到游戏功能的映射. 游戏手柄可以绑定:

- 左右摇杆 (方向和按下)
- 手柄按钮. 通常右手柄 Xbox 为 "A", "B", "X" 和 "Y", Playstation 为 "方块", "圆圈", "三角" 和 "十叉".
- 方向按钮.
- 左右肩按钮.
- 开始, 后退, 暂停按钮

![](images/input/gamepad_bindings.png)

::: important
下面的例子中使用了上图的映射绑定配置. 映射与命名可以根据项目需要自由设置.
:::

## 十字键
十字键可以生成按下, 抬起和连按消息. 获取十字键消息的方法如下 (按下和抬起):

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

## 摇杆
摇杆拨动到阈值以外就可以持续生成输入消息 (阈值配置见下文). 获取摇杆消息的方法如下:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- 左摇杆向下拨动
        print(action.value) -- 取值范围 0.0 到 -1.0
    end
end
```

摇杆处于某方向极值的时候还会生成按下和抬起消息. 这样类似十字键的消息很适合用作方向导航:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- 左摇杆向下拨动到头
    end
end
```

## 多手柄
Defold 基于其宿主操作系统支持多个手柄, 事件里 `gamepad` 项对应手柄输入来源:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- 手柄0号玩家申请加入游戏
        end
    end
end
```

## Connect 和 Disconnect
游戏手柄还有 `Connected` 和 `Disconnected` 两种事件用以通知手柄的连接(包括一开始就连着的手柄)和断开.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- 手柄0号已连接
        end
    elseif action_id == hash("gamepad_dicconnected") then
        if action.gamepad == 0 then
          -- 手柄0号已断开
        end
    end
end
```

## 手柄原始数据
(更新于 Defold 1.2.183)

手柄输入绑定提供了一个 `Raw` 事件给出按键, 十字键或者摇杆的原始 (不使用阈值) 数据.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## 手柄配置文件
每种手柄分别对应一份映射文件, 可以在 *gamepads* 配置文件中设置. Defold 自带一个通用的手柄映射配置文件:

![Gamepad settings](images/input/gamepads.png)

如需自定义文件, 可以配合使用这个工具:

[Click to download gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

这个工具包含 Windows, Linux 和 macOS 的可运行文件. 命令行启动方法:

```sh
./gdc
```

这个工具通过收集连接控制器的输入自动生成映射文件. 新的映射文件可以在 *game.project* 里进行指定或者混合使用:

![Gamepad settings](images/input/gamepad_setting.png)

### 未映射手柄
(更新于 Defold 1.2.186)

如果手柄没有配置消息映射的话, 就只有 "connected", "disconnected" 和 "raw" 三种事件. 这种情况下只能使用手柄原始数据来控制游戏.

(更新于 Defold 1.4.8)

可以通过查看 action 的 `gamepad_unknown` 值来确定输入行为是否来源于未知手柄:

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

## HTML5上的游戏手柄
HTML5平台同样支持游戏手柄, 效果和原生应用一样. 游戏手柄的支持基于 [标准游戏手柄API](https://www.w3.org/TR/gamepad/), 并且受绝大多数浏览器支持 ([详见此图表](https://caniuse.com/?search=gamepad)). 万一遇到不支持的浏览器 Defold 会忽略所有游戏手柄的操作. 可以通过检查浏览器的`navigator`对象中是否存在`getGamepads`函数来判断其是否支持游戏手柄:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end
if supports_gamepads() then
    print("Platform supports gamepads")
end
```

运行在 `iframe` 上的游戏要确保 `iframe` 的 `gamepad` 权限已被开启:

```html
<iframe allow="gamepad"></iframe>
```


### 标准手柄
(自 Defold 1.4.1 版本起)

如果连着的手柄被浏览器视为标准手柄, 则它会使用 [手柄配置文件](/manuals/input-gamepads/#gamepads-settings-file) (在 `/builtins` 目录下有一个标准手柄映射配置文件 `default.gamepads`) 里的 "Standard Gamepad" 映射. 所谓标准手柄是指包含个 16 按钮和 2 个摇杆的手柄, 布局类似 PlayStation 或者 Xbox 手柄 (更多详情请参考 [W3C 定义及按钮布局](https://w3c.github.io/gamepad/#dfn-standard-gamepad)). 如果连接着的手柄未被视为标准手柄 Defold 会根据硬件类型在手柄配置文件里寻找匹配的映射.

## Windows 上的手柄
在 Windows 上, 只支持 XBox 360 兼容手柄. To hook up your 360 controller to your Windows machine, [make sure it is setup correctly](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).
## 安卓手柄
(更新于 Defold 1.2.183)

Android 和其他平台一样支持手柄的输入事件. 手柄支持基于 [Android 按键和运动事件输入系统](https://developer.android.com/training/game-controllers/controller-input). 通过上文提到的 *gamepad* 文件把安卓输入事件转化成 Defold 手柄事件.

安卓手柄输入按键到 *gamepad* 文件手柄事件对应表如下:

| 按键输入 | 事件编号 | 引擎版本 |
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

| 摇杆输入  | 事件编号 |
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

为了正确使用手柄事件映射请参考上表以及 Google Play Store 上的手柄映射测试小工具.
