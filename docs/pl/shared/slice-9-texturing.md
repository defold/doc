## Teksturowanie Slice-9

Węzły GUI typu box i komponenty Sprite czasem zawierają elementy, których rozmiar zależy od kontekstu: panele i okna dialogowe, które trzeba dopasować do zawartości, albo pasek zdrowia, który trzeba przeskalować, aby pokazać pozostałe zdrowie przeciwnika. Gdy zastosujesz teksturowanie do przeskalowanego węzła lub sprite'a, może to powodować problemy wizualne.

Zwykle silnik skaluje teksturę tak, aby pasowała do prostokątnych granic, ale zdefiniowanie brzegowych obszarów slice-9 pozwala ograniczyć, które części tekstury mają być skalowane:

![Skalowanie GUI](../shared/images/gui_slice9_scaling.png)

Węzeł box *Slice9* składa się z 4 liczb określających liczbę pikseli dla lewego, górnego, prawego i dolnego marginesu, które nie mają być skalowane w zwykły sposób:

![Właściwości Slice 9](../shared/images/gui_slice9_properties.png)

Marginesy ustawia się zgodnie z ruchem wskazówek zegara, zaczynając od lewej krawędzi:

![Sekcje Slice 9](../shared/images/gui_slice9.png)

- Narożne segmenty nigdy nie są skalowane.
- Segmenty krawędzi są skalowane tylko wzdłuż jednej osi. Lewy i prawy segment krawędzi są skalowane pionowo. Górny i dolny segment krawędzi są skalowane poziomo.
- Centralny obszar tekstury jest w razie potrzeby skalowany zarówno w poziomie, jak i w pionie.

Opisane powyżej skalowanie tekstury *Slice9* jest stosowane tylko wtedy, gdy zmieniasz rozmiar węzła box albo komponentu Sprite:

![Rozmiar węzła GUI](../shared/images/gui_slice9_size.png)

![Rozmiar Sprite'a](../shared/images/sprite_slice9_size.png)

::: important
Jeśli zmienisz parametr `scale` węzła box lub Sprite'a (albo obiektu gry), sam węzeł lub Sprite i tekstura zostaną przeskalowane bez zastosowania parametrów *Slice9*.
:::

::: important
Podczas używania teksturowania slice-9 w Sprite'ach właściwość [Sprite Trim Mode](https://defold.com/manuals/atlas/#image-properties) obrazu musi być ustawiona na `Off`.
:::


### Mipmapy i slice-9
Ze względu na sposób działania mipmapowania w rendererze skalowanie fragmentów tekstury może czasem powodować artefakty. Dzieje się tak, gdy zmniejszasz fragmenty poniżej oryginalnego rozmiaru tekstury. Renderer wybiera wtedy dla fragmentu mipmapę o niższej rozdzielczości, co skutkuje artefaktami wizualnymi.

![Mipmapy Slice 9](../shared/images/gui_slice9_mipmap.png)

Aby uniknąć tego problemu, upewnij się, że fragmenty tekstury, które będą skalowane, są na tyle małe, by nigdy nie były zmniejszane, a jedynie powiększane.
