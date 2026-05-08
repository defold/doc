Właściwość *Blend Mode* określa, w jaki sposób grafika komponentu ma być mieszana z grafiką znajdującą się za nią. Poniżej przedstawiono dostępne tryby mieszania i sposób ich obliczania:

Alpha
: Normalne blendowanie: `src.a * src.rgb + (1 - src.a) * dst.rgb`

Add
: Rozjaśnia tło wartościami kolorów odpowiednich pikseli komponentu: `src.rgb + dst.rgb`

Multiply
: Przyciemnia tło wartościami kolorów odpowiednich pikseli komponentu: `src.rgb * dst.rgb`

Screen
: Odwrotność Multiply. Rozjaśnia tło i wartości kolorów odpowiednich pikseli komponentu: `src.rgb - dst.rgb * dst.rgb`
