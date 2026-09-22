Die Eigenschaft *Blend Mode* legt fest, wie die Grafik einer Komponente (component) mit der dahinterliegenden Grafik gemischt wird. Dies sind die verfügbaren Mischmodi und ihre Berechnungen:

Alpha
: Normale Mischung: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Hellt den Hintergrund mit den Farbwerten der entsprechenden Pixel der Komponente auf: `src.rgb + dst.rgb`

Multiply
: Dunkelt den Hintergrund mit den Werten der entsprechenden Pixel der Komponente ab: `src.rgb * dst.rgb`

Screen
: Gegenteil von Multiply. Erhöht die Helligkeit des Hintergrunds und die Werte der entsprechenden Pixel der Komponente: `src.rgb - dst.rgb * dst.rgb`
