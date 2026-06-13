---
title: Manual de clipping de GUI
brief: Este manual describe cómo crear nodos GUI que enmascaran otros nodos mediante clipping con stencil.
---

# Clipping

Los nodos GUI se pueden usar como nodos de *clipping*: máscaras que controlan cómo se renderizan otros nodos. Este manual explica cómo funciona esta funcionalidad.

## Crear un nodo de clipping

Los nodos de tipo Box, Text y Pie se pueden usar para clipping. Para crear un nodo de clipping, agrega un nodo en tu GUI y luego configura sus propiedades según corresponda:

Clipping Mode
: El modo usado para el clipping.
  - `None` renderiza el nodo sin aplicar clipping.
  - `Stencil` hace que el nodo escriba en la máscara stencil actual.

Clipping Visible
: Márcalo para renderizar el contenido del nodo.

Clipping Inverted
: Márcalo para escribir en la máscara la inversión de la forma del nodo.

Luego agrega como hijos del nodo de clipping los nodos que quieres que se recorten.

![Crear clipping](images/gui-clipping/create.png)

## Máscara stencil

El clipping funciona haciendo que los nodos escriban en un *stencil buffer*. Este buffer contiene máscaras de clipping: información que indica a la tarjeta gráfica si un pixel debe renderizarse o no.

- Un nodo sin un nodo clipper padre, pero con el modo de clipping definido como `Stencil`, escribirá su forma (o su forma inversa) en una nueva máscara de clipping almacenada en el stencil buffer.
- Si un nodo de clipping tiene un nodo clipper padre, recortará la máscara de clipping del padre. Un nodo hijo de clipping nunca puede _extender_ la máscara de clipping actual; solo puede recortarla más.
- Los nodos que no son nodos clipper y son hijos de nodos clipper se renderizarán con la máscara de clipping creada por la jerarquía de padres.

![Jerarquía de clipping](images/gui-clipping/setup.png)

Aquí, tres nodos están configurados en una jerarquía:

- Los nodos con forma de hexágono y cuadrado son ambos nodos clipper de stencil.
- El hexágono crea una nueva máscara de clipping; el cuadrado la recorta más.
- El nodo circular es un nodo Pie normal, así que se renderizará con la máscara de clipping creada por sus nodos clipper superiores.

Para esta jerarquía son posibles cuatro combinaciones de nodos clipper normales e invertidos. El área verde marca la parte del círculo que se renderiza. El resto queda enmascarado:

![Máscaras stencil](images/gui-clipping/modes.png)

## Limitaciones de stencil

- El número total de nodos clipper de stencil no puede exceder 256.
- La profundidad máxima de anidamiento de nodos hijos _stencil_ es de 8 niveles. (Solo cuentan los nodos con clipping de stencil.)
- El número máximo de nodos stencil del mismo nivel es 127. Por cada nivel que se baja en una jerarquía stencil, el límite máximo se reduce a la mitad.
- Los nodos invertidos tienen un costo mayor. Hay un límite de 8 nodos de clipping invertidos y cada uno reducirá a la mitad la cantidad máxima de nodos de clipping no invertidos.
- Los nodos stencil renderizan una máscara stencil a partir de la _geometría_ del nodo (no de la textura). Es posible invertir la máscara configurando la propiedad *Inverted clipper*.


## Capas

Las capas se pueden usar para controlar el orden de renderizado (y el batching) de los nodos. Al usar capas y nodos de clipping, se reemplaza el orden habitual de las capas. El orden de capas siempre tiene prioridad sobre el orden de clipping: si las asignaciones de capas se combinan con nodos de clipping, el clipping podría ocurrir fuera de orden si un nodo padre con clipping activado pertenece a una capa superior a la de sus hijos. Los hijos sin una capa asignada seguirán respetando la jerarquía y, por lo tanto, se dibujarán y se recortarán después del padre.

::: sidenote
Un nodo de clipping y su jerarquía se dibujan primero si el nodo tiene una capa asignada, y en el orden normal si no hay ninguna capa asignada.
:::

![Capas y clipping](images/gui-clipping/layers.png)

En este ejemplo, ambos nodos clipper, "`Donut BG`" y "`BG`", usan la misma capa 1. El orden de renderizado entre ellos seguirá el mismo orden de la jerarquía, donde "`Donut BG`" se renderiza antes de "`BG`". Sin embargo, el nodo hijo "`Donut Shadow`" está asignado a la capa 2, que tiene un orden de capa más alto y por lo tanto se renderizará después de ambos nodos de clipping. En este caso, el orden de renderizado será:

- `Donut BG`
- `BG`
- `BG Frame`
- `Donut Shadow`

Aquí puedes ver que el objeto "`Donut Shadow`" será recortado por ambos nodos de clipping debido a las capas, aunque solo es hijo de uno de ellos.
