---
title: 关卡完成代码示例
brief: 在本示例项目中，您学习显示关卡完成时可能出现的分数计数效果。
---
# 关卡完成 - 示例项目

<iframe width="560" height="315" src="https://www.youtube.com/embed/tSdTSvku1o8" frameborder="0" allowfullscreen></iframe>

在本示例项目中，您可以[从编辑器打开](/manuals/project-setup/)或[从GitHub下载](https://github.com/defold/sample-levelcomplete)，我们演示了显示关卡完成时可能出现的分数计数效果。总分数会逐渐累加，当达到不同分数等级时会出现三颗星星。该示例还使用了重新加载功能，以便在调整值时快速周转。

场景由游戏中的消息触发。
该消息包含获得的总分数以及三颗星星应该在哪个分数等级出现。
当这种情况发生时，标题文本（"关卡完成！"）会淡入，同时缩小到常规大小（100%）。这是在下面的`on_message()`中完成的。

标题文本动画完成后，总分数开始计数。每次发生这种情况时，当前分数都会增加一小步。然后我们检查是否已经跨越了某个星星等级，如果是，则开始星星的动画（见下文）。只要我们还没有达到目标分数，总分数就会以弹跳效果进行动画。
随着接近总分数，它也会增长到最大比例。同样，它的颜色会逐渐从白色变为绿色。这是在`inc_score()`中完成的。

每次星星出现时，它都会淡入并缩小到常规大小。这是在`animate_star()`中完成的。

当星星完成动画后，较小的星星会在大星星周围以圆形生成。这是在`spawn_small_stars()`中完成的。

然后它们被动画化为从星星中随机射出。它们在向外扩展时，速度和比例都是随机的。然后它们淡出并最终被删除。这是在`animate_small_star()`和`delete_small_star()`中完成的。

当分数达到总分数时，高分印记会淡入并缩小回原位。这是在`inc_score()`的末尾启动的，并在`animate_imprint()`中执行。

`setup()`函数确保节点具有正确的初始值。通过从`on_reload()`调用`setup()`，我们确保每次从Defold Editor重新加载脚本时都正确设置了所有内容。

```lua
-- 文件: level_complete.gui_script

-- 分数每秒递增的速度
local score_inc_speed = 51100
-- 每次更新分数之间的时间间隔
local dt = 0.03
-- 计数开始时分数的比例
local score_start_scale = 0.7
-- 达到目标分数时分数的比例
local score_end_scale = 1.0
-- 每次递增时分数"弹跳"的程度
local score_bounce_factor = 1.1
-- 每颗大星星生成的小星星数量
local small_star_count = 16

local function setup(self)
    -- 使标题颜色透明
    local c = gui.get_color(self.heading)
    c.w = 0
    gui.set_color(self.heading, c)
    -- 使标题阴影透明
    c = gui.get_shadow(self.heading)
    c.w = 0
    gui.set_shadow(self.heading, c)
    -- 初始设置标题为两倍比例
    local s = 2
    gui.set_scale(self.heading, vmath.vector3(s, s, s))
    -- 设置初始分数（0）
    gui.set_text(self.score, "0")
    -- 设置分数颜色为不透明白色
    gui.set_color(self.score, vmath.vector4(1, 1, 1, 1))
    -- 设置比例以便分数在计数时可以增长
    gui.set_scale(self.score, vmath.vector4(score_start_scale, score_start_scale, 1, 0))

    -- 使所有大星星透明
    for i=1,#self.stars do
        gui.set_color(self.stars[i], vmath.vector4(1, 1, 1, 0))
    end
    -- 使印记透明
    gui.set_color(self.imprint, vmath.vector4(1, 1, 1, 0))
    -- 当前显示的分数
    self.current_score = 0
    -- 计数时的目标分数
    self.target_score = 0
end

function init(self)
    -- 检索节点以便更容易访问
    self.heading = gui.get_node("heading")
    self.stars = {gui.get_node("star_left"), gui.get_node("star_mid"), gui.get_node("star_right")}
    self.score = gui.get_node("score")
    self.imprint = gui.get_node("imprint")
    -- 分数的起始颜色
    self.score_start_color = vmath.vector4(1, 1, 1, 1)
    -- 保存分数颜色并在稍后计数时向其动画
    self.score_end_color = gui.get_color(self.score)
    setup(self)
end

-- 删除小星星，当星星完成动画时调用
local function delete_small_star(self, small_star)
    gui.delete_node(small_star)
end

-- 根据给定的初始位置和角度为小星星设置动画
local function animate_small_star(self, pos, angle)
    -- 小星星的移动方向
    local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0, 0)
    -- 创建小星星
    local small_star = gui.new_box_node(pos + dir * 20, vmath.vector3(64, 64, 0))
    -- 设置其纹理
    gui.set_texture(small_star, "small_star")
    -- 设置其颜色为全白
    gui.set_color(small_star, vmath.vector4(1, 1, 1, 1))
    -- 设置起始比例为低
    local start_s = 0.3
    gui.set_scale(small_star, vmath.vector3(start_s, start_s, 1))
    -- 每个小星星的比例变化
    local end_s_var = 1
    -- 这颗星星的实际结束比例
    local end_s = 0.5 + math.random() * end_s_var
    gui.animate(small_star, gui.PROP_SCALE, vmath.vector4(end_s, end_s, 1, 0), gui.EASING_NONE, 0.5)
    -- 行进距离的变化（本质上是星星的速度）
    local dist_var = 300
    -- 星星将行进的实际距离
    local dist = 400 + math.random() * dist_var
    gui.animate(small_star, gui.PROP_POSITION, pos + dir * dist, gui.EASING_NONE, 0.5)
    gui.animate(small_star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_OUT, 0.3, 0.2, delete_small_star)
end

-- 生成多个小星星
local function spawn_small_stars(self, star)
    -- 小星星将围绕生成的大星星的位置
    local p = gui.get_position(star)
    for i = 1,small_star_count do
        -- 计算特定小星星的角度
        local angle = 2 * math.pi * i/small_star_count
        -- 以及位置
        local pos = vmath.vector3(p.x, p.y, 0)
        -- 生成并为小星星设置动画
        animate_small_star(self, pos, angle)
    end
end

-- 开始大星星淡入的动画
local function animate_star(self, star)
    -- 淡入持续时间
    local fade_in = 0.2
    -- 使其透明
    gui.set_color(star, vmath.vector4(1, 1, 1, 0))
    -- 淡入
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in)
    -- 初始比例
    local scale = 5
    gui.set_scale(star, vmath.vector3(scale, scale, 1))
    -- 缩小回原位
    gui.animate(star, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, 0, spawn_small_stars)
end

-- 开始印记淡入的动画
local function animate_imprint(self)
    -- 等待一段时间后印记出现
    local delay = 0.8
    -- 淡入持续时间
    local fade_in = 0.2
    -- 初始比例
    local scale = 4
    gui.set_scale(self.imprint, vmath.vector4(scale, scale, 1, 0))
    -- 缩小回原位
    gui.animate(self.imprint, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, delay)
    -- 同时淡入
    gui.animate(self.imprint, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in, delay)
end

-- 将分数向目标递增一步
local function inc_score(self, node)
    -- 这一步骤分数递增的量
    local score_inc = score_inc_speed * dt
    -- 递增后的新分数
    local new_score = self.current_score + score_inc
    for i = 1,#self.stars do
        -- 如果我们跨越了星星出现的分数等级，则开始为大星星设置动画
        if self.current_score < self.star_levels[i] and new_score >= self.star_levels[i] then
            animate_star(self, self.stars[i])
        end
    end
    -- 更新分数，但限制在目标分数
    self.current_score = math.min(new_score, self.target_score)
    -- 更新屏幕上的分数
    gui.set_text(self.score, tostring(self.current_score))
    -- 如果我们尚未完成，继续动画和递增
    if self.current_score < self.target_score then
        -- 我们离目标有多近
        local f = self.current_score / self.target_score
        -- 混合颜色以获得缓慢的淡入效果
        local c = vmath.lerp(f, self.score_start_color, self.score_end_color)
        gui.animate(self.score, gui.PROP_COLOR, c, gui.EASING_NONE, dt, 0, inc_score)
        -- 这一步的新比例
        local s = vmath.lerp(f, score_start_scale, score_end_scale)
        -- 通过弹跳因子增加比例
        local sp = s * score_bounce_factor
        -- 从弹跳比例动画回适当比例
        gui.set_scale(self.score, vmath.vector4(sp, sp, 1, 0))
        gui.animate(self.score, gui.PROP_SCALE, vmath.vector4(s, s, 1, 0), gui.EASING_NONE, dt)
    else
        -- 我们完成了，淡入印记
        -- 注意！在实际情况下，这应该与实际存储的高分进行检查
        animate_imprint(self)
    end
end

function on_message(self, message_id, message, sender)
    -- 有人告诉我们应该显示关卡完成场景
    if message_id == hash("level_completed") then
        -- 检索获得的分数以及星星应该在哪个分数等级显示
        self.target_score = message.score
        self.star_levels = message.star_levels
        -- 淡入标题（"关卡完成"）
        local c = gui.get_color(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_COLOR, c, gui.EASING_IN, dt, 0.0, inc_score)
        c = gui.get_shadow(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_SHADOW, c, gui.EASING_IN, dt, 0.0)
        -- 将其缩小回原位
        gui.animate(self.heading, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, 0.2, 0.0)
    end
end

-- 当脚本重新加载时调用此函数
-- 通过设置场景并模拟关卡完成，我们获得了一个非常快速的工作流程来进行调整
function on_reload(self)
    -- 确保任何设置更改都被考虑在内
    setup(self)
    -- 模拟关卡已完成
    msg.post("#gui", "level_completed", {score = 102000, star_levels = {40000, 70000, 100000}})
end
```