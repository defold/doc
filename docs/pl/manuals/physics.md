---
title: Fizyka w Defoldzie
brief: Ta instrukcja prezentuje fizykę w Defoldzie.
---

# Fizyka

Defold zawiera zmodyfikowaną wersję silnika fizycznego [Box2D](http://www.box2d.org) (wersja 2.1) do symulacji fizyki 2D oraz silnik fizyczny Bullet (wersja 2.77) do fizyki 3D. Pozwala to na symulację oddziaływań fizyki klasycznej Newtona między różnymi rodzajami obiektów kolizji (_collision objects_). Ta instrukcja wyjaśnia, jak to działa.

Główne koncepcje silników fizycznych używanych w Defoldzie to:

* **Collision objects** - Obiekt kolizji - komponent, który stosujesz, aby nadać obiektowi gry właściwości fizyczne. Obiekt kolizji posiada właściwości fizyczne, takie jak masa, tarcie i kształt. [Dowiedz się, jak tworzyć obiekt kolizji](/manuals/physics-objects).
* **Collision shapes** - Kształty kolizi - obiekty kolizji mogą używać kilku kształtów podstawowych (primitive shapes) lub pojedynczego kształtu złożonego (complex shape), aby określić jego rozszerzenie przestrzenne (spatial extension). [Dowiedz się, jak dodawać kształty do obiektu kolizji](/manuals/physics-groups).
* **Collision groups** - Grupy kolizji - wszystkie obiekty kolizji muszą należeć do zdefiniowanej grupy, a każdy obiekt kolizji może określić listę innych grup, z którymi może kolidować. [Dowiedz się, jak korzystać z grup kolizji](/manuals/physics-groups).
* **Collision messages** - Wiadomości kolizji - gdy dwa obiekty kolizji zderzają się, silnik fizyczny wysyła wiadomości do obiektów gry, do których należą komponenty obiektów kolizji. [Dowiedz się więcej o wiadomościach kolizji](/manuals/physics-messages).

Oprócz samych obiektów kolizji, można również definiować ograniczenia (**constraints**) obiektu kolizji, bardziej znane jako łączenia (**joints**), aby połączyć ze sobą dwa obiekty kolizji i ograniczyć lub w inny sposób zastosować siłę oraz wpływać na ich zachowanie w symulacji fizycznej. [Dowiedz się więcej o łączeniach](/manuals/physics-joints).

Możesz również badać i odczytywać świat fizyczny wzdłuż specjalnego liniowego promienia (**ray cast**). [Dowiedz się więcej o promieniach](/manuals/physics-ray-casts).

## Jednostki używane w symulacji silnika fizycznego

Silnik fizyczny symuluje fizykę klasyczną Newtona i został zaprojektowany do współpracy z jednostkami MKS - metrów, kilogramów i sekund. Ponadto silnik fizyczny jest dostrojony, aby dobrze działał z poruszającymi się obiektami o rozmiarze w zakresie od 0,1 do 10 metrów (obiekty statyczne mogą być większe), a domyślnie silnik traktuje 1 jednostkę (piksel) jako 1 metr. Ta konwersja między pikselami a metrami jest wygodna na poziomie symulacji, ale z perspektywy tworzenia gier nie jest zbyt przydatna. Domyślnie kształt kolizji o rozmiarze 200 pikseli jest traktowany jako obiekt o rozmiarze 200 metrów, co jest znacznie poza zalecanym zakresem, przynajmniej dla obiektu poruszającego się.

W ogólności wymagane jest dostosowanie skali symulacji fizycznej, aby działała dobrze z typowym rozmiarem obiektów w grze. Skalę symulacji fizycznej można zmienić w pliku *game.project* za pomocą ustawienia skali fizyki - [physics scale setting](/manuals/project-settings/#physics). Ustawienie tej wartości na przykład na 0,02 oznacza, że 200 pikseli będzie traktowane jako 4 metry. Należy zauważyć, że grawitacja (również zmieniana w *game.project*) musi zostać zwiększona, aby dostosować się do zmiany skali.

## Aktualizacja fizyki

Zaleca się regularną aktualizację silnika fizycznego, aby zapewnić stabilną symulację (w przeciwieństwie do aktualizacji w nieregularnych odstępach czasu zależnych od częstotliwości klatek). Możesz używać stałej aktualizacji dla fizyki, zaznaczając opcję używania stałego kroku czasowego: ["Use Fixed Timestep"](/manuals/project-settings/#physics) w sekcji `Physics` w pliku *game.project*. Częstotliwość aktualizacji jest kontrolowana przez częstotliwość stałej aktualizacji: ["Fixed Update Frequency"](/manuals/project-settings/#engine) w sekcji `Engine` w pliku *game.project*. Gdy używasz stałego kroku czasowego dla fizyki, zaleca się również korzystanie ze specjalnej funkcji cyklu życia `fixed_update(self, dt)` do interakcji z obiektami kolizji w grze, na przykład podczas stosowania sił do nich.

## Uwagi i typowe problemy

Pełnomocnicy kolekcji
: za pomocą pełnomocników kolekcji (collection proxies) można załadować więcej niż jedną kolekcję najwyższego poziomu lub inaczej *świat gry* do silnika. Przy takim rozwiązaniu ważne jest, aby wiedzieć, że każda kolekcja najwyższego poziomu to *osobny* świat fizyczny. Interakcje fizyczne ([kolizje, trigery/wyzwalacze](/manuals/physics-messages) i [promienie ray-cast](/manuals/physics-ray-casts))

Kolizje nie wykrywane
: Jeśli masz problemy z obsługą lub właściwym wykrywaniem kolizji, upewnij się, że zapoznałeś się z [debugowaniem fizyki w instrukcji debugowania](/manuals/debugging/#debugging-problems-with-physics).
