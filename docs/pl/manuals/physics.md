---
title: Fizyka w Defold
brief: Defold zawiera silniki fizyki 2D i 3D. Pozwalają one symulować newtonowskie interakcje fizyczne między różnymi typami obiektów kolizji.
---

# Fizyka

Defold zawiera zmodyfikowaną wersję silnika fizycznego [Box2D](http://www.box2d.org) (wersja 2.2.1) do symulacji fizyki 2D oraz silnik fizyczny Bullet (wersja 2.77) do fizyki 3D. Umożliwia to symulowanie interakcji zgodnych z fizyką Newtona między różnymi typami _obiektów kolizji_. Ten podręcznik wyjaśnia, jak to działa.

Główne pojęcia silników fizycznych używanych w Defold to:

* **Collision objects** - Obiekty kolizji - komponent używany do nadania obiektowi gry właściwości fizycznych. Obiekt kolizji ma właściwości fizyczne, takie jak masa, tarcie i kształt. [Dowiedz się, jak utworzyć obiekt kolizji](/manuals/physics-objects).
* **Collision shapes** - Kształty kolizji - obiekt kolizji może używać kilku prostych kształtów albo jednego złożonego kształtu, aby określić swój zasięg przestrzenny. [Dowiedz się, jak dodać kształty do obiektu kolizji](/manuals/physics-shapes).
* **Collision groups** - Grupy kolizji - wszystkie obiekty kolizji muszą należeć do zdefiniowanej grupy, a każdy obiekt kolizji może określić listę innych grup, z którymi może się zderzać. [Dowiedz się, jak używać grup kolizji](/manuals/physics-groups).
* **Collision messages** - Wiadomości kolizji - gdy dwa obiekty kolizji się zderzą, silnik fizyczny wysyła wiadomości do obiektów gry, do których należą te komponenty. [Dowiedz się więcej o wiadomościach kolizji](/manuals/physics-messages)

Oprócz samych obiektów kolizji możesz też definiować obiekt kolizji **ograniczenia**, częściej nazywane **joints**, aby połączyć dwa obiekty kolizji i ograniczyć ich ruch albo w inny sposób wpływać na ich zachowanie w symulacji fizycznej. [Dowiedz się więcej o joints](/manuals/physics-joints).

Możesz też sondować i odczytywać świat fizyczny wzdłuż liniowego promienia, znanego jako **ray cast**. [Dowiedz się więcej o ray castach](/manuals/physics-ray-casts).

## Jednostki używane przez symulację silnika fizycznego

Silnik fizyczny symuluje fizykę Newtona i został zaprojektowany tak, aby dobrze działać z jednostkami metrów, kilogramów i sekund (MKS). Ponadto silnik jest dostrojony do pracy z poruszającymi się obiektami o rozmiarze od 0,1 do 10 metrów (obiekty statyczne mogą być większe), a domyślnie traktuje 1 jednostkę (piksel) jako 1 metr. To przeliczanie pikseli na metry jest wygodne na poziomie symulacji, ale z perspektywy tworzenia gier nie jest zbyt użyteczne. Przy domyślnych ustawieniach kształt kolizji o rozmiarze 200 pikseli będzie traktowany jak obiekt o rozmiarze 200 metrów, czyli znacznie poza zalecanym zakresem, przynajmniej dla obiektu poruszającego się.

Ogólnie rzecz biorąc, trzeba przeskalować symulację fizyczną tak, aby dobrze działała z typowym rozmiarem obiektów w grze. Skalę symulacji fizycznej można zmienić w pliku *game.project* za pomocą [ustawienia skali fizyki](/manuals/project-settings/#physics). Na przykład ustawienie tej wartości na 0,02 oznaczałoby, że 200 pikseli byłoby traktowane jako 4 metry. Pamiętaj, że grawitację, również ustawianą w *game.project*, trzeba zwiększyć, aby uwzględnić zmianę skali.

## Aktualizacje fizyki

Zaleca się regularne aktualizowanie silnika fizycznego, aby zapewnić stabilną symulację, zamiast wykonywać aktualizacje w potencjalnie nieregularnych odstępach zależnych od liczby klatek na sekundę. Możesz włączyć stałą aktualizację fizyki, zaznaczając ustawienie [<kbd>Use Fixed Timestep</kbd>](/manuals/project-settings/#physics) w sekcji <kbd>Physics</kbd> pliku *game.project*. Częstotliwość aktualizacji jest kontrolowana przez ustawienie [<kbd>Fixed Update Frequency</kbd>](/manuals/project-settings/#engine) w sekcji <kbd>Engine</kbd> pliku *game.project*. Gdy używasz stałego kroku czasowego dla fizyki, zaleca się również korzystanie z funkcji cyklu życia `fixed_update(self, dt)` do interakcji z obiektami kolizji w grze, na przykład podczas przykładania do nich sił.

## Zastrzeżenia i typowe problemy

Pełnomocnicy kolekcji
: Za pomocą pełnomocników kolekcji można załadować do silnika więcej niż jedną kolekcję najwyższego poziomu, czyli *świat gry*. W takiej sytuacji ważne jest, aby wiedzieć, że każda kolekcja najwyższego poziomu jest osobnym światem fizycznym. Interakcje fizyczne ([kolizje, wyzwalacze](/manuals/physics-messages) oraz [ray casty](/manuals/physics-ray-casts)) zachodzą wyłącznie między obiektami należącymi do tego samego świata. Dlatego nawet jeśli obiekty kolizji z dwóch światów wizualnie znajdują się dokładnie w tym samym miejscu, nie może między nimi dojść do żadnej interakcji fizycznej.

Kolizje nie są wykrywane
: Jeśli masz problemy z nieprawidłową obsługą lub wykrywaniem kolizji, koniecznie przeczytaj o [debugowaniu fizyki w podręczniku Debugging](/manuals/debugging/#debugging-problems-with-physics).
