---
title: O editor de cena do Defold
brief: O Scene Editor é onde você edita coleções, objetos de jogo, GUIs, efeitos de partículas e outros assets visuais. Este manual explica seleção, ferramentas e como navegar pela visualização de cena em 2D e 3D, incluindo o modo de câmera livre e configurações de câmera.
---

# O editor de cena do Defold

O **Scene Editor** é o editor visual usado para construir e editar cenas, como coleções, objetos de jogo e outros assets visuais.

Por padrão, muitas cenas visuais abrem em uma visualização **2D ortográfica**. Para trabalho em 3D, você pode mudar para um layout orientado a 3D, ativar um plano de grade 3D e usar uma câmera **perspectiva**.

## Abrindo o Scene Editor

Abra o Scene Editor dando duplo clique em um recurso visual no painel *Assets*, como:

- **Estrutura de cena** - coleções (`.collection`), objetos de jogo (`.go`)
- **Assets 2D** - atlas (`.atlas`), tilemaps (`.tilemap`), sprites (`.sprite`), tile sources (`.tilesource`)
- **Assets 3D** - modelos (`.model`, `.glb`, `.gltf`)
- **UI** - cenas GUI (`.gui`)
- **Efeitos** - efeitos de partículas (`.particlefx`)
- E outros

## Navegação na visualização de cena (controles de câmera)

A câmera do Scene Editor pode ser controlada com mouse e teclado. Os controles disponíveis dependem de você estar usando a navegação padrão da câmera ou o **Free Camera Mode**.

### Navegação padrão (todos os editores visuais)

Estes controles estão disponíveis em editores visuais:

- **Pan**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Zoom**
  - <kbd>Mouse Wheel</kbd>, ou
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Rotacionar/orbitar (3D) ao redor da seleção**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

Você também pode usar **Frame Selection** (<kbd>F</kbd>) para focar a câmera na seleção atual.

## Orientação de cena 2D e 3D

A visualização de cena pode ser usada em fluxos de trabalho 2D e 3D:

- Em **2D**, você normalmente trabalha em uma visualização ortográfica com uma grade orientada a 2D.
- Em **3D**, você normalmente:
  - Realinha a visualização para uma orientação 3D,
  - Usa uma câmera **perspectiva**,
  - Escolhe um plano de grade apropriado (frequentemente **Y** para "chão").

Você pode acessar essas funções pela barra de ferramentas e pelo menu **View**.

![Scene Editor 3D](images/editor/3d_scene.png)

## Visão geral da barra de ferramentas

No canto superior direito da visualização de cena há uma barra de ferramentas com ferramentas e opções de visualização usadas com frequência (da esquerda para a direita):

- **Move tool** (<kbd>W</kbd>)
- **Rotate tool** (<kbd>E</kbd>)
- **Scale tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) - alterna entre orientação 2D e 3D (atalho <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Toolbar](images/editor/toolbar.png)

## Selecionando e manipulando objetos

### Selecionando objetos

Use <kbd>Left Mouse Click</kbd> em objetos na janela principal para selecioná-los. O retângulo (ou cuboide) ao redor do objeto na visualização do editor será destacado em ciano para indicar qual item está selecionado. O objeto selecionado também é destacado na visualização `Outline`, como na imagem acima.

  Você também pode selecionar objetos assim:

- <kbd>Left Mouse Click</kbd> e <kbd>Drag</kbd> para selecionar todos os objetos dentro da região de seleção.
- <kbd>Left Mouse Click</kbd> em objetos no `Outline`; mantendo <kbd>⇧ Shift</kbd> pressionado, você pode expandir a seleção, ou mantendo <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>, pode selecionar/desselecionar o item clicado.

#### Move tool

![Move tool](images/editor/icon_move.png){.left}

Para mover objetos, use a *Move Tool*. Você pode encontrá-la na barra de ferramentas no canto superior direito do editor de cena ou pressionar a tecla <kbd>W</kbd>.

![Move object](images/editor/move.png){.inline}![Move object 3D](images/editor/move_3d.png){.inline}

O gizmo muda e mostra um conjunto de manipuladores - quadrados e setas (o manipulador selecionado ficará laranja) que você pode <kbd>Drag</kbd> para mover:

- uma alça quadrada central ciano para mover o objeto apenas no espaço da tela,
- 3 setas vermelha, verde e azul ao longo de cada eixo para mover o objeto apenas no eixo X, Y ou Z indicado.
- 3 alças quadradas vermelha, verde e azul (com contorno e preenchimento transparente) para mover o objeto apenas no plano indicado, por exemplo X-Y (azul) e (visível ao rotacionar a câmera em 3D) os planos X-Z (verde) e Y-Z (vermelho).

#### Rotate tool

![Rotate tool](images/editor/icon_rotate.png){.left}

Para rotacionar objetos, use a *Rotate Tool* selecionando-a na barra de ferramentas ou pressionando a tecla <kbd>E</kbd>.

![Rotate object](images/editor/rotate.png){.inline}![Rotate object 3D](images/editor/rotate_3d.png){.inline}

Essa ferramenta consiste em quatro manipuladores circulares (o manipulador selecionado ficará laranja) que você pode <kbd>Drag</kbd> para rotacionar:

- um manipulador ciano (círculo externo, maior) que rotaciona o objeto no espaço da tela
- 3 manipuladores circulares menores, vermelho, verde e azul, que permitem rotação em torno dos eixos X, Y e Z separadamente. Na visualização 2D ortográfica, dois deles ficam perpendiculares aos eixos X e Y, então os círculos aparecem apenas como duas linhas cruzando o objeto.

#### Scale tool

![Scale tool](images/editor/icon_scale.png){.left}

Para escalar objetos, use a *Scale Tool* selecionando-a na barra de ferramentas ou pressionando a tecla <kbd>R</kbd>.

![Scale object](images/editor/scale.png){.inline}![Scale object 3D](images/editor/scale_3d.png){.inline}

Essa ferramenta consiste em um conjunto de manipuladores quadrados/cúbicos (o manipulador selecionado ficará laranja) que você pode <kbd>Drag</kbd> para escalar:

- um cubo ciano no centro escala o objeto uniformemente em todos os eixos (incluindo Z).
- 3 manipuladores cúbicos vermelho, azul e verde escalam o objeto ao longo dos eixos X, Y e Z separadamente.
- 3 manipuladores quadrados vermelho, verde e azul (com contorno e preenchimento transparente) escalam o objeto nos planos X-Y, X-Z ou Y-Z separadamente.

### Filtros de visibilidade

Clique no **Visibility Eye Icon** (`👁`) na barra de ferramentas para alternar a visibilidade de vários tipos de componentes, além de caixas delimitadoras e linhas-guia (`Component Guides` ou o atalho <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) ou <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>(Mac)).

![Visibility filters](images/editor/visibilityfilters.png)

## Configurações da grade

A grade pode ser personalizada para se ajustar ao seu fluxo de trabalho (especialmente útil em 3D). Clique no botão **Grid Settings** (`▦`) para abrir o popup de configurações da grade.

![Grid Settings](images/editor/grid_popup.png)

As configurações incluem:

- **Grid size (X/Y/Z)**
  Define o espaçamento entre as linhas da grade ao longo de cada eixo. Use valores menores para posicionamento preciso de objetos pequenos, ou valores maiores para uma visão geral mais ampla.
- **Active plane (X/Y/Z)**
  Seleciona em qual plano a grade é desenhada. Em fluxos de trabalho 2D, normalmente é **Z** (o plano X-Y padrão). Em fluxos 3D, **Y** é comum para representar um plano de chão/piso.
- **Grid color**
  Define a cor das linhas da grade. Útil para contraste contra diferentes fundos de cena.
- **Grid opacity**
  Controla a transparência das linhas da grade. Valores menores tornam a grade menos intrusiva, mantendo-a como referência.
- Um botão **Reset to Defaults**
  Restaura todas as configurações da grade para seus valores originais.

## Tipo de câmera: Perspective vs Orthographic

O Scene Editor suporta ambos:

- Câmera **Orthographic** (comum em fluxos de trabalho 2D)
- Câmera **Perspective** (comum em fluxos de trabalho 3D)

Use o alternador de câmera na barra de ferramentas para trocar. Em cenas 3D, a navegação em perspectiva normalmente parece mais natural.

## Free Camera Mode

Para navegação 3D rápida, o Scene Editor fornece o **Free Camera Mode**, uma câmera em primeira pessoa / estilo "FPS".

### Ativando o Free Camera Mode

- Segure <kbd>Right Mouse Button</kbd> - o Free Camera Mode fica ativo enquanto o botão estiver pressionado
- <kbd>Shift</kbd> + <kbd>`</kbd> (crase) - alterna o Free Camera Mode para ligado, mantendo-o ativo após soltar

::: sidenote
Em alguns layouts de teclado (por exemplo, sueco), a tecla de crase é uma tecla morta e pode não acionar o atalho como esperado. Você
pode reatribuir esse atalho em `File ▸ Preferences ▸ Keys` e informar um atalho para `Scene -> Free Camera -> Activate`
:::

Quando o Free Camera Mode está ativo, a Scene View é destacada com uma linha ao redor das bordas.

### Saindo do Free Camera Mode

- Solte <kbd>Right Mouse Button</kbd> (quando ativado ao segurar), ou
- <kbd>Left Mouse Button</kbd>, <kbd>Right Mouse Button</kbd> (pressionar e soltar), ou pressione <kbd>Esc</kbd> quando o Free Camera Mode tiver sido ativado como alternância.

### Olhando ao redor (mouse look)

Enquanto o Free Camera Mode está ativo, estas teclas controlam o movimento da câmera (em vez das ferramentas do editor):

- Mova o mouse para controlar **yaw** (esquerda/direita) e **pitch** (cima/baixo)
- O pitch é limitado para evitar que a câmera vire de cabeça para baixo

Você também pode opcionalmente inverter o eixo Y (veja **Free camera settings** abaixo).

### Movimento

Enquanto o Free Camera Mode está ativo:

- <kbd>W</kbd> - para frente
- <kbd>S</kbd> - para trás
- <kbd>A</kbd> - para a esquerda
- <kbd>D</kbd> - para a direita
- <kbd>E</kbd> - para cima
- <kbd>Q</kbd> - para baixo

::: sidenote
Todas as teclas de movimento podem ser reatribuídas em `File ▸ Preferences ▸ Keys`. Depois procure por `Scene -> Free Camera`
:::

Modificadores de velocidade:

- Segure <kbd>Shift</kbd> - mover mais rápido
- Segure <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> - mover mais devagar / com mais precisão

### Walking mode (opcional)

O Free Camera Mode suporta **Walking Mode**.

Quando ativado:
- O movimento para cima/baixo é restringido para se comportar mais como caminhada em primeira pessoa presa a um plano de chão.
- Isso é útil ao explorar um nível e querer um movimento "no chão" consistente.

## Popup de configurações da câmera

O botão da câmera perspectiva na barra de ferramentas tem um popup de configurações relacionadas à câmera.

![Perspective Camera Settings](images/editor/camera_popup.png)

O popup contém:

- **Move Speed**
  Ajusta a velocidade de movimento da câmera livre.

- **Look Sensitivity**
  Ajusta a rapidez com que a câmera rotaciona em resposta ao movimento do mouse.

- **Invert Y**
  Inverte a visão vertical pelo mouse.

- **Walking Mode**
  Restringe o movimento para uma navegação semelhante a caminhar no chão.

- **Reset to Defaults**
  Restaura as configurações padrão da câmera.
