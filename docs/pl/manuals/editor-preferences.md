---
title: Preferencje edytora
brief: Możesz zmieniać ustawienia edytora w oknie Preferences.
---

# Preferencje edytora

Możesz zmieniać ustawienia edytora w oknie Preferences. Okno otwierasz z menu <kbd>File -> Preferences</kbd>.

## General

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Włącza wyszukiwanie zmian zewnętrznych, gdy edytor odzyskuje fokus.

Open Bundle Target Folder
: Włącza otwieranie folderu docelowego bundla po zakończeniu procesu bundlowania.

Enable Texture Compression
: Włącza [kompresję tekstur](/manuals/texture-profiles) dla wszystkich buildów tworzonych z edytora.

Escape Quits Game
: Zamyka uruchomiony build gry po naciśnięciu <kbd>Esc</kbd>.

Track Active Tab in Asset Browser
: Plik edytowany na wybranej karcie w panelu *Editor* zostanie zaznaczony w Asset Browser, znanym też jako panel *Asset*.

Lint Code on Build
: Włącza [lintowanie kodu](/manuals/writing-code/#linting-configuration) podczas budowania projektu. Ta opcja jest włączona domyślnie, ale można ją wyłączyć, jeśli lintowanie w dużym projekcie trwa zbyt długo.

Engine Arguments
: Argumenty przekazywane do pliku wykonywalnego dmengine, gdy edytor buduje i uruchamia projekt.
 Używaj jednego argumentu na linię. Na przykład:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```

## Code

![](images/editor/preferences_code.png)

Custom Editor
: Bezwzględna ścieżka do zewnętrznego edytora. Na macOS powinna to być ścieżka do pliku wykonywalnego wewnątrz .app, na przykład `/Applications/Atom.app/Contents/MacOS/Atom`.

Open File
: Wzorzec używany przez zewnętrzny edytor do wskazania pliku, który ma zostać otwarty. Wzorzec `{file}` zostanie zastąpiony nazwą pliku do otwarcia.

Open File at Line
: Wzorzec używany przez zewnętrzny edytor do wskazania pliku i numeru linii. Wzorzec `{file}` zostanie zastąpiony nazwą pliku do otwarcia, a `{line}` numerem linii.

Code editor font
: Nazwa czcionki zainstalowanej w systemie, której używa edytor kodu.

Zoom on Scroll
: Określa, czy podczas przewijania w edytorze kodu z wciśniętym przyciskiem Cmd/Ctrl ma się zmieniać rozmiar czcionki.

Auto-insert closing parens
: Automatycznie wstawia pasujące znaki zamykające podczas edytowania kodu. Ta opcja jest domyślnie włączona.

### Otwieranie plików skryptów w Visual Studio Code

![](images/editor/preferences_vscode.png)

Aby otwierać pliki skryptów z Defold Editor bezpośrednio w Visual Studio Code, ustaw poniższe wartości, podając ścieżkę do pliku wykonywalnego:

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

Ustaw te parametry, aby otwierać konkretne pliki i linie:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

Znak `.` jest tutaj wymagany, aby otworzyć cały obszar roboczy, a nie pojedynczy plik.

## Extensions

![](images/editor/preferences_extensions.png)

Build Server
: Adres URL serwera buildów używanego podczas budowania projektu zawierającego [native extensions](/manuals/extensions). Możesz dodać do adresu URL nazwę użytkownika i token dostępu, aby korzystać z uwierzytelnionego dostępu do serwera buildów. Użyj zapisu `username:token@build.defold.com`. Uwierzytelniony dostęp jest wymagany przy buildach dla Nintendo Switch oraz podczas korzystania z własnej instancji build servera z włączonym uwierzytelnianiem ([zobacz dokumentację build servera](https://github.com/defold/extender/blob/dev/README_SECURITY.md), aby uzyskać więcej informacji). Nazwę użytkownika i hasło można też ustawić jako zmienne środowiskowe `DM_EXTENDER_USERNAME` i `DM_EXTENDER_PASSWORD`.

Build Server Username
: Nazwa użytkownika do uwierzytelniania.

Build Server Password
: Hasło do uwierzytelniania. Zostanie zapisane w pliku preferencji w postaci zaszyfrowanej.

Build Server Headers
: Dodatkowe nagłówki wysyłane do build servera podczas budowania native extensions. Jest to ważne przy korzystaniu z CloudFlare lub podobnych usług razem z extenderem.

## Tools

![](images/editor/preferences_tools.png)

ADB path
: Ścieżka do narzędzia wiersza poleceń [ADB](https://developer.android.com/tools/adb) zainstalowanego w tym systemie. Jeśli ADB jest zainstalowane, edytor Defold użyje go do instalowania i uruchamiania zbudowanych APK na podłączonym urządzeniu z Androidem. Domyślnie edytor sprawdza znane lokalizacje, więc ścieżkę trzeba podać tylko wtedy, gdy ADB jest zainstalowane w niestandardowym miejscu.

ios-deploy path
: Ścieżka do narzędzi wiersza poleceń [ios-deploy](https://github.com/ios-control/ios-deploy) zainstalowanych w tym systemie. Dotyczy to tylko macOS. Podobnie jak w przypadku ścieżki ADB, edytor Defold użyje tego narzędzia do instalowania i uruchamiania zbundlowanych aplikacji iOS na podłączonym iPhonie. Domyślnie edytor sprawdza znane lokalizacje, więc ścieżkę trzeba podać tylko wtedy, gdy korzystasz z niestandardowej instalacji ios-deploy.

## Keymap

![](images/editor/preferences_keymap.png)

Możesz konfigurować skróty klawiaturowe edytora i sterowanie myszą w zakładce Keymap. Aby zmienić polecenie, kliknij je dwukrotnie, naciśnij <kbd>Enter</kbd> albo <kbd>Space</kbd>, albo użyj menu kontekstowego wiersza.

Skróty klawiaturowe są widoczne jako kombinacje klawiszy w kolumnie *Shortcuts*. Sterowanie myszą pojawia się na tej samej liście z oznaczeniem:

- <kbd>MB</kbd> oznacza przypisanie przycisku myszy, opcjonalnie połączone z <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd> lub <kbd>Alt</kbd>.
- <kbd>MM</kbd> oznacza klawisz modyfikujący używany przez akcję myszy.

Niektóre elementy sterowania myszą ponownie wykorzystują przypisania z domyślnej Scene 2D Camera, więc wiersz może pokazywać przypisanie jeszcze przed jego dostosowaniem. Zwykle są one wyświetlane ciemniejszym kolorem. Jeśli ustawisz własne przypisanie dla tego wiersza, Defold użyje go zamiast domyślnego. Użyj *Reset to Defaults*, aby usunąć zmianę i wrócić do działania wbudowanego lub odziedziczonego.

Ostrzeżenia są wyświetlane na pomarańczowo. Najedź na ostrzeżenie, aby zobaczyć szczegóły. Ostrzeżenia zwykle oznaczają:
- skrót można wpisać jako tekst i może on kolidować z polami tekstowymi.
- ten sam skrót albo przypisanie myszy jest już używane przez inne polecenie.
