---
title: HUD代码示例
brief: 在本示例项目中，您将学习分数计数的效果。
---
# HUD - 示例项目

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

在本示例项目中，您可以[从编辑器打开](/manuals/project-setup/)或[从GitHub下载](https://github.com/defold/sample-hud)，我们演示了分数计数的效果。分数随机出现在屏幕上，模拟玩家在不同位置获得分数的游戏。

分数出现后会浮动一段时间。为了实现这一点，我们将分数设置为透明，然后淡入它们的颜色。我们还使它们向上动画。这是在下面的`on_message()`中完成的。

然后它们向上移动到屏幕顶部的总分数处，在那里它们被相加。
在向上移动的同时，它们也稍微淡出。这是在`float_done()`中完成的。

当它们到达顶部分数时，它们的数量被添加到一个目标分数中，总分数向这个目标分数计数。这是在`swoosh_done()`中完成的。

当脚本更新时，它会检查目标分数是否已经增加，总分数是否需要计数。当这是真的时，总分数以较小的步长递增。
然后总分数的比例被动画化，以产生弹跳效果。这是在`update()`中完成的。

每次总分数递增时，我们生成一些较小的星星，并使它们从总分数处动画出来。星星在`spawn_stars()`、`fade_out_star()`和`delete_star()`中被生成、动画和删除。

```lua
-- 文件: hud.gui_script
-- 分数每秒计数的速度
local score_inc_speed = 1000

function init(self)
    -- 目标分数是游戏中的当前分数
    self.target_score = 0
    -- 当前分数，正朝着目标分数计数
    self.current_score = 0
    -- 在hud中显示的分数
    self.displayed_score = 0
    -- 保存显示分数的节点引用，以备后用
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- 星星已完成动画，删除它
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- 在删除之前淡出星星
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- 分数节点的位置，用于放置星星
    local p = gui.get_position(self.score_node)
    -- 星星生成位置的距离
    local start_distance = 0
    -- 星星停止的距离
    local end_distance = 240
    -- 星星圆圈中每个星星之间的角度距离
    local angle_step = 2 * math.pi / amount
    -- 随机化起始角度
    local angle = angle_step * math.random()
    for i=1,amount do
        -- 通过步长增加角度，以获得均匀分布的星星
        angle = angle + angle_step
        -- 星星移动的方向
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- 星星的起始/结束位置
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- 创建星星节点
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- 设置其纹理
        gui.set_texture(star, "star")
        -- 设置为透明
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- 淡入
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- 动画位置
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- 检查分数是否需要更新
    if self.current_score < self.target_score then
        -- 为这个时间步长增加分数，以朝着目标分数增长
        self.current_score = self.current_score + score_inc_speed * dt
        -- 限制分数，使其不会超过目标分数
        self.current_score = math.min(self.current_score, self.target_score)
        -- 向下取整分数，使其可以不带小数显示
        local floored_score = math.floor(self.current_score)
        -- 检查显示的分数是否应该更新
        if self.displayed_score ~= floored_score then
            -- 更新显示的分数
            self.displayed_score = floored_score
            -- 更新分数节点的文本
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- 将分数节点的比例设置为比正常稍大
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- 然后将比例动画回原始值
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- 生成星星
            spawn_stars(self, 4)
        end
    end
end

-- 这个函数存储添加的分数，以便显示的分数可以在更新函数中计数
local function swoosh_done(self, node)
    -- 从节点检索分数
    local amount = tonumber(gui.get_text(node))
    -- 增加目标分数，请参阅更新函数中分数如何更新以匹配目标分数
    self.target_score = self.target_score + amount
    -- 删除临时分数
    gui.delete_node(node)
end

-- 这个函数使节点从首先浮动到飞向显示的总分数
local function float_done(self, node)
    local duration = 0.2
    -- 飞向显示的分数
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- 在飞行的同时也部分淡出
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- 注册添加的分数，此消息可以由任何想要增加分数的人发送
    if message_id == hash("add_score") then
        -- 创建一个新的临时分数节点
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- 为它使用小字体
        gui.set_font(node, "small_score")
        -- 初始透明
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- 淡入
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- 浮动
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

在main.script中，我们接收触摸/鼠标输入，然后发送消息到gui脚本，使用触摸位置创建新的分数。

```lua
-- 点击/触摸时获取触摸位置，并通过消息将其发送到hud gui脚本以及得分点数量。

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- 使用输入action.x和action.y作为触摸的x和y位置
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```