---
title: Przykład animacji menu głównego
brief: W tym przykładowym projekcie poznasz efekty służące do prezentacji menu głównego.
---
# Animacja menu głównego - projekt przykładowy

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

W tym przykładowym projekcie, który możesz [otworzyć w edytorze](/manuals/project-setup/) albo [pobrać z GitHub](https://github.com/defold/sample-main-menu-animation), pokazujemy efekty służące do prezentacji menu głównego. Menu zawiera tło i dwie pozycje menu.
Projekt jest gotowy: ma menu.gui oraz menu.gui_script, do których zastosowano kod pokazany poniżej. Zasoby graficzne zostały dodane do atlasu images.atlas i przypisane do węzłów w menu.gui.

Do tła i obu pozycji menu zastosowano te same animacje, ale z różnymi opóźnieniami. Jest to skonfigurowane poniżej w `init()`.

Pierwsza animacja polega na tym, że każdy węzeł płynnie się pojawia, a jednocześnie jego skala zmienia się z 70% do 110%.
Jest to realizowane w `anim1()`.

W kolejnych animacjach skala zmienia się tam i z powrotem z 110% do 98%, potem do 106%, a następnie do 100%. Daje to efekt odbicia i jest realizowane w `anim2()`, `anim3()` oraz `anim4()`.

Na końcu tło ma dodatkowo delikatny efekt zanikania, który jest realizowany w `anim5()`.

```lua
-- plik: menu.gui_script

-- funkcje animX reprezentują oś czasu animacji
-- najpierw wykonywana jest anim1, po jej zakończeniu anim2 itd.
-- anim1 do anim4 tworzą sprężysty efekt odbicia.
-- anim5 zmniejsza wartość alpha i jest używana tylko dla tła.

local function anim5(self, node)
	if gui.get_node("background") == node then
		-- szczególny przypadek dla tła: animuj alpha do 60%
		local to_color = gui.get_color(node)
		to_color.w = 0.6
		gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUTCUBIC, 2.4, 0.1)
	end
end

local function anim4(self, node)
	-- animuj skalę do 100%
	local s = 1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim5)
end

local function anim3(self, node)
	-- animuj skalę do 106%
	local s = 1.06
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim4)
end

local function anim2(self, node)
	-- animuj skalę do 98%
	local s = 0.98
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim3)
end

local function anim1(node, d)
	-- ustaw skalę na 70%
	local start_scale = 0.7
	gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

	-- pobierz bieżący kolor i ustaw alpha na 0, aby węzeł płynnie się pojawił
	local from_color = gui.get_color(node)
	local to_color = gui.get_color(node)
	from_color.w = 0
	gui.set_color(node, from_color)

	-- animuj wartość alpha od 0 do 1
	gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_INOUTCUBIC, 0.4, d)

	-- animuj skalę od 70% do 110%
	local s = 1.1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.4, d, anim2)
end

function init(self)
	-- uruchom animacje dla wszystkich węzłów
	-- tło, obszary przycisków i tekst są animowane w ten sam sposób
	-- d to opóźnienie startu animacji
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
