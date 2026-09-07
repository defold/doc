---
title: メインメニューのアニメーションのサンプル
brief: このサンプルプロジェクトでは、メインメニューを表示するための演出を学びます。
---
# メインメニューのアニメーション - サンプルプロジェクト {#main-menu-animation-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

[エディターから開く](/manuals/project-setup/)か、[GitHub からダウンロードする](https://github.com/defold/sample-main-menu-animation)ことができるこのサンプルプロジェクトでは、メインメニューを表示するための演出を紹介します。メニューは背景と2つのメニュー項目で構成されています。
このプロジェクトには、以下のコードを適用した menu.gui と menu.gui_script が設定済みです。画像アセットは images.atlas という名前のアトラス（atlas）に追加され、menu.gui のノード（node）に適用されています。

背景と2つのメニュー項目には、それぞれ同じアニメーションを適用していますが、開始までの遅延時間は異なります。これは以下の `init()` で設定しています。

最初のアニメーションでは、各ノードのスケールを70%から110%に変化させながらフェードインさせます。
これは `anim1()` で行います。

続くアニメーションでは、スケールを110%から98%、106%、そして100%へと、拡大と縮小を繰り返すように変化させます。これにより弾むような効果が得られます。この処理は `anim2()`、`anim3()`、`anim4()` で行います。

背景には、最後にわずかにフェードアウトする特別な処理があり、`anim5()` で適用します。

```lua
-- file: menu.gui_script

-- the functions animX represents the animation time-line
-- first is anim1 executed, when finished anim2 is executed, etc
-- anim1 to anim4 creates a bouncing rubber effect.
-- anim5 fades down alpha and is only used for the background

local function anim5(self, node)
	if gui.get_node("background") == node then
		-- special case for background. animate alpha to 60%
		local to_color = gui.get_color(node)
		to_color.w = 0.6
		gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUTCUBIC, 2.4, 0.1)
	end
end

local function anim4(self, node)
	-- animate scale to 100%
	local s = 1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim5)
end

local function anim3(self, node)
	-- animate scale to 106%
	local s = 1.06
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim4)
end

local function anim2(self, node)
	-- animate scale to 98%
	local s = 0.98
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim3)
end

local function anim1(node, d)
	-- set scale to 70%
	local start_scale = 0.7
	gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

	-- get current color and set alpha to 0 to fade up
	local from_color = gui.get_color(node)
	local to_color = gui.get_color(node)
	from_color.w = 0
	gui.set_color(node, from_color)

	-- animate alpha value from 0 to 1
	gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_INOUTCUBIC, 0.4, d)

	-- animate scale from %70 to 110%
	local s = 1.1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.4, d, anim2)
end

function init(self)
	-- start animations for all nodes
	-- background, button-boxes and text are animated equally
	-- d is the animation start delay
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
