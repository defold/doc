## Optymalizacja limitów liczby komponentów

Plik ustawień *game.project* zawiera wiele wartości określających maksymalną liczbę danego zasobu, który może istnieć jednocześnie, zwykle w przeliczeniu na załadowaną kolekcję, nazywaną też światem (ang. world). Silnik Defold używa tych wartości do wstępnej alokacji pamięci, aby ograniczyć dynamiczne alokacje i fragmentację pamięci podczas działania gry.

Struktury danych Defold używane do reprezentowania komponentów i innych zasobów są zoptymalizowane pod kątem jak najmniejszego zużycia pamięci, ale przy ustawianiu tych wartości nadal trzeba zachować ostrożność, aby nie przydzielać więcej pamięci, niż naprawdę potrzeba.

Aby dodatkowo zoptymalizować zużycie pamięci, proces budowania w Defold analizuje zawartość gry i nadpisuje wartości maksymalne tam, gdzie można z całkowitą pewnością określić dokładną liczbę:

* Jeśli kolekcja nie zawiera żadnych komponentów `Factory`, zostanie zaalokowana dokładna liczba każdego komponentu i obiektu gry, a wartości maksymalne zostaną zignorowane.
* Jeśli kolekcja zawiera komponent `Factory`, obiekty tworzone przez tę fabrykę zostaną przeanalizowane, a dla komponentów możliwych do utworzenia przez `Factory` oraz dla obiektów gry zostaną użyte wartości maksymalne.
* Jeśli kolekcja zawiera komponent `Factory` albo `Collection factory` z włączoną opcją `Dynamic Prototype`, ta kolekcja będzie używać liczników maksymalnych.
