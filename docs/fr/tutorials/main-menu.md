---
title: Exemple d'animation de menu principal
brief: Ce projet d'exemple vous apprend à utiliser des effets pour présenter un menu principal.
---
# Animation du menu principal - projet d'exemple {#main-menu-animation-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

Dans ce projet d'exemple, que vous pouvez [ouvrir depuis l'éditeur](/manuals/project-setup/) ou [télécharger depuis GitHub](https://github.com/defold/sample-main-menu-animation), nous vous présentons des effets permettant d'afficher un menu principal. Le menu contient un arrière-plan et deux éléments de menu.
Ce projet est déjà configuré avec menu.gui et menu.gui_script et le code présenté ci-dessous. Les ressources d'image sont ajoutées à un atlas nommé images.atlas et sont appliquées à des nœuds dans menu.gui.

Les mêmes animations sont appliquées à l'arrière-plan et aux deux éléments de menu, mais avec des délais différents. Cela est configuré dans `init()` ci-dessous.

La première animation fait apparaître chaque nœud en fondu tout en faisant passer son échelle de 70 % à 110 %.
C'est ce que fait `anim1()`.

Lors des animations suivantes, l'échelle varie successivement de 110 % à 98 %, puis à 106 % et enfin à 100 %. Cela produit un effet de rebond, réalisé dans `anim2()`, `anim3()` et `anim4()`.

Un léger effet de fondu sortant est appliqué spécifiquement à l'arrière-plan à la fin, dans `anim5()`.

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
