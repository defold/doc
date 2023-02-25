## Pobieranie

Przejdź na [stronę pobierania Defold](https://defold.com/download/), gdzie znajdziesz przycisk "Pobierz" ("Download") dla odpowiednich systemów operacyjnych (Windows, macOS i Linux(Ubuntu)) :

![download editor](../shared/images/editor_download.png)

## Instalacja

Instalacja w systemie macOS
: Pobrany plik to obraz DMG zawierający program.

  1. Znajdź plik "Defold-x86_64-macos.dmg" i <kbd>dwukrotnie kliknij</kbd> na niego, aby otworzyć obraz.
  2. Przeciągnij aplikację "Defold" do linku folderu "Applications".

  Aby uruchomić edytor, otwórz folder "Applications" i <kbd>dwukrotnie kliknij</kbd> plik "Defold".

  ![Defold macOS](../shared/images/macos_content.png)

Instalacja w systemie Windows
: Pobrany plik to spakowane archiwum ZIP do wypakowania:

  1. Znajdź plik "Defold-x86_64-win32.zip", <kbd>kliknij prawym przyciskiem myszki</kbd> (lub <kbd>naciśnij i przytrzymaj</kbd>) archiwum i wybierz *Wypakuj pliki*(/*Extract All*), i podążaj za instrukcjami programu do wypakowywania, żeby wypakować archiwum do folderu "Defold".
  2. Przenieś folder "Defold" do "C:\Program Files (x86)\"

  Aby uruchomić edytor, otwórz folder "Defold" i <kbd>dwukrotnie kliknij</kbd> plik "Defold.exe".

  ![Defold windows](../shared/images/windows_content.png)

Instalacja w systemie Linux
: Pobrany plik to spakowane archiwum ZIP do wypakowania:

  1. W terminalu znajdź plik "Defold-x86_64-linux.zip" i wypakuj go do docelowego katalogu "Defold".

     ```bash
     $ unzip Defold-x86_64-linux.zip -d Defold
     ```

  Aby uruchomić edytor, przejdź do lokalizacji, gdzie wypakowałeś archiwum i uruchom `Defold` lub <kbd>dwukrotnie kliknij</kbd> go w eksploratorze plików.

  ```bash
  $ cd Defold
  $ ./Defold
  ```

  Jeśli napotkasz jakiekolwiek problemy podczas instalacji, uruchamiania edytora, projektu lub działania programu sprawdź to w sekcji [Linux FAQ](/faq/faq#linux-issues).

## Instalacja starszej wersji

### Ze strony Defold na GitHubie

Każda stabilna wersja Defolda jest umieszczana na [GitHubie](https://github.com/defold/defold/releases).

### Ze strony pobierania Defold

Możesz pobrać i zainstalować starsze wersje Defolda używając poniższych wzorów linków:

* Windows: https://d.defold.com/archive/%sha1%/stable/editor2/Defold-x86_64-win32.zip
* macOS: https://d.defold.com/archive/%sha1%/stable/editor2/Defold-x86_64-macos.dmg
* Linux: https://d.defold.com/archive/%sha1%/stable/editor2/Defold-x86_64-linux.zip

Gdzie zamienić należy `%sha1%` na odpowiedni hash danej wersji Defolda. Hashe każdej wersji Defolda można znaleźć na stronie https://d.defold.com/stable/ (upewnij się, że usuwasz pierwszy znak `#` i kopiujesz tylko część liczbową):

![download editor](../shared/images/old_version_sha1.png)
