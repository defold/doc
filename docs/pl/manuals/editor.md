---
title: Edytor Defold
brief: Ta instrukcja opisuje ogólnie Edytor Defold, jak wygląda i działa oraz jak w nim się poruszać.
---

# Edytor Defold

Edytor Defold pozwala przeglądać i zarządzać plikami w Twoim projekcie w wydajny sposób. Edytowanie różnych plików otwiera odpowiednie widoki ukazujące wszystkie niezbędne informacje.

## Uruchamianie Edytora

Kiedy uruchamiasz Edytor Defold zostaje najpierw otwarte okno wyboru i tworzenia projektu. Wybierz spośród:

Home (Strona domowa)
: Kliknij, żeby zobaczyć swoje ostatnio otwierane projekty. To jest domyślny widok.

New Project (Nowy Projekt)
: Kliknij, jeśli chcesz stworzyć nowy projekt. Następnie wybierz bazę swojego projektu spośród dostępnych szablonów (z zakładki *From Template*), tutoriali (*From Tutorial*) lub wypróbować jecen z przykładowych projektów (*From Sample*).

  ![new project](images/editor/new_project.png)

  Kiedy utworzysz nowy projekt będzie on zapisany na Twoim lokalnym dysku, tak jak wszystkie zmiany, które w nim zrobisz.

Szczegóły dotyczące różnych zakładek znajdziesz w [instrukcji do rozpoczynania projektu](https://www.defold.com/manuals/project-setup/).

## Widoki w Edytorze

Edytor Defold jest podzielony na oddzielne widoki/sekcje, które zawierają specyficzne informacje.

![Editor 2](images/editor/editor2_overview.png)

Widok *Assets* (Zasoby)
: Zawiera listę wszystkich plików projektu, reprezentowaną podobnie do systemowego eksploratora plików, zgodnie z hierarchią katalogów. Możesz klikać, przewijać i rozwijać elementy:

   - <kbd>Kliknij dwukrotnie lewym przyciskem myszki</kbd> nazwę pliku, żeby otworzyć go w Edytorze.
   - <kbd>Przeciągaj i upuszczaj</kbd> pliki, aby zmieniać ich lokalizację w strukturze projektu lub dodawać nowe pliki z dysku.
   - <kbd>Kliknij prawy przycisk myszki</kbd>, żeby otworzyć _menu kontekstowe_, z którego możesz utworzyć nowe pliki i foldery, zmienić nazwę, usunąć czy śledzić zależności i wiele więcej.

Widok *Editor* (Edytor)

: Centralna sekcja wyświetla aktualnie otwarty plik w Edytorze odpowiedniem dla danego typu pliku. Wszystkie rodzaje takich Edytorów, które są wizualne pozwalają na manipulację widokiem kamery:

- Przesuwanie: <kbd>Alt + Lewy przycisk myszki</kbd>.
- Oddalanie/przybliżanie: <kbd>Alt + Prawy przycisk myszki</kbd> (myszki trójprzyciskowe) lub <kbd>Ctrl + Lewy przycisk myszki</kbd> (jeden przycisk). Jeśli myszka ma kółko, może ono być również używane do przybliżania i oddalania.
- Obracaj w 3D: <kbd>Ctrl + Lewy przycisk myszki</kbd>.

W prawym górnym rogu Edytora aktualnie otwartego pliku (sceny) znajduje się zestaw narzędzi obsługi widoku kamery: *Move* (Przesuwanie), *Rotate* (Obracanie) and *Scale* (Skalowanie).

![toolbar](images/editor/toolbar.png)

Widok *Outline* (Zawartość pliku)
: Widok ten pokazuje zawartość aktualnie otwartego pliku, w strukturze drzewa. Odzwierciedla widok Edytora i pozwala na wykonywanie operacji na zawartości:

   - <kbd>Kliknij lewym przyciskem myszki</kbd> aby wybrać wskazany element. Przytrzymaj klawisz <kbd>Shift</kbd> lub <kbd>Option</kbd>, żeby zaznaczyć wiele elementów.
   - <kbd>Przeciągaj i upuszczaj</kbd> elementy, żeby zmieniać ich położenie w strukturze. Upuść obiekty gry (game object) na innym obiekcie w kolekcji, żeby stworzyć relację rodzic-dziecko.
   - <kbd>Kliknij prawy przycisk myszki</kbd>, żeby otworzyć _menu kontekstowe_, z którego możesz utworzyć nowe komponenty, usunąć wybrane i wiele więcej.

Widok *Properties* (Właściwości))
: Widok ten pokazuje właściwości aktualnie wybranego komponentu, takie jak Pozycja, Rotacja, Animacja, Id, etc.

Widok *Tools* (Narzędzia)
: Dolny widok pokazuje w zależności od wybranej zakładki: konsolę (ang. *Console*) wyświetlającą logi działającego programu, Edytor krzywych (ang. *Curve Editor*) umożliwiający edytowanie wykresu krzywej, używany np. przy tworzeniu efektów cząsteczkowych (particle fx), błędy budowania (ang. *Build Errors*) i wyniki wyszukiwania (ang. *Search Results*). Konsola jest również używana podczas używania zintegrowanego debuggera.

Widok *Changed Files* (Zmienione pliki):
: Widok pokazuje wszystkie pliki, które zostały zmienione, dodane lub usunięte z Twojego projektu od ostatniej zapisanej w systemie kontroli wersji zmiany (commit). This view lists any files that has been changed, added or deleted in your project. By synchronizing the project regularly you can bring your local copy in sync with what is stored in the project Git repository, that way you can collaborate within a team, and you won’t lose your work if unfortune strikes. Some file oriented operations can be performed in this view:

   - <kbd>Double click</kbd> a file to open a diff view of the file. Editor 2 opens the file in a suitable editor, just like in the assets view.
   - <kbd>Right click</kbd> a file to open a pop up menu from where you can open a diff view, revert all changes done to the file, find the file on the filesystem and more (editor 2).

## Edytowanie równolegle (Side-by-side)

Jeśli masz otwartych kilka plików jednocześnie, dla każdego z nich pokazywana jest osobna zakładka na górnym pasku Edytora Defold. Możliwe jest również otworzenie dwóch Edytorów/.paneli naraz, jeden obok drugiego. Wybierz plik, <kbd>klikająć prawym przyciskiem myszy</kbd> na danej zakładce w górnym pasku i wybierz <kbd>Move to Other Tab Pane</kbd> z menu kontekstowego.

![2 panes](images/editor/2-panes.png)

Następnie, możesz również z tego samego menu kontekstowego wybrać opcje <kbd>Swap With Other Tab Pane</kbd>, żeby zamienić panele miejscami lub <kbd>Join Tab Panes</kbd>, żeby z powrotem połączyć panele w jeden.

## Edytor sceny

Kliknij dwukrotnie lewym przyciskiem myszki na kolekcji lub obiekcie gry, żeby otworzyć *Edytor Sceny*:

![Select object](images/editor/select.png)

Wybieranie obiektów:
: Kliknij na obiekt w głównym oknie, żeby go wybrać. Prostokąt wokół wybranego obiektu zostanie podświetlony na zielono. Wybrany obiekty zostanie również podświetlony w widoku *Outline* po prawej stronie.

  Obiekty możesz wybierać również:

  - <kbd>Klikając i przeciągając</kbd>, żeby wybrać wszystkie obiekty w zaznaczonym, prostokątnym obszarze.
  - <kbd>Klikając</kbd> na obiekt w widoku Outline po prawej stronie.

  Naciśnij i przytrzymaj <kbd>Shift</kbd> lub <kbd>⌘</kbd> (Mac) / <kbd>Ctrl</kbd> (Win/Linux) podczas wybierania obiektów, aby wybrać więcej na raz.

Narzędzie przesuwania (Move)
: ![Move tool](images/editor/icon_move.png){.left}
  Do przesuwania obiektów można użyć narzędzia przesuwania *Move*. Znajdziesz je w pasku narzędzi w prawym górnym rogu Edytora sceny lub klikając klawisz <kbd>W</kbd>.

  ![Move object](images/editor/move.png)

  Nad wybranym obiektem wyświetla się zestaw wizualnych manipulatorów (kwadraty i strzałki). Klikaj i przeciągaj środkowym kwadratem, aby dowolnie przesuwać obiektem po ekranie lub klikaj i przeciągaj pojedyncze strzałki, aby przesuwać obiekt tylko wzdłuż wybranej osi. Są tutaj również kwadratowe wskaźniki umożliwiające poruszanie się po płaszczyznach XY oraz X-Z i Y-Z (widoczne po obróceniu kamery).

Narzędzie obracania (Rotate)
: ![Rotate tool](images/editor/icon_rotate.png){.left}
  Do obracania obiektów, można użyć narzędzia obracania *Rotate* wybierając je z górnego paska narzędzi lub naciskając klawisz <kbd>E</kbd>.

  ![Move object](images/editor/rotate.png)

  Nad wybranym obiektem wyświetla się zestaw wizualnych, okrągłych manipulatorów. Pomarańczowy manipulator obraca obiektem w płaszczyźnie ekranu, a pozostałe wokół osi X, Y i Z. Pamiętaj, że domyślny widok jest prostopadły do osi X i Y, więc okręgi służące do obrotu wokół tych osi są widoczne wtedy po prostu jako linie.

Narzędzie skalowania (Scale)
: ![Scale tool](images/editor/icon_scale.png){.left}
  Do skalowania obiektów, można użyć narzędzia skalowania *Scale* wybierając je z górnego paska narzędzi lub naciskając klawisz <kbd>R</kbd>.

  ![Scale object](images/editor/scale.png)

  Nad wybranym obiektem wyświetla się zestaw wizualnych, kwadratowych manipulatorów. Środkowy kwadrat skaluje obiekt jednakowo wzdłuż każdej z osi (włącznie z osią Z), a pozostałe odpowiednio wokół osi X, Y i Z. Oprócz tego pokazane są wtedy również kwadraty pozwalające na skalowanie wzdłuż dwóch osi jednocześnie, parami: X-Y, X-Z i Y-Z.

## Tworzenie nowego pliku

Żeby utworzyć nowy plik kliknij z górnego menu <kbd>File ▸ New...</kbd> i wybierz typ pliku z menu lub użyj menu kontekstowego:

<kbd>Kliknij prawy przycisk myszki</kbd> na docelowej lokalizacji w panelu *Assets* po lewej stronie i wybierz <kbd>New... ▸ [file type]</kbd>:

![create file](images/editor/create_file.png)

Podaj odpowiednią nazwę dla pliku. Pełna nazwa pliku uwzględniająca końcówkę znajduję się w polu *Path* (ścieżka) w oknie dialogowym:

![create file name](images/editor/create_file_name.png)

## Importowanie plików do projektu

Aby dodać pliki (obrazki, dźwięki, modele, itp.) do Twojego projektu, po prostu przeciągnij i upuść je w odpowiednim miejscu w panelu *Assets* po lewej stronie. Utworzysz w ten sposób _kopię_ danego pliku w docelowej lokalizacji projektu. Przeczytaj więcej na temat [importowania plików w tej instrukcji](/manuals/importing-assets/).

![Import files](images/editor/import.png)

## Aktualizowanie Edytora

Edytor automatycznie wyszukuje aktualizacje, jeśli ma dostęp do internetu. Kiedy aktualizacja jest dostępna, informacja o możliwości zaktualizowania pojawi się w prawym dolnym rogu Edytora i na stronie startowej z wyborem projektu. Naciśnięcie przycisku `Update Available` spowoduje pobranie aktualizacji i zainstalowanie jej.

![Update from project selection](images/editor/update-project-selection.png)

![Update from editor](images/editor/update-main.png)

## Skróty klawiszowe

Skróty opisane są w [instrukcji o skrótach klawiszowych](/manuals/editor-keyboard-shortcuts).

## Logi Edytora
Jeśli napotkasz jakiekolwiek problemy z Edytorem Defold warto [to zaraportować](/manuals/getting-help/#getting-help). Dobrą pkratyką jest dodanie plików z logami z Edytora. Można je znaleźć tutaj:

  * Windows: `C:\Użytkownicy\ **Twoja nazwa użytkownika** \AppData\Local\Defold` (ang: `C:\Users\ **Your Username** \AppData\Local\Defold`)
  * macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
  * Linux: `~/.Defold`

Można też dostać się do logów, kiedy Edytor jest uruchomiony z linii poleceń lub terminalu. Aby uruchomić Edytor z terminalu w systemie macOS użyj komendy:

```
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```


## FAQ
:[Editor FAQ](../shared/editor-faq.md)
