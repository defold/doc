---
title: Praca z bibliotekami w Defold
brief: Funkcja bibliotek pozwala dzielić zasoby między projektami. Ten podręcznik wyjaśnia, jak to działa.
---

# Biblioteki (Libraries)

Funkcja Bibliotek pozwala dzielić zasoby między projektami. To proste, ale bardzo potężne narzędzie, które możesz wykorzystać na wiele sposobów.

Biblioteki są przydatne w następujących sytuacjach:

* aby skopiować zasoby z gotowego projektu do nowego. Jeśli tworzysz sequel swojej wcześniejszej gry, to łatwy sposób, aby szybko ruszyć z pracą.
* aby stworzyć bibliotekę szablonów, które można kopiować do projektów i potem dostosowywać albo specjalizować.
* aby zbudować jedną lub więcej bibliotek gotowych obiektów lub skryptów, do których można się odwołać bezpośrednio. To wygodne przy przechowywaniu wspólnych modułów skryptowych albo wspólnych zasobów graficznych, dźwiękowych i animacyjnych.

## Ustawianie udostępniania biblioteki

Załóżmy, że chcesz zbudować bibliotekę zawierającą wspólne sprite’y oraz źródła kafelków (tile sources). Rozpocznij od [utworzenia nowego projektu](/manuals/project-setup/). Zdecyduj, które foldery chcesz udostępnić z projektu, i dopisz ich nazwy do właściwości *`include_dirs`* w ustawieniach projektu (w pliku *game.project*). Jeśli chcesz wymienić więcej niż jedną lokalizację, oddziel nazwy spacjami:

![Include directories](images/libraries/libraries_include_dirs.png)

Zanim dodasz tę bibliotekę do innego projektu, musisz podać sposób na jej znalezienie.

## URL biblioteki

Biblioteki odwołują się przez standardowy adres URL. Dla projektu hostowanego na GitHubie będzie to adres URL do wydania projektu:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: important
Zalecane jest, żeby zawsze opierać się na konkretnym wydaniu (release) projektu biblioteki zamiast na gałęzi głównej (master). Dzięki temu to Ty decydujesz, kiedy wprowadzić zmiany z biblioteki do swojego projektu, zamiast automatycznie pobierać najnowsze (i potencjalnie łamiące) zmiany z gałęzi master.
:::

::: important
Zaleca się zawsze przejrzeć biblioteki stron trzecich przed ich użyciem. Dowiedz się więcej o [bezpieczeństwie przy korzystaniu z bibliotek stron trzecich](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Podstawowe uwierzytelnianie

Do adresu URL biblioteki możesz dodać nazwę użytkownika i hasło/token, aby wykonać podstawowe uwierzytelnianie, gdy biblioteka nie jest publicznie dostępna:

```
https://username:password@github.com/defold/private/archive/main.zip
```

Pola `username` i `password` zostaną wyciągnięte i dodane jako nagłówek żądania `Authorization`. Takie rozwiązanie działa na każdym serwerze obsługującym podstawowe uwierzytelnianie.

::: important
Uważaj, żeby nie udostępniać ani nie wyciekać swojego tokena dostępu ani hasła, bo w niepowołanych rękach może to mieć poważne konsekwencje.
:::

Aby nie trzymać poświadczeń w jawnej postaci w adresie URL, możesz użyć wzorca do zamiany ciągu i przechowywać dane jako zmienne środowiskowe:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

W powyższym przykładzie nazwa użytkownika i token zostaną pobrane ze zmiennych środowiskowych `PRIVATE_USERNAME` i `PRIVATE_TOKEN`.

#### Uwierzytelnianie GitHub

Aby pobrać zawartość prywatnego repozytorium na GitHubie, musisz [wygenerować token dostępu osobistego](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) i użyć go jako hasła.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Uwierzytelnianie GitLab

Aby pobrać zawartość prywatnego repozytorium na GitLabie, musisz [wygenerować token dostępu osobistego](https://docs.gitlab.com/ee/security/token_overview.html) i przekazać go jako parametr w adresie URL.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Zaawansowane uwierzytelnianie

Podczas korzystania z podstawowego uwierzytelniania token i nazwa użytkownika są współdzielone ze wszystkimi repozytoriami używanymi przez projekt. W większym zespole może to stanowić problem. Rozwiązaniem jest użycie użytkownika „tylko do odczytu”, który ma dostęp do biblioteki, ale nie może jej edytować. Na GitHubie wymaga to organizacji, zespołu i użytkownika tylko do odczytu.

Kroki na GitHubie:
* [Utwórz organizację](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Utwórz zespół w ramach organizacji](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Przenieś wybrane prywatne repozytorium do organizacji](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Nadaj zespołowi dostęp „tylko do odczytu” do repozytorium](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Dodaj lub wybierz użytkownika, który dołączy do zespołu](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Użyj powyższego sposobu podstawowego uwierzytelniania, aby wygenerować token dla tego użytkownika

W tym momencie dane uwierzytelniające nowego użytkownika można zatwierdzić i wypchnąć do repozytorium. Każda osoba pracująca z prywatnym repozytorium może pobierać je jako bibliotekę, nie mając jednocześnie praw do edycji.

::: important
Token użytkownika tylko do odczytu jest w pełni dostępny dla każdego, kto ma dostęp do repozytorium gry korzystającej z biblioteki.
:::

Rozwiązanie to zostało opisane na forum Defold i [przedyskutowane w tym wątku](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Ustawianie zależności do biblioteki

Otwórz projekt, w którym chcesz korzystać z biblioteki. W ustawieniach projektu dodaj adres URL biblioteki do właściwości *dependencies*. Możesz wskazać wiele projektów zależnych, dodając je jeden po drugim za pomocą przycisku `+` i usuwając przyciskiem `-`:

![Dependencies](images/libraries/libraries_dependencies.png)

Potem wybierz <kbd>Project ▸ Fetch Libraries</kbd>, aby zaktualizować zależności biblioteczne. Odbywa się to automatycznie przy otwieraniu projektu, więc będziesz musiał wykonać tę operację tylko wtedy, gdy chcesz odświeżyć zależności bez ponownego otwierania projektu — np. gdy dodasz lub usuniesz bibliotekę albo gdy ktoś zsynchronizuje zmiany w jednej z bibliotek.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Teraz foldery, które udostępniłeś, pojawią się w panelu *Assets* i możesz korzystać z wszystkich zawartych tam zasobów. Wszelkie zsynchronizowane zmiany w projekcie biblioteki będą dostępne w Twoim projekcie.

![Library setup done](images/libraries/libraries_done.png)

## Edytowanie plików w zależnościach bibliotek

Pliki z bibliotek nie mogą być zapisane. Możesz wprowadzać zmiany, a edytor uwzględni je podczas budowania, co jest przydatne do testów. Sam plik pozostanie jednak niezmieniony, a wszystkie modyfikacje zostaną odrzucone po jego zamknięciu.

Jeśli chcesz zmienić pliki biblioteki, utwórz własnego forka i wprowadź zmiany tam. Inną opcją jest skopiowanie całego katalogu biblioteki do katalogu projektu i korzystanie z lokalnej kopii. W takim przypadku lokalny folder zasłoni oryginalną zależność, więc usuń wpis w `game.project` z listy zależności (nie zapomnij potem wybrać <kbd>Project ▸ Fetch Libraries</kbd>).

`builtins` to też biblioteka dostarczana przez silnik. Jeśli chcesz edytować jej pliki, skopiuj je do projektu i korzystaj z lokalnych kopii zamiast oryginalnych plików `builtins`. Na przykład, aby zmodyfikować `default.render_script`, skopiuj zarówno `/builtins/render/default.render`, jak i `/builtins/render/default.render_script` do katalogu projektu jako `my_custom.render` i `my_custom.render_script`. Następnie edytuj lokalny `my_custom.render`, by odnosił się do `my_custom.render_script` zamiast domyślnego, a w ustawieniach Render w `game.project` ustaw swój `my_custom.render`.

Jeśli kopiujesz materiał i chcesz używać go we wszystkich komponentach pewnego typu, przydatne może być użycie [szablonów projektowych `per-project templates`](/manuals/editor/#creating-new-project-files).

## Zepsute zależności

Udostępnianie bibliotek obejmuje tylko pliki znajdujące się w udostępnionych folderach. Jeśli stworzysz coś, co odwołuje się do zasobu spoza tej struktury, ścieżki referencji zostaną zerwane.

## Kolizja nazw

Ponieważ możesz podać wiele adresów URL projektów w polu *dependencies* ustawień projektu, może pojawić się kolizja nazw. Dzieje się tak wtedy, gdy dwie lub więcej zależnych bibliotek zawierają folder o tej samej nazwie w ustawieniu *`include_dirs`*.

Defold rozwiązuje kolizje nazw, ignorując wszystko poza ostatnią referencją do folderu o danej nazwie w kolejności, w jakiej podano adresy URL w liście *dependencies*. Na przykład, jeżeli dodasz trzy biblioteki posiadające folder *items* w `include_dirs`, tylko jeden folder *items* będzie dostępny — ten z projektu będącego ostatnim na liście zależności.
