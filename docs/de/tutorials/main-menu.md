---
title: Beispiel für die Animation eines Hauptmenüs
brief: In diesem Beispielprojekt lernst du Effekte kennen, mit denen du ein Hauptmenü präsentieren kannst.
---
# Animation eines Hauptmenüs - Beispielprojekt {#main-menu-animation-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

In diesem Beispielprojekt, das du [im Editor öffnen](/manuals/project-setup/) oder [von GitHub herunterladen](https://github.com/defold/sample-main-menu-animation) kannst, zeigen wir Effekte zur Präsentation eines Hauptmenüs. Das Menü enthält einen Hintergrund und zwei Menüeinträge.
Das Projekt ist bereits mit den Dateien menu.gui und menu.gui_script sowie dem unten gezeigten Code eingerichtet. Die Bild-Assets sind einem Atlas namens images.atlas hinzugefügt und den Knoten (nodes) in menu.gui zugewiesen.

Auf den Hintergrund und die beiden Menüeinträge werden jeweils dieselben Animationen angewendet, allerdings mit unterschiedlichen Verzögerungen. Dies wird unten in `init()` eingerichtet.

Bei der ersten Animation wird jeder Knoten allmählich eingeblendet und dabei von 70 % auf 110 % skaliert.
Dies geschieht in `anim1()`.

Während der folgenden Animationen wechselt die Skalierung von 110 % auf 98 %, dann auf 106 % und schließlich auf 100 %. Dadurch entsteht der Federeffekt, der in `anim2()`, `anim3()` und `anim4()` umgesetzt wird.

Der Hintergrund wird zum Schluss zusätzlich leicht ausgeblendet. Dies geschieht in `anim5()`.

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
