La proprietà *Blend Mode* definisce come la grafica del componente viene fusa con la grafica sottostante. Queste sono le modalità di fusione disponibili e il modo in cui vengono calcolate:

Alpha
: Fusione normale: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Schiarisce lo sfondo con i valori di colore dei pixel corrispondenti del componente: `src.rgb + dst.rgb`

Multiply
: Scurisce lo sfondo con i valori dei pixel corrispondenti del componente: `src.rgb * dst.rgb`

Screen
: Opposto di Multiply. Schiarisce lo sfondo e i valori dei pixel corrispondenti del componente: `src.rgb - dst.rgb * dst.rgb`
