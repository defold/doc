La propriété *Blend Mode* définit la façon dont les éléments graphiques du composant (component) doivent être fusionnés avec ceux qui se trouvent derrière lui. Voici les modes de fusion disponibles et leur calcul :

Alpha
: Fusion normale : `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Éclaircit l'arrière-plan avec les valeurs de couleur des pixels correspondants du composant : `src.rgb + dst.rgb`

Multiply
: Assombrit l'arrière-plan avec les valeurs des pixels correspondants du composant : `src.rgb * dst.rgb`

Screen
: Inverse de Multiply. Éclaircit l'arrière-plan et les valeurs des pixels correspondants du composant : `src.rgb - dst.rgb * dst.rgb`
