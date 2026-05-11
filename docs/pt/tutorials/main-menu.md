---
title: Exemplo de animação de menu principal
brief: Neste projeto de exemplo, você aprende efeitos para apresentar um menu principal.
---
# Animação de menu principal - projeto de exemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/dPQpSlt3ahw" frameborder="0" allowfullscreen></iframe>

Neste projeto de exemplo, que você pode [abrir pelo editor](/manuals/project-setup/) ou [baixar do GitHub](https://github.com/defold/sample-main-menu-animation), demonstramos efeitos para apresentar um menu principal. O menu contém um plano de fundo e dois itens de menu.
Este projeto já está configurado com um menu.gui e um menu.gui_script aplicados com o código mostrado abaixo. Assets de imagem são adicionados a um atlas chamado images.atlas e aplicados a nodes em menu.gui.

Cada um, o plano de fundo e os dois itens de menu, recebe as mesmas animações, mas com atrasos diferentes. Isso é configurado em `init()` abaixo.

A primeira animação faz cada node aparecer gradualmente enquanto sua escala vai de 70% para 110%.
Isso é feito em `anim1()`.

Durante as animações seguintes, a escala é animada para frente e para trás, de 110% para 98%, depois para 106% e então para 100%. Isso cria o efeito de quique e é feito em `anim2()`, `anim3()` e `anim4()`.

O plano de fundo tem um desaparecimento leve especial no final, aplicado em `anim5()`.

```lua
-- file: menu.gui_script

-- as funcoes animX representam a linha do tempo da animacao
-- primeiro anim1 e executada; ao terminar, anim2 e executada, e assim por diante
-- anim1 ate anim4 criam um efeito elastico com quique.
-- anim5 reduz o alfa e e usada apenas para o plano de fundo

local function anim5(self, node)
	if gui.get_node("background") == node then
		-- caso especial para o plano de fundo. anima alfa para 60%
		local to_color = gui.get_color(node)
		to_color.w = 0.6
		gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUTCUBIC, 2.4, 0.1)
	end
end

local function anim4(self, node)
	-- anima a escala para 100%
	local s = 1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim5)
end

local function anim3(self, node)
	-- anima a escala para 106%
	local s = 1.06
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim4)
end

local function anim2(self, node)
	-- anima a escala para 98%
	local s = 0.98
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.24, 0, anim3)
end

local function anim1(node, d)
	-- define a escala para 70%
	local start_scale = 0.7
	gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

	-- obtem a cor atual e define alfa como 0 para aparecer gradualmente
	local from_color = gui.get_color(node)
	local to_color = gui.get_color(node)
	from_color.w = 0
	gui.set_color(node, from_color)

	-- anima o valor de alfa de 0 para 1
	gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_INOUTCUBIC, 0.4, d)

	-- anima a escala de 70% para 110%
	local s = 1.1
	gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUTCUBIC, 0.4, d, anim2)
end

function init(self)
	-- inicia animacoes para todos os nodes
	-- plano de fundo, caixas de botao e texto sao animados igualmente
	-- d e o atraso inicial da animacao
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
