---
title: Manual de fontes no Defold
brief: Este manual descreve como o Defold lida com fontes e como colocar fontes na tela em seus jogos.
---

# Arquivos de fonte

Fontes são usadas para renderizar texto em componentes Label e nodes GUI de texto. O Defold oferece suporte a vários formatos de arquivo de fonte:

- TrueType
- OpenType
- BMFont

Tanto a engine de layout de texto legada quanto a completa oferecem suporte a contornos TrueType e contornos OpenType CFF1/CFF2, incluindo geração em tempo de execução a partir de recursos `.ttf` e `.otf`.

Para saber como aplicar estilos a trechos individuais de texto e trabalhar com links e sprites inseridos no texto, consulte o [manual de marcação de texto formatado](/manuals/font-richtext).

Para fontes TrueType e OpenType, a propriedade *Mode* seleciona como os glifos são renderizados:

- **Bitmap** usa imagens rasterizadas dos glifos.
- **SDF** (campo de distância com sinal) armazena as distâncias até as bordas dos glifos em uma textura, permitindo um redimensionamento mais flexível que Bitmap.
- **Vector** renderiza as faces dos glifos a partir de dados de curvas, mantendo sua nitidez quando redimensionadas. Efeitos de contorno e sombra ainda usam dados de bitmap.

Recursos de fonte recém-criados usam o modo **Vector** e geração de glifos **Dynamic**. Recursos de fonte existentes mantêm seus modos Bitmap ou SDF. Fontes BMFont sempre usam o bitmap fornecido.

O modo Vector exige suporte gráfico a texturas `RGBA16F` e `R32UI` e não é compatível com OpenGL ES 2 nem WebGL 1. Use fontes Bitmap ou SDF e materiais correspondentes ao trabalhar com adaptadores gráficos sem suporte; não há fallback automático de Vector para SDF. Consulte [Fontes vetoriais](#vector-fonts) para configurar.

## Fontes offline ou em runtime

A propriedade *Glyph Generation* seleciona quando os dados dos glifos de cada fonte são gerados:

- **Static** gera os glifos selecionados durante o build (offline). *Characters* e *All Chars* controlam quais glifos são incluídos. O arquivo-fonte `.ttf` ou `.otf` não é incluído no bundle para geração em tempo de execução.
- **Dynamic** inclui o arquivo-fonte `.ttf` ou `.otf` no bundle e gera glifos sob demanda em tempo de execução. *Prewarm Text* prepara os glifos quando a fonte é carregada. Outros glifos podem ser gerados depois, conforme necessário.

Fontes SDF e Vector oferecem suporte às duas opções. Fontes Bitmap e BMFont usam geração Static. Cada recurso de fonte é configurado de forma independente, portanto um projeto pode combinar fontes Static e Dynamic.

A geração Dynamic pode reduzir o tamanho do bundle e o uso de memória em tempo de execução, principalmente em fontes com grandes conjuntos de caracteres. Ela exige o sistema completo de layout de texto na engine; consulte [Habilitando fontes em tempo de execução](#enabling-runtime-fonts).

<a id="text-layout-support-eg-right-to-left"></a>

## Suporte a layout de texto (por exemplo, da direita para a esquerda)

As fontes em runtime também têm o benefício de oferecer suporte completo a layout de texto, por exemplo, da direita para a esquerda.
Atualmente usamos as bibliotecas [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) e [SkriBidi](https://github.com/memononen/Skribidi).

Veja [Habilitando fontes em runtime](/manuals/font#enabling-runtime-fonts)

O editor usa o renderizador de fontes da engine para pré-visualizar fontes e texto de cenas. A modelagem de texto e o layout da direita para a esquerda exigem [fontes em runtime](#enabling-runtime-fonts) e a opção **Use full text layout system** no App Manifest. Para fontes offline, a prévia respeita as configurações **Characters** e **All Chars** da fonte.

## Coleção de fontes

O formato de arquivo `.fontc` também é conhecido como coleção de fontes. No modo offline, apenas uma fonte é associada a ele.
Ao usar fontes em runtime, você pode associar mais de um arquivo de fonte (`.ttf` ou `.otf`) à coleção de fontes.

Isso permite usar uma coleção de fontes ao renderizar vários textos em idiomas diferentes, mantendo baixo o uso de memória.
Por exemplo, carregar uma coleção com a fonte japonesa, então associar essa fonte à fonte principal atual, seguido pelo descarregamento da coleção de fontes japonesas.

## Criando uma fonte

Para criar uma fonte para uso no Defold, crie um novo arquivo Font selecionando <kbd>File ▸ New...</kbd> no menu e, em seguida, selecione <kbd>Font</kbd>. Você também pode clicar com o botão direito em um local no navegador *Assets* e selecionar <kbd>New... ▸ Font</kbd>.

![Nome da nova fonte](images/font/new_font_name.png)

Dê um nome ao novo arquivo de fonte e clique em <kbd>Ok</kbd>. O novo arquivo de fonte agora abre no editor.

Arraste a fonte que deseja usar para o navegador *Assets* e solte-a em um local adequado.

Defina a propriedade *Font* como o arquivo de fonte. Para uma fonte `.ttf` ou `.otf`, selecione *Mode* e *Glyph Generation* e configure as demais propriedades conforme necessário. Para geração Dynamic, conclua também a [configuração de fontes em tempo de execução](#enabling-runtime-fonts).

![Propriedades da fonte com modo Vector e geração de glifos Dynamic](images/font/font_properties.png)

Para fontes Vector, use *Font Size* em um componente Label ou nó de texto de GUI para alterar o tamanho do texto exibido. *Outline/Shadow Bitmap Size* controla a resolução dos bitmaps dos efeitos independentemente do tamanho do texto exibido.

Para fontes Bitmap e SDF, defina *Size* no recurso de fonte para escolher o tamanho dos glifos gerados. Os tamanhos de BMFont vêm do arquivo-fonte `.fnt`. Para alterar o tamanho de exibição dessas fontes, redimensione o componente Label ou o nó de texto de GUI.

## Propriedades {#properties}

*Font*
: O arquivo TTF, OTF ou *`.fnt`* a usar para gerar os dados da fonte.

*Material*
: O material usado para renderizar esta fonte. Ele deve corresponder ao modo da fonte; consulte [Materiais de fontes](#font-materials).

*Mode*
: A técnica de renderização para uma fonte `.ttf` ou `.otf`: **Bitmap**, **SDF** ou **Vector**. Substitui a antiga propriedade *Output Format*. Essa propriedade não é exibida para fontes BMFont.

*Glyph Generation*
: **Static** gera os dados dos glifos durante o build. **Dynamic** os gera em tempo de execução e exige o [sistema completo de layout de texto](#enabling-runtime-fonts). Essa propriedade está disponível para fontes SDF e Vector. No modo Bitmap, ela é fixada em Static e não é exibida para fontes BMFont.

*Render Mode*
: A organização das camadas para fontes Bitmap geradas. Essa propriedade só é exibida no modo Bitmap para fontes `.ttf` e `.otf`. Para fontes SDF, Vector e BMFont, o Defold seleciona a organização das camadas automaticamente.

  - **Single Layer** produz um único quad para cada caractere.
  - **Multi Layer** produz quads separados para a forma do glifo, o contorno e a sombra. As camadas são renderizadas de trás para frente, impedindo que um caractere oculte caracteres renderizados anteriormente quando o contorno é mais largo que a distância entre os glifos. Isso também habilita os deslocamentos de sombra das propriedades *Shadow X/Y*.

*Size*
: O tamanho dos glifos em pixels usado ao gerar dados de fontes Bitmap ou SDF. Para fontes BMFont, o tamanho é lido do arquivo `.fnt` e não pode ser editado aqui.

*Outline/Shadow Bitmap Size*
: No modo Vector, esta propriedade substitui *Size*. Ela controla a resolução do bitmap dos efeitos habilitados de contorno e sombra, tanto na geração Static quanto na Dynamic. Fica desabilitada quando nenhum dos efeitos está habilitado, pois as faces dos glifos usam dados de curvas. Alterar *Font Size* de um Label ou nó de texto de GUI não altera essa resolução compartilhada de bitmap.

*Antialias*
: Define se deve suavizar os glifos ao gerar dados de fontes Bitmap. Desabilite para uma renderização pixel perfect. Essa propriedade só é exibida no modo Bitmap para fontes `.ttf` e `.otf`.

*Alpha*
: A transparência do glifo. 0.0--1.0, onde 0.0 significa transparente e 1.0 opaco.

*Outline Alpha*
: A transparência do contorno gerado. 0.0--1.0.

*Outline Width*
: A largura do contorno gerado em pixels. Defina como 0 para não ter contorno.

*Shadow Alpha*
: A transparência da sombra gerada. 0.0--1.0.

::: sidenote
O shader de fonte Bitmap integrado oferece suporte a sombras nos modos de renderização *Single Layer* e *Multi Layer*. Para fontes Bitmap geradas que usam renderização *Single Layer* e não precisam de sombras, um material personalizado pode usar `/builtins/fonts/font-singlelayer.fp`. Fontes SDF e Vector exigem shaders correspondentes ao seu modo; consulte [Materiais de fontes](#font-materials).
:::

*Shadow Blur*
: A quantidade de desfoque aplicada à sombra gerada. Defina como 0 para uma sombra nítida.

*Shadow X/Y*
: O deslocamento horizontal e vertical, em pixels, da sombra gerada. Para fontes Bitmap geradas, use o modo de renderização *Multi Layer* para aplicar esses deslocamentos. O Defold seleciona as camadas apropriadas automaticamente para fontes SDF e Vector.

*Characters*
: Na geração Static, os caracteres a incluir na fonte compilada. Por padrão, este campo contém os caracteres ASCII imprimíveis (códigos de caracteres 32–126). Adicione ou remova caracteres para controlar quais glifos ficam disponíveis em tempo de execução.

*Prewarm Text*
: Na geração Dynamic, esta propriedade substitui *Characters*. O texto é usado para gerar glifos e preparar o cache quando a fonte é carregada. Ela não restringe quais caracteres podem ser gerados depois. Você também pode preparar texto a partir de um script com [`font.prewarm_text()`](/ref/font/#font.prewarm_text).

::: sidenote
Os caracteres ASCII imprimíveis são:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Na geração Static, inclui todos os glifos disponíveis na fonte de origem em vez de limitar a fonte a *Characters*. Essa propriedade fica oculta para fontes Dynamic.

*Cache Width/Height*
: Limita o tamanho do bitmap de cache de glifos usado por fontes Bitmap e SDF e pelos efeitos de contorno e sombra de fontes Vector. Ao renderizar texto, a engine procura o glifo no bitmap de cache. Se ele não existir ali, será adicionado ao cache antes da renderização. Se o bitmap de cache for pequeno demais para conter todos os glifos solicitados, um erro será sinalizado (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Se definido como 0, o tamanho do cache é definido automaticamente e crescerá até no máximo 2048x4096.

## Materiais de fontes {#font-materials}

Use um material que corresponda ao modo da fonte. O *Material* do recurso de fonte é usado por nós de texto de GUI. Componentes Label têm uma propriedade *Material* separada que também deve corresponder à fonte:

| Modo ou origem da fonte | Material de fonte para texto de GUI | Material do componente Label |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

Alterar *Mode* no editor de fontes troca entre os materiais integrados Bitmap, SDF e Vector correspondentes quando um desses materiais já está atribuído à fonte. Materiais personalizados não são substituídos automaticamente. Verifique também a propriedade *Material* de todos os componentes Label que usam a fonte.

## Fontes vetoriais {#vector-fonts}

Fontes vetoriais renderizam as faces dos glifos a partir de curvas, mantendo sua nitidez quando o tamanho do texto exibido muda. Para configurar uma fonte que gera seus glifos em tempo de execução:

1. Crie um recurso `.font`, por exemplo `/fonts/ui.font`, e selecione uma fonte TrueType ou OpenType na propriedade *Font*. A fonte integrada `/builtins/fonts/vera_mo_bd.ttf` pode ser usada para texto comum.
2. Defina *Mode* como **Vector**, *Glyph Generation* como **Dynamic** e *Material* como `/builtins/fonts/font-vector.material`. Esses são os valores padrão para recursos de fonte recém-criados.
3. Habilite **Use full text layout system** em um App Manifest atribuído ao seu projeto. Siga [Habilitando fontes em tempo de execução](#enabling-runtime-fonts) para configurar a engine personalizada.
4. Habilite [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) em *game.project*.
5. Atribua a fonte a um [Label](/manuals/label/) ou adicione-a a *Fonts* de uma cena de GUI e selecione-a em um [nó de texto](/manuals/gui-text/). Para um Label, defina também o *Material* do componente como `/builtins/fonts/label-vector.material`. Defina *Font Size* do componente ou nó com o tamanho de exibição desejado.

As faces dos glifos Vector usam texturas de curvas, mas contornos e sombras habilitados ainda geram dados de bitmap SDF e consomem memória de textura do cache de glifos. *Outline/Shadow Bitmap Size* define essa resolução de bitmap independentemente de *Font Size* do Label ou nó de texto de GUI. Defina *Outline Alpha* e *Shadow Alpha* como `0` quando esses efeitos não forem necessários para evitar gerar seus dados de bitmap.

### Emojis coloridos {#color-emoji}

Fontes Vector podem renderizar emojis coloridos COLRv1, incluindo cores de paleta e gradientes lineares e radiais. Os modos Bitmap e SDF não renderizam cores COLRv1. Use a configuração Dynamic Vector acima e adicione uma fonte de emojis COLRv1 como fallback à coleção de fontes. O texto comum continua usando a fonte original.

Por exemplo, copie a [fonte Noto Color Emoji](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf) COLRv1 para seu projeto como `/fonts/NotoColorEmoji-Regular.ttf`. Escolha a versão COLRv1: outras fontes de emojis podem usar um formato de cores diferente mesmo quando o nome do arquivo termina em `.ttf`.

Acrescente `/fonts/NotoColorEmoji-Regular.ttf` a **Project ▸ Custom Resources** em *game.project*. Sem outros recursos personalizados, a configuração é:

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Um caminho de fonte escrito em Lua não faz o arquivo da fonte ser incluído no bundle. [Custom Resources](/manuals/project-settings/#custom-resources) disponibiliza esse arquivo de fonte para [`font.add_font()`](/ref/font/#font.add_font), que o carrega pelo sistema de recursos. Passe o caminho da fonte de origem como string ao carregá-la do bundle.

Adicione o fallback uma vez por recurso de fonte compartilhado. A alteração afeta todos os Labels e nós de texto de GUI que usam essa fonte, e adicionar o mesmo fallback duas vezes gera um erro. Se usar tanto o [exemplo de Label](/manuals/label/#vector-fonts-and-color-emoji) quanto o [exemplo de GUI](/manuals/gui-text/#vector-fonts-and-color-emoji) com o mesmo `.font`, coordene a inicialização para que o fallback seja adicionado uma vez antes que qualquer exemplo prepare ou exiba texto. Os exemplos preparam o texto completo após adicionar o fallback e o exibem quando o callback informa sucesso.

## Fontes de campo de distância

Fontes de campo de distância armazenam a distância até a borda do glifo na textura, em vez de dados bitmap. Quando a engine renderiza a fonte, um shader especial é necessário para interpretar os dados de distância e usá-los para desenhar o glifo. Fontes de campo de distância exigem mais recursos do que fontes bitmap, mas permitem maior flexibilidade de tamanho.

![Fonte de campo de distância](images/font/df_font.png)

Selecione **SDF** em *Mode* e escolha **Static** ou **Dynamic** em *Glyph Generation*. Use *`/builtins/fonts/font-df.material`* para a fonte e *`/builtins/fonts/label-df.material`* para componentes Label, ou materiais personalizados que processem dados de campo de distância.

## Bitmap BMFonts

Além de bitmaps gerados, o Defold oferece suporte a fontes bitmap pré-geradas no formato "BMFont". Essas fontes consistem em uma folha de fonte PNG com todos os glifos. Além disso, um arquivo *`.fnt`* contém informações sobre onde cada glifo pode ser encontrado na folha, bem como informações de tamanho e kerning. (Observe que o Defold não oferece suporte à versão XML do formato *`.fnt`* usada pelo Phaser e algumas outras ferramentas.)

Esses tipos de fonte não oferecem melhoria de desempenho em relação a fontes bitmap geradas a partir de arquivos TrueType ou OpenType, mas podem incluir gráficos arbitrários, cores e sombras diretamente na imagem.

Adicione os arquivos *`.fnt`* e *`.png`* gerados ao seu projeto Defold. Esses arquivos devem ficar na mesma pasta. Crie um novo arquivo de fonte e defina a propriedade *Font* como o arquivo *`.fnt`*. O Defold usa o bitmap fornecido e lê seu tamanho do arquivo `.fnt`. *Mode* e *Glyph Generation* não são exibidos para fontes BMFont.

::: sidenote
Para criar uma BMFont, você precisa usar uma ferramenta capaz de gerar os arquivos apropriados. Existem várias opções:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), uma ferramenta apenas para Windows fornecida pela AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), um aplicativo gratuito baseado em Adobe Air para Windows e macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), uma ferramenta Java de código aberto.
* [Glyph Designer](https://71squared.com/glyphdesigner), uma ferramenta comercial para macOS da 71 Squared.
* [bmGlyph](https://www.bmglyph.com), uma ferramenta comercial para macOS da Sovapps.
:::

![BMfont](images/font/bm_font.png)

Defina o *Material* da fonte como *`/builtins/fonts/font-fnt.material`*. Para componentes Label, use *`/builtins/fonts/label-fnt.material`*.

## Artefatos e boas práticas

Em geral, fontes bitmap são melhores quando a fonte é renderizada sem escala. Elas são mais rápidas para renderizar na tela do que fontes de campo de distância.

Fontes de campo de distância respondem muito bem ao aumento de escala. Fontes bitmap, por outro lado, por serem apenas imagens pixeladas, aumentam de tamanho fazendo os pixels crescerem conforme a fonte é escalada, resultando em artefatos blocados. A seguir há um exemplo com tamanho de fonte de 48 pixels, ampliado 4 vezes.

![Fontes ampliadas](images/font/scale_up.png)

Ao reduzir a escala, texturas bitmap podem ser reduzidas com boa qualidade e eficiência, com antialiasing feito pela GPU. Uma fonte bitmap preserva melhor sua cor do que uma fonte de campo de distância. Aqui está um zoom da mesma fonte de exemplo com tamanho de 48 pixels, reduzida para 1/5 do tamanho:

![Fontes reduzidas](images/font/scale_down.png)

Fontes de campo de distância precisam ser renderizadas para um tamanho-alvo grande o suficiente para conter informações de distância capazes de expressar as curvas dos glifos da fonte. Esta é a mesma fonte acima, mas com tamanho de 18 pixels e ampliada 10 vezes. Fica claro que isso é pequeno demais para codificar as formas desta tipografia:

![Artefatos de campo de distância](images/font/df_artifacts.png)

Se não quiser suporte a sombra ou contorno, defina os respectivos valores alfa como zero. Caso contrário, os dados de sombra e contorno ainda serão gerados, consumindo memória desnecessária. No modo Vector, desabilitar ambos os efeitos evita gerar seus dados de bitmap; as faces dos glifos continuam usando dados de curvas.

## Cache de fontes
Recursos de fonte Bitmap e SDF usam uma textura de cache de glifos e dados de fonte em tempo de execução. Fontes Vector armazenam as faces dos glifos como dados de curvas e usam um cache de bitmap para efeitos de contorno e sombra habilitados. O layout de textura descrito abaixo se aplica a fontes Bitmap e SDF.

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

## Habilitando fontes em runtime {#enabling-runtime-fonts}

A geração em tempo de execução é configurada por recurso de fonte:

1. Abra o recurso `.font` e selecione uma fonte TrueType (`.ttf`) ou OpenType (`.otf`).
2. Defina *Mode* como **SDF** ou **Vector** e *Glyph Generation* como **Dynamic**.
3. Escolha os [materiais correspondentes de fonte e Label](#font-materials).
4. Adicione um [App Manifest](/manuals/app-manifest), atribua-o a *Native Extensions ▸ App Manifest* em *game.project* e habilite **Use full text layout system**. Isso compila uma engine personalizada com suporte à geração de fontes em tempo de execução e ao layout completo de texto.
5. Defina *Prewarm Text* com o texto que será exibido logo após o carregamento da fonte. Para texto necessário posteriormente, use [`font.prewarm_text()`](/ref/font/#font.prewarm_text) e aguarde seu callback antes de exibi-lo.

Novos recursos de fonte já usam o modo Vector e geração Dynamic, mas ainda exigem a configuração do App Manifest descrita acima.

### Script de fontes

#### Pré-aquecendo o cache de glifos

Fontes Dynamic geram os glifos necessários para *Prewarm Text* quando a fonte é carregada. O campo é interpretado como texto a ser disposto, preparando o cache para os glifos de que o texto precisa. *All Chars* não está disponível para fontes Dynamic.

Você também pode chamar `font.prewarm_text(font_collection, text, callback)` para uma fonte Dynamic. O callback informa quando todos os glifos ausentes foram adicionados ao cache e o texto pode ser exibido com segurança. Essa função não pode ser usada com fontes Static.

### Adicionando/removendo fontes de uma coleção de fontes

Para fontes Dynamic, é possível adicionar ou remover fontes de origem (`.ttf` ou `.otf`) de uma coleção de fontes.
Isso é útil quando uma fonte grande foi dividida em vários arquivos para diferentes conjuntos de caracteres (por exemplo, CJK).

::: important
Adicionar uma fonte a uma coleção de fontes não carrega nem renderiza automaticamente todos os glifos.
:::

```lua
function init(self)
    -- Obtenha a coleção de fontes de destino.
    self.font_collection = go.get("#label", "font")

    -- Obtenha a primeira fonte atribuída à coleção do idioma selecionado.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associe-a à coleção de destino e aumente sua contagem de referências.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remova a associação e libere a referência à fonte.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
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
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
