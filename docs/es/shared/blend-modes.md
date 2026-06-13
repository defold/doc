La propiedad *Blend Mode* define cómo deben mezclarse los gráficos del componente con los gráficos que hay detrás. Estos son los modos de mezcla disponibles y cómo se calculan:

Alpha
: Mezcla normal: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Aclara el fondo con los valores de color de los píxeles correspondientes del componente: `src.rgb + dst.rgb`

Multiply
: Oscurece el fondo con los valores de los píxeles correspondientes del componente: `src.rgb * dst.rgb`

Screen
: Lo opuesto a Multiply. Aclara el fondo y los valores de los píxeles correspondientes del componente: `src.rgb - dst.rgb * dst.rgb`
