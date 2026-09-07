---
title: Ignorowanie plików projektu Defold
brief: Ten podręcznik opisuje, jak ignorować pliki i foldery w projekcie Defold.
---

# Ignorowanie plików

Można skonfigurować edytor Defold i narzędzia tak, aby ignorowały pliki i foldery w projekcie. Jest to przydatne, jeśli projekt zawiera pliki z rozszerzeniami, które kolidują z rozszerzeniami używanymi przez Defold. Jednym z takich przykładów są pliki języka Go z rozszerzeniem `.go`, które jest takie samo jak to używane przez edytor dla plików obiektów gry.

## Plik `.defignore`
Pliki i foldery do wykluczenia są definiowane w pliku o nazwie `.defignore` w katalogu głównym projektu. Plik powinien zawierać listę plików i folderów do wykluczenia, po jednym wpisie na wiersz. Przykład:

```
/path/to/file.png
/otherpath
```

To wykluczy plik `/path/to/file.png` oraz wszystko pod ścieżką `/otherpath`.
Każdy wiersz musi zaczynać się od `/` i jest dopasowywany do ścieżek projektu względem katalogu głównego projektu. Wzorzec pasuje do ścieżki, jeśli jest jej równy lub jest jednym z jej folderów nadrzędnych. Dopasowanie rozróżnia wielkość liter.

### Symbole wieloznaczne

Wzorce mogą zawierać symbole wieloznaczne:

* `*` pasuje do dowolnej liczby znaków z wyjątkiem `/`
* `?` pasuje do dokładnie jednego znaku z wyjątkiem `/`
* `**` pasuje do dowolnej liczby znaków, włącznie z `/`

Wszystkie pozostałe znaki są dopasowywane dosłownie. Przykład:

```
/levels/*/tiled
/**/generated
/assets/temp_??.png
```

To wykluczy folder `tiled` w każdym bezpośrednim podfolderze `/levels` (na przykład `/levels/01/tiled`), każdy folder o nazwie `generated` w dowolnym podfolderze oraz pliki takie jak `/assets/temp_01.png`.

Zwróć uwagę, że `**` nie pasuje do otaczających go ukośników, więc `/levels/**` pasuje do wszystkiego wewnątrz `/levels`, ale nie do samego folderu `/levels`, a `/**/generated` nie pasuje do `/generated` w katalogu głównym projektu.

## Plik `.defunload`

W przypadku niektórych dużych projektów zawierających wiele niezależnych modułów możesz chcieć wykluczyć część z nich z ładowania, aby zmniejszyć użycie pamięci i skrócić czas ładowania w edytorze. Aby to zrobić, możesz umieścić ścieżki przeznaczone do wykluczenia z ładowania w pliku `.defunload` w katalogu projektu.

W praktyce plik `.defunload` pozwala ukryć część projektu przed edytorem, nie powodując błędu budowania, gdy odwołujesz się do ukrytych zasobów.

Wzorce w pliku `.defunload` używają tych samych reguł co plik `.defignore`. Niewczytane kolekcje i obiekty gry będą zachowywać się tak, jakby były puste, gdy odwołują się do nich załadowane zasoby. Inne zasoby pasujące do wzorców `.defunload` znajdą się w stanie niewczytanym i nie będzie można ich wyświetlić w edytorze. Jeśli jednak załadowany zasób będzie od nich zależał, niewczytane zasoby i ich zależności zostaną załadowane automatycznie.

Na przykład, jeśli sprite zależy od obrazów w atlasie, atlas musi zostać załadowany, w przeciwnym razie brakujący obraz zostanie zgłoszony jako błąd. Jeśli tak się stanie, powiadomienie ostrzeże użytkownika o sytuacji i poda informacje o tym, który niewczytany zasób został przywołany i skąd.

Edytor uniemożliwi użytkownikowi dodawanie odwołań do zasobów `.defunload` z poziomu załadowanych zasobów, więc taka sytuacja występuje tylko wtedy, gdy zasoby są odczytywane z dysku.

W przeciwieństwie do pliku `.defignore`, po edycji pliku `.defunload` trzeba uruchomić ponownie edytor, aby zmiany zaczęły obowiązywać.
