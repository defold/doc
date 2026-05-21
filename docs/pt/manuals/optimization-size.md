---
title: Otimizando o tamanho de um jogo Defold
brief: Este manual descreve como otimizar o tamanho de um jogo Defold.
---

# Otimizando o tamanho do jogo

O tamanho do seu jogo pode ser um fator crítico de sucesso para plataformas como web e mobile, enquanto é menos importante em desktop e consoles, onde espaço em disco é barato e geralmente abundante.

### iOS e Android
A Apple e o Google definiram limites de tamanho de aplicação ao baixar por redes móveis (em oposição ao download por Wi-Fi). Para Android, esse limite é de 200 MB para apps publicados com [app bundles](https://developer.android.com/guide/app-bundle#size_restrictions). No iOS, os usuários receberão um aviso se a aplicação tiver mais de 200 MB, mas ainda poderão prosseguir com o download.

::: sidenote
De acordo com um estudo de 2017, a cada aumento de 6 MB no tamanho de um APK, a taxa de conversão de instalação cai 1%. ([fonte](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5
Poki e muitas outras plataformas de jogos web recomendam que o download inicial não seja maior que 5 MB.

O Facebook recomenda que um Facebook Instant Game inicie em menos de 5 segundos e, de preferência, em menos de 3 segundos. O que isso significa para o tamanho real da aplicação não é claramente definido, mas estamos falando de um tamanho na faixa de até 20 MB.

Anúncios jogáveis geralmente são limitados entre 2 e 5 MB, dependendo da rede de anúncios.

## Estratégias de otimização de tamanho
Você pode otimizar o tamanho da aplicação de duas formas: reduzindo o tamanho da engine e/ou reduzindo o tamanho dos assets do jogo.

Para entender melhor o que compõe o tamanho da sua aplicação, você pode [gerar um relatório de build](/manuals/bundling/#build-reports) ao empacotar. É bastante comum que sons e gráficos ocupem a maior parte do tamanho de qualquer jogo.

::: important
O Defold criará uma árvore de dependências ao compilar e empacotar sua aplicação. O sistema de build começará pela coleção bootstrap especificada no arquivo *game.project* e inspecionará cada coleção, objeto de jogo e componente referenciado para criar uma lista dos assets em uso. Somente esses assets serão incluídos no pacote final da aplicação. Qualquer coisa que não seja referenciada diretamente será excluída. Embora seja bom saber que assets não usados não serão incluídos, você, como desenvolvedor, ainda precisa considerar o que entra na aplicação final, o tamanho dos assets individuais e o tamanho total do pacote da aplicação. 
:::

## Otimizar o tamanho da engine
Uma forma rápida de reduzir o tamanho da engine é remover funcionalidades da engine que você não usa. Isso é feito no [arquivo de manifesto da aplicação](https://defold.com/manuals/app-manifest/), onde é possível remover componentes da engine de que você não precisa. Exemplos:

* Physics - Se seu jogo não usa física Box2D ou Bullet3D, é fortemente recomendado remover as engines de física
* LiveUpdate - Se seu jogo não usa LiveUpdate, ele pode ser removido
* Image loaded - Se seu jogo não carrega e decodifica imagens manualmente usando `image.load()`
* BasisU - Se seu jogo tem poucas texturas, compare o tamanho da build sem BasisU (removido via manifesto da aplicação) e sem compressão de textura com uma build com BasisU e texturas comprimidas. Para jogos com texturas limitadas, pode ser mais vantajoso reduzir o tamanho do binário e ignorar a compressão de texturas. Além disso, não usar o transcodificador pode reduzir a quantidade de memória necessária para executar o jogo.

## Otimizar o tamanho dos assets
Os maiores ganhos em otimizações de tamanho de assets geralmente vêm da redução do tamanho de sons e texturas.

### Otimizar sons
O Defold oferece suporte a estes formatos:
* .wav
* .ogg
* .opus

Arquivos de som devem usar amostras de 16 bits.
Nossos decodificadores de som ajustam as taxas de amostragem para cima ou para baixo conforme necessário para o dispositivo de som atual.

Sons mais curtos, como efeitos sonoros, costumam ser comprimidos com mais intensidade, enquanto arquivos de música têm menos compressão.
Nenhuma compressão é feita pelo Defold, então o desenvolvedor precisa lidar com isso especificamente para cada formato de áudio.

Você pode editar os sons em um software externo de edição de som (ou pela linha de comando usando, por exemplo, [ffmpeg](https://ffmpeg.org)) para reduzir a qualidade ou converter entre formatos. Considere também converter sons de estéreo para mono para reduzir ainda mais o tamanho do conteúdo.

### Otimizar texturas
Você tem várias opções quando se trata de otimizar as texturas usadas pelo seu jogo, mas a primeira coisa a fazer é verificar o tamanho das imagens adicionadas a um atlas ou usadas como tilesource. Você nunca deve usar imagens maiores do que o necessário no seu jogo. Importar imagens grandes e reduzi-las para o tamanho apropriado desperdiça memória de textura e deve ser evitado. Comece ajustando o tamanho das imagens em um software externo de edição de imagem para o tamanho real necessário no seu jogo. Para coisas como imagens de fundo, também pode ser aceitável usar uma imagem pequena e ampliá-la para o tamanho desejado. Depois que as imagens estiverem no tamanho correto e adicionadas a atlases ou usadas em tilesources, você também precisa considerar o tamanho dos próprios atlases. O tamanho máximo de atlas que pode ser usado varia entre plataformas e hardware gráfico.

::: sidenote
[Este post do fórum](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) sugere várias dicas sobre como redimensionar várias imagens usando scripts ou software de terceiros.
:::

* Tamanho máximo de textura em HTML5 informado ao [projeto Web3D Survey](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE)
* Tamanho máximo de textura no iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* O tamanho máximo de textura no Android varia bastante, mas em geral todos os dispositivos razoavelmente novos suportam pelo menos 4096x4096.

Se um atlas for grande demais, você precisa dividi-lo em vários atlases menores, usar atlases multipágina ou escalar o atlas inteiro usando um perfil de textura. O sistema de perfis de textura no Defold permite não só escalar atlases inteiros, mas também aplicar algoritmos de compressão para reduzir o tamanho do atlas em disco. Você pode [ler mais sobre perfis de textura no manual](/manuals/texture-profiles/). Se você não souber o que usar, tente começar com estas configurações como ponto de partida para personalizações posteriores:

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
Você pode ler mais sobre como otimizar e gerenciar texturas [neste post do fórum](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Otimizar fontes
O tamanho das suas fontes será menor se você especificar quais símbolos vai usar e definir isso em [Characters](/manuals/font/#properties) em vez de usar a caixa de seleção All Chars.

### Excluir conteúdo para download sob demanda
Outra forma de reduzir o tamanho inicial da aplicação é excluir partes do conteúdo do jogo do pacote da aplicação e baixá-las sob demanda. O Defold fornece um sistema chamado Live Update para excluir conteúdo para download sob demanda.

O conteúdo excluído pode ser qualquer coisa, desde níveis inteiros até personagens desbloqueáveis, skins, armas ou veículos. Se seu jogo tem muito conteúdo, organize o processo de carregamento para que a coleção bootstrap e a coleção do primeiro nível incluam apenas os recursos mínimos necessários para esse nível. Você faz isso usando proxies de coleção ou fábricas com a caixa de seleção "Exclude" habilitada. Divida os recursos de acordo com o progresso do jogador. Essa abordagem garante carregamento eficiente de recursos e mantém baixo o uso inicial de memória. Saiba mais no [manual do Live Update](/manuals/live-update/).

## Otimizações de tamanho específicas do Android
Builds Android devem oferecer suporte a arquiteturas de CPU de 32 bits e 64 bits. Ao [empacotar para Android](/manuals/android), você pode especificar quais arquiteturas de CPU incluir:

![Signing Android bundle](images/android/sign_bundle.png)

O Google Play oferece suporte a [vários APKs](https://developer.android.com/google/play/publishing/multiple-apks) por release de um jogo, o que significa que você pode reduzir o tamanho da aplicação gerando dois APKs, um para cada arquitetura de CPU, e enviando ambos para o Google Play.

Você também pode usar uma combinação de [APK Expansion Files](https://developer.android.com/google/play/expansion-files) e [conteúdo Live Update](/manuals/live-update) graças à [extensão APKX no Portal de Assets](https://defold.com/assets/apkx/).
