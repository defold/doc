---
title: Mapa RPG - przykładowy projekt
brief: W tym przykładowym projekcie poznasz jeden ze sposobów tworzenia bardzo dużych map RPG.
---
# Mapa RPG - przykładowy projekt

W tym przykładowym projekcie, który możesz [otworzyć w edytorze](/manuals/project-setup/) albo [pobrać z GitHuba](https://github.com/defold/sample-rpgmap), pokazujemy jeden ze sposobów tworzenia bardzo dużych map RPG w silniku Defold. Projekt opiera się na następujących założeniach:

1. Świat jest prezentowany po jednym ekranie naraz. Dzięki temu gra może naturalnie zawierać wrogów i postacie NPC w granicach pojedynczego ekranu. Projektant poziomów ma pełną kontrolę nad tym, jak świat jest prezentowany na ekranie gracza.
2. Postać gracza powinna móc podróżować dowolnie daleko bez pojawiania się problemów z precyzją zmiennoprzecinkową. Zwykle powoduje to dziwne drżenie obiektów, gdy oddalą się od początku układu współrzędnych.
3. Ruch gracza jest ograniczany przez przeszkody na mapie, więc projektant poziomów może prowadzić gracza między ekranami za pomocą drzew, skał, wody i innych przeszkód.
4. Powinno dać się dowolnie łączyć mapy kafelków, sprite'y i inną zawartość wizualną.

Najpierw uruchom przykład i przejdź przez świat o wymiarach 3x3 ekranów, żeby poczuć jego układ. Postacią sterujesz klawiszami strzałek.

## Główna kolekcja

Otwórz `"/main/main.collection"`, aby zobaczyć kolekcję bootstrapową tego przykładu.

![](images/rpgmap/main_collection.png)

Główna kolekcja zawiera obiekt gry postaci gracza sterowany klawiszami strzałek w 8 kierunkach oraz drugi obiekt gry o nazwie `game`, który kontroluje przebieg gry. Obiekt gry (ang. game object) `game` składa się ze skryptu i po jednym komponencie fabryki kolekcji (Collection factory) dla każdego ekranu w grze. Fabryki noszą nazwy zgodnie ze schematem nazewnictwa siatki ekranów.

Skrypt `"/main/game.script"` śledzi, na którym ekranie znajduje się obecnie gracz. Skrypt reaguje też na niestandardową wiadomość `load_screen`. Ta wiadomość wczytuje nowy ekran i zamienia go miejscami z bieżącym ekranem w kierunku ruchu bohatera. Na początku ekran jest wczytywany na środku widoku i nie ma jeszcze innego ekranu, z którym można by go zamienić.

## Zmiana ekranów

Bohaterem steruje skrypt `"/main/hero.script"`. Skrypt sprawdza, czy obiekt gry bohatera przekracza górną, dolną, lewą lub prawą linię położoną blisko krawędzi ekranu:

![](images/rpgmap/change_screen.png)

1. Gdy bohater zbliży się wystarczająco do krawędzi ekranu, do skryptu obiektu `game` jest wysyłana wiadomość, aby wczytać następny ekran.
2. Następna kolekcja ekranu jest tworzona przez wywołanie `factory.create()` na odpowiednim komponencie Collection factory. Zawartość kolekcji jest ustawiana poza ekranem.
3. Następny ekran przesuwa się do środka widoku, a bieżący ekran przesuwa się w przeciwnym kierunku. Postać gracza przesuwa się też o tę samą odległość i z tą samą prędkością.
4. Stary bieżący ekran, który jest już poza ekranem, zostaje usunięty, a następny ekran staje się nowym bieżącym ekranem.
5. Bohater pojawia się z animacją w nowym ekranie, a gracz odzyskuje sterowanie.

Wszystko to dzieje się w ciągu sekundy, więc przejście jest płynne i nie zakłóca rozgrywki.

## Ekrany

Każdy ekran w świecie gry jest zbudowany w osobnej kolekcji zawierającej mapę kafelków (ang. tilemap), obiekt kolizji (ang. collision object) i inne obiekty gry unikalne dla danego ekranu. Aby ułatwić zarządzanie ekranami i ich wczytywanie, kolekcje ekranów nazwano według prostego schematu:

![](images/rpgmap/screens.png)

Każda kolekcja ekranu nosi nazwę zgodną ze swoją pozycją w siatce świata. Pierwsza liczba to pozycja X w siatce, a druga to pozycja Y.

W widoku *Assets* przejdź do kolekcji `"/main/screens/0-0.collection"` i otwórz ją. Opisuje ona ekran w lewym dolnym rogu mapy:

![](images/rpgmap/screen_collection.png)

Zauważ, że istnieje obiekt gry o nazwie `root`, który jest rodzicem całej zawartości ekranu. To kolejna konwencja użyta w przykładzie i ma bardzo ważne znaczenie: kiedy ekran pojawia się w widoku, trzeba przesunąć tylko obiekt gry `root`. Wszystkie obiekty potomne są automatycznie przesuwane razem z obiektem nadrzędnym. Jeśli na ekranie są specjalne obiekty gry, można je też swobodnie animować, ponieważ ich ruch jest względny wobec obiektu nadrzędnego `root`. Gdy ekran jest przewijany do widoku lub poza niego, te obiekty potomne poruszają się razem z ekranem. Dodatkowy kod jest potrzebny tylko wtedy, gdy obiekt musi przemieszczać się między ekranami.

Pszczoły na ekranie 0-1 są prostą ilustracją tego pomysłu:

![](images/rpgmap/bees.png)

## Edycja ekranów w kontekście świata

Każdy ekran ma własną mapę kafelków, którą można edytować we wbudowanym edytorze map kafelków. Główną wadą pracy nad każdym ekranem w izolacji jest to, że trudno wtedy zobaczyć, jak łączy się on z sąsiednimi ekranami, a to ważny element budowania ciągłości w świecie gry.

Z tego powodu utworzono specjalną kolekcję. Otwórz `"/main/map/test_layout.collection"`, aby zobaczyć tę kolekcję testowego układu świata:

![](images/rpgmap/test_layout.png)

Jedynym celem tej kolekcji jest służenie jako narzędzie edycyjne podczas tworzenia gry. Edytowanie konkretnego ekranu obok kolekcji testowego układu daje kontekst dla ekranu, nad którym właśnie pracujesz, i znacznie uprzyjemnia pracę:

![](images/rpgmap/side_by_side.png)

Wszelkie zmiany w mapie kafelków ekranu (tutaj w prawym panelu) są natychmiast widoczne w kolekcji testowej (w lewym panelu). Zwróć też uwagę, że kolekcja testowego układu nie jest dodawana do statycznej hierarchii, więc jest automatycznie wykluczana ze wszystkich buildów.

## Podsumowanie

Jak widzisz, ten przykład został zbudowany zgodnie z określonymi ograniczeniami dotyczącymi świata gry i sposobu, w jaki bohater przez niego przechodzi. Jeśli twoja gra ma inne wymagania, prawdopodobnie potrzebujesz innego rozwiązania. Na przykład jeśli gra wymaga, by kamera poruszała się płynnie po mapie świata, potrzebujesz innego sposobu podziału zawartości, innego mechanizmu wczytywania, a także innych narzędzi pomagających tworzyć świat gry.

To kończy omówienie przykładowej mapy RPG. Jak zawsze możesz używać zawartości przykładu w dowolny sposób. Aby dowiedzieć się więcej o Defold, zajrzyj na nasze [strony dokumentacji](https://defold.com/learn) z dodatkowymi przykładami, samouczkami, instrukcjami i dokumentacją API.

Jeśli napotkasz problem albo masz pytania, [odwiedź nasze forum](https://forum.defold.com/).

Miłego tworzenia!
