---
title: Słowniczek Defold
brief: Ten słowniczek zawiera krótkie opisy wszystkiego, co możesz napotkać podczas pracy w Defold.
---

# Słowniczek Defold

Ten słowniczek daje krótkie opisy wszystkich rzeczy, z którymi możesz się spotkać podczas pracy w Defold. W większości przypadków znajdziesz też odnośnik do bardziej szczegółowej dokumentacji.

## Animation set (Zestaw animacji)

![Animation set](images/icons/animationset.png){.left} Zasób Animation set zawiera listę plików .dae lub innych plików .animationset, z których odczytywane są animacje. Dodawanie jednego pliku .animationset do drugiego jest wygodne, jeśli chcesz współdzielić częściowe zestawy animacji między kilkoma modelami. Szczegóły znajdziesz w [instrukcji animacji modeli](/manuals/model-animation/).

## Atlas (Atlas)

![Atlas](images/icons/atlas.png){.left} Atlas to zbiór osobnych obrazów skompilowanych w większy arkusz ze względów wydajnościowych i pamięciowych. Może zawierać nieruchome obrazy albo sekwencje obrazów tworzące animację poklatkową. Atlasy są używane przez różne komponenty do współdzielenia zasobów graficznych. Więcej w [dokumentacji Atlasa](/manuals/atlas).

## Builtins (Wbudowane zasoby)

![Builtins](images/icons/builtins.png){.left} Folder projektu builtins jest tylko do odczytu i zawiera przydatne domyślne zasoby. Znajdziesz w nim domyślny renderer, render script, materiały i inne elementy. Jeśli potrzebujesz własnych modyfikacji któregoś z tych zasobów, po prostu skopiuj go do projektu i edytuj według potrzeb.

## Camera (Kamera)

![Camera](images/icons/camera.png){.left} Komponent kamery pomaga określić, która część świata gry ma być widoczna i jak ma być rzutowana. Często przypina się kamerę do obiektu gry gracza albo tworzy osobny obiekt gry z kamerą, która podąża za graczem z użyciem wygładzania. Więcej w [dokumentacji kamery](/manuals/camera).

## Collision object (Obiekt kolizji)

![Collision object](images/icons/collision-object.png){.left} Obiekty kolizji rozszerzają obiekty gry o właściwości fizyczne, takie jak kształt przestrzenny, masa, tarcie i odbicie. Te właściwości decydują o tym, jak obiekt kolizji ma zderzać się z innymi obiektami kolizji. Najczęściej spotykane typy obiektów kolizji to obiekty kinematyczne, dynamiczne i wyzwalacze. Obiekt kinematyczny daje szczegółowe informacje o kolizji, na które musisz zareagować ręcznie, a obiekt dynamiczny jest automatycznie symulowany przez silnik fizyki zgodnie z prawami Newtona. Wyzwalacze to proste kształty wykrywające wejście lub wyjście innych kształtów. Szczegóły znajdziesz w [dokumentacji Fizyki](/manuals/physics).

## Component (Komponent)

Komponenty służą do nadawania obiektom gry konkretnej formy lub funkcjonalności, takiej jak grafika, animacja, zachowanie opisane skryptem czy dźwięk. Nie istnieją samodzielnie, tylko muszą być częścią obiektów gry. W Defold dostępnych jest wiele rodzajów komponentów. Opis znajdziesz w [instrukcji o blokach budujących](/manuals/building-blocks).

## Collection (Kolekcja)

![Collection](images/icons/collection.png){.left} Kolekcje są mechanizmem Defold do tworzenia szablonów, czyli tego, co w innych silnikach nazywa się prefabami, w których można wielokrotnie używać hierarchii obiektów gry. Są to struktury drzewiaste zawierające obiekty gry i inne kolekcje. Kolekcja jest zawsze zapisana w pliku i trafia do gry albo statycznie, gdy umieścisz ją ręcznie w edytorze, albo dynamicznie, gdy ją utworzysz w locie. Więcej w [instrukcji o blokach budujących](/manuals/building-blocks).

## Collection factory (Fabryka kolekcji)

![Collection factory](images/icons/collection-factory.png){.left} Komponent Collection factory służy do dynamicznego tworzenia hierarchii obiektów gry w uruchomionej grze. Szczegóły znajdziesz w [instrukcji fabryki kolekcji](/manuals/collection-factory).

## Collection proxy (Pełnomocnik kolekcji)

![Collection](images/icons/collection.png){.left} Collection proxy służy do wczytywania i aktywowania kolekcji w locie, gdy aplikacja lub gra działa. Najczęściej używa się go do wczytywania poziomów przed ich uruchomieniem. Szczegóły znajdziesz w [dokumentacji pełnomocnika kolekcji](/manuals/collection-proxy).

## Cubemap (Cubemap)

![Cubemap](images/icons/cubemap.png){.left} Cubemap to specjalny typ tekstury złożony z 6 różnych tekstur mapowanych na ściany sześcianu. Jest to przydatne przy renderowaniu skyboxów oraz różnych map odbić i oświetlenia.

## Debugging (Debugowanie)

W pewnym momencie gra zacznie zachowywać się w nieoczekiwany sposób i trzeba będzie ustalić, co jest nie tak. Nauka debugowania to sztuka, a na szczęście Defold ma wbudowany debugger, który pomaga w tej pracy. Więcej w [instrukcji debugowania](/manuals/debugging).

## Display profiles (Profile wyświetlania)

![Display profiles](images/icons/display-profiles.png){.left} Plik zasobu display profiles służy do określania układów GUI zależnych od orientacji, proporcji obrazu lub modelu urządzenia. Pomaga to dostosować UI do różnych urządzeń. Więcej w [instrukcji układów GUI](/manuals/gui-layouts).

## Factory (Fabryka)

![Factory](images/icons/factory.png){.left} W niektórych sytuacjach nie da się ręcznie umieścić wszystkich potrzebnych obiektów gry w kolekcji, więc trzeba tworzyć je dynamicznie, w locie. Na przykład gracz może wystrzeliwać pociski i każdy strzał powinien być tworzony oraz wysyłany dalej, gdy gracz naciska spust. Do tworzenia obiektów gry dynamicznie, z wcześniej przygotowanej puli obiektów, służy komponent factory. Szczegóły znajdziesz w [instrukcji factory](/manuals/factory).

## Font (Czcionka)

![Font file](images/icons/font.png){.left} Zasób Font powstaje z pliku czcionki TrueType lub OpenType. Określa rozmiar renderowanej czcionki oraz rodzaj dekoracji, takich jak obrys i cień. Fonty są używane przez komponenty GUI i Label. Szczegóły znajdziesz w [instrukcji fontu](/manuals/font/).

## Fragment shader (Fragment shader)

![Fragment shader](images/icons/fragment-shader.png){.left} To program uruchamiany na procesorze graficznym dla każdego piksela, czyli fragmentu, wielokąta podczas jego rysowania na ekranie. Zadaniem fragment shader jest określenie koloru każdego wynikowego fragmentu. Można to zrobić przez obliczenia, odczyty z tekstur, albo połączenie obu metod. Więcej w [instrukcji shaderów](/manuals/shader).

## Gamepads (Gamepads)

![Gamepads](images/icons/gamepad.png){.left} Plik zasobu gamepads określa, jak wejścia z konkretnych urządzeń gamepad są mapowane na wyzwalacze wejścia dla danej platformy. Szczegóły znajdziesz w [instrukcji wejścia](/manuals/input).

## Game object (Obiekt gry)

![Game object](images/icons/game-object.png){.left} Obiekty gry to proste obiekty mające własny cykl życia podczas działania gry. Są kontenerami i zwykle zawierają komponenty wizualne albo dźwiękowe, takie jak sound lub sprite. Mogą też mieć zachowanie dodane przez komponenty skryptowe. Tworzysz je i umieszczasz w kolekcjach w edytorze albo generujesz dynamicznie w czasie działania za pomocą factory. Więcej w [instrukcji o blokach budujących](/manuals/building-blocks).

## GUI (GUI)

![GUI component](images/icons/gui.png){.left} Komponent GUI zawiera elementy służące do budowy interfejsów użytkownika: tekst oraz kolorowe lub teksturowane bloki. Elementy można organizować hierarchicznie, skryptować i animować. Komponenty GUI zwykle służą do tworzenia HUD-ów, systemów menu i powiadomień na ekranie. Sterują nimi skrypty GUI, które definiują zachowanie GUI i obsługę interakcji użytkownika. Więcej w [dokumentacji GUI](/manuals/gui).

## GUI script (Skrypt GUI)

![GUI script](images/icons/script.png){.left} Skrypty GUI służą do sterowania zachowaniem komponentów GUI. Kontrolują animacje GUI i sposób, w jaki użytkownik wchodzi z nimi w interakcję. Szczegóły znajdziesz w [instrukcji Lua w Defold](/manuals/lua).

## Hot reload (Szybkie przeładowanie)

Edytor Defold pozwala aktualizować zawartość już uruchomionej gry na desktopie i urządzeniach. Ta funkcja jest bardzo potężna i może znacząco usprawnić proces tworzenia. Więcej w [instrukcji hot reload](/manuals/hot-reload).

## Input binding (Wiązania wejść)

![Input binding](images/icons/input-binding.png){.left} Pliki Input binding określają, jak gra ma interpretować wejścia sprzętowe, takie jak mysz, klawiatura, ekran dotykowy i gamepad. Plik mapuje wejścia sprzętowe na wysokopoziomowe akcje wejściowe, takie jak jump i move_forward. W komponentach skryptowych nasłuchujących wejścia możesz opisać, jakie działania ma wykonać gra lub aplikacja po otrzymaniu określonego wejścia. Szczegóły znajdziesz w [instrukcji wejścia](/manuals/input).

## Label (Etykieta)

![Label](images/icons/label.png){.left} Komponent Label pozwala dołączyć tekst do dowolnego obiektu gry. Renderuje fragment tekstu przy użyciu określonego fontu, w przestrzeni gry. Więcej w [instrukcji etykiety](/manuals/label).

## Library (Biblioteka)

![Game object](images/icons/builtins.png){.left} Defold pozwala współdzielić dane między projektami za pomocą mechanizmu bibliotek. Możesz z niego korzystać, aby tworzyć współdzielone biblioteki dostępne we wszystkich projektach, dla siebie albo dla całego zespołu. Więcej w [dokumentacji bibliotek](/manuals/libraries).

## Lua language (Język Lua)

Język programowania Lua jest używany w Defold do tworzenia logiki gry. Lua to mały, wydajny i bardzo elastyczny język skryptowy. Obsługuje programowanie proceduralne, obiektowe, funkcyjne, oparte na danych oraz opis danych. Więcej o języku znajdziesz na oficjalnej stronie Lua: https://www.lua.org/ oraz w [instrukcji Lua w Defold](/manuals/lua).

## Lua module (Moduł Lua)

![Lua module](images/icons/lua-module.png){.left} Moduły Lua pozwalają strukturyzować projekt i tworzyć wielokrotnego użytku kod biblioteczny. Więcej w [instrukcji modułów Lua](/manuals/modules/).

## Material (Materiał)

![Material](images/icons/material.png){.left} Materiały definiują sposób renderowania różnych obiektów przez określenie shaderów i ich właściwości. Więcej w [instrukcji materiałów](/manuals/material).

## Message (Wiadomość)

Komponenty komunikują się ze sobą i z innymi systemami za pomocą przekazywania wiadomości. Reagują też na zestaw predefiniowanych wiadomości, które zmieniają ich stan albo wyzwalają konkretne działania. Możesz wysyłać wiadomości, aby ukrywać grafikę lub poruszać obiektami fizycznymi. Silnik używa też wiadomości do powiadamiania komponentów o zdarzeniach, na przykład gdy kształty fizyczne zderzają się ze sobą. Mechanizm przekazywania wiadomości wymaga odbiorcy dla każdej wysłanej wiadomości. Dlatego wszystko w grze ma unikalny adres. Aby ułatwić komunikację między obiektami, Defold rozszerza Lua o przekazywanie wiadomości. Defold udostępnia też bibliotekę przydatnych funkcji.

Na przykład kod Lua potrzebny do ukrycia komponentu sprite na obiekcie gry wygląda tak:

```lua
msg.post("#weapon", "disable")
```

Tutaj `"#weapon"` jest adresem komponentu sprite bieżącego obiektu. `"disable"` to wiadomość, na którą reagują komponenty sprite. Dokładniejsze wyjaśnienie działania tego mechanizmu znajdziesz w [dokumentacji przekazywania wiadomości](/manuals/message-passing).

## Model (Model)

![Model](images/icons/model.png){.left} Komponent modelu 3D może importować zasoby siatki, szkieletu i animacji glTF do gry. Więcej w [instrukcji modelu](/manuals/model/).

## ParticleFX (ParticleFX)

![ParticleFX](images/icons/particlefx.png){.left} Cząstki są bardzo przydatne do tworzenia efektownych wizualnie efektów, szczególnie w grach. Możesz ich użyć do mgły, dymu, ognia, deszczu albo opadających liści. Defold zawiera rozbudowany edytor ParticleFX, który pozwala budować i dostrajać efekty podczas ich działania w czasie rzeczywistym. Szczegóły znajdziesz w [dokumentacji ParticleFX](/manuals/particlefx).

## Profiling (Profilowanie)

Dobra wydajność jest kluczowa w grach, dlatego ważne jest, aby móc profilować wydajność i pamięć, mierzyć grę oraz znajdować wąskie gardła i problemy z pamięcią wymagające naprawy. Więcej o dostępnych w Defold narzędziach profilujących znajdziesz w [instrukcji profilowania](/manuals/profiling).

## Render (Render)

![Render](images/icons/render.png){.left} Pliki Render zawierają ustawienia używane podczas renderowania gry na ekranie. Określają, którego render script użyć do renderowania oraz jakich materiałów użyć. Więcej w [instrukcji renderowania](/manuals/render/).

## Render script (Skrypt do renderowania)

![Render script](images/icons/script.png){.left} Render script to skrypt Lua sterujący tym, jak gra lub aplikacja ma być renderowana na ekranie. Istnieje domyślny render script, który pokrywa większość typowych przypadków, ale możesz napisać własny, jeśli potrzebujesz niestandardowych modeli oświetlenia i innych efektów. Szczegóły działania pipeline renderowania i wykorzystania skryptów Lua w Defold znajdziesz w [instrukcji renderowania](/manuals/render/) oraz w [instrukcji Lua w Defold](/manuals/lua).

## Script (Skrypt)

![Script](images/icons/script.png){.left} Skrypt to komponent zawierający program definiujący zachowanie obiektu gry. Dzięki skryptom możesz określić zasady gry i sposób, w jaki obiekty mają reagować na różne interakcje, zarówno z graczem, jak i z innymi obiektami. Wszystkie skrypty są pisane w Lua. Aby pracować z Defold, ty lub ktoś z twojego zespołu musi nauczyć się programować w Lua. Omówienie Lua i szczegóły użycia skryptów Lua w Defold znajdziesz w [instrukcji Lua w Defold](/manuals/lua).

## Sound (Dźwięk)

![Sound](images/icons/sound.png){.left} Komponent sound odpowiada za odtwarzanie określonego dźwięku. Obecnie Defold obsługuje pliki WAV i Ogg Vorbis. Więcej w [instrukcji dźwięku](/manuals/sound).

## Sprite (Sprite)

![Sprite](images/icons/sprite.png){.left} Sprite to komponent, który rozszerza obiekty gry o grafikę. Wyświetla obraz z Tile source albo Atlasu. Sprite ma wbudowaną obsługę animacji poklatkowych i animacji opartych na kościach. Sprite’y są zwykle używane do postaci i przedmiotów.

## Texture profiles (Profile teksturowania)

![Texture profiles](images/icons/texture-profiles.png){.left} Plik zasobu texture profiles jest używany w procesie bundlowania do automatycznego przetwarzania i kompresowania danych obrazowych w atlasach, Tile source, Cubemapach oraz osobnych teksturach używanych w modelach, GUI i innych elementach. Więcej w [instrukcji profili teksturowania](/manuals/texture-profiles).

## Tile map (Mapa kafelków)

![Tile map](images/icons/tilemap.png){.left} Komponent tile map wyświetla obrazy z tile source w jednej lub kilku nakładających się siatkach. Najczęściej służy do tworzenia otoczenia gry: podłoża, ścian, budynków i przeszkód. Tile map może wyświetlać kilka warstw wyrównanych jedna nad drugą z określonym trybem mieszania. Przydaje się to na przykład do umieszczania roślinności nad kafelkami trawy. Można też dynamicznie zmieniać obraz wyświetlany w kafelku. Pozwala to na przykład zniszczyć most i uczynić go nieprzejezdnym, po prostu zastępując kafelki obrazami zniszczonego mostu i odpowiednimi kształtami fizyki. Więcej w [dokumentacji tile map](/manuals/tilemap).

## Tile source (Źródło kafelków)

![Tile source](images/icons/tilesource.png){.left} Tile source opisuje teksturę złożoną z wielu mniejszych obrazów o tym samym rozmiarze. Można z niej definiować animacje poklatkowe na podstawie sekwencji obrazów. Tile source może też automatycznie obliczać kształty kolizji z danych obrazu. Jest to bardzo przydatne przy tworzeniu kafelkowych poziomów, z którymi obiekty mogą się zderzać i wchodzić w interakcje. Tile source są używane przez komponenty tile map, a także Sprite i ParticleFX, do współdzielenia zasobów graficznych. Zwróć uwagę, że atlasy często lepiej się sprawdzają niż tile source. Więcej w [dokumentacji tile map](/manuals/tilemap).

## Vertex shader (Vertex shader)

![Vertex shader](images/icons/vertex-shader.png){.left} Vertex shader oblicza geometrię ekranu dla prymitywnych kształtów wielokąta danego komponentu. Dla każdego typu komponentu wizualnego, czy to sprite, tile map czy model, kształt jest reprezentowany przez zbiór pozycji wierzchołków wielokąta. Program vertex shader przetwarza każdy wierzchołek w przestrzeni świata i oblicza końcowe współrzędne, jakie powinien mieć każdy wierzchołek prymitywu. Więcej w [instrukcji shaderów](/manuals/shader).
