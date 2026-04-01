---
title: Praca offline
brief: Ta instrukcja opisuje, jak pracować offline w projektach zawierających zależności, a w szczególności rozszerzenia natywne.
---

# Praca offline

W większości przypadków Defold nie wymaga połączenia z internetem. Są jednak sytuacje, w których jest ono potrzebne:

* Automatyczne aktualizacje
* Zgłaszanie problemów
* Pobieranie zależności
* Budowanie rozszerzeń natywnych


## Automatyczne aktualizacje

Defold okresowo sprawdza, czy są dostępne nowe aktualizacje. To sprawdzanie odbywa się na [oficjalnej stronie pobierania](https://d.defold.com). Jeśli aktualizacja zostanie wykryta, zostanie automatycznie pobrana.

Jeśli masz połączenie z internetem tylko przez krótki czas i nie chcesz czekać, aż automatyczna aktualizacja uruchomi się sama, możesz ręcznie pobrać nowe wersje Defold z [oficjalnej strony pobierania](https://d.defold.com).


## Zgłaszanie problemów

Jeśli w edytorze zostanie wykryty problem, otrzymasz możliwość zgłoszenia go do trackera problemów Defold. Ten tracker jest [hostowany na GitHubie](https://www.github.com/defold/editor2-issues), więc do zgłoszenia problemu potrzebujesz połączenia z internetem.

Jeśli napotkasz problem w trybie offline, możesz zgłosić go później ręcznie, korzystając z [opcji <kbd>Report Issue</kbd> w menu <kbd>Help</kbd>](/manuals/getting-help/#report-a-problem-from-the-editor) w edytorze.


## Pobieranie zależności

Defold obsługuje mechanizm, dzięki któremu twórcy mogą współdzielić kod i zasoby za pomocą [projektów bibliotek (Library Projects)](/manuals/libraries/). Biblioteki są plikami ZIP, które można hostować w dowolnym miejscu w sieci. Projekty bibliotek Defold zwykle znajdziesz na GitHubie i w innych internetowych repozytoriach kodu źródłowego.

Projekt może dodać bibliotekę jako [zależność projektu w ustawieniach projektu](/manuals/project-settings/#dependencies). Zależności są pobierane lub aktualizowane, gdy projekt zostanie otwarty albo gdy z menu *<kbd>Project</kbd>* wybierzesz *<kbd>Fetch Libraries</kbd>*.

Jeśli musisz pracować offline w wielu projektach, możesz pobrać zależności z wyprzedzeniem, a następnie udostępniać je za pomocą lokalnego serwera. Zależności z GitHuba są zwykle dostępne na karcie Releases w repozytorium projektu:

![Adres URL biblioteki na GitHubie](images/libraries/libraries_library_url_github.png)

Możesz łatwo utworzyć lokalny serwer za pomocą Pythona:

    python -m SimpleHTTPServer

To utworzy serwer w bieżącym katalogu, który udostępnia pliki pod adresem `localhost:8000`. Jeśli bieżący katalog zawiera pobrane zależności, możesz dodać je do pliku *game.project*:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Budowanie rozszerzeń natywnych

Defold obsługuje mechanizm, dzięki któremu twórcy mogą dodawać kod natywny, aby rozszerzać możliwości silnika, za pomocą [Native Extensions](/manuals/extensions/). Defold zapewnia prosty punkt wejścia do pracy z rozszerzeniami natywnymi dzięki rozwiązaniu budowania opartemu na chmurze.

Przy pierwszym budowaniu projektu zawierającego rozszerzenie natywne kod natywny zostanie skompilowany do niestandardowego silnika Defold na serwerach budowania Defold i odesłany na Twój komputer. Taki silnik zostanie zapisany w pamięci podręcznej projektu i będzie używany ponownie przy kolejnych kompilacjach, o ile nie dodasz, nie usuniesz ani nie zmienisz żadnych rozszerzeń natywnych oraz nie zaktualizujesz edytora.

Jeśli musisz pracować offline, a Twój projekt zawiera rozszerzenia natywne, musisz wcześniej przynajmniej raz zbudować go pomyślnie, aby mieć pewność, że w pamięci podręcznej projektu znajduje się kopia niestandardowego silnika.
