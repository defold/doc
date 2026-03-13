---
title: Zarządzanie zasobami w Defold
brief: Ta instrukcja wyjaśnia, jak Defold automatycznie zarządza zasobami i jak ręcznie sterować ich ładowaniem, by pilnować zużycia pamięci oraz rozmiaru bundla.
---

# Zarządzanie zasobami

Jeśli tworzysz bardzo małą grę, ograniczenia platformy docelowej, takie jak zużycie pamięci, rozmiar bundla, moc obliczeniowa czy pobór energii, mogą w ogóle nie stanowić problemu. Jednak przy większych grach, szczególnie na urządzeniach mobilnych, zużycie pamięci bywa jednym z najważniejszych ograniczeń. Doświadczony zespół przygotowuje budżety zasobów z uwzględnieniem ograniczeń platformy. Defold udostępnia zestaw funkcji pomagających zarządzać pamięcią i rozmiarem bundla. Ta instrukcja daje ich przegląd.

## Statyczne drzewo zasobów

Podczas budowania gry w Defold statycznie deklarujesz drzewo zasobów. Każdy element gry jest włączony do tego drzewa, począwszy od kolekcji bootstrapowej, zwykle o nazwie `main.collection`. Drzewo zasobów podąża za wszystkimi odwołaniami i zawiera wszystkie zasoby z nimi powiązane:

- dane obiektów gry i komponentów, takie jak atlasy czy dźwięki
- prototypy komponentów Factory, czyli obiekty gry i kolekcje
- odwołania komponentów pełnomocników kolekcji
- [Custom Resources](/manuals/project-settings/#custom-resources) zadeklarowane w *game.project*

![Resource tree](images/resource/resource_tree.png)

::: sidenote
Defold ma też pojęcie [bundle resources](/manuals/project-settings/#bundle-resources). Są one dołączane do bundla aplikacji, ale nie należą do drzewa zasobów. Mogą to być zarówno pliki pomocnicze specyficzne dla platformy, jak i zewnętrzne pliki [wczytywane z systemu plików](/manuals/file-access/#how-to-access-files-bundled-with-the-application) i używane przez grę, na przykład banki dźwięków FMOD.
:::

Podczas *bundlowania* do gry zostanie dołączone tylko to, co znajduje się w drzewie zasobów. Wszystko, do czego nie prowadzi żadne odwołanie w drzewie, zostanie pominięte. Nie trzeba ręcznie wybierać, co uwzględnić lub wykluczyć.

Podczas *uruchamiania* gry silnik startuje od bootstrapowego korzenia drzewa i ładuje zasoby do pamięci:

- wszystkie wskazane kolekcje wraz z ich zawartością
- obiekty gry i dane komponentów
- prototypy komponentów Factory

Silnik nie ładuje jednak automatycznie następujących typów zasobów wskazanych w drzewie:

- kolekcji światów gry wskazywanych przez pełnomocników kolekcji; światy gry są relatywnie duże, więc ich ładowanie i zwalnianie trzeba wyzwalać ręcznie w kodzie; szczegóły znajdziesz w [instrukcji Collection proxy](/manuals/collection-proxy)
- plików dodanych przez ustawienie *Custom Resources* w *game.project*; te pliki wczytuje się ręcznie funkcją [`sys.load_resource()`](/ref/sys/#sys.load_resource)

Domyślny sposób bundlowania i ładowania zasobów w Defold można zmieniać, aby precyzyjnie sterować tym, kiedy i jak zasoby trafiają do pamięci.

![Resource loading](images/resource/loading.png)

## Dynamiczne ładowanie zasobów Factory

Zasoby wskazywane przez komponenty Factory są zwykle ładowane do pamięci razem z samym komponentem. Dzięki temu są gotowe do użycia od razu, gdy Factory istnieje w czasie działania. Aby zmienić to zachowanie i odroczyć ładowanie zasobów Factory, zaznacz pole *Load Dynamically*.

![Load dynamically](images/resource/load_dynamically.png)

Po zaznaczeniu tego pola silnik nadal dołączy wskazane zasoby do bundla gry, ale nie załaduje ich automatycznie. Zamiast tego masz dwie możliwości:

1. Wywołaj [`factory.create()`](/ref/factory/#factory.create) albo [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create), gdy chcesz tworzyć obiekty. Spowoduje to synchroniczne załadowanie zasobów, a następnie utworzenie nowych instancji.
2. Wywołaj [`factory.load()`](/ref/factory/#factory.load) albo [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load), aby załadować zasoby asynchronicznie. Gdy będą gotowe do tworzenia instancji, otrzymasz callback.

Szczegóły działania znajdziesz w [instrukcji Factory](/manuals/factory) i [instrukcji Collection factory](/manuals/collection-factory).

## Zwalnianie dynamicznie wczytanych zasobów

Defold utrzymuje liczniki referencji dla wszystkich zasobów. Jeśli licznik zasobu spadnie do zera, oznacza to, że nic już się do niego nie odwołuje. Wtedy zasób jest automatycznie usuwany z pamięci. Przykładowo, jeśli usuniesz wszystkie obiekty utworzone przez Factory i dodatkowo usuniesz obiekt zawierający komponent Factory, zasoby wcześniej wskazywane przez tę fabrykę zostaną zwolnione.

Dla fabryk oznaczonych jako *Load Dynamically* możesz wywołać [`factory.unload()`](/ref/factory/#factory.unload) albo [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload). To wywołanie usuwa referencję komponentu Factory do zasobu. Jeśli nic innego nie odwołuje się już do tego zasobu, na przykład wszystkie utworzone obiekty zostały usunięte, zasób zostanie zwolniony z pamięci.

## Wykluczanie zasobów z bundla

W przypadku pełnomocników kolekcji można pominąć w procesie bundlowania wszystkie zasoby, do których odwołuje się komponent. Jest to przydatne, jeśli chcesz zminimalizować rozmiar bundla. Na przykład przy uruchamianiu gry w przeglądarce jako HTML5 przeglądarka pobiera cały bundle przed rozpoczęciem wykonywania gry.

![Exclude](images/resource/exclude.png)

Po oznaczeniu pełnomocnika kolekcji jako *Exclude* wskazany zasób nie trafi do bundla gry. Zamiast tego wykluczone kolekcje możesz przechowywać w wybranej chmurze. [Instrukcja Live update](/manuals/live-update/) wyjaśnia, jak działa ta funkcja.
