## Teksturowanie Slice-9

Węzły box GUI i komponenty Sprite czasami zawierają elementy zależne od kontekstu ich rozmiaru: panele i okna dialogowe, które trzeba przeskalować, aby dopasować je do zawartości, albo pasek życia, który trzeba przeskalować, aby pokazać pozostałą wartość zdrowia przeciwnika. Takie elementy mogą powodować problemy wizualne, gdy zastosujesz teksturowanie do przeskalowanego węzła lub komponentu Sprite.

Zwykle silnik skaluje teksturę tak, aby pasowała do prostokątnych granic, ale zdefiniowanie obszarów krawędzi Slice-9 pozwala ograniczyć, które części tekstury mają być skalowane:

![Skalowanie GUI](../shared/images/gui_slice9_scaling.png)

Węzeł box *Slice9* składa się z 4 liczb określających liczbę pikseli dla lewego, górnego, prawego i dolnego marginesu, które nie powinny być zwykle skalowane:

![Właściwości Slice 9](../shared/images/gui_slice9_properties.png)

Marginesy ustawia się zgodnie z ruchem wskazówek zegara, zaczynając od lewej krawędzi:

![Sekcje Slice 9](../shared/images/gui_slice9.png)

- Segmenty narożne nigdy nie są skalowane.
- Segmenty krawędzi są skalowane tylko wzdłuż jednej osi. Lewy i prawy segment krawędzi są skalowane pionowo. Górny i dolny segment krawędzi są skalowane poziomo.
- Centralny obszar tekstury jest skalowany w poziomie i pionie w razie potrzeby.

Opisane powyżej skalowanie tekstury *Slice9* jest stosowane tylko wtedy, gdy zmieniasz rozmiar węzła box albo komponentu Sprite:

![Rozmiar węzła GUI](../shared/images/gui_slice9_size.png)

![Rozmiar Sprite'a](../shared/images/sprite_slice9_size.png)

::: important
Jeśli zmienisz parametr scale węzła box lub komponentu Sprite albo obiektu gry, sam węzeł lub komponent Sprite i tekstura zostaną przeskalowane bez zastosowania parametrów *Slice9*.
:::

::: important
Podczas używania teksturowania Slice-9 w Sprite'ach właściwość [Sprite Trim Mode](https://defold.com/manuals/atlas/#image-properties) obrazu musi być ustawiona na Off.
:::


### Mipmapy i Slice-9
Ze względu na sposób działania mipmapowania w rendererze skalowanie fragmentów tekstury może czasem powodować artefakty. Dzieje się tak, gdy zmniejszasz fragmenty poniżej oryginalnego rozmiaru tekstury. Renderer wybiera wtedy dla segmentu mipmapę o niższej rozdzielczości, co skutkuje artefaktami wizualnymi.

![Mipmapy Slice 9](../shared/images/gui_slice9_mipmap.png)

Aby uniknąć tego problemu, upewnij się, że segmenty tekstury, które będą skalowane, są na tyle małe, by nigdy nie były zmniejszane, a jedynie powiększane.
