---
title: Criando um carro simples no Defold.
brief: Se você está começando no Defold, este guia ajudará você a se orientar no editor. Ele também explica as ideias básicas e os blocos de construção mais comuns no Defold - objetos de jogo, coleções, scripts e sprites.
---

# Criando um carro

Se você está começando no Defold, este guia ajudará você a se orientar no editor. Ele também explica as ideias básicas e os blocos de construção mais comuns no Defold: objetos de jogo, coleções, scripts e sprites.

Vamos começar a partir de um projeto vazio e avançar passo a passo até uma aplicação muito pequena e jogável. Ao final, esperamos que você tenha uma noção de como o Defold funciona e esteja pronto para encarar um tutorial mais extenso ou mergulhar direto nos manuais.

::: sidenote
Ao longo do tutorial, descrições detalhadas sobre conceitos e sobre como fazer certas etapas são marcadas como este parágrafo. Se você achar que essas seções entram em detalhes demais, pode pulá-las.
:::

## Criando um novo projeto

![New Project](images/new_empty.png)

1. Inicie o Defold.
2. Selecione *New Project* à esquerda.
3. Selecione a aba *From Template*.
4. Selecione *Empty Project*
5. Selecione uma localização para o projeto no seu disco local.
6. Clique em *Create New Project*.

## O editor

Comece criando um [novo projeto](/manuals/project-setup/) e abrindo-o no editor. Se você der um duplo clique no arquivo *main/main.collection*, o arquivo será aberto:

![Editor overview](../manuals/images/editor/editor2_overview.png)

O editor consiste nas seguintes áreas principais:

Assets pane
: Esta é uma visualização de todos os arquivos do seu projeto. Tipos de arquivo diferentes têm ícones diferentes. Dê um duplo clique em um arquivo para abri-lo em um editor designado para aquele tipo de arquivo. A pasta especial somente leitura *builtins* é comum a todos os projetos e inclui itens úteis, como um script de renderização padrão, uma fonte, materiais para renderizar vários componentes e outras coisas.

Main Editor View
: Dependendo do tipo de arquivo que você está editando, esta visualização mostrará um editor para esse tipo. O mais usado é o editor Scene que você vê aqui. Cada arquivo aberto é mostrado em uma aba separada.

Changed Files
: Contém uma lista de todas as edições que você fez no seu branch desde a última sincronização. Então, se você vir algo neste painel, há alterações que ainda não estão no servidor. Você pode abrir um diff somente texto e reverter alterações por essa visualização.

Outline
: O conteúdo do arquivo atualmente editado em uma visualização hierárquica. Você pode adicionar, excluir, modificar e selecionar objetos e componentes por essa visualização.

Properties
: As propriedades definidas no objeto ou componente atualmente selecionado.

Console
: Ao executar o jogo, esta visualização captura saída (logs, erros, informações de debug etc.) vindo da engine do jogo, além de quaisquer mensagens de debug personalizadas de `print()` e `pprint()` nos seus scripts. Se o seu app ou jogo não iniciar, o console é o primeiro lugar a verificar. Atrás do console há um conjunto de abas exibindo informações de erro, além de um editor de curvas usado ao criar efeitos de partículas.

## Executando o jogo

O template de projeto "Empty" é, de fato, completamente vazio. Mesmo assim, selecione <kbd>Project ▸ Build</kbd> para compilar o projeto e iniciar o jogo.

![Build](images/car/start_build_and_launch.png)

Uma tela preta talvez não seja muito empolgante, mas é uma aplicação de jogo Defold em execução, e podemos modificá-la facilmente para algo mais interessante. Então vamos fazer isso.

::: sidenote
O editor Defold trabalha com arquivos. Ao dar duplo clique em um arquivo no *Assets pane*, você o abre em um editor adequado. Depois, pode trabalhar com o conteúdo do arquivo.

Quando terminar de editar um arquivo, você precisa salvá-lo. Selecione <kbd>File ▸ Save</kbd> no menu principal. O editor dá uma dica adicionando um asterisco '\*' ao nome do arquivo na aba de qualquer arquivo que contenha alterações não salvas.

![File with unsaved changes](images/car/file_changed.png)
:::

## Montando o carro

A primeira coisa que vamos fazer é criar uma nova coleção. Uma coleção é um contêiner de objetos de jogo que você posicionou e organizou. Coleções são usadas com mais frequência para criar níveis de jogo, mas são muito úteis sempre que você precisa reutilizar grupos e/ou hierarquias de objetos de jogo que pertencem juntos. Pode ser útil pensar em coleções como uma espécie de prefab.

Clique na pasta *main* no *Assets pane*, depois clique com o botão direito e selecione <kbd>New ▸ Collection File</kbd>. Você também pode selecionar <kbd>File ▸ New ▸ Collection File</kbd> no menu principal.

![New Collection file](images/car/start_new_collection.png)

Nomeie o novo arquivo de coleção como *car.collection* e abra-o. Vamos usar essa coleção nova e vazia para construir um pequeno carro a partir de alguns objetos de jogo. Um objeto de jogo é um contêiner de componentes (como sprites, sons, scripts de lógica etc.) que você usa para criar seu jogo. Cada objeto de jogo é identificado de forma única no jogo por seu id. Objetos de jogo podem se comunicar entre si por passagem de mensagens, mas veremos mais sobre isso depois.

Também é possível criar um objeto de jogo no local em uma coleção, como fizemos aqui. Isso resulta em um objeto único. Você pode copiar esse objeto, mas cada cópia é separada---alterar uma não afeta as outras. Isso significa que, se você criar 10 cópias de um objeto de jogo e perceber que quer alterar todas, precisará editar todas as 10 instâncias do objeto. Portanto, objetos de jogo criados no local devem ser usados para objetos dos quais você não pretende fazer muitas cópias.

Porém, um objeto de jogo armazenado em um _arquivo_ funciona como um protótipo (também conhecido como "prefabs" ou "blueprints" em outras engines). Quando você coloca instâncias de um objeto de jogo armazenado em arquivo em uma coleção, cada objeto é colocado _por referência_---ele é um clone baseado no protótipo. Se decidir que precisa alterar o protótipo, cada objeto de jogo colocado com base nesse protótipo é atualizado instantaneamente.

![Add car gameobject](images/car/start_add_car_gameobject.png)

Selecione o node raiz "Collection" na visualização *Outline*, clique com o botão direito e selecione <kbd>Add Game Object</kbd>. Um novo objeto de jogo com o id "go" aparecerá na coleção. Marque-o e defina seu id como "car" na visualização *Properties*. Até aqui, "car" não tem nada de interessante. Ele está vazio, sem representação visual e sem lógica. Para adicionar uma representação visual, precisamos adicionar um _componente_ de sprite.

Componentes são usados para estender objetos de jogo com presença (gráficos, som) e funcionalidade (fábricas de spawn, colisões, comportamentos com script). Um componente não pode existir sozinho; ele precisa residir dentro de um objeto de jogo. Componentes geralmente são definidos no local no mesmo arquivo do objeto de jogo. Porém, se quiser reutilizar um componente, você pode armazená-lo em um arquivo separado (como pode fazer com objetos de jogo) e incluí-lo como referência em qualquer arquivo de objeto de jogo. Alguns tipos de componente (scripts Lua, por exemplo) precisam ser colocados em um arquivo de componente separado e então incluídos como referência nos seus objetos.

Observe que você não manipula componentes diretamente---você pode mover, rotacionar, escalar e animar propriedades de objetos de jogo que, por sua vez, contêm componentes.

![Add car component](images/car/start_add_car_component.png)

Selecione o objeto de jogo "car", clique com o botão direito e selecione <kbd>Add Component</kbd>, depois selecione *Sprite* e clique em *Ok*. Se você marcar o sprite na visualização *Outline*, verá que ele precisa de algumas propriedades definidas:

Image
: Isso requer uma fonte de imagem para o sprite. Crie um arquivo de atlas de imagem marcando "main" na visualização *Assets pane*, clicando com o botão direito e selecionando <kbd>New ▸ Atlas File</kbd>. Nomeie o novo arquivo de atlas como *sprites.atlas* e dê um duplo clique nele para abri-lo no editor de atlas. Salve os dois arquivos de imagem a seguir no seu computador e arraste-os para *main* na visualização *Assets pane*. Agora você pode marcar o node raiz Atlas no editor de atlas, clicar com o botão direito e selecionar <kbd>Add Images</kbd>. Adicione a imagem do carro e a do pneu ao atlas e salve. Agora você pode selecionar *sprites.atlas* como a fonte de imagem para o componente de sprite no objeto de jogo "car" na coleção "car".

Imagens para o nosso jogo:

![Car image](images/car/start_car.png)
![Tire image](images/car/start_tire.png)

Adicione estas imagens ao atlas:

![Sprites atlas](images/car/start_sprites_atlas.png)

![Sprite properties](images/car/start_sprite_properties.png)

Default Animation
: Defina isso como "car" (ou o nome que você deu à imagem do carro). Cada sprite precisa de uma animação padrão que é reproduzida quando ele é mostrado no jogo. Quando você adiciona imagens a um atlas, o Defold cria convenientemente animações de um frame (estáticas) para cada arquivo de imagem.

## Completando o carro

Continue adicionando mais dois objetos de jogo à coleção. Chame-os de "left_wheel" e "right_wheel" e coloque um componente de sprite em cada um, mostrando a imagem do pneu que adicionamos a *sprites.atlas*. Depois, pegue os objetos de jogo das rodas e solte-os sobre "car" para torná-los filhos de "car". Objetos de jogo que são filhos de outros objetos de jogo ficarão anexados ao pai quando o pai se mover. Eles também podem ser movidos individualmente, mas todo movimento acontece em relação ao objeto pai. Para os pneus, isso é perfeito, já que queremos que fiquem presos ao carro e possamos apenas rotacioná-los levemente para a esquerda e para a direita ao dirigir o carro. Uma coleção pode conter qualquer número de objetos de jogo, lado a lado ou organizados em árvores pai-filho complexas, ou uma mistura disso.

Mova os objetos de jogo dos pneus para o lugar selecionando-os e escolhendo <kbd>Scene ▸ Move Tool</kbd>. Pegue as setas de manipulação, ou o quadrado verde central, para mover o objeto até um bom lugar. A última coisa que precisamos fazer é garantir que os pneus sejam desenhados abaixo do carro. Fazemos isso definindo o componente Z da posição como -0.5. Todo item visual em um jogo é desenhado de trás para frente, ordenado pelo valor Z. Um objeto com valor Z de 0 será desenhado por cima de um objeto com valor Z de -0.5. Como o valor Z padrão do objeto de jogo do carro é 0, o novo valor nos objetos dos pneus os colocará sob a imagem do carro.

![Car collection complete](images/car/start_car_collection_complete.png)

## O script do carro

A última peça do quebra-cabeça é um _script_ para controlar o carro. Um script é um componente que contém um programa que define comportamentos de objetos de jogo. Com scripts, você pode especificar as regras do jogo e como os objetos devem responder a várias interações (com o jogador e também com outros objetos). Todos os scripts são escritos na linguagem de programação Lua. Para conseguir trabalhar com o Defold, você ou alguém da sua equipe precisa aprender a programar em Lua.

Marque "main" no *Assets pane*, clique com o botão direito e selecione <kbd>New ▸ Script File</kbd>. Nomeie o novo arquivo como *car.script* e então adicione-o ao objeto de jogo "car" marcando "car" na visualização *Outline*, clicando com o botão direito e selecionando <kbd>Add Component File</kbd>. Selecione *car.script* e clique em *OK*. Salve o arquivo de coleção.

Dê um duplo clique em *car.script* para abri-lo.

::: sidenote
O Defold fornece várias funções de ciclo de vida para programar lógica de jogo. Leia mais sobre elas no [Manual de Script](/manuals/script).
:::

Comece removendo as funções `final`, `on_message` e `on_reload`, pois não precisaremos delas
neste tutorial.

Em seguida, adicione as seguintes linhas de código antes do início da função init.

```lua
-- Constantes
local turn_speed = 0.1                           									  -- Fator de Slerp
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 graus
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 graus
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero grau
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vetor do centro dos pares de rodas traseiras e dianteiras

local acceleration = 100 																						-- A aceleracao do carro

-- prehash das entradas
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

As alterações feitas aqui são bem simples: acabamos de adicionar várias `constants` ao nosso script que usaremos depois para programar o carro.

::: sidenote
Observe como armazenamos os hashes antecipadamente em variáveis. Isso é uma boa prática, pois torna o código mais legível e performático.
:::

Em seguida, edite a função `init` para que ela contenha o seguinte:

```lua
function init(self)
	-- Envia uma mensagem ao script de renderizacao (veja builtins/render/default.render_script) para definir a clear color.
	-- Isso altera a cor de fundo do jogo. O vector4 contem informacoes de cor
	-- por canal de 0-1: Red = 0.2, Green = 0.2, Blue = 0.2 e Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Adquire foco de entrada para que possamos reagir a entrada
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Algumas variaveis
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocidade e aceleracao sao relativas ao carro (nao rotacionadas)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Vetor de entrada. Ele e modificado posteriormente na funcao on_input
	-- para armazenar a entrada.
	self.input = vmath.vector3()
end
```

Quer saber o que acabamos de alterar? Aqui está a explicação.

1. Enviamos uma mensagem ao nosso script de renderização pedindo que ele defina a cor de fundo como cinza. Scripts de renderização são scripts especiais no Defold que controlam como os objetos são mostrados na tela.
2. Para escutar ações de entrada em um componente de script ou script de GUI, a mensagem `acquire_input_focus` precisa ser enviada ao objeto de jogo que contém o componente. No nosso caso, enviamos essa mensagem ao gameobject que contém o script do carro.
3. Então declaramos algumas variáveis que usaremos para acompanhar o estado atual do nosso carro.

Foi fácil, não foi? Agora continuaremos editando a função `update` para que ela contenha o seguinte:

```lua
function update(self, dt)
	-- Define a aceleracao para a entrada y
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calcula as novas posicoes das rodas dianteiras e traseiras
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calcula a nova direcao do carro
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calcula nova velocidade com base na aceleracao atual
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Atualiza a posicao com base na velocidade e direcao atuais
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpola as rodas usando vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Atualiza a rotacao das rodas
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Define a rotacao do objeto de jogo para a direcao
	go.set_rotation(self.direction)

	-- redefine aceleracao e entrada
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

Essa foi uma função enorme! Mas não se preocupe, é assim que tudo funciona:

1. Primeiro definimos nosso vetor de aceleração com base no vetor de entrada. Isso garante que a aceleração do carro esteja na direção da entrada.
2. Em seguida, o deslocamento das duas rodas é calculado com base na lógica simples de que, enquanto as rodas traseiras do carro sempre se movem para frente, as rodas dianteiras se movem na direção para a qual estão viradas.
3. Com base no deslocamento das duas rodas, a nova direção de movimento do nosso carro é calculada.
4. Aqui, adicionamos a aceleração calculada à velocidade.
5. Por fim, atualizamos a posição do carro com base na velocidade atual.
6. Fazemos slerp do ângulo de direção com base na entrada esquerda/direita. Isso é feito para que as rodas não mudem instantaneamente sempre que a entrada muda.
7. A rotação das rodas é então definida com base no ângulo de direção atual do carro. Da mesma forma, a rotação do carro é definida com base na direção em que ele está se movendo atualmente.
8. Por fim, redefinimos os vetores de aceleração e entrada.

Finalmente, é hora de fazer nosso carro reagir à entrada. Atualize a função `on_input` para que ela fique assim:

```lua
function on_input(self, action_id, action)
	-- define o vetor de entrada para corresponder a tecla pressionada
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Essa função é, na verdade, bem simples: apenas aceitamos a entrada e definimos nosso vetor de entrada.

Não se esqueça de salvar suas edições.

## Entrada

Ainda não há ações de entrada configuradas, então vamos resolver isso. Abra o arquivo */input/game.input_bindings* e adicione mapeamentos *key_trigger* para "accelerate", "brake", "left" e "right". Vamos defini-los para as setas do teclado (KEY_LEFT, KEY_RIGHT, KEY_UP e KEY_DOWN):

![Input bindings](images/car/start_input_bindings.png)

## Adicionando o carro ao jogo

Agora o carro está pronto para rodar. Nós o criamos dentro de "car.collection", mas ele ainda não existe no jogo. Isso acontece porque a engine atualmente carrega "main.collection" na inicialização. Para corrigir isso, basta adicionar *car.collection* a *main.collection*. Abra *main.collection*, marque o node raiz "Collection" na visualização *Outline*, clique com o botão direito e selecione <kbd>Add Collection From File</kbd>, selecione *car.collection* e clique em *OK*. Agora o conteúdo de *car.collection* será colocado em *main.collection* como novas instâncias. Se você alterar o conteúdo de *car.collection*, cada instância da coleção será atualizada automaticamente quando o jogo for compilado.

![Adding the car collection](images/car/start_adding_car_collection.png)

Agora, selecione <kbd>Project ▸ Build</kbd> e dê uma volta com seu novo carro!
Você perceberá que agora consegue mover o carro como quiser. Mas algo ainda não está certo. Quando você solta os controles, o carro não para como deveria. É hora de adicionar isso!

## Arrasto ao resgate

Sempre que um objeto se move no mundo real, a força de arrasto atua contra ele, fazendo-o desacelerar. Essa força cresce aproximadamente de forma proporcional ao quadrado da velocidade do objeto em movimento e, portanto, pode ser descrita como `D = k * |V| * V`, em que `k` é uma constante, `V` é a velocidade e `|V|` é sua magnitude (velocidade escalar). Vamos adicionar isso.

Na seção de constantes no topo do script, adicione a seguinte constante

```lua
local drag = 1.1	        -- a constante de arrasto <1>
```

Depois, na função update, logo acima desta linha, adicione as seguintes linhas e salve o arquivo.

```lua
function update(self, dt)
	...
  -- Calcula nova velocidade com base na aceleracao atual
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Velocidade escalar e a magnitude da velocidade vetorial
	local speed = vmath.length_sqr(self.velocity)

	-- Aplica arrasto
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Para se ja estivermos lentos o suficiente
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Declare o valor de arrasto como uma constante.
2. Calcule a velocidade com que estamos nos movendo.
3. Aplique o arrasto à aceleração atual com base na fórmula.
4. Pare se o carro já estiver lento o suficiente.

## O script completo do carro

Depois de concluir as etapas acima, seu *car.script* deve ficar assim:

```lua
local turn_speed = 0.1                           				          	-- Fator de Slerp
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 graus
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 graus
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero grau
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vetor do centro dos pares de rodas traseiras e dianteiras

local acceleration = 100 		                      									-- A aceleracao do carro
local drag = 1.1                                                  	-- a constante de arrasto

function init(self)
	-- Envia uma mensagem ao script de renderizacao (veja builtins/render/default.render_script) para definir a clear color.
	-- Isso altera a cor de fundo do jogo. O vector4 contem informacoes de cor
	-- por canal de 0-1: Red = 0.2, Green = 0.2, Blue = 0.2 e Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Adquire foco de entrada para que possamos reagir a entrada
	msg.post(".", "acquire_input_focus")

	-- Algumas variaveis
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocidade e aceleracao sao relativas ao carro (nao rotacionadas)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Vetor de entrada. Ele e modificado posteriormente na funcao on_input
	-- para armazenar a entrada.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Define a aceleracao para a entrada y
	self.acceleration.y = self.input.y * acceleration

	-- Calcula as novas posicoes das rodas dianteiras e traseiras
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calcula a nova direcao do carro
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Velocidade escalar e a magnitude da velocidade vetorial
	local speed = vmath.length(self.velocity)

	-- Aplica arrasto
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Para se ja estivermos lentos o suficiente
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calcula nova velocidade com base na aceleracao atual
	self.velocity = self.velocity + self.acceleration * dt

	-- Atualiza a posicao com base na velocidade e direcao atuais
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpola as rodas usando vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Atualiza a rotacao das rodas
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Define a rotacao do objeto de jogo para a direcao
	go.set_rotation(self.direction)

	-- redefine aceleracao e entrada
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- define o vetor de entrada para corresponder a tecla pressionada
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Testando o jogo final

Agora, selecione <kbd>Project ▸ Build</kbd> no menu principal e dê uma volta com seu novo carro!

Isso conclui este tutorial introdutório. Aqui está um conjunto de desafios que talvez você queira encarar por conta própria:

1. Atualmente, o carro se move com a mesma aceleração para frente e para trás. Você pode querer alterar isso para que o carro se mova mais devagar quando estiver dando ré.
2. Transforme algumas das constantes (como acceleration) em `properties` para que elas possam ser alteradas para diferentes instâncias do carro.
3. Adicione sons ao seu carro e faça-o fazer vroom! ([Dica](manuals/sound/))

Agora vá em frente e mergulhe no Defold. Temos muitos [manuais e tutoriais](/learn) preparados para guiar você e, se ficar preso, será muito bem-vindo no [fórum](//forum.defold.com).

Boas criações com Defold!
