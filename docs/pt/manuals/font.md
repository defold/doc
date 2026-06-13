---
title: Manual de fontes no Defold
brief: Este manual descreve como o Defold lida com fontes e como colocar fontes na tela em seus jogos.
---

# Arquivos de fonte

Fontes são usadas para renderizar texto em componentes Label e nodes GUI de texto. O Defold oferece suporte a vários formatos de arquivo de fonte:

- TrueType
- OpenType
- BMFont

Fontes adicionadas ao seu projeto são convertidas automaticamente para um formato de textura que o Defold consegue renderizar. Há duas técnicas de renderização de fontes disponíveis, cada uma com seus próprios benefícios e desvantagens:

- Bitmap
- Campo de distância

## Fontes offline ou em runtime

Por padrão, a conversão para imagens de glifos rasterizadas acontece no momento do build (offline). A desvantagem é que cada fonte precisa rasterizar todos os glifos possíveis na etapa de build, produzindo texturas potencialmente muito grandes, que consomem memória e também aumentam o tamanho do pacote.

Ao usar "fontes em runtime", as fontes `.ttf` serão empacotadas como estão, e a rasterização acontecerá sob demanda em tempo de execução. Isso minimiza tanto o uso de memória em runtime quanto o tamanho do pacote.

## Suporte a layout de texto (por exemplo, da direita para a esquerda)

As fontes em runtime também têm o benefício de oferecer suporte completo a layout de texto, por exemplo, da direita para a esquerda.
Atualmente usamos as bibliotecas [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) e [SkriBidi](https://github.com/memononen/Skribidi).

Veja [Habilitando fontes em runtime](/manuals/font#enabling-runtime-fonts)

## Coleção de fontes

O formato de arquivo `.fontc` também é conhecido como coleção de fontes. No modo offline, apenas uma fonte é associada a ele.
Ao usar fontes em runtime, você pode associar mais de um arquivo de fonte (`.ttf`) à coleção de fontes.

Isso permite usar uma coleção de fontes ao renderizar vários textos em idiomas diferentes, mantendo baixo o uso de memória.
Por exemplo, carregar uma coleção com a fonte japonesa, então associar essa fonte à fonte principal atual, seguido pelo descarregamento da coleção de fontes japonesas.

## Criando uma fonte

Para criar uma fonte para uso no Defold, crie um novo arquivo Font selecionando <kbd>File ▸ New...</kbd> no menu e, em seguida, selecione <kbd>Font</kbd>. Você também pode clicar com o botão direito em um local no navegador *Assets* e selecionar <kbd>New... ▸ Font</kbd>.

![Nome da nova fonte](images/font/new_font_name.png)

Dê um nome ao novo arquivo de fonte e clique em <kbd>Ok</kbd>. O novo arquivo de fonte agora abre no editor.

![Nova fonte](images/font/new_font.png)

Arraste a fonte que deseja usar para o navegador *Assets* e solte-a em um local adequado.

Defina a propriedade *Font* para o arquivo de fonte e ajuste as propriedades da fonte conforme necessário.

## Propriedades

*Font*
: O arquivo TTF, OTF ou *`.fnt`* a usar para gerar os dados da fonte.

*Material*
: O material a usar ao renderizar esta fonte. Certifique-se de alterar isso para fontes de campo de distância e BMFonts (veja os detalhes abaixo).

*Output Format*
: O tipo de dado de fonte que será gerado.

  - `TYPE_BITMAP` converte o arquivo OTF ou TTF importado em uma textura de folha de fonte, na qual os dados bitmap são usados para renderizar nodes de texto. Os canais de cor são usados para codificar a forma da face, o contorno e a sombra projetada. Para arquivos *`.fnt`*, o bitmap da textura de origem é usado como está.
  - `TYPE_DISTANCE_FIELD` A fonte importada é convertida em uma textura de folha de fonte, em que os dados de pixel não representam pixels da tela, mas distâncias até a borda da fonte. Veja os detalhes abaixo.

*Render Mode*
: O modo de renderização a usar para renderização de glifos.

  - `MODE_SINGLE_LAYER` produz um único quad para cada caractere.
  - `MODE_MULTI_LAYER` produz quads separados para a forma do glifo, o contorno e as sombras, respectivamente. As camadas são renderizadas de trás para frente, o que impede que um caractere oculte caracteres renderizados anteriormente se o contorno for mais largo que a distância entre glifos. Esse modo de renderização também habilita o deslocamento adequado de sombra projetada, conforme especificado pelas propriedades Shadow X/Y no recurso de fonte.

*Size*
: O tamanho-alvo dos glifos em pixels.

*Antialias*
: Se a fonte deve ser antialiased ao ser gravada no bitmap-alvo. Defina como 0 se quiser renderização de fonte pixel perfect.

*Alpha*
: A transparência do glifo. 0.0--1.0, onde 0.0 significa transparente e 1.0 opaco.

*Outline Alpha*
: A transparência do contorno gerado. 0.0--1.0.

*Outline Width*
: A largura do contorno gerado em pixels. Defina como 0 para não ter contorno.

*Shadow Alpha*
: A transparência da sombra gerada. 0.0--1.0.

::: sidenote
O suporte a sombra é habilitado pelos shaders de material de fonte integrados e lida tanto com o modo de renderização de camada única quanto com o de múltiplas camadas. Se você não precisa de renderização de fonte em camadas ou suporte a sombra, é melhor usar um shader mais simples, como *`builtins/font-singlelayer.fp`*.
:::

*Shadow Blur*
: Para fontes bitmap, essa configuração indica o número de vezes que um pequeno kernel de desfoque será aplicado a cada glifo da fonte. Para fontes de campo de distância, essa configuração equivale à largura real do desfoque em pixels.

*Shadow X/Y*
: O deslocamento horizontal e vertical, em pixels, da sombra gerada. Essa configuração só afetará a sombra do glifo quando o Render Mode estiver definido como `MODE_MULTI_LAYER`.

*Characters*
: Quais caracteres incluir na fonte. Por padrão, este campo inclui os caracteres ASCII imprimíveis (códigos de caractere 32-126). Você pode adicionar ou remover caracteres deste campo para incluir mais ou menos caracteres na fonte.

Para fontes em runtime, esse texto funciona como um pré-aquecimento de cache com os glifos corretos. Isso acontece durante o tempo de carregamento. Veja `font.prewarm_text()`.

::: sidenote
Os caracteres ASCII imprimíveis são:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Se você marcar esta propriedade, todos os glifos disponíveis no arquivo de origem serão incluídos na saída.

*Cache Width/Height*
: Restringe o tamanho do bitmap de cache de glifos. Quando a engine renderiza texto, ela procura o glifo no bitmap de cache. Se ele não existir ali, será adicionado ao cache antes da renderização. Se o bitmap de cache for pequeno demais para conter todos os glifos que a engine precisa renderizar, um erro será sinalizado (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Se definido como 0, o tamanho do cache é definido automaticamente e crescerá até no máximo 2048x4096.

## Fontes de campo de distância

Fontes de campo de distância armazenam a distância até a borda do glifo na textura, em vez de dados bitmap. Quando a engine renderiza a fonte, um shader especial é necessário para interpretar os dados de distância e usá-los para desenhar o glifo. Fontes de campo de distância exigem mais recursos do que fontes bitmap, mas permitem maior flexibilidade de tamanho.

![Fonte de campo de distância](images/font/df_font.png)

Certifique-se de alterar a propriedade *Material* da fonte para *`builtins/fonts/font-df.material`* (ou qualquer outro material que consiga lidar com os dados de campo de distância) ao criar a fonte; caso contrário, a fonte não usará o shader correto ao ser renderizada na tela.

## Bitmap BMFonts

Além de bitmaps gerados, o Defold oferece suporte a fontes bitmap pré-geradas no formato "BMFont". Essas fontes consistem em uma folha de fonte PNG com todos os glifos. Além disso, um arquivo *`.fnt`* contém informações sobre onde cada glifo pode ser encontrado na folha, bem como informações de tamanho e kerning. (Observe que o Defold não oferece suporte à versão XML do formato *`.fnt`* usada pelo Phaser e algumas outras ferramentas.)

Esses tipos de fonte não oferecem melhoria de desempenho em relação a fontes bitmap geradas a partir de arquivos TrueType ou OpenType, mas podem incluir gráficos arbitrários, cores e sombras diretamente na imagem.

Adicione os arquivos *`.fnt`* e *`.png`* gerados ao seu projeto Defold. Esses arquivos devem ficar na mesma pasta. Crie um novo arquivo de fonte e defina a propriedade *font* para o arquivo *`.fnt`*. Certifique-se de que *output_format* esteja definido como `TYPE_BITMAP`. O Defold não gerará um bitmap, mas usará o fornecido no PNG.

::: sidenote
Para criar uma BMFont, você precisa usar uma ferramenta capaz de gerar os arquivos apropriados. Existem várias opções:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), uma ferramenta apenas para Windows fornecida pela AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), um aplicativo gratuito baseado em Adobe Air para Windows e macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), uma ferramenta Java de código aberto.
* [Glyph Designer](https://71squared.com/glyphdesigner), uma ferramenta comercial para macOS da 71 Squared.
* [bmGlyph](https://www.bmglyph.com), uma ferramenta comercial para macOS da Sovapps.
:::

![BMfont](images/font/bm_font.png)

Para que a fonte renderize corretamente, não se esqueça de definir a propriedade material como *`builtins/fonts/font-fnt.material`* ao criar a fonte.

## Artefatos e boas práticas

Em geral, fontes bitmap são melhores quando a fonte é renderizada sem escala. Elas são mais rápidas para renderizar na tela do que fontes de campo de distância.

Fontes de campo de distância respondem muito bem ao aumento de escala. Fontes bitmap, por outro lado, por serem apenas imagens pixeladas, aumentam de tamanho fazendo os pixels crescerem conforme a fonte é escalada, resultando em artefatos blocados. A seguir há um exemplo com tamanho de fonte de 48 pixels, ampliado 4 vezes.

![Fontes ampliadas](images/font/scale_up.png)

Ao reduzir a escala, texturas bitmap podem ser reduzidas com boa qualidade e eficiência, com antialiasing feito pela GPU. Uma fonte bitmap preserva melhor sua cor do que uma fonte de campo de distância. Aqui está um zoom da mesma fonte de exemplo com tamanho de 48 pixels, reduzida para 1/5 do tamanho:

![Fontes reduzidas](images/font/scale_down.png)

Fontes de campo de distância precisam ser renderizadas para um tamanho-alvo grande o suficiente para conter informações de distância capazes de expressar as curvas dos glifos da fonte. Esta é a mesma fonte acima, mas com tamanho de 18 pixels e ampliada 10 vezes. Fica claro que isso é pequeno demais para codificar as formas desta tipografia:

![Artefatos de campo de distância](images/font/df_artifacts.png)

Se você não quiser suporte a sombra ou contorno, defina seus respectivos valores alpha como zero. Caso contrário, dados de sombra e contorno ainda serão gerados, ocupando memória desnecessária.

## Cache de fontes
Um recurso de fonte no Defold resulta em duas coisas em tempo de execução: uma textura e os dados da fonte.

* Os dados da fonte consistem em uma lista de entradas de glifos, cada uma contendo algumas informações básicas de kerning e os dados bitmap daquele glifo.
* A textura é chamada internamente de "glyph cache texture" e será usada ao renderizar texto para uma fonte específica.

Em tempo de execução, ao renderizar texto, a engine primeiro percorre os glifos a serem renderizados para verificar quais estão disponíveis no cache de textura. Cada glifo ausente do cache de textura de glifos disparará um upload de textura a partir dos dados bitmap armazenados nos dados da fonte.

Cada glifo é colocado internamente no cache de acordo com a linha de base da fonte, o que permite calcular coordenadas locais de textura do glifo dentro de sua célula de cache correspondente em um shader. Isso significa que você pode obter certos efeitos de texto, como gradientes ou sobreposições de textura, dinamicamente. A engine expõe métricas sobre o cache ao shader por meio de uma constante especial de shader chamada `texture_size_recip`, que contém as seguintes informações nos componentes do vetor:

* `texture_size_recip.x` é o inverso da largura do cache
* `texture_size_recip.y` é o inverso da altura do cache
* `texture_size_recip.z` é a razão entre a largura da célula de cache e a largura do cache
* `texture_size_recip.w` é a razão entre a altura da célula de cache e a altura do cache

Por exemplo, para gerar um gradiente em um fragment shader, basta escrever:

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Para mais informações sobre uniforms de shader, consulte o [manual de shader](/manuals/shader).

## Habilitando fontes em runtime

É possível usar geração em runtime para fontes do tipo SDF ao usar fontes TrueType (`.ttf`).
Essa abordagem pode reduzir bastante o tamanho do download e o consumo de memória em runtime de um jogo Defold.
A pequena desvantagem é a natureza assíncrona da geração de cada glifo.

* Habilite o recurso definindo `font.runtime_generation` em game.project.

* Adicione um [App Manifest](/manuals/app-manifest) e habilite a opção `Use full text layout system`.
Isso compila uma engine personalizada com esse recurso habilitado.

::: sidenote
Este recurso está atualmente experimental, mas com a intenção de ser usado como o fluxo de trabalho padrão no futuro.
:::

::: important
A configuração `font.runtime_generation` afeta todas as fontes `.ttf` do projeto.
:::


### Script de fontes

#### Pré-aquecendo o cache de glifos

Para tornar fontes em runtime mais fáceis de usar, elas dão suporte ao pré-aquecimento do cache de glifos.
Isso significa que a fonte gerará os glifos listados em *Characters* na fonte.

::: sidenote
Se `All Chars` estiver selecionado, não haverá pré-aquecimento, pois isso anula o propósito de não precisar gerar todos os glifos ao mesmo tempo.
:::

Se o campo `Characters` do arquivo `.fontc` estiver definido, ele é usado como texto para descobrir quais glifos precisam ser atualizados no cache de glifos.

Também é possível atualizar manualmente o cache de glifos chamando `font.prewarm_text(font_collection, text, callback)`. Ela fornece um callback para informar quando todos os glifos ausentes foram adicionados ao cache de glifos e é seguro apresentar o texto na tela.

### Adicionando/removendo fontes de uma coleção de fontes

Para fontes em runtime, é possível adicionar ou remover fontes (`.ttf`) de uma coleção de fontes.
Isso é útil quando uma fonte grande foi dividida em vários arquivos para diferentes conjuntos de caracteres (por exemplo, CJK).

::: important
Adicionar uma fonte a uma coleção de fontes não carrega nem renderiza automaticamente todos os glifos.
:::

```lua
-- obtém a fonte principal
local font_collection = go.get("#label", "font")
font.add_font(font_collection, self.language_ttf_hash)

-- obtém a fonte do idioma selecionado
local font_collection_language = go.get("localization_japanese#label", "font")
local font_info = font.get_info(font_collection_language)
self.language_ttf_hash = font_info.fonts[1].path_hash -- obtém a primeira fonte (a especificada no editor)
font.add_font(self.font_collection, self.language_ttf_hash) -- aumenta a contagem de referência da fonte
```

```lua
-- remove a referência da fonte
font.add_font(self.font_collection, self.language_ttf_hash)
```

### Pré-aquecendo glifos

Para mostrar corretamente um texto com uma fonte em runtime, os glifos precisam ser resolvidos. `font.prewarm_text()` faz isso para você.
É uma operação assíncrona e, quando termina e você recebe o callback, é seguro avançar para mostrar qualquer mensagem que contenha os glifos.

::: important
Se o cache de glifos ficar cheio, o glifo mais antigo no cache será removido.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      label.set_text(self.label, info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
