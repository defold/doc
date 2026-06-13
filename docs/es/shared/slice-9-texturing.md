## Texturizado slice-9

Los nodos caja GUI (box-nodes) y los componentes Sprite a veces incluyen elementos cuyo tamaño depende del contexto: paneles y diálogos que deben redimensionarse para ajustarse al contenido, o una barra de salud que debe redimensionarse para mostrar la salud restante de un enemigo. Esto puede causar problemas visuales cuando aplicas texturizado al nodo o sprite redimensionado.

Normalmente, el motor escala la textura para ajustarla a los límites rectangulares, pero al definir áreas de borde slice-9 es posible limitar qué partes de la textura deben escalarse:

![Escalado GUI](../shared/images/gui_slice9_scaling.png)

La propiedad *Slice9* del nodo caja consta de 4 números que especifican la cantidad de píxeles de los márgenes izquierdo, superior, derecho e inferior que no deben escalarse de la forma normal:

![Propiedades Slice 9](../shared/images/gui_slice9_properties.png)

Los márgenes se establecen en sentido horario, comenzando por el borde izquierdo:

![Secciones Slice 9](../shared/images/gui_slice9.png)

- Los segmentos de las esquinas nunca se escalan.
- Los segmentos de los bordes se escalan a lo largo de un solo eje. Los segmentos de los bordes izquierdo y derecho se escalan verticalmente. Los segmentos de los bordes superior e inferior se escalan horizontalmente.
- El área central de la textura se escala horizontal y verticalmente según sea necesario.

El escalado de textura *Slice9* descrito arriba solo se aplica cuando cambias el tamaño del nodo caja o del sprite:

![Tamaño de nodo caja GUI](../shared/images/gui_slice9_size.png)

![Tamaño de Sprite](../shared/images/sprite_slice9_size.png)

::: important
Si cambias el parámetro de escala del nodo caja o sprite (o del objeto de juego), el nodo o sprite y la textura se escalan sin aplicar los parámetros *Slice9*.
:::

::: important
Al usar texturizado slice-9 en Sprites, el [Sprite Trim Mode de la imagen](https://defold.com/manuals/atlas/#image-properties) debe estar configurado en Off.
:::


### Mipmaps y slice-9

Debido a la forma en que funciona mipmapping en el renderizador, el escalado de segmentos de textura a veces puede mostrar artefactos. Esto ocurre cuando _se reduce la escala_ de segmentos por debajo del tamaño original de la textura. Entonces el renderizador selecciona un mipmap de menor resolución para el segmento, lo que produce artefactos visuales.

![Mipmapping Slice 9](../shared/images/gui_slice9_mipmap.png)

Para evitar este problema, asegúrate de que los segmentos de la textura que se escalarán sean lo suficientemente pequeños como para que nunca se escalen hacia abajo, solo hacia arriba.
