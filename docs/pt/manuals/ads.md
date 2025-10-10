---
title: Mostrando anúncios no Defold
brief: Mostrar vários tipos de anúncios é uma maneira comum de monetizar jogos para web e mobile. Este manual mostra várias maneiras de monetizar seu jogo usando anúncios.
---

# Anúncios

Os anúncios tornaram-se uma forma muito comum de monetizar jogos para web e mobile e se transformaram em uma indústria de bilhões de dólares. Como desenvolvedor, você é pago com base no número de pessoas que assistem aos anúncios que você exibe em seu jogo. Geralmente é tão simples quanto: mais visualizações equivalem a mais dinheiro, mas outros fatores também têm um impacto no quanto você é pago:

* A qualidade do anúncio - anúncios relevantes têm maior chance de obter interação e atenção dos seus jogadores.
* O formato do anúncio - anúncios de banner geralmente pagam menos, enquanto anúncios em tela cheia assistidos do início ao fim pagam mais.
* A rede de anúncios - o valor que você recebe varia de uma rede de anúncios para outra.

::: sidenote
CPM = Custo por mil. O valor que um anunciante paga por mil visualizações. O CPM varia entre as redes de anúncios e os formatos de anúncio.
:::

## Formatos

Existem muitos tipos diferentes de formatos de anúncio que podem ser usados em jogos. Alguns dos mais comuns são anúncios de banner, intersticiais e com recompensa:

### Anúncios de banner

Anúncios de banner são baseados em texto, imagem ou vídeo e cobrem uma parte relativamente pequena da tela, geralmente no topo ou na parte inferior. Os anúncios de banner são muito fáceis de implementar e se encaixam muito bem com jogos casuais de tela única, onde é fácil reservar uma área da tela para anúncios. Os anúncios de banner maximizam a exposição, pois os usuários jogam seu jogo sem interrupção.

### Anúncios intersticiais

Anúncios intersticiais são experiências grandes em tela cheia com animações e, às vezes, também conteúdo interativo de *rich media*. Os anúncios intersticiais são normalmente exibidos entre as fases ou sessões de jogo, pois é uma pausa natural na experiência do jogo. Os anúncios intersticiais normalmente geram menos visualizações do que os anúncios de banner, mas o custo (CPM) é muito maior do que o dos anúncios de banner, resultando em uma receita publicitária geral significativa.

### Anúncios com recompensa

Anúncios com recompensa (também conhecidos como anúncios com incentivos) são opcionais e, portanto, menos intrusivos do que muitas outras formas de anúncios. Os anúncios com recompensa são geralmente experiências em tela cheia, como os anúncios intersticiais. O usuário pode escolher uma recompensa em troca de visualizar o anúncio - por exemplo, *loot*, vidas, tempo ou alguma outra moeda ou benefício no jogo. Os anúncios com recompensa geralmente têm o custo mais alto (CPM), mas o número de visualizações está diretamente relacionado às taxas de aceitação do usuário. Os anúncios com recompensa só terão um ótimo desempenho se as recompensas forem valiosas o suficiente e oferecidas no momento certo.


## Redes de anúncios

O [Portal de Assets da Defold](/tags/stars/ads/) contém vários assets que se integram com provedores de anúncios:

* [AdMob](https://defold.com/assets/admob-defold/) - Mostra anúncios usando a rede Google AdMob.
* [Enhance](https://defold.com/assets/enhance/) - Suporta uma série de redes de anúncios diferentes. Requer uma etapa adicional de pós-build.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Mostra anúncios no seu Facebook Instant Game.
* [IronSource](https://defold.com/assets/ironsource/) - Mostra anúncios usando a rede de anúncios IronSource.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Mostra anúncios usando a rede Unity Ads.


# Como integrar anúncios no seu jogo

Quando você decidir sobre uma rede de anúncios para integrar ao seu jogo, você precisa seguir as instruções de instalação e uso para aquele *asset* específico. O que você normalmente faz é primeiro adicionar a extensão como uma [dependência de projeto](/manuals/libraries/#setting-up-library-dependencies). Depois de adicionar o asset ao seu projeto, você pode prosseguir com a integração e chamar as funções específicas do asset para carregar e exibir anúncios.


# Combinando anúncios e compras dentro do aplicativo

É bastante comum em jogos mobile oferecer uma [compra dentro do aplicativo](/manuals/iap) para se livrar dos anúncios permanentemente.


## Saiba mais

Existem muitos recursos online para aprender quando se trata de otimizar a receita de anúncios:

* Google AdMob [Monetize jogos mobile com anúncios](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Formatos de anúncio populares e como usá-los](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Veiculação de anúncios em jogos: 10 dicas de especialistas](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
