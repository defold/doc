---
title: Adaptar gráficos a distintos tamaños de pantalla
brief: Este manual explica cómo adaptar tu juego y sus gráficos a distintos tamaños de pantalla.
---

# Introducción {#introduction}

Hay varias cosas que debes considerar al adaptar tu juego y sus gráficos a distintos tamaños de pantalla:

* ¿Es un juego retro con gráficos pixel-perfect de baja resolución o un juego moderno con gráficos de calidad HD?
* ¿Cómo debería comportarse el juego al jugarlo en pantalla completa en distintos tamaños de pantalla?
  * ¿El jugador debería ver más contenido del juego en una pantalla de alta resolución o los gráficos deberían hacer zoom de forma adaptativa para mostrar siempre el mismo contenido?
* ¿Cómo debería manejar el juego relaciones de aspecto distintas a la que configuraste en *game.project*?
  * ¿El jugador debería ver más contenido del juego? ¿O tal vez debería haber barras negras? ¿O tal vez elementos GUI redimensionados?
* ¿Qué tipo de menús y componentes GUI en pantalla necesitas y cómo deberían adaptarse a distintos tamaños y orientaciones de pantalla?
  * ¿Los menús y otros componentes GUI deberían cambiar de layout cuando cambia la orientación o deberían conservar el mismo layout sin importar la orientación?

Este manual abordará algunos de estos puntos y sugerirá buenas prácticas.


## Cómo cambiar la forma en que se renderiza tu contenido {#how-to-change-how-your-content-is-rendered}

El script de render de Defold te da control total sobre todo el pipeline de renderizado. El script de render decide el orden, además de qué cosas dibujar y cómo dibujarlas. El comportamiento predeterminado del script de render es dibujar siempre la misma área de píxeles, definida por el ancho y la altura en el archivo *game.project*, sin importar si se redimensiona la ventana o si la resolución real de la pantalla no coincide. Esto hará que el contenido se estire si cambia la relación de aspecto y que se acerque o aleje si cambia el tamaño de la ventana. En algunos juegos esto puede ser aceptable, pero es más probable que quieras mostrar más o menos contenido del juego si la resolución de pantalla o la relación de aspecto es distinta, o al menos asegurarte de aplicar zoom al contenido sin cambiar la relación de aspecto. El comportamiento predeterminado de estiramiento se puede cambiar fácilmente y puedes leer más sobre cómo hacerlo en el [manual de Render](https://www.defold.com/manuals/render/#default-view-projection).


## Gráficos retro/8-bit {#retro8-bit-graphics}

Los gráficos retro/8-bit suelen referirse a juegos que emulan el estilo gráfico de consolas o computadoras antiguas, con baja resolución y una paleta de colores limitada. Por ejemplo, Nintendo Entertainment System (NES) tenía una resolución de pantalla de 256x240, Commodore 64 tenía 320x200 y Gameboy tenía 160x144; todas son apenas una fracción del tamaño de las pantallas modernas. Para que los juegos que emulan este estilo gráfico y esta resolución de pantalla sean jugables en una pantalla moderna de alta resolución, los gráficos deben escalarse o acercarse varias veces. Una forma sencilla de hacerlo es dibujar todos tus gráficos con la baja resolución y el estilo que quieres emular, y hacer zoom sobre los gráficos cuando se renderizan. Esto se puede lograr fácilmente en Defold usando el script de render y [Fixed Projection](/manuals/render/#fixed-projection) configurado con un valor de zoom adecuado.

Tomemos este tileset y personaje del jugador ([fuente](https://ansimuz.itch.io/grotto-escape-game-art-pack)) y usémoslos para un juego retro 8-bit con una resolución de 320x200:

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

Configurar 320x200 en el archivo *game.project* e iniciar el juego se vería así:

![](images/screen_size/retro-original_320x200.png)

¡La ventana es absolutamente diminuta en una pantalla moderna de alta resolución! Aumentar cuatro veces el tamaño de la ventana hasta 1280x800 la hace más adecuada para una pantalla moderna:

![](images/screen_size/retro-original_1280x800.png)

Ahora que el tamaño de la ventana es más razonable, también necesitamos hacer algo con los gráficos. Son tan pequeños que es muy difícil ver qué ocurre en el juego. Podemos usar el script de render para definir una proyección fija y con zoom:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
Se puede lograr el mismo resultado adjuntando un [componente Camera](/manuals/camera/) a un objeto de juego, marcando *Orthographic Projection* y definiendo *Orthographic Zoom* en 4.0:

![](images/screen_size/retro-camera_zoom.png)
:::

Esto dará el siguiente resultado:

![](images/screen_size/retro-zoomed_1280x800.png)

Esto es mejor. Tanto la ventana como los gráficos tienen un buen tamaño, pero si miramos con más detalle hay un problema evidente:

![](images/screen_size/retro-zoomed_linear.png)

¡Los gráficos se ven borrosos! Esto se debe a la forma en que los gráficos ampliados se muestrean desde la textura al ser renderizados por la GPU. La configuración predeterminada en el archivo *game.project*, en la sección *Graphics*, es *linear*:

![](images/screen_size/retro-settings_linear.png)

Cambiar esto a *nearest* dará el resultado que buscamos:

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

Ahora tenemos gráficos nítidos y *pixel-perfect* para nuestro juego retro. Hay aún más cosas que considerar, como desactivar subpíxeles para sprites en *game.project*:

![](images/screen_size/retro-subpixels.png)

Cuando la opción *Subpixels* está desactivada, los sprites nunca se renderizarán en medios píxeles y, en su lugar, siempre se ajustarán al píxel completo más cercano.

## Gráficos de alta resolución {#high-resolution-graphics}

Cuando trabajamos con gráficos de alta resolución, necesitamos plantear la configuración del proyecto y del contenido de una forma distinta a la usada para gráficos retro/8-bit. Con gráficos bitmap debes crear tu contenido de tal manera que se vea bien en una pantalla de alta resolución cuando se muestre a escala 1:1.

Al igual que con los gráficos retro/8-bit, necesitas cambiar el script de render. En este caso quieres que los gráficos escalen con el tamaño de la pantalla mientras se conserva la relación de aspecto original:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

Esto hará que la pantalla se redimensione para mostrar siempre la misma cantidad de contenido que se especifica en el archivo *game.project*, posiblemente con contenido adicional mostrado arriba y abajo o a los lados, dependiendo de si la relación de aspecto es diferente.

Debes configurar el ancho y la altura en el archivo *game.project* con un tamaño que te permita mostrar el contenido de tu juego sin escalar.

### Configuración High DPI y pantallas retina {#high-dpi-setting-and-retina-screens}

Si también quieres dar soporte a pantallas retina de alta resolución, puedes activarlo en el archivo *game.project*, en la sección Display:

![](images/screen_size/highdpi-enabled.png)

High DPI permite que el juego use la densidad de píxeles de la pantalla para su resolución de renderizado. Los ajustes *Width* y *Height* siguen definiendo la resolución lógica del proyecto, mientras que la escala de renderizado depende de la plataforma y la pantalla. Por ejemplo, con una escala de 2, las imágenes importadas al doble de su tamaño previsto y dibujadas a 0.5x pueden conservar sus detalles en una pantalla de alta densidad.

En HTML5, la escala parte de la relación de píxeles del dispositivo que proporciona el navegador. `html5.min_pixel_ratio` y `html5.max_pixel_ratio` permiten limitarla cuando `display.high_dpi` está activado. Cada límite tiene el valor predeterminado `0` (desactivado), y se admiten valores fraccionarios, incluso inferiores a `1`. Estos límites cambian la resolución de renderizado del canvas sin alterar su tamaño de visualización CSS. Con High DPI desactivado, la relación permanece en `1`. Consulta [Límites de la relación de píxeles](/manuals/html5/#pixel-ratio-limits) para ver un ejemplo que limita el renderizado en pantallas de alta densidad.


## Crear una GUI adaptativa {#creating-an-adaptive-gui}

El sistema para crear componentes GUI se basa en una serie de bloques de construcción básicos, o [nodos](/manuals/gui/#node-types), y aunque puede parecer demasiado simple, se puede usar para crear desde botones hasta menús y popups complejos. Las GUIs que crees pueden configurarse para adaptarse automáticamente a cambios de tamaño y orientación de pantalla. Por ejemplo, puedes mantener *nodos* anclados a la parte superior, inferior o a los lados de la pantalla, y los *nodos* pueden conservar su tamaño o estirarse. La relación entre nodos, así como su tamaño y apariencia, también puede configurarse para cambiar cuando cambia el tamaño o la orientación de la pantalla.

### Propiedades de *nodo* {#node-properties}

Cada *nodo* de una GUI tiene un punto de pivote, un anclaje horizontal y vertical, además de un modo de ajuste.

* El punto de pivote define el punto central de un nodo.
* El modo de anclaje controla cómo se altera la posición vertical y horizontal del nodo cuando los límites de la escena, o los límites del nodo padre, se estiran para ajustarse al tamaño físico de la pantalla.
* La configuración del modo de ajuste controla qué le sucede a un nodo cuando los límites de la escena, o los límites del nodo padre, se ajustan para encajar en el tamaño físico de la pantalla.

Puedes aprender más sobre estas propiedades [en el manual de GUI](/manuals/gui/#node-properties).

### Layouts

Defold soporta GUIs que se adaptan automáticamente a cambios de orientación de pantalla en dispositivos móviles. Al usar esta funcionalidad puedes diseñar una GUI que se adapte a la orientación y la relación de aspecto de un rango de tamaños de pantalla. También es posible crear layouts que coincidan con modelos de dispositivo concretos. Puedes aprender más sobre este sistema en el [manual de GUI Layouts](/manuals/gui-layouts/)


## Probar distintos tamaños de pantalla {#testing-different-screen-sizes}

El menú *Debug* contiene una opción para simular la resolución de un modelo de dispositivo concreto o una resolución personalizada. Mientras la aplicación está en ejecución, puedes seleccionar <kbd>Debug->Simulate Resolution</kbd> y elegir uno de los modelos de dispositivo de la lista. La ventana de la aplicación en ejecución se redimensionará y podrás ver cómo se ve tu juego en una resolución distinta o con una relación de aspecto distinta.

![](images/screen_size/simulate-resolution.png)
