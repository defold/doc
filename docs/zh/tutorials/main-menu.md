---
title: 主菜单动画示例
brief: 在本示例项目中，您将学习如何呈现主菜单的效果。
---
# 主菜单动画 - 示例项目

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

在本示例项目中，您可以[从编辑器打开](/manuals/project-setup/)或[从GitHub下载](https://github.com/defold/sample-main-menu-animation)，我们展示了如何呈现主菜单的效果。菜单包含一个背景和两个菜单项。
这个项目已经设置好了menu.gui和menu.gui_script，应用了下面显示的代码。图像资源已添加到名为images.atlas的图集中，并应用到menu.gui中的节点上。

背景和两个菜单项中的每一个都应用了相同的动画，但有不同的延迟。这在下面的`init()`中设置。

第一个动画是让每个节点在从70%缩放到110%的同时淡入。
这是在`anim1()`中完成的。

在接下来的动画中，缩放从110%到98%，再到106%，然后到100%来回动画。这产生了弹跳效果，在`anim2()`、`anim3()`和`anim4()`中完成。

背景在最后有一个特殊的轻微淡出效果，这在`anim5()`中应用。

```lua
-- file: menu.gui_script

-- 函数animX代表动画时间线
-- 首先执行anim1，完成后执行anim2，依此类推
-- anim1到anim4创建弹跳橡胶效果。
-- anim5降低alpha值，仅用于背景

local function anim5(self, node)
	if gui.get_node("background") == node then
		-- 背景的特殊情况。将alpha动画到60%
		local to_color = gui.get_color(node)
		to_color.w = 0.6
		gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUTCUBIC, 2.4, 0.1)
	end
end

local function anim4(self, node)
	-- 将缩放动画到100%
	local s = 1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim5)
end

local function anim3(self, node)
	-- 将缩放动画到106%
	local s = 1.06
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim4)
end

local function anim2(self, node)
	-- 将缩放动画到98%
	local s = 0.98
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim3)
end

local function anim1(node, d)
	-- 将缩放设置为70%
	local start_scale = 0.7
	gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

	-- 获取当前颜色并将alpha设置为0以淡入
	local from_color = gui.get_color(node)
	local to_color = gui.get_color(node)
	from_color.w = 0
	gui.set_color(node, from_color)

	-- 将alpha值从0动画到1
	gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_INOUTCUBIC, 0.4, d)

	-- 将缩放从70%动画到110%
	local s = 1.1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.4, d, anim2)
end

function init(self)
	-- 为所有节点启动动画
	-- 背景、按钮框和文本都同样动画
	-- d是动画开始延迟
	local d = 0.4
	anim1(gui.get_node("new_game"), d)
	anim1(gui.get_node("new_game_shadow"), d)
	anim1(gui.get_node("new_game_button"), d)

	d = 0.3
	anim1(gui.get_node("quit"), d)
	anim1(gui.get_node("quit_shadow"), d)
	anim1(gui.get_node("quit_button"), d)

	d = 0.1
	anim1(gui.get_node("background"), d)
end
```