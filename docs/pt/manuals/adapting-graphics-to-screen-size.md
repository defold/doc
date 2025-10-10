---
title: Adaptando gráficos a diferentes tamanhos de tela
brief: Este manual explica como adaptar seu jogo e gráficos a diferentes tamanhos de tela.
---

# Introdução

Existem vários pontos a considerar ao adaptar seu jogo e gráficos a diferentes tamanhos de tela:

* Seu jogo é retrô, com gráficos pixel-perfect de baixa resolução, ou moderno, com gráficos em HD?
* Como o jogo deve se comportar quando jogado em tela cheia em diferentes tamanhos de tela?
  * O jogador deve ver mais conteúdo do jogo em uma tela de alta resolução ou os gráficos devem ser ajustados automaticamente para sempre mostrar o mesmo conteúdo?
* Como o jogo deve lidar com proporções de tela diferentes da configurada em *game.project*?
  * O jogador deve ver mais conteúdo do jogo? Ou talvez deveriam aparecer barras pretas? Ou talvez os elementos da interface precisem ser redimensionados?
* Que tipo de menus e componentes GUI (interface gráfica) você precisa e como eles devem se adaptar a diferentes tamanhos de tela e orientações?
  * Menus e outros componentes da interface devem mudar de layout quando a orientação mudar, ou devem manter o mesmo layout independentemente da orientação?

Este manual abordará alguns desses pontos e sugerirá boas práticas.


## Como alterar a forma como seu conteúdo é renderizado

O render script do Defold dá controle total sobre todo o pipeline de renderização. O script de renderização decide a ordem, o que desenhar e como desenhar. O comportamento padrão do script de renderização é sempre desenhar a mesma área de pixels, definida pela largura e altura no arquivo *game.project*, independentemente se a janela é redimensionada ou se a resolução da tela real não corresponde. Isso fará com que o conteúdo seja esticado se a proporção da tela mudar e ampliado ou reduzido se o tamanho da janela mudar. Em alguns jogos isso pode ser aceitável, mas na maioria dos casos você vai querer mostrar mais ou menos conteúdo do jogo se a resolução da tela ou a proporção forem diferentes, ou pelo menos garantir que o conteúdo seja ampliado sem alterar a proporção. O comportamento padrão de esticamento pode ser facilmente alterado, e você pode ler mais sobre como fazer isso no [Render manual](https://www.defold.com/manuals/render/#default-view-projection).


## Gráficos retrô/8-bit

Gráficos retrô/8-bit geralmente se referem a jogos que emulam o estilo gráfico de antigos consoles ou computadores, com baixa resolução e paleta de cores limitada. Por exemplo, o Nintendo Entertainment System (NES) tinha resolução de 256x240, o Commodore 64 tinha 320x200 e o Gameboy tinha 160x144, todos muito menores que telas modernas. Para tornar jogos com esse estilo gráfico jogáveis em telas modernas de alta resolução, os gráficos precisam ser ampliados várias vezes. Uma maneira simples de fazer isso é desenhar todos os gráficos na baixa resolução que você deseja emular e ampliá-los durante a renderização. Isso pode ser feito facilmente no Defold usando o *render script* e a [Projeção Fixa](/manuals/render/#fixed-projection) configurada com o valor de zoom adequado.

Vamos pegar este tileset e personagem ([fonte](https://ansimuz.itch.io/grotto-escape-game-art-pack)) para um jogo retrô 8-bit com resolução de 320x200:

<img width="64" height="32" alt="image" src="https://github.com/user-attachments/assets/fcb2d785-9060-4932-8b09-ca5e26820d1a" /><br>

<img width="128" height="128" alt="image" src="https://github.com/user-attachments/assets/0ba54969-6f6c-4954-9ae1-3bb6f7f3e3ac" />

Definir 320x200 no arquivo *game.project* e executar o jogo ficaria assim:

<img width="216" height="167" alt="image" src="https://github.com/user-attachments/assets/f4c3d605-0ca2-472c-a980-94a85af5a85e" />

A janela é minúscula em uma tela moderna de alta resolução! Aumentar a janela quatro vezes para 1280x800 torna mais adequado a uma tela moderna:

<img width="696" height="467" alt="image" src="https://github.com/user-attachments/assets/e1be0521-d988-423f-8657-08ca36102b5f" />

Agora que o tamanho da janela é mais razoável, precisamos ajustar os gráficos. Eles estão tão pequenos que é difícil ver o que acontece no jogo. Podemos usar o render script para configurar uma projeção fixa e ampliada:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
O mesmo resultado pode ser obtido anexando um [Componente de câmera](manuals/camera/) a um objeto de jogo, marcando *Orthographic Projection* e ajustando *Orthographic Zoom* para 4.0:

<img width="800" height="918" alt="image" src="https://github.com/user-attachments/assets/0776ef75-7151-4b52-ae6b-b56629a16b16" />
:::

O que resultará nisto:

<img width="696" height="467" alt="image" src="https://github.com/user-attachments/assets/3fe5d3f5-4108-4d1e-8272-a4c1e9e4f14d" />

Assim está melhor. A janela e os gráficos têm um bom tamanho, mas se olharmos de perto, há um problema óbvio:

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/02f96ef3-be0a-4d5b-88e0-32d9921d4488" />

Os gráficos ficam borrados! Isso ocorre devido à forma como a GPU amostra gráficos ampliados a partir da textura. A configuração padrão no arquivo *game.project* na seção *Graphics* é *linear*:

<img width="770" height="306" alt="image" src="https://github.com/user-attachments/assets/6a4f040d-f98f-4b22-9bcf-0fcfea0baff5" />

Alterar essa opção para *nearest* dará o resultado que queremos:

<img width="770" height="308" alt="image" src="https://github.com/user-attachments/assets/1213372b-6d5e-4021-97cb-c2d68dc57088" /><br>

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/fa07c27e-73b9-423a-b84f-1d69bcc3b486" />

Agora temos gráficos nítidos, *pixel-perfect*, para nosso jogo retrô. Há outros pontos a considerar, como desabilitar subpixels para sprites em *game.project*:

<img width="317" height="178" alt="image" src="https://github.com/user-attachments/assets/2f9a2bd5-3e0f-4ff8-969f-1ea3871df4c8" />

Quando a opção *Subpixels* está desabilitada, os sprites nunca são renderizados em meio pixel e sempre se ajustam ao pixel completo mais próximo.

## Gráficos em alta resolução

Para gráficos em alta resolução, o projeto e a configuração do conteúdo devem ser tratados de forma diferente dos gráficos retrô/8-bit. Com gráficos bitmap, você precisa criar seu conteúdo de forma que fique bom em uma tela de alta resolução quando exibido em escala 1:1.

Assim como nos gráficos retrô, você precisa alterar o render script. Neste caso, você quer que os gráficos escalem com o tamanho da tela, mantendo a proporção original:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

Isso garante que a tela seja redimensionada para sempre mostrar a mesma quantidade de conteúdo definida no arquivo *game.project*, possivelmente exibindo conteúdo adicional acima e abaixo ou nas laterais, dependendo da diferença de proporção.

Configure a largura e altura no arquivo *game.project* para permitir que o conteúdo do seu jogo seja exibido sem escalonamento.

### Configuração de High DPI e telas Retina

Se você deseja suportar telas Retina de alta resolução, pode ativar isso na seção Display do arquivo *game.project*:

<img width="298" height="187" alt="image" src="https://github.com/user-attachments/assets/116d9e2a-2627-42a4-9e74-0725dd565df0" />

Isso cria um back buffer de alta DPI em displays que tenham suporte a isso. O jogo será renderizado com o dobro da resolução configurada em Largura e Altura, mantendo a resolução lógica usada em scripts e propriedades. Isso significa que todas as medidas permanecem iguais e qualquer conteúdo renderizado em escala 1x parecerá igual. Mas se você importar imagens de alta resolução e escalá-las para 0,5x, elas serão exibidas em alta DPI.

## Criando uma GUI adaptativa

O sistema de criação de componentes GUI é baseado em blocos básicos, ou [nodes](/manuals/gui/#node-types), e embora pareça simples, ele permite criar desde botões até menus complexos e popups. As GUIs podem ser configuradas para se adaptarem automaticamente a mudanças de tamanho de tela e orientação. Você pode manter *nodes* ancorados ao topo, embaixo ou lados da tela, e eles podem manter seu tamanho ou se esticarem. A relação entre *nodes*, assim como seu tamanho e aparência, também pode mudar seguinfo mudanças na resolução ou orientação da tela.

### Propriedades dos *Nodes*

Cada *node* em uma GUI possui um ponto de pivô, âncoras horizontais e verticais, e um modo de ajuste.

* O ponto de pivô define o centro do *node*.
* O modo de âncora controla como a posição vertical e horizontal do *node* muda quando os limites da cena ou do *node* pai são ajustados para caber na tela física.
* O modo de ajuste define o que acontece com o *node* quando os limites da cena ou do *node* pai são ajustados para caber na tela física.

Mais detalhes sobre essas propriedades estão [no Manual de GUI](/manuals/gui/#node-properties).

### Layouts

O Defold suporta GUIs que se adaptam automaticamente a mudanças de orientação em dispositivos móveis. Com isso, você pode criar uma GUI que se ajuste à orientação e proporção de vários tamanhos de tela. Também é possível criar layouts específicos para determinados modelos de dispositivos. Mais informações estão no [manual de Layouts de GUI](/manuals/gui-layouts/)


## Testando diferentes tamanhos de tela

O menu *Debug* contém uma opção para simular a resolução de um modelo de dispositivo específico ou de uma resolução personalizada. Com o aplicativo em execução, selecione <kbd>Debug->Simulate Resolution</kbd> e escolha um modelo da lista. A janela do aplicativo será redimensionada e você poderá ver como o jogo se comporta em diferentes resoluções ou proporções de tela.

<img width="826" height="547" alt="image" src="https://github.com/user-attachments/assets/b526260c-a8c8-4dc8-bcaf-2b49f66f7a8c" />
