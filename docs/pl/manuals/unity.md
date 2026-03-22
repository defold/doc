---
title: Defold dla użytkowników Unity
brief: Ten przewodnik pomaga szybko przesiąść się na Defold, jeśli masz doświadczenie z Unity. Omawia kilka kluczowych pojęć używanych w Unity i wyjaśnia odpowiadające im narzędzia oraz metody w Defold.
---

# Defold dla użytkowników Unity

Jeśli masz wcześniejsze doświadczenie z Unity, ten przewodnik pomoże ci szybko zacząć pracować w Defold. Skupia się na podstawach i odsyła do oficjalnych instrukcji Defold, gdy potrzebujesz głębszych szczegółów.

## Wprowadzenie

Defold to całkowicie darmowy, prawdziwie wieloplatformowy silnik 3D do gier z edytorem dla Windows, Linux i macOS. Pełny kod źródłowy jest dostępny na [GitHub](https://github.com/defold/defold/).

Defold stawia na wydajność, nawet na słabszych urządzeniach. Jego architektura oparta na komponentach i danych jest trochę podobna do podejścia DOTS w Unity.

Defold jest znacznie mniejszy niż Unity. Rozmiar silnika z pustym projektem wynosi od 1 do 3 MB na wszystkich platformach. Możesz usunąć dodatkowe części silnika i przenieść część zawartości gry do [Live Update](/manuals/live-update), aby pobierać ją osobno później. Porównanie rozmiarów oraz inne powody, dla których warto wybrać Defold, opisano na stronie [Dlaczego Defold](https://defold.com/why/).

Aby dostosować Defold do swoich potrzeb, możesz użyć własnych lub gotowych rozwiązań:

1. W pełni skryptowalny pipeline renderowania (skrypt renderowania + materiały/shadery) z kilkoma backendami do wyboru (OpenGL, Vulkan itd.).
2. Kod i komponenty jako Native Extensions (C++/C#).
3. Skrypty edytora i widżety UI do dostosowywania edytora.
3. Zmodyfikowana wersja silnika i edytora, ponieważ dostępny jest pełny kod źródłowy i pipeline budowania.

Polecamy też film Game From Scratch o [Defold dla programistów Unity](https://www.youtube.com/watch?v=-3CzCbd4QZ0).

---

## Instalacja

1. Pobierz Defold dla swojego systemu operacyjnego.
2. Rozpakuj archiwum i uruchom program.

To wszystko. Bez huba, bez dodatkowych SDK, toolchainów ani instalacji pakietów platform. Dlatego mówimy, że Defold ma zerową konfigurację początkową.

Jeśli potrzebujesz więcej szczegółów, przeczytaj krótką [instrukcję instalacji](/manuals/installation).

### Wersje

Defold jest często aktualizowany i nie ma gałęzi „LTS”. Zawsze zalecamy używanie najnowszej wersji. Nowe wersje są wydawane regularnie - zwykle co miesiąc, z około dwutygodniową publiczną betą. Defold możesz zaktualizować bezpośrednio w edytorze.

---

## Ekran powitalny

Defold wita cię ekranem powitalnym podobnym do Unity Hub, z którego możesz otwierać ostatnie projekty:

![Porównanie ekranów powitalnych](images/unity/unity_defold_start.png)

Możesz też rozpocząć nowy projekt z:
- `Templates` - podstawowe puste projekty do szybszego startu dla konkretnej platformy lub gatunku,
- `Tutorials` - prowadzone ścieżki nauki, które pomagają postawić pierwsze kroki,
- `Samples` - oficjalne lub społecznościowe przykłady zastosowań i demonstracje,

![Porównanie szablonów powitalnych](images/unity/unity_defold_templates.png)

Gdy utworzysz i/lub otworzysz swój pierwszy projekt, zostanie on otwarty w Defold Editor.

## Witaj, świecie

To szybki sposób, aby sprawnie zrobić coś w Defold, wykonać kroki, a potem wrócić do czytania reszty instrukcji.

1. Wybierz pusty projekt z `Templates`, wpisz nazwę w `Title`, wybierz lokalizację i utwórz go, klikając `Create New Project`. Zostanie otwarty w Defold Editor.
![Krok 1 Hello World](images/unity/helloworld_1.png)
2. Po lewej stronie, w panelu `Assets`, otwórz folder `main` i kliknij dwukrotnie `main.collection`, aby go otworzyć.
3. Po prawej stronie, w panelu `Outline`, kliknij prawym przyciskiem myszy `Collection` i wybierz `Add Game Object`.
![Krok 2 Hello World](images/unity/helloworld_2.png)
4. Kliknij prawym przyciskiem myszy utworzony obiekt gry `go` i wybierz `Add Component`, a następnie `Label`.
![Krok 3 Hello World](images/unity/helloworld_3.png)
5. Niżej, po lewej stronie, w panelu `Properties` wpisz coś we właściwości `Text`.
6. W głównym, centralnym widoku sceny przeciągnij, przesuń i upuść etykietę tak, aby znalazła się w pobliżu `(480,320,0)`, albo zmień tę wartość w `Properties`: `Position`.
![Krok 4 Hello World](images/unity/helloworld_4.png)
7. Po zmianie pozycji etykiety zapisz projekt, klikając `File` -> `Save All` albo używając skrótu <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> na Macu).
8. Zbuduj projekt, klikając `Project` -> `Build` albo używając skrótu <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> na Macu).
![Krok 5 Hello World](images/unity/helloworld_5.png)

Właśnie zbudowałeś swój pierwszy projekt w Defold i powinieneś zobaczyć tekst w oknie. Pojęcia obiektu gry i komponentu powinny być ci już znane. Kolekcje, Outline, Properties oraz to, dlaczego trzeba było przesunąć etykietę trochę w górę i w prawo, wyjaśniamy poniżej.

---

## Przegląd edytora Defold

Tutaj pokażemy Defold Editor z perspektywy tego, co użytkownik Unity może chcieć wiedzieć na początku, ale zachęcamy, aby potem zajrzeć do pełnej [instrukcji przeglądu edytora](/manuals/editor-overview).

### Porównanie edytorów

Pierwsza różnica, którą zauważysz między Unity a Defold, to domyślny układ edytora. Pokazujemy Unity Editor z lekko zmodyfikowanym układem, aby odpowiadał domyślnemu układowi Defold. Umieszczono je obok siebie, aby łatwiej porównać główne panele, dzięki czemu łatwiej rozpoznasz zakładki Unity.

![Porównanie edytorów](images/unity/defold_unity_editor.png)

Domyślnie Defold Editor otwiera się w ortograficznym podglądzie 2D. Jeśli będziesz pracować nad projektem 3D albo po prostu chcesz uzyskać wrażenie bliższe Unity, zalecamy przełączenie z 2D na 3D przez odznaczenie przełącznika `2D` na pasku narzędzi i zmianę projekcji kamery na perspektywiczną przez zaznaczenie przełącznika `Perspective`:

![Pasek narzędzi Defold](images/unity/defold_2d.png)

Możesz też dostosować `Grid Settings` na pasku narzędzi tak, aby używały płaszczyzny `Y`, tak jak w Unity:

![Ustawienia 3D Defold](images/unity/defold_3d.png)

### Przegląd paneli Defold

Defold Editor jest podzielony na 6 głównych paneli.

![Edytor 2](images/editor/editor_overview.png)

Poniżej znajduje się porównanie nazewnictwa i różnic funkcjonalnych w Defold:

| Defold | Unity | Różnice |
|---|---|---|
| 1. `Assets` | Project (Assets Browser) | W Defold panel `Assets` jest dokowany po lewej stronie. Defold nie tworzy żadnych plików `meta`. |
| 2. `Main Editor` | Scene View | Defold Editor jest kontekstowy (inne edytory dla różnych typów plików), podczas gdy Unity używa osobnych, wyspecjalizowanych okien (np. Animator, Shader Graph). Defold ma też wbudowany edytor kodu. |
| 3. `Outline` | Hierarchy | Defold pokazuje tylko aktualnie otwarty plik lub zaznaczony element (obiekt gry albo komponent), a nie globalną hierarchię. |
| 4. `Properties` | Inspector | Defold pokazuje tylko właściwości **bieżącego zaznaczenia** w `Outline`, a nie wszystkich komponentów w obiekcie gry. |
| 5. `Tools` | Console | Defold udostępnia narzędzia w zakładkach takich jak `Console`, `Curve Editor`, `Build Errors`, `Search Results`, `Breakpoints` i `Debugger`. |
| 6. `Changed Files` | Unity Version Control (Plastic) | W Defold, gdy Git jest już zintegrowany z projektem, zmienione pliki są pokazywane tutaj. Nadal możesz korzystać z Git zewnętrznie. |

Inne przydatne nazewnictwo związane z edytorem:

| Defold | Unity | Różnice |
|---|---|---|
| `Game Build` | Game Preview | Pokazuje uruchomioną grę zbudowaną przez silnik. Defold może uruchamiać wiele instancji gry z poziomu edytora, podobnie jak Unity 6+ Multiplayer Play Mode. W Defold gra zawsze uruchamia się w osobnym oknie, a nie dokowanym. Defold może też uruchomić grę na zewnętrznym urządzeniu, np. telefonie, podobnie jak Unity Remote. |
| `Tabs` | Tabs | Defold umożliwia edycję obok siebie w dwóch panelach w widoku Main Editor. Zakładki i panele są dokowane w jednym oknie edytora; widoczność paneli można przełączać (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>), a ich rozmiar regulować. |
| `Toolbar` | Toolbar / Scene View Options | Dopiero w nowszych wersjach Unity narzędzia transformacji zostały przeniesione do widoku Scene, podobnie jak w Defold. |
| `Console` | Console | `Console` w Defold nie można odczepić. Błędy budowania w Defold pojawiają się w osobnej zakładce `Build Errors`. |
| `Build Errors` | Compilation Errors in Console | Skrypty Lua są interpretowane, więc nie ma błędów kompilacji. Twój projekt jest jednak budowany i niektóre błędy mogą pojawić się podczas budowania. Defold używa też Lua Language Server do statycznej analizy skryptów. |
| `Search Results` | Search / Project Search | Filtrowanie według typów i etykiet nie jest dostępne w Defold. |
| `Curve Editor` | Unity Curve Editor | `Curve Editor` w Defold pozwala edytować tylko krzywe właściwości efektów cząsteczkowych. |
| `[Debugger](/manuals/debugging/)` | Visual Studio Debugger | `Debugger` jest w Defold w pełni zintegrowany od razu po instalacji. Jest też dodatkowa zakładka do śledzenia, włączania i wyłączania breakpointów. |

---

## Kluczowe pojęcia

Jeśli uogólnisz wystarczająco mocno, kluczowe pojęcia stojące za większością silników gier są bardzo podobne. Mają pomagać twórcom gier budować je łatwiej, jak z klocków, podczas gdy silnik sam obsługuje złożone zadania zależne od platformy.

### Elementy składowe

Defold operuje tylko kilkoma podstawowymi elementami składowymi:

![Elementy składowe](images/unity/blocks.png)

Więcej szczegółów znajdziesz w pełnej instrukcji o [elementach składowych Defold](/manuals/building-blocks/).

### Obiekty gry 
Defold używa **"Game Objects"** podobnie jak Unity. W obu silnikach obiekty gry są kontenerami danych z identyfikatorem i wszystkie mają transformacje: pozycję, obrót i skalę, ale w Defold transformacja jest wbudowana, a nie dostarczana przez osobny komponent.

Możesz tworzyć relacje rodzic-dziecko między obiektami gry. W Defold można to zrobić tylko w edytorze, wewnątrz `Collection` (wyjaśnionej niżej), albo dynamicznie w skrypcie. Obiekty gry nie mogą zawierać innych obiektów gry jako zagnieżdżonych obiektów tak, jak ma to miejsce w Unity.

### Komponenty
W obu silnikach obiekty gry można rozszerzać o **"Components"**. Defold udostępnia minimalny zestaw niezbędnych komponentów. Różnica między 2D i 3D jest mniejsza niż w Unity (np. przy colliderach), więc komponentów jest ogólnie mniej, a niektórych z Unity może ci zabraknąć.

Więcej o [komponentach Defold przeczytasz tutaj](/manuals/components/).

Poniższa tabela pokazuje podobne komponenty Unity, aby ułatwić szybkie porównanie, wraz z linkami do instrukcji każdego komponentu Defold:

| Defold | Unity | Różnice |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | W Defold tintu (właściwości koloru) można zmieniać tylko z poziomu kodu. |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | Defold ma wbudowany Tilemap Editor obsługujący kwadratowe siatki (ale istnieje rozszerzenie np. dla [Hexagon](https://github.com/selimanac/defold-hexagon/)) i nie ma wbudowanych reguł autotilingu. Narzędzia takie jak [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) czy [Sprite Fusion](https://defold.com/assets/spritefusion/) mają opcje eksportu do Defold. |
| [Label](/manuals/label/) | Text / TextMeshPro | Defold ma rozszerzenie [RichText](https://defold.com/assets/richtext/) do bogatego formatowania, podobnie jak TextMeshPro. |
| [Sound](/manuals/sound/) | AudioSource | Defold ma tylko globalne źródło dźwięku (nieprzestrzenne). Dla Defold dostępne jest oficjalne rozszerzenie [FMOD](https://github.com/defold/extension-fmod). |
| [Factory](/manuals/factory/) | Prefab Instantiate() | W Defold Factory to komponent z określonym prototypem (prefabem). |
| [Collection Factory](/manuals/collection-factory/) | - (No direct component equivalent) | Komponent Collection Factory w Defold może tworzyć wiele obiektów gry naraz i ustawiać relacje rodzic-dziecko już w momencie tworzenia. |
| [Collision Object](/manuals/physics-object) | Rigidbody + Collider | W Defold obiekty fizyki i kształty kolizji są połączone w jednym komponencie. |
| [Collision Shapes](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | W Defold kształty (box, sphere, capsule) są konfigurowane wewnątrz komponentu Collision Object. Oba rozwiązania obsługują kształty kolizji z tilemap oraz dane convex hull. |
| [Camera](/manuals/camera/) | Camera | W Unity kamera ma trochę więcej wbudowanych ustawień renderowania i post-processingu, podczas gdy Defold przekazuje to do własnej kontroli użytkownika przez skrypt renderowania. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | GUI w Defold to potężny komponent do tworzenia kompletnych interfejsów i szablonów. Unity nie ma jednego równoważnego komponentu UI, tylko kilka frameworków UI. Defold ma też rozszerzenie [ImGui](https://github.com/britzl/extension-imgui). |
| [GUI Script](/manuals/gui-script/) | Unity UI / uGUI scripts | GUI w Defold można kontrolować przez skrypty GUI, używając dedykowanego `gui` API. |
| [Model](/manuals/model/) | MeshRenderer + Material | W Defold komponent Model łączy plik modelu 3D, tekstury i materiał ze shaderami. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | W Defold Mesh to komponent do zarządzania zbiorem wierzchołków z poziomu kodu. Jest podobny do Model w Defold, ale jeszcze niższego poziomu. |
| [ParticleFX](/manuals/particlefx/) | Particle System | Edytor efektów cząsteczkowych Defold obsługuje efekty 2D/3D z wieloma właściwościami i pozwala animować je w czasie za pomocą krzywych w Curve Editor. Nie obsługuje Trails ani Collisions. |
| [Script](/manuals/script/) | Script | Więcej szczegółów o różnicach programistycznych wyjaśniamy niżej. |

#### Rozszerzenia i własne komponenty

Defold ma też oficjalne komponenty [Spine](/manuals/extension-spine/) i [Rive](/manuals/extension-rive/) dostępne przez rozszerzenia.

Możesz też tworzyć własne [niestandardowe komponenty](https://github.com/defold/extension-simpledata) przy użyciu Native Extensions, np. taki społecznościowy [Object Interpolation Component](https://github.com/indiesoftby/defold-object-interpolation).

Niektóre komponenty Unity nie mają w Defold gotowego odpowiednika out of the box, na przykład: Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth czy Animator. Całą tę funkcjonalność można jednak zaimplementować w skryptach, a gotowe rozwiązania już istnieją - na przykład różne pipeline'y oświetlenia, komponent Mesh do generowania dowolnych siatek (w tym terenu) albo [Hyper Trails](https://defold.com/assets/hypertrails/) do konfigurowalnych efektów śladu. Defold może też w przyszłości dodać nowe wbudowane komponenty, takie jak światła.

### Zasoby

Niektóre komponenty wymagają **"Resources"**, podobnie jak w Unity, na przykład sprite'y i modele potrzebują tekstur. Kilka z nich porównano w tabeli poniżej:

| Defold | Unity | Różnice |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold ma też [rozszerzenie dla Texture Packer](https://defold.com/extension-texturepacker/). |
| [Tile source](/manuals/tilesource/) | Tile Palette + Asset | W Defold tile source może służyć jako tekstura dla tilemap, ale także dla sprite'ów lub cząsteczek. |
| [Font](/manuals/font/) | Font | Używany przez komponent Label w Defold albo przez węzły tekstowe w GUI, podobnie jak Text/TextMeshPro w Unity. |
| [Material](/manuals/material/) | Material | W Defold shadery nazywają się: vertex program i fragment program. |

### Kolekcja kontra scena

W Defold obiekty gry i komponenty mogą być umieszczane w osobnych plikach, podobnie jak prefaby w Unity, albo definiowane w łączącym pliku **"Collection"**.

Kolekcja w Defold to w praktyce plik tekstowy ze statycznym opisem sceny. Nie jest to obiekt działający w czasie działania programu. Definiuje jedynie to, jakie obiekty gry mają zostać utworzone w grze oraz jak mają zostać ustanowione relacje rodzic-dziecko między tymi obiektami.

#### Światy gry

Sceny Unity domyślnie współdzielą ten sam globalny stan gry i tę samą symulację fizyki, czyli w praktyce ten sam *świat*. W Defold masz dwie opcje:
1. Utworzyć obiekty gry z pojedynczego pliku obiektu gry przez `Factory` albo z pliku kolekcji przez `Collection Factory` w już utworzonym *świecie*, podobnie jak prefaby.
2. Utworzyć w czasie działania oddzielny *świat* gry z własnymi obiektami gry, światem fizyki, operacjami silnika i przestrzenią adresową, korzystając z kolekcji wczytanej podczas bootstrapu albo z komponentu `Collection Proxy`.

Fabryki i komponenty proxy są omówione także niżej.
Więcej o kolekcjach przeczytasz w [instrukcji o elementach składowych](/manual/building-blocks/#collections).

---

## Zasoby projektu i assety

Unity i Defold przechowują zawartość gry w katalogu projektu, ale różnią się sposobem śledzenia i przygotowywania zasobów.

### Assety

Unity trzyma assety w `Assets/` i generuje pliki `meta`. Defold nie ma plików meta. Projekt w Defold to po prostu struktura twoich folderów, dokładnie taka jak na dysku - a panel `Assets` zawsze ją odzwierciedla.

### Formaty zasobów

Unity importuje i konwertuje assety do innych formatów w tle. W Defold pracujesz bezpośrednio z zasobami źródłowymi (`.png`, `.gltf`, `.wav`, `.ogg` itd.) i przypisujesz je do `Components`.

Unity może używać pojedynczego obrazu jako Sprite. W Defold obrazy mogą być używane bezpośrednio przez Model/Mesh, ale Sprite/GUI/Tilemap/Particles wymagają atlasu (spakowanych tekstur) albo tilesource (kafelków opartych na siatce).

Większość zasobów Defold jest przechowywana jako tekst, więc dobrze współpracuje z systemami kontroli wersji.

### Pamięć podręczna biblioteki

Unity generuje katalog `Library/` dla importowanych assetów. Defold nie ma takiego katalogu; assety są przetwarzane podczas budowania, a wynik buforowany jest w katalogu builda (oraz opcjonalnych lokalnych/zdalnych cache'ach budowania).

---

## Pisanie kodu

Częstą pułapką dla osób przechodzących z Unity jest traktowanie skryptów Defold jak `MonoBehaviour` i dołączanie jednego do *każdego* obiektu gry. Oczywiście można pisać w stylu obiektowym, a nawet istnieją biblioteki, które w tym pomagają, ale zalecanym podejściem, zwłaszcza przy wielu podobnych obiektach gry, jest używanie skryptów jako systemów lub menedżerów. Jeden skrypt może kontrolować setki lub tysiące obiektów i ich komponentów, nawet jeśli same obiekty nie mają własnych skryptów, dzięki silnemu adresowaniu i systemowi wiadomości w Defold. Tworzenie osobnego skryptu dla każdego obiektu jest rzadko potrzebne i może prowadzić do nieproduktywnej złożoności.

Przykład pokazujący, jak wykorzystać właściwości skryptu Defold, fabryki, adresowanie i wiadomości do sterowania wieloma jednostkami, znajdziesz [tutaj](https://defold.com/examples/factory/spawn_manager/).

Dobre instrukcje o pisaniu kodu:
- [Instrukcja o skryptach](/manuals/script/)
- [Pisanie kodu](/manual/writing-code)
- [Debugowanie](/manuals/debugging/)

### Lua

Skrypty Defold są pisane w dynamicznie typowanym, wieloparadygmatycznym języku [Lua](https://www.lua.org/).

Istnieje kilka typów skryptów Lua: `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script` oraz moduły `*.lua`.

### Teal

Defold wspiera używanie transpilerów, które generują kod Lua, takich jak [Teal](https://teal-language.org/) - statycznie typowany dialekt Lua, ale ta funkcjonalność jest bardziej ograniczona i wymaga dodatkowej konfiguracji. Szczegóły są dostępne w [repozytorium rozszerzenia Teal](https://github.com/defold/extension-teal).

### Native Extensions C++/C#

W Defold możesz pisać Native Extensions w C++ i C#. Jeśli bardzo dobrze znasz C#, technicznie możliwe jest zbudowanie większości logiki gry w rozszerzeniu C# i wywoływanie jej z małego skryptu bootstrapowego Lua, choć wymaga to zaawansowanej znajomości API i nie jest zalecane dla początkujących.

Więcej o rozszerzeniach przeczytasz w [instrukcji Native Extensions Defold](/manual/extensions.md).

### Wbudowany edytor kodu

Defold Editor zawiera wbudowany edytor kodu z podpowiadaniem kodu, podświetlaniem składni, szybkim podglądem dokumentacji, lintingiem i wbudowanym debuggerem.

![Edytor kodu Defold](/images/editor/code-editor.png)

### VS Code i inne edytory

Nadal możesz używać własnego zewnętrznego edytora, jeśli wolisz. Wszystkie komponenty Defold i powiązane pliki są tekstowe, więc możesz edytować je dowolnym edytorem tekstu, ale musisz zachować prawidłowe formatowanie i strukturę elementów, ponieważ są oparte na Protobuf.

Jeśli przywykłeś do VS Code i chcesz używać go do pisania kodu swojej gry, zalecamy zainstalowanie [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) albo [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) z Visual Studio Marketplace.

Możesz też skonfigurować preferencje Defold Editor tak, aby pliki tekstowe otwierały się domyślnie w VS Code (lub innym zewnętrznym edytorze). Szczegóły znajdziesz w [instrukcji preferencji edytora](/manuals/editor-preferences/).

### Shadery - GLSL

Defold używa GLSL (OpenGL Shading Language) do shaderów - `Vertex Programs` i `Fragment Programs`, podobnie jak Unity. Chociaż Defold nie oferuje czegoś takiego jak Shader Graph w Unity (co może być wadą), nadal możesz tworzyć równoważne shadery, pisząc kod.

Więcej o shaderach przeczytasz w [instrukcji o shaderach](/manuals/shader).

#### Materiały

Defold używa koncepcji `Material`, która łączy shadery `.fp` i `.vp`, samplery (tekstury) oraz inne elementy, takie jak Vertex Attributes albo Constants.

Więcej o materiałach przeczytasz w [instrukcji o materiałach](/manuals/material).

---

## System wiadomości

W Defold obiekty nie trzymają bezpośrednich referencji do siebie nawzajem. Nie ma `GetComponent`, nie ma wywołań metod między obiektami z poziomu skryptów i nie ma globalnego dostępu do sceny jak w Unity.

Zamiast tego skrypty komunikują się przez przekazywanie wiadomości: wysyłasz wiadomości do innych skryptów zamiast bezpośrednio wywoływać metody albo odwoływać się do komponentów. To, co te obiekty zrobią z wiadomościami, zależy już od nich.

Na początku może to wydawać się nieznane, ale sprzyja luźnemu powiązaniu i zmniejsza ścisłe zależności.


### Wysyłanie wiadomości

W Unity komunikacja zwykle wygląda tak:

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Obiekty mogą więc bezpośrednio odwoływać się do siebie nawzajem i wywoływać metody na innych skryptach. Wszystko istnieje w jednej współdzielonej przestrzeni sceny.

W Defold wysyłasz wiadomość z jednego skryptu do innego skryptu (lub innego komponentu):

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

A potem możesz obsłużyć te wiadomości w skrypcie:

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Na razie zignoruj `#` i `hash`, wrócimy do tego później. Reszta powinna być prosta. Możesz wysłać wiadomość do dowolnego komponentu (nawet do tego samego skryptu) dowolnego utworzonego obiektu gry.

#### Komponenty inne niż skrypty

Czasem wysyłasz wiadomości na przykład do komponentów `Sprite` albo `Collision`, aby je włączyć lub wyłączyć. Czasem komponenty wysyłają wiadomości do twojego skryptu, na przykład gdy dochodzi do kolizji, abyś mógł ją obsłużyć. Defold wewnętrznie używa tego samego systemu wiadomości zarówno do zdarzeń silnika, jak i do komunikacji w rozgrywce.

System wiadomości jest do pewnego stopnia podobny do Unity SendMessage albo systemów zdarzeń, choć adresowanie i konwencje są inne.

Więcej szczegółów znajdziesz w [Instrukcji o przekazywaniu wiadomości](/manuals/message-passing/).

### Adresowanie

Obiekty i komponenty w Defold są identyfikowane przez adresy, znane jako URL-e.

Każdy utworzony obiekt i komponent ma własny unikalny adres i nie musisz przechodzić po grafie sceny, aby go znaleźć. Dzięki temu adresowanie jest jawne i bezpośrednie.

Prosty URL w Defold może wyglądać tak:
```lua
"/player"
```

To jest *pojęciowo* podobne do:
```c#
GameObject.Find("player")
```

Teraz czas wyjaśnić, dlaczego w adresach użyto `"/"` i `"#"`.

URL Defold (podobny do [URL](https://en.wikipedia.org/wiki/URL)) składa się z trzech części:

```yaml
socket: /path #fragment
```

albo, opisując to bardziej w nazewnictwie Defold:

```yaml
collection: /gameobject #component 
```
W powyższych opisach spacje dodano tylko po to, aby wizualnie rozdzielić te 3 części.

W skrócie:
1. `collection:` identyfikuje kontekst kolekcji, z `:` na końcu.
2. `/path` identyfikuje obiekt gry, z `/` poprzedzającym identyfikator.
3. `#fragment` identyfikuje konkretny komponent na tym obiekcie (na przykład skrypt, sprite albo komponent kolizji), z `#` poprzedzającym identyfikator.

#### Adres statyczny

Te identyfikatory są ustalane przy tworzeniu każdego z nich i nigdy się nie zmieniają, nawet jeśli zmienisz relacje rodzic-dziecko. Możesz je ustawić we właściwości `Id` w plikach albo otrzymać w czasie działania z wywołań `factory.create` lub `collectionfactory.create`, podczas instancjowania.

#### Adresowanie względne

Nie zawsze musisz używać pełnego URL.

Jeśli wysyłasz wiadomości w obrębie tej samej kolekcji (tego samego *świata*), możesz pominąć część `socket`:

```yaml
/gameobject #component
```
Jeśli wysyłasz do komponentu w tym samym obiekcie gry, możesz pominąć także część obiektu gry:

```yaml
#component
```

Dwa przydatne skróty to:
- `#` do wysyłania do tego komponentu *Script*
- `.` do wysyłania do wszystkich komponentów w tym *Game Object*

Adresowanie względne i skróty pozwalają pisać URL-e, które można ponownie wykorzystać w różnych kontekstach i obiektach gry bez podawania pełnych ścieżek.

### Wiadomości do GUI i renderowania

Ponieważ Defold oddziela świat GUI od świata obiektów gry, możesz też wysyłać wiadomości z komponentów `.script` w świecie obiektów gry do `.gui_script`.

Możesz również wysyłać wiadomości do specjalnych przestrzeni nazw systemu, używając identyfikatora zaczynającego się od `@`. Na przykład system renderowania można adresować przez `@render:` i użyć tego do sterowania niektórymi wbudowanymi funkcjami renderowania, takimi jak zmiana projekcji w domyślnym skrypcie renderowania:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Więcej szczegółów znajdziesz w [instrukcji o adresowaniu](/manuals/addressing/).

---

## Prefaby i instancje

Unity może instancjować wszystko w scenie statycznie lub dynamicznie, a Defold może zrobić to samo. W Unity bierzesz Prefab i wywołujesz `Instantiate(prefab)`. W Defold masz 3 komponenty do instancjowania zawartości:

- `Factory` - instancjuje **pojedynczy obiekt gry** z danego prototypu: pliku `*.go` (prefaba).
- `Collection Factory` - instancjuje **zestaw obiektów gry** z relacjami rodzic-dziecko z danego prototypu: pliku `*.collection`.
- `Collection Proxy` - **ładuje** i instancjuje nowy *świat* z pliku `*.collection`.

### Factory

Gdy zdefiniujesz komponent `Factory` i ustawisz jego właściwość `Prototype` na odpowiedni plik obiektu gry, tworzenie instancji sprowadza się po prostu do wywołania w kodzie:

```lua
factory.create("#my_factory")
```

Używa to adresu komponentu, w tym przypadku - względnej ścieżki z identyfikatorem `"#my_factory"`.

Zwraca identyfikator nowo utworzonej instancji, więc jeśli potrzebujesz użyć go później, warto zapisać go w zmiennej:

```lua
local new_instance_id = factory.create("#my_factory")
```

Pamiętaj, że w Defold nie musisz ręcznie tworzyć puli obiektów - silnik sam obsługuje pooling wewnętrznie.

Więcej szczegółów znajdziesz w [instrukcji o fabryce](/manuals/factory/). 

### Collection Factory

Różnica między komponentami `Factory` i `Collection Factory` polega na tym, że Collection Factory może jednocześnie utworzyć **wiele** obiektów gry i zdefiniować przy tworzeniu relacje rodzic-dziecko zgodnie z plikiem `*.collection`.

Takiego rozróżnienia nie ma w Unity - nie ma tam dedykowanej koncepcji odpowiadającej `Collection Factory` w Defold. Najbliższą analogią jest po prostu zagnieżdżony Prefab, który zawiera hierarchię obiektów.

Zwraca **table** z identyfikatorami wszystkich utworzonych instancji:

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Więcej szczegółów znajdziesz w [instrukcji o Collection Factory](/manuals/collection-factory/).

#### Własne właściwości instancji

Wywołując `factory.create()` lub `collectionfactory.create()`, możesz też podać opcjonalne parametry, takie jak pozycja, obrót, skala i właściwości skryptu, aby dokładnie kontrolować, gdzie i jak pojawi się instancja oraz jak będzie się zachowywać, na przykład:

```lua
factory.create("#my_factory", my_position, my_rotation, my_scale, my_properties)
```

#### Dynamiczne wczytywanie

Zarówno w komponentach `Factory`, jak i `Collection Factory` możesz oznaczyć `Prototype` do dynamicznego wczytywania zasobów, aby ciężkie assety były ładowane do pamięci tylko wtedy, gdy są potrzebne, i zwalniane, gdy przestają być używane.

Więcej szczegółów znajdziesz w [instrukcji zarządzania zasobami](/manuals/resource/). 

### Collection Proxy

`Collection Proxy` odnosi się do konkretnego pliku `*.collection`, ale zamiast wstrzykiwać obiekty do *bieżącego świata* (jak robią to fabryki), **ładuje i instancjuje nowy świat gry**. Jest to trochę podobne do wczytywania całej sceny w Unity, ale z silniejszym rozdzieleniem.

W Unity możesz wczytać scenę addytywną na przykład tak:

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

W Defold nową kolekcję wczytujesz po prostu, wysyłając wiadomość do komponentu `Collection Proxy`:

```lua
msg.post("#myproxy", "load")
```

1. Gdy wysyłasz do proxy wiadomość `"load"` (lub `"async_load"` w przypadku wczytywania asynchronicznego), silnik alokuje nowy świat, instancjuje tam wszystko z tej kolekcji i izoluje go.
2. Gdy wczytywanie się zakończy, proxy odsyła wiadomość `"proxy_loaded"`, sygnalizując, że świat jest gotowy.
3. Następnie zwykle wysyłasz wiadomości `"init"` i `"enable"`, aby obiekty w tym nowym świecie rozpoczęły swój normalny cykl życia.

Aby komunikować się między wczytanymi światami, musisz używać jawnych wiadomości z URL-ami, które zawierają nazwę świata (`collection:`, czyli pierwszą część URL).

Takie odseparowanie może być ogromną zaletą przy implementowaniu przejść między poziomami, minigierek lub dużych modularnych systemów, ponieważ zapobiega niezamierzonym interakcjom, a dodatkowo pozwala w razie potrzeby osobno sterować tempem aktualizacji, na przykład na potrzeby pauzy albo spowolnienia czasu.

Jeśli kiedykolwiek używałeś wielu scen w Unity i potrzebowałeś, żeby działały niezależnie, potraktuj `Collection Proxy` jako sposób przeniesienia tej koncepcji bezpośrednio do Defold.

Więcej szczegółów znajdziesz w [instrukcji o Collection Proxy](/manuals/collection-proxy/).

---

## Cykl życia aplikacji

Znasz już zestaw zdarzeń cyklu życia Unity: `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` albo `OnApplicationQuit`.

Defold również ma jasno określony cykl życia aplikacji, ale pojęcia i terminologia są inne. Defold udostępnia etapy cyklu życia przez zestaw predefiniowanych wywołań zwrotnych Lua, które są wywoływane przez silnik podczas inicjalizacji, każdej klatki i finalizacji.

Oto porównanie:

| Defold | Unity | Komentarz |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold ma jeden punkt wejścia inicjalizacji i jedno wywołanie zwrotne - init(). Jest wywoływane dla każdego komponentu w momencie jego utworzenia. |
| `on_input` | Input Methods | Defold odbiera wejścia, gdy [ustawiono fokus wejścia dla skryptu](/manuals/input/#input-focus). Jest to przetwarzane jako pierwsze w pętli aktualizacji. |
| `fixed_update()` | `FixedUpdate()` | Wywoływane ze stałym krokiem czasowym. Aby włączyć to w Defold, musisz ustawić `Use Fixed Timestep` - [szczegóły](https://defold.com/manuals/project-settings/#use-fixed-timestep). Od wersji 1.12.0 uruchamia się przed `update()`. |
| `update()` | `Update()` | Wywoływane raz na klatkę z delta time. |
| `late_update()` | `LateUpdate()` | Wywoływane po `update()`, tuż przed renderowaniem klatki. Dostępne od 1.12.0. |
| `on_message` | Message Receiver | Podstawowe wywołanie zwrotne Defold do odbierania wiadomości. Jest przetwarzane, gdy w kolejce znajduje się dowolna wiadomość. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold wywołuje `final()` dla każdego komponentu, gdy jego obiekt gry zostanie usunięty w czasie działania (`go.delete()`) albo gdy świat/kolekcja zostanie zwolniony, a także podczas zamykania aplikacji dla wszystkich pozostałych obiektów. |

::: sidenote
Pamiętaj, że Defold nie gwarantuje żadnej kolejności wykonywania między komponentami, gdy kilka z nich jest inicjalizowanych, aktualizowanych lub usuwanych naraz. Zachęca się do projektowania odseparowanego.

### Inicjalizacja

Można myśleć o `init()` w Defold jako o połączeniu elementów `Awake()`, `Start()` i `OnEnable()` z Unity w jeden punkt wejścia, w którym silnik już wszystko przygotował i możesz bezpiecznie ustawić stan komponentu.

### Kiedy obsługiwane są wiadomości?

Ponieważ wiadomości można już wysyłać w `init()`, są one rozsyłane jako pierwsze tuż po inicjalizacji.

Wiadomości są następnie obsługiwane po każdej wewnętrznej pętli przetwarzania, za każdym razem, gdy coś znajduje się w kolejce, więc `on_message()` może zostać wywołane na przykład nawet kilka razy w jednej pętli aktualizacji.

### Pętla aktualizacji

W każdej klatce Defold wykonuje sekwencję operacji - obsługę wejścia, rozsyłanie wiadomości, uruchamianie aktualizacji skryptów i GUI, stosowanie fizyki, transformacji, a na końcu renderowanie grafiki.

### Finalizacja

W Defold czyszczenie jest zawsze powiązane z usunięciem lub zwolnieniem świata, a jedynym punktem wyjścia dla pojedynczego komponentu jest `final()`.

Subtelna różnica względem modelu Unity polega na tym, że nie ma rozróżnienia między wyłączeniem komponentu a zamknięciem całej aplikacji.

### Renderowanie

Skrypt renderowania (`*.render_script`) jest częścią pipeline'u renderowania, który również uczestniczy w cyklu życia za pomocą własnych callbacków `init()`, `update()` i `on_message()`, ale działają one na wątku renderowania i są odseparowane od logiki skryptów obiektów gry i GUI.

Więcej szczegółów znajdziesz w [instrukcji o cyklu życia aplikacji](/manuals/application-lifecycle/).

---

## GUI

GUI w Defold to osobny, dedykowany framework dla interfejsów użytkownika - menu, nakładek, okien dialogowych i innych elementów, podobnie jak UI Toolkit albo uGUI z Canvas.

GUI jest komponentem i jest odseparowane od obiektów gry oraz kolekcji. Zamiast obiektów gry pracujesz z węzłami GUI ułożonymi w hierarchię i sterowanymi przez skrypt GUI.

### Węzły GUI

Gdy otworzysz plik komponentu `*.gui` w Defold, zobaczysz płótno, na którym umieszczasz `"GUI nodes"`. To podstawowe elementy budujące GUI. Możesz dodawać węzły GUI typu:

- Box (prostokątny kształt z teksturą)
- Text (z dowolną czcionką)
- Pie (element w postaci wycinka koła z radialnym wypełnieniem i teksturą)
- ParticleFX
- Template (cały zagnieżdżony plik `.gui`, jak prefab GUI)
- oraz węzeł Spine, gdy używasz rozszerzenia Spine.

### Skrypt GUI

Komponent GUI ma specjalną właściwość dla skryptów GUI - przypisujesz do każdego komponentu jeden plik `*.gui_script`, a to pozwala modyfikować zachowanie komponentu, więc jest to bardzo podobne do zwykłych skryptów, z tą różnicą, że nie używa przestrzeni nazw `go.*` (która służy do skryptów obiektów gry). Zamiast tego korzysta ze specjalnego API w przestrzeni nazw `gui.*`, które działa tylko wewnątrz skryptów GUI (`*.gui_script`). Można o tym myśleć jak o osobnej scenie Unity UI (uGUI) z Canvas.

### Renderowanie GUI

Elementy GUI są renderowane niezależnie od kamery gry, zwykle w przestrzeni ekranu, ale to zachowanie można zmienić w niestandardowych pipeline'ach renderowania.

Więcej szczegółów znajdziesz w [instrukcji o GUI](/manuals/gui/).

## Gdzie są Sorting Layers?

To bardzo częste źródło nieporozumień podczas migracji z Unity.

Komponenty GUI mają `Layers` i działa to niemal tak samo jak „Sorting Layers” w Unity, ale dla innych komponentów, takich jak `Sprites`, `Tilemaps`, `Models` itd. nie ma bezpośredniego odpowiednika.

Zamiast tego zwykle łączy się:
- precyzyjne porządkowanie wzdłuż osi Z przy użyciu domyślnej kamery albo głębokości przy użyciu komponentu Camera,
- zgrubne porządkowanie przez skrypt renderowania z użyciem render predicates - aby wybierać, co ma być rysowane na podstawie tagów materiałów.

Nie próbuj jednak naśladować Sorting Layers z Unity za pomocą wielu tagów, ponieważ w Defold tagi są mechanizmem na poziomie renderowania. Nadużywanie ich może zepsuć batching i zwiększyć narzut rysowania.

---

## Co dalej?

- [Przykłady Defold](/examples)
- [Samouczki](/tutorials)
- [Instrukcje](/manuals)
- [Dokumentacja API](/ref/go)
- [FAQ](/faq/faq)

Jeśli masz pytania albo utkniesz, [Forum Defold](//forum.defold.com) albo [Discord](https://defold.com/discord/) to świetne miejsca, żeby poprosić o pomoc.
