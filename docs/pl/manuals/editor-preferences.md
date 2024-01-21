---
title: Preferencje Edytora
brief: Ta instrukcja przedstawia co oznaczają i jak zmodyfikować Preferencje Edytora.
---

# Preferencje Edytora

Możesz dostosować ustawienia Edytora z poziomu okna Preferencji. Okno Preferencji otwiera się z menu <kbd>File -> Preferences</kbd>.

## General (Ogólne)

![](images/editor/preferences_general.png)

Load External Changes on App Focus (Wczytaj zewnętrzne zmiany po aktywowaniu aplikacji)
: Umożliwia skanowanie zewnętrznych zmian, gdy Edytor zostaje aktywnie wybrany w systemie.

Open Bundle Target Folder (Otwórz folder docelowy pakietu)
: Umożliwia otwarcie folderu docelowego pakietu po zakończeniu procesu pakowania.

Enable Texture Compression (Włącz kompresję tekstur)
: Umożliwia kompresję tekstur dla wszystkich kompilacji utworzonych z Edytora.

Escape Quits Game (Klawisz Escape zamyka grę)
: Zatrzymuje działającą kompilację twojej gry za pomocą klawisza <kbd>Esc</kbd>.

Track Active Tab in Asset Browser (Śledź aktywną kartę w przeglądarce zasobów)
: Plik edytowany na wybranej karcie w panelu Edytor zostanie zaznaczony w Przeglądarce Zasobów (znanej również jako panel *Assets*).

Path to custom keymap (Ścieżka do niestandardowej mapy klawiszy)
: Absolutna ścieżka do pliku zawierającego niestandardowe skróty klawiaturowe.

## Code (Kod)

![](images/editor/preferences_code.png)

Custom Editor (Niestandardowy Edytor)
: Absolutna ścieżka do zewnętrznego Edytora. Na macOS powinna to być ścieżka do pliku wykonywalnego wewnątrz .app (np. `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File (Otwórz plik)
: Wzorzec używany przez niestandardowy Edytor do określenia, który plik ma być otwarty. Wzorzec `{file}` zostanie zastąpiony nazwą pliku do otwarcia.

Open File at Line (Otwórz plik w linii)
: Wzorzec używany przez niestandardowy edytor do określenia, który plik ma być otwarty i na której linii. Wzorzec `{file}` zostanie zastąpiony nazwą pliku do otwarcia, a `{line}` numerem linii.

Code editor font (Czcionka edytora kodu)
: Nazwa zainstalowanej systemowej czcionki do użycia w edytorze kodu.

### Otwieranie plików skryptów w programie Visual Studio Code

![](images/editor/preferences_vscode.png)

Aby otworzyć pliki skryptów bezpośrednio z Edytora Defold w programie Microsoft Visual Studio Code, musisz ustawić następujące ustawienia, określając ścieżkę do pliku wykonywalnego:

- macOS: /Applications/Visual Studio Code.app/Contents/MacOS/Electron
- Linux: /usr/bin/code
- Windows: C:\Program Files\Microsoft VS Code\Code.exe

Ustaw te parametry, aby otwierać konkretne pliki i linie:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

Znak . jest wymagany, aby otworzyć cały workspace, a nie pojedynczy plik.

## Rozszerzenia

![](images/editor/preferences_extensions.png)

Serwer budowania (Build Server)
: URL serwera budowania używanego podczas kompilacji projektu zawierającego rozszerzenia natywne (native extensions). Możliwe jest dodanie nazwy użytkownika i tokena dostępowego do URL w celu autoryzowanego dostępu do serwera budowania. Aby określić nazwę użytkownika (username) i token dostępowy, użyj następującej notacji: `username:token@build.defold.com`. Autoryzowany dostęp jest wymagany dla kompilacji na platformę Nintendo Switch oraz w przypadku uruchamiania własnej instancji serwera kompilacji z włączoną autoryzacją (dokładne informacje znajdziesz w [dokumentacji serwera budowania](https://github.com/defold/extender/blob/dev/README_SECURITY.md). Nazwę użytkownika i hasło można także ustawić jako zmienne środowiskowe systemu `DM_EXTENDER_USERNAME` i `DM_EXTENDER_PASSWORD`.

Nagłówki serwera budowania
: dodatkowe nagłówki serwera budowania przy budowaniu rozszerzeń natywnych. Jest to ważne, jeśli korzystasz z usługi CloudFlare lub podobnych usług z extenderem.

## Narzędzia

![](images/editor/preferences_tools.png)

Ścieżka ADB
: Ścieżka do narzędzia linii komend [ADB](https://developer.android.com/tools/adb) zainstalowanego na tym systemie. Jeśli masz zainstalowane ADB na swoim systemie, edytor Defold użyje go do instalacji i uruchamiania spakowanych plików APK na połączonym urządzeniu z systemem Android. Domyślnie edytor sprawdza, czy ADB jest zainstalowane w znanych lokalizacjach, więc musisz podać ścieżkę tylko wtedy, gdy masz zainstalowane ADB w niestandardowym miejscu.

Ścieżka ios-deploy
: Ścieżka do narzędzi linii komend ios-deploy zainstalowanych na tym systemie (dotyczy tylko macOS). Podobnie jak w przypadku ścieżki ADB, edytor Defold będzie używać tego narzędzia do instalacji i uruchamiania spakowanych aplikacji iOS na połączonym iPhone. Domyślnie edytor sprawdza, czy ios-deploy jest zainstalowane w znanych lokalizacjach, więc musisz podać ścieżkę tylko wtedy, gdy korzystasz z niestandardowej lokalizacji własnej instalacji ios-deploy.
