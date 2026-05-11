---
title: Efeitos de partículas no Defold
brief: Este manual explica como o componente Particle FX funciona e como editá-lo para criar efeitos visuais de partículas.
---

# Particle FX

Efeitos de partículas são usados para melhorar visualmente os jogos. Você pode usá-los para criar explosões, respingos de sangue, rastros, clima ou qualquer outro efeito.

![ParticleFX Editor](images/particlefx/editor.png)

Efeitos de partículas consistem em uma série de emissores e modificadores opcionais:

Emissor
: Um emissor é uma forma posicionada que emite partículas distribuídas uniformemente pela forma. O emissor contém propriedades que controlam a geração de partículas, além da imagem ou animação, tempo de vida, cor, forma e velocidade das partículas individuais.

Modificador
: Um modificador afeta a velocidade das partículas geradas para fazê-las acelerar ou desacelerar em uma direção específica, mover-se radialmente ou girar ao redor de um ponto. Modificadores podem afetar as partículas de um único emissor ou de um emissor específico.

## Criando um efeito

Selecione <kbd>New... ▸ Particle FX</kbd> no menu de contexto do navegador *Assets*. Nomeie o novo arquivo de efeito de partículas. O editor abrirá o arquivo usando o [Scene Editor](/manuals/editor/#the-scene-editor).

O painel *Outline* mostra o emissor padrão. Selecione o emissor para exibir suas propriedades no painel *Properties* abaixo.

![Default particles](images/particlefx/default.png)

Para adicionar um novo emissor ao efeito, clique com o botão direito na raiz do *Outline* e selecione <kbd>Add Emitter ▸ [type]</kbd> no menu de contexto. Observe que você pode alterar o tipo do emissor nas propriedades do emissor.

Para adicionar um novo modificador, clique com o botão direito no local do modificador no *Outline* (a raiz do efeito ou um emissor específico) e selecione <kbd>Add Modifier</kbd>; então selecione o tipo do modificador.

![Add modifier](images/particlefx/add_modifier.png)

![Add modifier select](images/particlefx/add_modifier_select.png)

Um modificador que fica na raiz do efeito (não como filho de um emissor) afeta todas as partículas do efeito.

Um modificador adicionado como filho de um emissor afeta apenas aquele emissor.

## Pré-visualizando um efeito

* Selecione <kbd>View ▸ Play</kbd> no menu para pré-visualizar o efeito. Talvez seja necessário afastar a câmera para ver o efeito corretamente.
* Selecione <kbd>View ▸ Play</kbd> novamente para pausar o efeito.
* Selecione <kbd>View ▸ Stop</kbd> para parar o efeito. Reproduzi-lo novamente reinicia o efeito a partir do estado inicial.

Ao editar um emissor ou modificador, o resultado fica visível imediatamente no editor, mesmo com o efeito pausado:

![Edit particles](images/particlefx/rotate.gif)

## Propriedades do emissor

Id
: Identificador do emissor (usado ao definir constantes de renderização para emissores específicos).

Position/Rotation
: Transformação do emissor relativa ao componente ParticleFX.

Play Mode
: Controla como o emissor é reproduzido:
  - `Once` para o emissor depois que ele atinge sua duração.
  - `Loop` reinicia o emissor depois que ele atinge sua duração.

Size Mode
: Controla como as animações flipbook serão dimensionadas:
  - `Auto` mantém o tamanho de cada frame da animação flipbook conforme a imagem de origem.
  - `Manual` define o tamanho da partícula de acordo com a propriedade de tamanho.

Emission Space
: Em qual espaço geométrico as partículas geradas existirão:
  - `World` move as partículas independentemente do emissor.
  - `Emitter` move as partículas em relação ao emissor.

Duration
: O número de segundos durante os quais o emissor deve emitir partículas.

Start Delay
: O número de segundos que o emissor deve esperar antes de emitir partículas.

Start Offset
: O número de segundos dentro da simulação de partículas em que o emissor deve começar; em outras palavras, por quanto tempo o emissor deve pré-aquecer o efeito.

Image
: O arquivo de imagem (Tile source ou Atlas) a usar para texturizar e animar as partículas.

Animation
: A animação do arquivo *Image* a usar nas partículas.

Material
: O material a usar para sombrear as partículas.

Blend Mode
: Os modos de blend disponíveis são `Alpha`, `Add` e `Multiply`.

Max Particle Count
: Quantas partículas originadas deste emissor podem existir ao mesmo tempo.

Emitter Type
: A forma do emissor
  - `Circle` emite partículas de um local aleatório dentro de um círculo. As partículas são direcionadas para fora a partir do centro. O diâmetro do círculo é definido por *Emitter Size X*.

  - `2D Cone` emite partículas de um local aleatório dentro de um cone plano (um triângulo). As partículas são direcionadas para fora pelo topo do cone. *Emitter Size X* define a largura do topo e *Y* define a altura.

  - `Box` emite partículas de um local aleatório dentro de uma caixa. As partículas são direcionadas para cima ao longo do eixo Y local da caixa. *Emitter Size X*, *Y* e *Z* definem largura, altura e profundidade respectivamente. Para um retângulo 2D, mantenha o tamanho Z em zero.

  - `Sphere` emite partículas de um local aleatório dentro de uma esfera. As partículas são direcionadas para fora a partir do centro. O diâmetro da esfera é definido por *Emitter Size X*.

  - `Cone` emite partículas de um local aleatório dentro de um cone 3D. As partículas são direcionadas para fora pelo disco superior do cone. *Emitter Size X* define o diâmetro do disco superior e *Y* define a altura do cone.

  ![emitter types](images/particlefx/emitter_types.png)

Particle Orientation
: Como as partículas emitidas são orientadas:
  - `Default` define a orientação como orientação unitária
  - `Initial Direction` mantém a orientação inicial das partículas emitidas.
  - `Movement Direction` ajusta a orientação das partículas de acordo com sua velocidade.

Inherit Velocity
: Um valor de escala que define quanto da velocidade do emissor as partículas devem herdar. Esse valor só está disponível quando *Space* está definido como `World`. A velocidade do emissor é estimada a cada frame.

Stretch With Velocity
: Marque para escalar qualquer alongamento de partícula na direção do movimento.

### Modos de blend
:[blend-modes](../shared/blend-modes.md)

## Propriedades animáveis do emissor

Essas propriedades têm dois campos: um valor e uma variação. A variação é aplicada aleatoriamente a cada partícula gerada. Por exemplo, se o valor for 50 e a variação for 3, cada partícula gerada receberá um valor entre 47 e 53 (50 +/- 3).

![Property](images/particlefx/property.png)

Ao marcar o botão de key, o valor da propriedade é controlado por uma curva ao longo da duração do emissor. Para redefinir uma propriedade com key, desmarque o botão de key.

![Property keyed](images/particlefx/key.png)

O *Curve Editor* (disponível entre as abas na visualização inferior) é usado para modificar a curva. Propriedades com key não podem ser editadas na visualização *Properties*, apenas no *Curve Editor*. <kbd>Clique e arraste</kbd> os pontos e tangentes para modificar o formato da curva. <kbd>Clique duas vezes</kbd> na curva para adicionar pontos de controle. Para remover um ponto de controle, <kbd>clique duas vezes</kbd> nele.

![ParticleFX Curve Editor](images/particlefx/curve_editor.png)

Para aplicar zoom automático no Curve Editor e exibir todas as curvas, pressione <kbd>F</kbd>.

As propriedades a seguir podem ser animadas ao longo do tempo de reprodução do emissor:

Spawn Rate
: O número de partículas a emitir por segundo.

Emitter Size X/Y/Z
: As dimensões da forma do emissor; veja *Emitter Type* acima.

Particle Life Time
: O tempo de vida de cada partícula gerada, em segundos.

Initial Speed
: A velocidade inicial de cada partícula gerada.

Initial Size
: O tamanho inicial de cada partícula gerada. Se você definir *Size Mode* como `Automatic` e usar uma animação flipbook como fonte de imagem, essa propriedade será ignorada.

Initial Red/Green/Blue/Alpha
: Os valores iniciais de tint dos componentes de cor das partículas.

Initial Rotation
: Os valores iniciais de rotação (em graus) das partículas.

Initial Stretch X/Y
: Os valores iniciais de alongamento (em unidades) das partículas.

Initial Angular Velocity
: A velocidade angular inicial (em graus/segundo) de cada partícula gerada.

As propriedades a seguir podem ser animadas ao longo do tempo de vida das partículas:

Life Scale
: O valor de escala ao longo da vida de cada partícula.

Life Red/Green/Blue/Alpha
: O valor de tint do componente de cor ao longo da vida de cada partícula.

Life Rotation
: O valor de rotação (em graus) ao longo da vida de cada partícula.

Life Stretch X/Y
: O valor de alongamento (em unidades) ao longo da vida de cada partícula.

Life Angular Velocity
: A velocidade angular (em graus/segundo) ao longo da vida de cada partícula.

## Modificadores

Há quatro tipos de modificadores disponíveis que afetam a velocidade das partículas:

`Acceleration`
: Aceleração em uma direção geral.

`Drag`
: Reduz a aceleração das partículas proporcionalmente à velocidade da partícula.

`Radial`
: Atrai ou repele partículas em direção a/para longe de uma posição.

`Vortex`
: Afeta partículas em uma direção circular ou espiralada ao redor da sua posição.

  ![modifiers](images/particlefx/modifiers.png)

## Propriedades do modificador

Position/Rotation
: A transformação do modificador relativa ao seu pai.

Magnitude
: A intensidade do efeito que o modificador exerce sobre as partículas.

Max Distance
: A distância máxima dentro da qual as partículas são afetadas por este modificador. Usado apenas para Radial e Vortex.

## Controlando um efeito de partículas

Para iniciar e parar um efeito de partículas a partir de um script:

```lua
-- inicia o componente de efeito "particles" no objeto de jogo atual
particlefx.play("#particles")

-- para o componente de efeito "particles" no objeto de jogo atual
particlefx.stop("#particles")
```

Para iniciar e parar um efeito de partículas a partir de um script de GUI, consulte o [manual de GUI Particle FX](/manuals/gui-particlefx#controlling-the-effect) para mais informações.

::: sidenote
Um efeito de partículas continuará emitindo partículas mesmo se o objeto de jogo ao qual o componente de efeito de partículas pertencia for excluído.
:::
Veja a [documentação de referência de Particle FX](/ref/particlefx) para mais informações.

## Constantes de material

O material padrão de efeitos de partículas tem as seguintes constantes, que podem ser alteradas usando `particlefx.set_constant()` e redefinidas usando `particlefx.reset_constant()` (consulte o [manual de Material para mais detalhes](/manuals/material/#vertex-and-fragment-constants)):

`tint`
: O tint de cor do efeito de partículas (`vector4`). O vector4 é usado para representar o tint com x, y, z e w correspondendo ao tint vermelho, verde, azul e alfa. Consulte a [referência da API para ver um exemplo](/ref/particlefx/#particlefx.set_constant:url-constant-value).


## Configuração do projeto

O arquivo *game.project* tem algumas [configurações do projeto](/manuals/project-settings#particle-fx) relacionadas a partículas.
