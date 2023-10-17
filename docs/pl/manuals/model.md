---
title: Modele 3D w Defoldzie
brief: Ta instrukcja opisuje, jak wprowadzać modele 3D, szkielety i animacje do gry.
---

# Modele 3D

Defold to od podstaw silnik 3D. Nawet gdy pracujesz tylko z materiałami 2D, całe renderowanie odbywa się w 3D, ale jest rzutowane ortograficznie na ekran. Defold pozwala na wykorzystywanie pełnej zawartości 3D poprzez dodawanie aktywów 3D lub Modeli do swoich kolekcji. Możesz budować gry wyłącznie w 3D, korzystając tylko z aktywów 3D, lub łączyć zawartość 3D i 2D, jak sobie życzysz. Komponent typu Model jest jednym z komponentów do obsługi elementów trójwymiarowych.

## Tworzenie komponentu Modelu

Komponenty Modelu tworzy się tak samo jak każdy inny komponent obiektu gry. Możesz to zrobić na dwa sposoby:

- Utwórz plik Modelu, klikając prawym przyciskiem myszy w przeglądarki Aktywów i wybierając opcję <kbd>New... ▸ Model</kbd>.
- Utwórz komponent osadzony bezpośrednio w obiekcie gry, klikając prawym przyciskiem myszy w obiekcie gry w widoku Konspekt i wybierając <kbd>Add Component ▸ Model</kbd>.

![Model w obiekcie gry](images/model/model.png)

Po utworzeniu siatki musisz określić szereg właściwości (properties):

### Właściwości Modeli

Oprócz właściwości *Id*, *Position* i *Rotation* istnieją następujące właściwości specyficzne dla komponentu typu Mesh:

*Mesh*
: Siatka - ta właściwość powinna odnosić się do pliku glTF *.gltf* lub Collada *.dae*, który zawiera siatkę trójwymiarową, którą chcesz użyć. Jeśli plik zawiera wiele siatek, zostanie odczytana tylko pierwsza.

*Material*
: Materiał - ustaw tę właściwość na materiał, który utworzyłeś i nadaje się do tekstur obiektu 3D. Dostępny jest wbudowany plik *model.material*, który można użyć jako punkt wyjścia.

*Texture*
: Tekstura - ta właściwość powinna wskazywać na plik obrazu tekstury, który chcesz zastosować do obiektu.

*Skeleton*
: Szkielet - ta właściwość powinna odnosić się do pliku glTF *.gltf* lub Collada *.dae*, który zawiera szkielet do użycia w animacji. Należy zauważyć, że Defold wymaga jednego korzenia hierarchii kostnej (root bone).

*Animations*
: Animacje - ustaw to na Plik zestawu animacji (*Animation Set*), który zawiera animacje, które chcesz użyć na modelu.

*Default Animation*
: Domyślna Animacja - to animacja (z zestawu animacji), która będzie najpierw automatycznie odtwarzana na modelu.

## Manipulacja w Edytorze

Mając komponent Modelu, możesz swobodnie edytować i manipulować komponentem lub otaczającym obiektem gry za pomocą zwykłych narzędzi Edytora Sceny (*Scene Editor*), aby dostosować model do swoich potrzeb.

![Wiggler w grze](images/model/ingame.png){srcset="images/model/ingame@2x.png 2x"}

## Manipulacja w czasie rzeczywistym

Możesz manipulować modelami w czasie działania programu za pomocą różnych funkcji i właściwości (zobacz [dokumentację API](/ref/model/)) w celu uzyskania informacji na temat użycia).

### Animacja w czasie rzeczywistym

Defold oferuje wsparcie dla kontroli animacji w czasie działania programu. Więcej informacji można znaleźć w [instrukcji dotyczącej animacji modelu](/manuals/model-animation):

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

Kursor odtwarzania animacji można animować ręcznie lub za pomocą systemu animacji właściwości:

```lua
-- ustaw animację biegu
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animuj kursor animacji
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

### Modyfikacja właściwości Modelu

Model ma również wiele różnych właściwości, które można manipulować za pomocą funkcji `go.get()` i `go.set()`:

`animation`
: aktualna animacja modelu (typ `hash`) (TYLKO DO ODCZYTU). Zmieniasz animację, używając `model.play_anim()` (patrz wyżej).

`cursor`
: znormalizowany kursor animacji (typ `number`).

`material`
: materiał modelu (typ `hash`). Możesz to zmieniać za pomocą właściwości zasobów materiału i `go.set()`. Obejrzyj [dokumentację API](/ref/model/#material) w celu uzyskania przykładu.

`playback_rate`
: prędkość odtwarzania animacji (typ `number`).

`textureN`
: tekstury modelu, gdzie N to 0-7 (typ `hash`). Możesz to zmieniać za pomocą właściwości zasobów tekstury i `go.set()`. Obejrzyj [dokumentację API](/ref/model/#textureN) w celu uzyskania przykładu.

## Materiały

Oprogramowanie 3D zwykle pozwala na ustawienie właściwości wierzchołków obiektu, takie jak kolor i nakładanie tekstur. Te informacje trafiają do pliku glTF *.gltf* lub Collada *.dae*, który eksportujesz z oprogramowania 3D. W zależności od wymagań gry będziesz musiał wybrać lub utworzyć odpowiednie i _wydajne_ materiały dla swoich obiektów. Materiał łączy w sobie programy cieniowania (shadery) z zestawem parametrów do renderowania obiektu.

Dostępny jest prosty materiał modelu 3D w wbudowanym folderze materiałów. Jeśli potrzebujesz tworzyć niestandardowe materiały dla swoich modeli, zobacz [dokumentację materiałów](/manuals/material) w celu uzyskania dalszych informacji. W [dokumentacji shaderów](/manuals/shader) znajdziesz informacje na temat działania takich programów cieniowania.

### Stałe materiału

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: Kolor modelu (type `vector4`). Wektor 4-składnikowy jest używany do reprezentacji odcienia z wartościami X, Y, Z i W odpowiadającymi za czerwień, zielony, niebieski i kolor alfa (przezroczystości).

## Renderowanie

Domyślny skryp renderowanie (render script) jest napisany pod gry 2D i nie działa dobrze z modelami 3D. Kopiując domyślny skrypt i dodając kilka lini kodu możesz szybko włączyć renderowanie obiektów trójwymiarowych dla Twoich Modeli. Na przykład:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(render.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

Zobacz [dokumnetację renderowania](/manuals/render) w celu uzyskania dalszych informacji o skryptach renderowania.
