## Texturização Slice-9

Nós box de GUI e componentes Sprite às vezes têm elementos sensíveis ao contexto em relação ao tamanho: painéis e diálogos que precisam ser redimensionados para caber no conteúdo contido, ou uma barra de vida que precisa ser redimensionada para mostrar a vida restante de um inimigo. Isso pode causar problemas visuais quando você aplica texturização ao nó ou sprite redimensionado.

Normalmente, a engine escala a textura para caber nos limites retangulares, mas ao definir áreas de borda slice-9 é possível limitar quais partes da textura devem ser escaladas:

![Escala de GUI](../shared/images/gui_slice9_scaling.png)

O nó box *Slice9* consiste em 4 números que especificam o número de pixels para as margens esquerda, superior, direita e inferior que não devem ser escaladas normalmente:

![Propriedades Slice 9](../shared/images/gui_slice9_properties.png)

As margens são definidas no sentido horário, começando pela borda esquerda:

![Seções Slice 9](../shared/images/gui_slice9.png)

- Segmentos de canto nunca são escalados.
- Segmentos de borda são escalados ao longo de um único eixo. Os segmentos das bordas esquerda e direita são escalados verticalmente. Os segmentos das bordas superior e inferior são escalados horizontalmente.
- A área central da textura é escalada horizontal e verticalmente conforme necessário.

A escala de textura *Slice9* descrita acima é aplicada somente quando você altera o tamanho do nó box ou do sprite:

![Tamanho do nó box de GUI](../shared/images/gui_slice9_size.png)

![Tamanho do Sprite](../shared/images/sprite_slice9_size.png)

::: important
Se você alterar o parâmetro de escala do nó box ou do sprite (ou no objeto de jogo), o nó ou sprite e a textura serão escalados sem aplicar os parâmetros *Slice9*.
:::

::: important
Ao usar texturização slice-9 em Sprites, o [Sprite Trim Mode da imagem](https://defold.com/manuals/atlas/#image-properties) deve ser definido como Off.
:::


### Mipmaps e slice-9
Devido à forma como o mipmapping funciona no renderizador, a escala de segmentos de textura às vezes pode exibir artefatos. Isso acontece quando você _reduz a escala_ dos segmentos abaixo do tamanho original da textura. O renderizador então seleciona um mipmap de resolução menor para o segmento, resultando em artefatos visuais.

![Mipmapping Slice 9](../shared/images/gui_slice9_mipmap.png)

Para evitar esse problema, certifique-se de que os segmentos da textura que serão escalados sejam pequenos o suficiente para nunca serem reduzidos, apenas ampliados.
