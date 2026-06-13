---
title: Ejemplo de animación de menú principal
brief: En este proyecto de ejemplo, aprenderás efectos para presentar un menú principal.
---
# Animación de menú principal - proyecto de ejemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

En este proyecto de ejemplo, que puedes [abrir desde el editor](/manuals/project-setup/) o [descargar desde GitHub](https://github.com/defold/sample-main-menu-animation), demostramos efectos para presentar un menú principal. El menú contiene un fondo y dos elementos de menú.
Este proyecto ya está configurado con un menu.gui y un menu.gui_script aplicado con el código que se muestra más abajo. Los assets de imagen se agregan a un atlas llamado images.atlas y se aplican a nodos en menu.gui.

Cada uno, el fondo y los dos elementos de menú, tiene las mismas animaciones aplicadas, pero con distintos retrasos. Esto se configura en `init()` más abajo.

Las primeras animaciones hacen que cada nodo aparezca gradualmente mientras se escala de 70% a 110%.
Esto se hace en `anim1()`.

Durante las siguientes animaciones, la escala se anima hacia adelante y hacia atrás de 110% a 98%, a 106% y luego a 100%. Esto da el efecto de rebote y se hace en `anim2()`, `anim3()` y `anim4()`.

El fondo tiene un pequeño desvanecimiento especial al final, que se aplica en `anim5()`.

```lua
-- file: menu.gui_script

-- las funciones animX representan la línea de tiempo de animación
-- primero se ejecuta anim1; al terminar, se ejecuta anim2, etc.
-- anim1 a anim4 crean un efecto de goma con rebote.
-- anim5 reduce el alfa y solo se usa para el fondo

local function anim5(self, node)
	if gui.get_node("background") == node then
		-- caso especial para el fondo. anima el alfa a 60%
		local to_color = gui.get_color(node)
		to_color.w = 0.6
		gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUTCUBIC, 2.4, 0.1)
	end
end

local function anim4(self, node)
	-- anima la escala a 100%
	local s = 1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim5)
end

local function anim3(self, node)
	-- anima la escala a 106%
	local s = 1.06
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim4)
end

local function anim2(self, node)
	-- anima la escala a 98%
	local s = 0.98
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim3)
end

local function anim1(node, d)
	-- define la escala en 70%
	local start_scale = 0.7
	gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

	-- obtiene el color actual y define el alfa en 0 para aparecer gradualmente
	local from_color = gui.get_color(node)
	local to_color = gui.get_color(node)
	from_color.w = 0
	gui.set_color(node, from_color)

	-- anima el valor alfa de 0 a 1
	gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_INOUTCUBIC, 0.4, d)

	-- anima la escala de %70 a 110%
	local s = 1.1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.4, d, anim2)
end

function init(self)
	-- inicia animaciones para todos los nodos
	-- el fondo, las cajas de botones y el texto se animan por igual
	-- d es el retraso de inicio de la animación
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
