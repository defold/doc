---
title: Defold 游戏手柄输入教程
brief: 本教程介绍了游戏手柄输入的功能.
---

::: 注意
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

::: 注意
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

## Connect and Disconnect
游戏手柄还有 `Connected` 和 `Disconnected` 两种事件用以通知手柄连接和断开.

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

## 手柄配置文件
在 Windows 上, 只支持 XBox 360 兼容手柄. 安装方法请见 http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows

每种手柄分别对应一份映射文件, 可以在 *gamepads* 配置文件中设置. Defold 自带一个通用的手柄映射配置文件:

![Gamepad settings](images/input/gamepads.png){srcset="images/input/gamepads@2x.png 2x"}

如需自定义文件, 可以配合使用这个工具:

[Click to download gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

这个工具包含 Windows, Linux 和 macOS 的可运行文件. 命令行启动方法:

```sh
./gdc
```

这个工具通过收集连接控制器的输入自动生成映射文件. 新的映射文件可以在 "game.project" 里进行指定或者混合使用:

![Gamepad settings](images/input/gamepad_setting.png){srcset="images/input/gamepad_setting@2x.png 2x"}
