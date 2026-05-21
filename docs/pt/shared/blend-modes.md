A propriedade *Blend Mode* define como os gráficos do componente devem ser mesclados com os gráficos atrás dele. Estes são os modos de mesclagem disponíveis e como eles são calculados:

Alpha
:: Mesclagem normal: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
:: Clareia o fundo com os valores de cor dos pixels correspondentes do componente: `src.rgb + dst.rgb`

Multiply
:: Escurece o fundo com os valores dos pixels correspondentes do componente: `src.rgb * dst.rgb`

Screen
:: O oposto de Multiply. Clareia o fundo e os valores dos pixels correspondentes do componente: `src.rgb - dst.rgb * dst.rgb`
