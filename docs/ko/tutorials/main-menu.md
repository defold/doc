---
title: 메인 메뉴 애니메이션 샘플
brief: 이 샘플 프로젝트에서는 메인 메뉴를 표현하는 효과를 배웁니다.
---
# 메인 메뉴 애니메이션 - 샘플 프로젝트

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

[에디터에서 열거나](/manuals/project-setup/) [GitHub에서 다운로드할 수 있는](https://github.com/defold/sample-main-menu-animation) 이 샘플 프로젝트에서는 메인 메뉴를 표현하는 효과를 보여줍니다. 메뉴에는 배경과 두 개의 메뉴 항목이 들어 있습니다.
이 프로젝트는 아래에 표시된 코드가 적용된 menu.gui와 menu.gui_script로 이미 설정되어 있습니다. 이미지 에셋은 images.atlas라는 아틀라스에 추가되어 있으며 menu.gui의 노드에 적용되어 있습니다.

배경과 두 개의 메뉴 항목에는 모두 같은 애니메이션이 적용되지만, 각기 다른 지연 시간이 사용됩니다. 이 설정은 아래의 `init()`에서 이루어집니다.

첫 번째 애니메이션은 각 노드가 70%에서 110%로 스케일되는 동안 페이드 인되게 합니다.
이는 `anim1()`에서 처리됩니다.

이어지는 애니메이션에서는 스케일이 110%에서 98%, 106%, 다시 100%로 앞뒤로 애니메이션됩니다. 이렇게 튀어 오르는 효과가 만들어지며, `anim2()`, `anim3()`, `anim4()`에서 처리됩니다.

배경에는 마지막에 살짝 페이드 아웃되는 특수 효과가 있으며, 이는 `anim5()`에서 적용됩니다.

```lua
-- 파일: menu.gui_script

-- animX 함수는 애니메이션 타임라인을 나타냅니다
-- 먼저 anim1이 실행되고, 완료되면 anim2가 실행되는 식입니다
-- anim1부터 anim4까지는 통통 튀는 고무 같은 효과를 만듭니다.
-- anim5는 알파를 낮추며 배경에만 사용됩니다

local function anim5(self, node)
	if gui.get_node("background") == node then
		-- 배경을 위한 특수 케이스입니다. 알파를 60%로 애니메이션합니다
		local to_color = gui.get_color(node)
		to_color.w = 0.6
		gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUTCUBIC, 2.4, 0.1)
	end
end

local function anim4(self, node)
	-- 스케일을 100%로 애니메이션합니다
	local s = 1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim5)
end

local function anim3(self, node)
	-- 스케일을 106%로 애니메이션합니다
	local s = 1.06
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim4)
end

local function anim2(self, node)
	-- 스케일을 98%로 애니메이션합니다
	local s = 0.98
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim3)
end

local function anim1(node, d)
	-- 스케일을 70%로 설정합니다
	local start_scale = 0.7
	gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

	-- 현재 색상을 가져오고 페이드 인을 위해 알파를 0으로 설정합니다
	local from_color = gui.get_color(node)
	local to_color = gui.get_color(node)
	from_color.w = 0
	gui.set_color(node, from_color)

	-- 알파 값을 0에서 1로 애니메이션합니다
	gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_INOUTCUBIC, 0.4, d)

	-- 스케일을 70%에서 110%로 애니메이션합니다
	local s = 1.1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.4, d, anim2)
end

function init(self)
	-- 모든 노드의 애니메이션을 시작합니다
	-- 배경, 버튼 박스, 텍스트는 같은 방식으로 애니메이션됩니다
	-- d는 애니메이션 시작 지연 시간입니다
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
