---
title: Preferencje edytora
brief: Ustawienia edytora możesz zmieniać w oknie Preferences.
---

# Preferencje edytora

Ustawienia edytora możesz zmieniać w oknie Preferences. Okno otwiera się z menu <kbd>File -> Preferences</kbd>.

## General (Ogólne)

![](images/editor/preferences_general.png)

Load External Changes on App Focus (Wczytaj zewnętrzne zmiany po aktywowaniu aplikacji)
: Włącza skanowanie zmian zewnętrznych, gdy edytor odzyskuje fokus.

Open Bundle Target Folder (Otwórz folder docelowy pakietu)
: Włącza otwieranie folderu docelowego bundla po zakończeniu procesu bundlowania.

Enable Texture Compression (Włącz kompresję tekstur)
: Włącza [kompresję tekstur](/manuals/texture-profiles) dla wszystkich buildów wykonywanych z poziomu edytora.

Escape Quits Game (Klawisz Escape zamyka grę)
: Zamyka uruchomiony build gry po naciśnięciu <kbd>Esc</kbd>.

Track Active Tab in Asset Browser (Śledź aktywną kartę w przeglądarce zasobów)
: Plik edytowany na aktualnie wybranej karcie w panelu *Editor* zostanie zaznaczony w Asset Browser, nazywanym też panelem *Asset*.

Lint Code on Build
: Włącza [linting kodu](/manuals/writing-code/#konfiguracja-lintingu) podczas budowania projektu. Ta opcja jest domyślnie włączona, ale można ją wyłączyć, jeśli linting w dużym projekcie trwa zbyt długo.

Engine Arguments
: Argumenty przekazywane do pliku wykonywalnego `dmengine`, gdy edytor buduje i uruchamia projekt.
 Używaj jednego argumentu na linię. Na przykład:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```

## Code

![](images/editor/preferences_code.png)

Custom Editor (Niestandardowy Edytor)
: Bezwzględna ścieżka do zewnętrznego edytora. W macOS powinna to być ścieżka do pliku wykonywalnego wewnątrz `.app`, na przykład `/Applications/Atom.app/Contents/MacOS/Atom`.

Open File
: Wzorzec używany przez zewnętrzny edytor do wskazania pliku, który ma zostać otwarty. Wzorzec `{file}` zostanie zastąpiony nazwą pliku.

Open File at Line
: Wzorzec używany przez zewnętrzny edytor do wskazania pliku i numeru linii. `{file}` zostanie zastąpione nazwą pliku, a `{line}` numerem linii.

Code editor font
: Nazwa czcionki zainstalowanej w systemie, używanej w edytorze kodu.

Zoom on Scroll
: Określa, czy podczas przewijania w edytorze kodu z wciśniętym Cmd/Ctrl ma się zmieniać rozmiar czcionki.

### Otwieranie plików skryptów w Visual Studio Code

![](images/editor/preferences_vscode.png)

Aby otwierać pliki skryptów z edytora Defold bezpośrednio w Visual Studio Code, ustaw poniższe wartości, podając ścieżkę do pliku wykonywalnego:

- macOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

Ustaw te parametry, aby otwierać konkretne pliki i linie:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

Znak `.` jest tutaj wymagany, aby otworzyć cały obszar roboczy, a nie pojedynczy plik.

## Extensions

![](images/editor/preferences_extensions.png)

Serwer budowania (Build Server)
: URL serwera buildów używanego podczas budowania projektu zawierającego [native extensions](/manuals/extensions). Do URL można dodać nazwę użytkownika i token dostępu, aby uwierzytelnić się przy dostępie do serwera buildów. Użyj notacji `username:token@build.defold.com`. Uwierzytelniony dostęp jest wymagany przy buildach na Nintendo Switch oraz przy korzystaniu z własnej instancji serwera buildów z włączonym uwierzytelnianiem ([zobacz dokumentację serwera buildów](https://github.com/defold/extender/blob/dev/README_SECURITY.md)). Nazwę użytkownika i hasło można też ustawić w zmiennych środowiskowych `DM_EXTENDER_USERNAME` i `DM_EXTENDER_PASSWORD`.

Build Server Username
: Nazwa użytkownika do uwierzytelniania.

Build Server Password
: Hasło do uwierzytelniania. Zostanie zapisane w pliku preferencji w postaci zaszyfrowanej.

Build Server Headers
: Dodatkowe nagłówki wysyłane do serwera buildów podczas budowania rozszerzeń natywnych. Jest to ważne przy korzystaniu z CloudFlare lub podobnych usług razem z extenderem.

## Tools

![](images/editor/preferences_tools.png)

ADB path (Ścieżka ADB)
: Ścieżka do narzędzia wiersza poleceń [ADB](https://developer.android.com/tools/adb) zainstalowanego w systemie. Jeśli ADB jest dostępne, edytor Defold użyje go do instalowania i uruchamiania zbudowanych plików APK na podłączonym urządzeniu z Androidem. Domyślnie edytor sprawdza kilka znanych lokalizacji, więc ścieżkę trzeba podawać tylko wtedy, gdy ADB jest zainstalowane niestandardowo.

ios-deploy path (Ścieżka ios-deploy)
: Ścieżka do narzędzia wiersza poleceń [ios-deploy](https://github.com/ios-control/ios-deploy) zainstalowanego w systemie. Dotyczy to tylko macOS. Podobnie jak przy `ADB path`, edytor Defold użyje tego narzędzia do instalowania i uruchamiania zbundlowanych aplikacji iOS na podłączonym iPhonie. Domyślnie edytor sprawdza kilka znanych lokalizacji, więc ścieżkę trzeba podać tylko wtedy, gdy korzystasz z niestandardowej instalacji `ios-deploy`.

## Keymap

![](images/editor/preferences_keymap.png)

Możesz konfigurować skróty klawiszowe edytora, zarówno dodając własne, jak i usuwając wbudowane. Aby edytować skrót, użyj menu kontekstowego dla wybranego polecenia w tabeli skrótów albo kliknij dwukrotnie lub naciśnij <kbd>Enter</kbd>, aby otworzyć okno dodawania nowego skrótu.

Przy niektórych skrótach mogą pojawić się ostrzeżenia, wyświetlane na pomarańczowo. Najedź kursorem na skrót, aby zobaczyć szczegóły. Typowe ostrzeżenia to:
- typeable shortcuts: wybrany skrót można wpisać w polach tekstowych. Upewnij się, że polecenie jest wyłączone w kontekstach edycji kodu i wprowadzania tekstu.
- conflicts: ten sam skrót jest przypisany do wielu różnych poleceń. Upewnij się, że w chwili wywołania skrótu aktywne jest najwyżej jedno z nich, w przeciwnym razie edytor wykona jedno z przypisanych poleceń w nieokreślony sposób.
