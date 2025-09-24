---
title: 视差代码示例
brief: 在本示例中，您将学习如何使用视差效果来模拟游戏世界中的深度。
---
# 视差 - 示例项目

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>

在本示例项目中，您可以[从编辑器打开](/manuals/project-setup/)或[从GitHub下载](https://github.com/defold/sample-parallax)，我们展示了如何使用视差效果来模拟游戏世界中的深度。
有两层云，其中一层看起来比另一层更远。还有一个动画飞碟作为点缀。

云层被构建为两个独立的游戏对象，每个都包含一个*瓦片地图*和*脚本*。
这些层以不同的速度移动，以产生视差效果。这是在下面的*background1.script*和*background2.script*的`update()`中完成的。

```lua
-- file: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- 背景是游戏对象中的瓦片地图
-- 我们移动游戏对象以产生视差效果

function update(self, dt)
    -- 每帧将x位置减少1个单位以产生视差效果
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- file: background2.script

-- 背景是游戏对象中的瓦片地图
-- 我们移动游戏对象以产生视差效果

function update(self, dt)
    -- 每帧将x位置减少0.5个单位以产生视差效果
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

飞碟是一个独立的游戏对象，包含一个*精灵*和一个*脚本*。
它以恒定速度向左移动。上下运动是通过使用Lua正弦函数（`math.sin()`）围绕固定值动画化其y分量获得的。这是在*spaceship.script*的`update()`中完成的。


```lua
-- file: spaceship.script

function init(self)
    -- 记住初始y位置，这样我们
    -- 可以在不更改脚本的情况下移动飞船
    self.start_y = go.get_position().y
    -- 将计数器设置为零。用于下面的正弦运动
    self.counter = 0
end

function update(self, dt)
    -- 每帧将x位置减少2个单位
    local p = go.get_position()
    p.x = p.x - 2

    -- 围绕初始y位置移动y位置
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- 更新位置
    go.set_position(p)

    -- 当飞船离开屏幕时移除它
    if p.x < - 32 then
        go.delete()
    end

    -- 增加计数器
    self.counter = self.counter + 1
end
```