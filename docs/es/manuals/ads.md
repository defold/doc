---
title: Mostrar anuncios en Defold
brief: Mostrar varios tipos de anuncios es una forma común de monetizar juegos web y móviles. Este manual muestra varias formas de monetizar tu juego usando anuncios.
---

# Anuncios

Los anuncios se han convertido en una forma muy común de monetizar juegos web y móviles, y en una industria multimillonaria. Como desarrollador, recibes pagos en función del número de personas que ven los anuncios que muestras en tu juego. Por lo general, es tan simple como que más espectadores equivalen a más dinero, pero otros factores también influyen en cuánto recibes:

* La calidad del anuncio - los anuncios relevantes tienen más probabilidades de generar interacción y atención de tus jugadores.
* El formato del anuncio - los anuncios de banner suelen pagar menos, mientras que los anuncios de pantalla completa vistos de principio a fin pagan más.
* La red publicitaria - la cantidad que recibes varía de una red publicitaria a otra.

::: sidenote
CPM = Cost per mille (costo por mil). Es la cantidad que paga un anunciante por cada mil vistas. El CPM varía entre redes publicitarias y formatos de anuncio.
:::

## Formatos

Hay muchos tipos diferentes de formatos de anuncio que pueden usarse en juegos. Algunos de los más comunes son los anuncios de banner, intersticiales y recompensados:

### Anuncios de banner

Los anuncios de banner se basan en texto, imagen o video, y cubren una parte relativamente pequeña de la pantalla, por lo general en la parte superior o inferior. Los anuncios de banner son muy fáciles de implementar y encajan muy bien con juegos casuales de una sola pantalla, donde es fácil reservar un área de la pantalla para publicidad. Los anuncios de banner maximizan la exposición mientras los usuarios juegan sin interrupciones.

### Anuncios intersticiales

Los anuncios intersticiales son grandes experiencias de pantalla completa con animaciones y, a veces, también *contenido multimedia enriquecido* e interactivo. Los anuncios intersticiales suelen mostrarse entre niveles o sesiones de juego, ya que es una pausa natural en la experiencia de juego. Los anuncios intersticiales suelen generar menos vistas que los anuncios de banner, pero el costo (CPM) es mucho más alto que el de los anuncios de banner, lo que resulta en ingresos publicitarios totales significativos.

### Anuncios recompensados

Los anuncios recompensados (también conocidos como anuncios incentivados) son opcionales y, por lo tanto, menos intrusivos que muchas otras formas de anuncios. Los anuncios recompensados suelen ser experiencias de pantalla completa, como los anuncios intersticiales. El usuario puede elegir una recompensa a cambio de ver el anuncio, por ejemplo *botín*, monedas, vidas, tiempo o alguna otra moneda o beneficio dentro del juego. Los anuncios recompensados suelen tener el costo (CPM) más alto, pero el número de vistas está directamente relacionado con las tasas de aceptación voluntaria de los usuarios. Los anuncios recompensados solo tendrán un gran rendimiento si las recompensas son lo bastante valiosas y se ofrecen en el momento adecuado.


## Redes publicitarias

El [Defold Asset Portal](/tags/stars/ads/) contiene varios assets que se integran con proveedores de anuncios:

* [AdMob](https://defold.com/assets/admob-defold/) - Muestra anuncios usando la red Google AdMob.
* [Enhance](https://defold.com/assets/enhance/) - Da soporte a varias redes publicitarias diferentes. Requiere un paso adicional posterior a la build.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Muestra anuncios en tu Facebook Instant Game.
* [IronSource](https://defold.com/assets/ironsource/) - Muestra anuncios usando la red publicitaria IronSource.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Muestra anuncios usando la red Unity Ads.


# Cómo integrar anuncios en tu juego

Cuando hayas elegido una red publicitaria para integrar en tu juego, debes seguir las instrucciones de instalación y uso de ese *asset* específico. Lo normal es añadir primero la extensión como una [dependencia del proyecto](/manuals/libraries/#setting-up-library-dependencies). Una vez que hayas añadido el asset a tu proyecto, puedes continuar con la integración y llamar a las funciones específicas del asset para cargar y mostrar anuncios.


# Combinar anuncios y compras in-app

Es bastante común en los juegos móviles ofrecer una [compra in-app](/manuals/iap) para eliminar los anuncios de forma permanente.


## Más información

Hay muchos recursos en línea de los que aprender cuando se trata de optimizar los ingresos por anuncios:

* Google AdMob [Monetize mobile games with ads](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Popular ad formats and how to use them](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Ad serving in games: 10 expert tips](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
