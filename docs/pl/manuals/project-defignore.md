---
title: Ignorowanie plików w projekcie Defold
brief: Ten podręcznik opisuje, jak ignorować pliki i foldery w Defold.
---

# Ignorowanie plików

Można skonfigurować edytor Defold i narzędzia tak, aby ignorowały pliki i foldery w projekcie. Jest to przydatne, jeśli projekt zawiera pliki z rozszerzeniami, które kolidują z rozszerzeniami używanymi przez Defold. Jednym z takich przykładów są pliki języka Go z rozszerzeniem `.go`, które jest takie samo jak to używane przez edytor dla plików obiektów gry (ang. game object).

## Plik `.defignore`
Pliki i foldery przeznaczone do wykluczenia są definiowane w pliku o nazwie `.defignore` w katalogu głównym projektu. Plik powinien zawierać listę plików i folderów do wykluczenia, po jednym wierszu na wpis. Przykład:

```
/path/to/file.png
/otherpath
```

To spowoduje wykluczenie pliku `/path/to/file.png` oraz wszystkiego pod ścieżką `/otherpath`.

## Plik `.defunload`

W przypadku niektórych dużych projektów zawierających wiele niezależnych modułów możesz chcieć wykluczyć część z nich z ładowania, aby zmniejszyć użycie pamięci i skrócić czas ładowania w edytorze. Aby to zrobić, możesz umieścić ścieżki przeznaczone do wykluczenia z ładowania w pliku `.defunload` poniżej katalogu projektu.

W praktyce plik `.defunload` pozwala ukryć część projektu przed edytorem, bez powodowania błędu kompilacji przy odwoływaniu się do ukrytych zasobów.

Wzorce w pliku `.defunload` używają tych samych reguł co plik `.defignore`. Niewczytane kolekcje i obiekty gry będą zachowywać się tak, jakby były puste, gdy odwołują się do nich załadowane zasoby. Inne zasoby pasujące do wzorców `.defunload` znajdą się w stanie niewczytanym i nie będzie można ich wyświetlić w edytorze. Jeśli jednak załadowany zasób będzie od nich zależał, niewczytane zasoby i ich zależności zostaną załadowane automatycznie.

Na przykład, jeśli sprite zależy od obrazów w atlasie, atlas musi zostać załadowany, w przeciwnym razie brakujący obraz zostanie zgłoszony jako błąd. Jeśli tak się stanie, powiadomienie ostrzeże użytkownika o sytuacji i poda informacje o tym, który niewczytany zasób został przywołany i skąd.

Edytor uniemożliwi użytkownikowi dodawanie odwołań do zasobów `.defunloaded` z poziomu załadowanych zasobów, więc taka sytuacja występuje tylko wtedy, gdy zasoby są odczytywane z dysku.

W przeciwieństwie do pliku `.defignore`, po edycji pliku `.defunload` trzeba uruchomić ponownie edytor, aby zmiany zaczęły obowiązywać.
