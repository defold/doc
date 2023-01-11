---
title: Defold 鼠标和触摸输入教程
brief: 本教程介绍了鼠标和触摸输入的功能.
---

::: sidenote
建议首先熟练掌握 Defold 中常规输入的消息处理方式, 例如输入消息获取以及脚本间输入消息广播顺序等. 关于输入系统详情请见 [输入系统教程](/manuals/input).
:::

# Mouse Triggers
鼠标触发器可以绑定鼠标按键和滚轮输入到游戏功能的映射.

![](images/input/mouse_bindings.png)

::: sidenote
鼠标按键输入 `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` 和 `MOUSE_BUTTON_MIDDLE` 等同于 `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` 和 `MOUSE_BUTTON_3`.
:::

::: sidenote
下面的例子中使用了上图的映射绑定配置. 映射与命名可以根据项目需要自由设置.
:::

## 鼠标键
鼠标键可以生成按下, 抬起和连按消息. 获取鼠标键消息的方法如下 (按下和抬起):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- 鼠标左键按下
        elseif action.released then
            -- 鼠标左键抬起
        end
    end
end
```

::: sidenote
单点触摸也会触发 `MOUSE_BUTTON_LEFT` (或 `MOUSE_BUTTON_1`) 事件.
:::

## 鼠标滚轮
鼠标滚轮可以生成滚动消息. 如果 `action.value` 为 `1` 代表转动, 为 `0` 代表不转动. (滚轮转动被当作一种按钮消息来处理. Defold 目前不支持触摸板上的滚轮输入.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- 鼠标滚轮向上滚动
        end
    end
end
```

## 鼠标移动
鼠标移动消息有点特别. 如果输入绑定表里没有鼠标的话, 鼠标移动事件也会被丢弃.

但是不用特地为了鼠标移动配置绑定, 因为鼠标移动时会自动生成事件, 其中 `action_id` 为 `nil` 并且 `action` 表保存了鼠标位置与移动距离.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- 游戏对象跟随鼠标/触摸
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# 触摸触发器
iOS 和 Android 设备上运行的原生应用与HTML5应用都支持单点和多点触摸输入.

![](images/input/touch_bindings.png)

## Single-touch
单点触摸不用在触摸映射部分进行设置. 而在 **鼠标映射设置了 `MOUSE_BUTTON_LEFT` 或称 `MOUSE_BUTTON_1`** 之后自行配置.

## Multi-touch
多点触摸在输入映射表里叫做 `touch`. 其元素索引为数字 `1`--`N`, 这里 `N` 是触摸点的编号. 其元素值为触摸点数据:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- 在触摸点的位置生成游戏对象
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: sidenote
多点触摸动作名不能与 `MOUSE_BUTTON_LEFT` 或 `MOUSE_BUTTON_1` 的动作名重名. 否则的话将导致事件覆盖, 就监听不到单点触摸事件了.
:::

::: sidenote
公共资源 [Defold 输入手柄](https://defold.com/assets/defoldinput/) 可以用来在多点触摸屏上模拟手柄输入.
:::


## 拾取检测
游戏里经常可见拾取操作. 可能是玩家点击界面按钮或者战略游戏里玩家选取一个作战单位, RPG 游戏点取宝箱等等. 不同组件有不同解决方法.

### 界面点击检测
界面有一个 `gui.pick_node(node, x, y)` 函数来判断点击输入是否处在某个节点范围之内. 详见 [API 文档](/ref/gui/#gui.pick_node:node-x-y), [指针悬停示例](https://www.defold.com/examples/pointer_over/) 或者 [按钮示例](https://www.defold.com/examples/button/).

### 游戏对象点击检测
游戏对象检测有点复杂, 因为摄像机移动和渲染脚本映射都会影响位置计算. 方法主要分为两种:

  1. 追踪游戏对象的位置和大小然后检测点选位置是否包含在内.
  2. 给游戏对象加入碰撞组件再在点选位置生成一个碰撞对象检查二者碰撞情况.

::: sidenote
公共资源 [Defold 输入库](https://github.com/britzl/defold-input) 是一个开箱即用的输入检测库.
:::

无论哪种方案都必须将鼠标手点选的屏幕坐标转换成游戏对象的世界坐标. 实现思路如下:

  * 手动跟踪渲染脚本使用的视口和投射用以进行坐标转换. 详见 [摄像机教程的这个示例](/manuals/camera/#鼠标位置转换为世界坐标).
  * 使用 [第三方摄像机解决方案](/manuals/camera/#第三方摄像机解决方案) 里面的屏幕到世界坐标转换函数.
