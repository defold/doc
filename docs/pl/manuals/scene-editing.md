---
title: Edytor scen Defold
brief: Edytor scen służy do edytowania kolekcji, obiektów gry, GUI, efektów cząsteczkowych i innych zasobów wizualnych. Ten podręcznik wyjaśnia zaznaczanie, narzędzia oraz poruszanie się po widoku sceny w 2D i 3D, w tym tryb swobodnej kamery i ustawienia kamery.
---

# Edytor scen Defold

**Scene Editor** to edytor wizualny używany do budowania i edytowania scen, takich jak kolekcje, obiekty gry i inne zasoby wizualne.

Domyślnie wiele scen wizualnych otwiera się w widoku **ortograficznym 2D**. Przy pracy w 3D możesz przełączyć się na układ zorientowany na 3D, włączyć płaszczyznę siatki 3D i użyć kamery **perspektywicznej**.

## Otwieranie edytora scen

Otwórz edytor scen, klikając dwukrotnie zasób wizualny w panelu *Assets*, na przykład:

- **Struktura sceny** - kolekcje (`.collection`), obiekty gry (`.go`)
- **Zasoby 2D** - atlas (`.atlas`), mapy kafelków (`.tilemap`), sprite'y (`.sprite`), źródła kafelków (`.tilesource`)
- **Zasoby 3D** - modele (`.model`, `.glb`, `.gltf`)
- **UI** - sceny GUI (`.gui`)
- **Efekty** - efekty cząsteczkowe (`.particlefx`)
- i inne

## Nawigacja widoku sceny (sterowanie kamerą)

Kamerą edytora scen można sterować myszą i klawiaturą. Dostępne sterowanie zależy od tego, czy używasz standardowej nawigacji kamery, czy **Free Camera Mode**.

### Standardowa nawigacja (wszystkie edytory wizualne)

Te działania są dostępne w edytorach wizualnych:

- **Przesuwanie**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Przybliżanie**
  - <kbd>Mouse Wheel</kbd> albo
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Obrót/orbita wokół zaznaczenia (3D)**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

Możesz też użyć **Frame Selection** (<kbd>F</kbd>), aby ustawić kamerę na bieżącym zaznaczeniu.

## Orientacja sceny 2D i 3D

Widok sceny może być używany zarówno w przepływie pracy 2D, jak i 3D:

- W **2D** zwykle pracujesz w widoku ortograficznym z siatką zorientowaną na 2D.
- W **3D** zwykle:
  - zmieniasz orientację widoku na 3D,
  - używasz kamery **perspektywicznej**,
  - wybierasz odpowiednią płaszczyznę siatki, często **Y** jako „podłoże”.

Te funkcje są dostępne z paska narzędzi oraz menu **View**.

![Edytor scen 3D](images/editor/3d_scene.png)

## Przegląd paska narzędzi

W prawym górnym rogu widoku sceny znajduje się pasek narzędzi z często używanymi narzędziami i opcjami widoku (od lewej do prawej):

- **Move tool** (<kbd>W</kbd>)
- **Rotate tool** (<kbd>E</kbd>)
- **Scale tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) - przełącza orientację 2D i 3D (skrót <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Pasek narzędzi](images/editor/toolbar.png)

## Zaznaczanie i manipulowanie obiektami

### Zaznaczanie obiektów

Kliknij obiekt w głównym oknie przyciskiem <kbd>Left Mouse Click</kbd>, aby go zaznaczyć. Prostokąt lub prostopadłościan otaczający obiekt w widoku edytora zostanie podświetlony na kolor cyjan, wskazując zaznaczony element. Zaznaczony obiekt zostanie też podświetlony w widoku `Outline`, jak na ilustracji powyżej.

  Obiekty można też zaznaczać w następujący sposób:

- <kbd>Left Mouse Click</kbd> i <kbd>Drag</kbd>, aby zaznaczyć wszystkie obiekty w obszarze zaznaczenia.
- <kbd>Left Mouse Click</kbd> na obiektach w `Outline`; przytrzymując <kbd>⇧ Shift</kbd>, możesz rozszerzać zaznaczenie, a przytrzymując <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>, zaznaczać lub odznaczać kliknięte elementy.

#### Move tool

![Move tool](images/editor/icon_move.png){.left}

Aby przesuwać obiekty, użyj *Move Tool*. Znajdziesz je na pasku narzędzi w prawym górnym rogu edytora scen albo włączysz klawiszem <kbd>W</kbd>.

![Przesuwanie obiektu](images/editor/move.png){.inline}![Przesuwanie obiektu 3D](images/editor/move_3d.png){.inline}

Gizmo zmienia się i pokazuje zestaw manipulatorów - kwadratów i strzałek. Zaznaczony manipulator zmienia kolor na pomarańczowy. Możesz je <kbd>Drag</kbd>, aby przesuwać:

- jeden cyjanowy środkowy kwadrat, który przesuwa obiekt tylko w przestrzeni ekranu,
- 3 czerwone, zielone i niebieskie strzałki wzdłuż osi, które przesuwają obiekt tylko po danej osi X, Y lub Z,
- 3 czerwone, zielone i niebieskie kwadratowe uchwyty z przezroczystym wypełnieniem, które przesuwają obiekt tylko po danej płaszczyźnie, np. X-Y (niebieska), a po obrocie kamery w 3D także X-Z (zielona) i Y-Z (czerwona).

#### Rotate tool

![Rotate tool](images/editor/icon_rotate.png){.left}

Aby obracać obiekty, użyj *Rotate Tool*, wybierając je na pasku narzędzi albo naciskając <kbd>E</kbd>.

![Obracanie obiektu](images/editor/rotate.png){.inline}![Obracanie obiektu 3D](images/editor/rotate_3d.png){.inline}

To narzędzie składa się z czterech okrągłych manipulatorów, które możesz <kbd>Drag</kbd>, aby obracać. Zaznaczony manipulator zmienia kolor na pomarańczowy:

- jeden cyjanowy manipulator, zewnętrzny i największy, obracający obiekt w przestrzeni ekranu,
- 3 mniejsze czerwone, zielone i niebieskie okrągłe manipulatory pozwalające obracać osobno wokół osi X, Y i Z. W ortograficznym widoku 2D dwa z nich są prostopadłe do osi X i Y, więc okręgi są widoczne tylko jako dwie linie przecinające obiekt.

#### Scale tool

![Scale tool](images/editor/icon_scale.png){.left}

Aby skalować obiekty, użyj *Scale Tool*, wybierając je na pasku narzędzi albo naciskając <kbd>R</kbd>.

![Skalowanie obiektu](images/editor/scale.png){.inline}![Skalowanie obiektu 3D](images/editor/scale_3d.png){.inline}

To narzędzie składa się z zestawu kwadratowych lub sześciennych manipulatorów, które możesz <kbd>Drag</kbd>, aby skalować. Zaznaczony manipulator zmienia kolor na pomarańczowy:

- jeden cyjanowy sześcian w środku skaluje obiekt równomiernie we wszystkich osiach, także w osi Z,
- 3 czerwone, niebieskie i zielone sześcienne manipulatory skalują obiekt osobno wzdłuż osi X, Y i Z,
- 3 czerwone, zielone i niebieskie kwadratowe manipulatory z przezroczystym wypełnieniem skalują obiekt osobno na płaszczyznach X-Y, X-Z lub Y-Z.

### Filtry widoczności

Kliknij **ikonę oka** (`👁`) na pasku narzędzi, aby przełączać widoczność różnych typów komponentów oraz obwiedni i linii pomocniczych (`Component Guides` albo skrót <kbd>Ctrl</kbd> + <kbd>H</kbd> w Windows/Linux lub <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd> na Macu).

![Filtry widoczności](images/editor/visibilityfilters.png)

## Ustawienia siatki

Siatkę można dostosować do swojego przepływu pracy, co jest szczególnie przydatne w 3D. Kliknij przycisk **Grid Settings** (`▦`), aby otworzyć okno ustawień siatki.

![Ustawienia siatki](images/editor/grid_popup.png)

Ustawienia obejmują:

- **Grid size (X/Y/Z)**
  Ustawia odstęp między liniami siatki wzdłuż każdej osi. Użyj mniejszych wartości do precyzyjnego rozmieszczania małych obiektów albo większych wartości do szerszego przeglądu.
- **Active plane (X/Y/Z)**
  Wybiera płaszczyznę, na której rysowana jest siatka. W przepływie pracy 2D jest to zwykle **Z**, czyli domyślna płaszczyzna X-Y. W przepływie pracy 3D często używa się **Y**, aby reprezentować podłoże.
- **Grid color**
  Ustawia kolor linii siatki. Przydaje się do uzyskania kontrastu z różnymi tłami sceny.
- **Grid opacity**
  Kontroluje przezroczystość linii siatki. Niższe wartości sprawiają, że siatka mniej przeszkadza, ale nadal służy jako punkt odniesienia.
- Przycisk **Reset to Defaults**
  Przywraca wszystkie ustawienia siatki do wartości początkowych.

## Typ kamery: Perspective i Orthographic

Edytor scen obsługuje oba typy:

- kamerę **Orthographic**, typową w przepływie pracy 2D,
- kamerę **Perspective**, typową w przepływie pracy 3D.

Do przełączania użyj przełącznika kamery na pasku narzędzi. W scenach 3D nawigacja perspektywiczna zwykle jest bardziej naturalna.

## Free Camera Mode

Do szybkiej nawigacji 3D edytor scen udostępnia **Free Camera Mode**, czyli kamerę pierwszoosobową w stylu FPS.

### Włączanie Free Camera Mode

- Przytrzymaj <kbd>Right Mouse Button</kbd> - Free Camera Mode działa tak długo, jak przycisk jest trzymany.
- <kbd>Shift</kbd> + <kbd>`</kbd> (backtick) - przełącza Free Camera Mode na stałe, pozostawiając go aktywnym po puszczeniu klawiszy.

::: sidenote
Na niektórych układach klawiatury, np. szwedzkim, klawisz backtick jest martwym klawiszem i skrót może nie zadziałać zgodnie z oczekiwaniami. Ten skrót można zmienić w `File ▸ Preferences ▸ Keys`, wpisując skrót dla `Scene -> Free Camera -> Activate`.
:::

Gdy Free Camera Mode jest aktywny, Scene View jest podświetlony linią wokół krawędzi.

### Wyłączanie Free Camera Mode

- Puść <kbd>Right Mouse Button</kbd>, jeśli tryb był aktywowany przytrzymaniem, albo
- naciśnij i puść <kbd>Left Mouse Button</kbd>, <kbd>Right Mouse Button</kbd> albo naciśnij <kbd>Esc</kbd>, jeśli Free Camera Mode został włączony przełącznikiem.

### Rozglądanie się (mouse look)

Gdy Free Camera Mode jest aktywny, te działania sterują ruchem kamery zamiast narzędziami edytora:

- Poruszaj myszą, aby kontrolować **yaw** (lewo/prawo) i **pitch** (góra/dół).
- Pitch jest ograniczony, aby kamera się nie odwróciła.

Możesz też opcjonalnie odwrócić oś Y; zobacz **Free camera settings** niżej.

### Poruszanie

Gdy Free Camera Mode jest aktywny:

- <kbd>W</kbd> - do przodu
- <kbd>S</kbd> - do tyłu
- <kbd>A</kbd> - w lewo
- <kbd>D</kbd> - w prawo
- <kbd>E</kbd> - w górę
- <kbd>Q</kbd> - w dół

::: sidenote
Wszystkie klawisze ruchu można zmienić w `File ▸ Preferences ▸ Keys`. Następnie wyszukaj `Scene -> Free Camera`.
:::

Modyfikatory prędkości:

- Przytrzymaj <kbd>Shift</kbd> - szybszy ruch
- Przytrzymaj <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> - wolniejszy, dokładniejszy ruch

### Walking mode (opcjonalnie)

Free Camera Mode obsługuje **Walking Mode**.

Gdy jest włączony:
- ruch w górę i w dół jest ograniczony tak, aby bardziej przypominał chodzenie po podłożu z perspektywy pierwszej osoby,
- jest to przydatne podczas eksplorowania poziomu, gdy chcesz zachować spójny ruch „po ziemi”.

## Okno ustawień kamery

Przycisk kamery perspektywicznej na pasku narzędzi ma okno ustawień związanych z kamerą.

![Ustawienia kamery perspektywicznej](images/editor/camera_popup.png)

Okno zawiera:

- **Move Speed**
  Dostosowuje prędkość ruchu swobodnej kamery.

- **Look Sensitivity**
  Dostosowuje szybkość obrotu kamery w odpowiedzi na ruch myszy.

- **Invert Y**
  Odwraca pionowy kierunek rozglądania się myszą.

- **Walking Mode**
  Ogranicza ruch do nawigacji przypominającej poruszanie się po podłożu.

- **Reset to Defaults**
  Przywraca domyślne ustawienia kamery.
