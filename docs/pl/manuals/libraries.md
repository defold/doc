---
title: Praca z projektami bibliotek w Defold
brief: Funkcja Libraries pozwala udostępniać zasoby między projektami. Ten podręcznik wyjaśnia, jak to działa.
---

# Biblioteki

Funkcja Libraries pozwala udostępniać zasoby między projektami. To prosty, ale bardzo potężny mechanizm, który możesz wykorzystać na wiele sposobów.

Biblioteki są przydatne w następujących sytuacjach:

* aby skopiować zasoby z ukończonego projektu do nowego. Jeśli tworzysz kontynuację wcześniejszej gry, to prosty sposób na szybki start.
* aby zbudować bibliotekę szablonów, które można kopiować do projektów, a potem dostosowywać lub specjalizować.
* aby zbudować jedną lub więcej bibliotek gotowych obiektów lub skryptów, do których można odwoływać się bezpośrednio. To bardzo wygodne do przechowywania wspólnych modułów skryptowych albo wspólnych zasobów graficznych, dźwiękowych i animacyjnych.

## Ustawianie udostępniania biblioteki

Załóżmy, że chcesz zbudować bibliotekę zawierającą współdzielone sprite'y oraz źródła kafelków. Zacznij od [utworzenia nowego projektu](/manuals/project-setup/). Zdecyduj, które foldery chcesz udostępnić z projektu, i dodaj ich nazwy do właściwości *`include_dirs`* w ustawieniach projektu. Jeśli chcesz wymienić więcej niż jeden folder, oddziel nazwy spacjami:

![Include directories](images/libraries/libraries_include_dirs.png)

Zanim dodasz tę bibliotekę do innego projektu, musisz mieć sposób na jej odnalezienie.

## Adres URL biblioteki

Biblioteki wskazuje się za pomocą standardowego adresu URL. W przypadku projektu hostowanego na GitHubie będzie to adres URL do wydania projektu:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

::: important
Zaleca się zawsze opierać na konkretnym wydaniu projektu biblioteki zamiast na gałęzi głównej (master). Dzięki temu to Ty decydujesz, kiedy wprowadzić zmiany z projektu biblioteki do swojego projektu, zamiast zawsze pobierać najnowsze, a potencjalnie łamiące zmiany z gałęzi master.
:::

::: important
Zaleca się zawsze przejrzeć biblioteki stron trzecich przed ich użyciem. Dowiedz się więcej o [zabezpieczaniu korzystania z oprogramowania stron trzecich](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Podstawowe uwierzytelnianie

Do adresu URL biblioteki możesz dodać nazwę użytkownika i hasło lub token, aby wykonać podstawowe uwierzytelnianie, gdy biblioteka nie jest publicznie dostępna:

```
https://username:password@github.com/defold/private/archive/main.zip
```

Pola `username` i `password` zostaną wyodrębnione i dodane jako nagłówek żądania `Authorization`. Takie rozwiązanie działa na każdym serwerze obsługującym podstawowe uwierzytelnianie dostępu.

::: important
Uważaj, aby nie udostępnić ani przypadkowo nie ujawnić wygenerowanego tokena dostępu osobistego lub hasła, bo w niepowołanych rękach może to mieć poważne konsekwencje.
:::

Aby uniknąć przypadkowego ujawnienia poświadczeń zapisanych jawnym tekstem w adresie URL biblioteki, możesz użyć wzorca zamiany ciągu i przechowywać poświadczenia jako zmienne środowiskowe:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

W powyższym przykładzie nazwa użytkownika i token zostaną odczytane ze zmiennych środowiskowych `PRIVATE_USERNAME` i `PRIVATE_TOKEN`.

#### Uwierzytelnianie GitHub

Aby pobrać zawartość prywatnego repozytorium na GitHubie, musisz [wygenerować token dostępu osobistego](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) i użyć go jako hasła.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Uwierzytelnianie GitLab

Aby pobrać zawartość prywatnego repozytorium na GitLabie, musisz [wygenerować token dostępu osobistego](https://docs.gitlab.com/ee/security/token_overview.html) i przekazać go jako parametr adresu URL.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Zaawansowane uwierzytelnianie

Podczas korzystania z podstawowego uwierzytelniania token i nazwa użytkownika są współdzielone ze wszystkimi repozytoriami używanymi przez projekt. W zespole większym niż jedna osoba może to stanowić problem. Rozwiązaniem jest użycie użytkownika „tylko do odczytu”, który ma dostęp do biblioteki, ale nie może jej edytować. Na GitHubie wymaga to organizacji, zespołu i użytkownika, który nie musi edytować repozytorium.

Kroki w GitHubie:
* [Utwórz organizację](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Utwórz zespół w ramach organizacji](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Przenieś wybrane prywatne repozytorium do organizacji](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Nadaj zespołowi dostęp „tylko do odczytu” do repozytorium](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Dodaj lub wybierz użytkownika, który ma należeć do tego zespołu](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Użyj powyższego sposobu podstawowego uwierzytelniania, aby utworzyć token dostępu osobistego dla tego użytkownika

W tym momencie dane uwierzytelniające nowego użytkownika można zatwierdzić i wypchnąć do repozytorium. Każda osoba pracująca z Twoim prywatnym repozytorium będzie mogła pobierać je jako bibliotekę bez uprawnień do edycji samej biblioteki.

::: important
Token użytkownika tylko do odczytu jest w pełni dostępny dla każdego, kto ma dostęp do repozytoriów gry korzystających z tej biblioteki.
:::

To rozwiązanie zostało zaproponowane na forum Defold i [omówione w tym wątku](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Ustawianie zależności do biblioteki

Otwórz projekt, z którego chcesz korzystać z biblioteki. W ustawieniach projektu dodaj adres URL biblioteki do właściwości *dependencies*. Możesz wskazać wiele projektów zależnych, dodając je po kolei za pomocą przycisku `+` i usuwając przyciskiem `-`:

![Dependencies](images/libraries/libraries_dependencies.png)

Teraz wybierz <kbd>Project ▸ Fetch Libraries</kbd>, aby zaktualizować zależności biblioteki. Dzieje się to automatycznie przy każdym otwarciu projektu, więc tę operację trzeba wykonać tylko wtedy, gdy zależności zmienią się bez ponownego otwierania projektu. Tak będzie na przykład wtedy, gdy dodasz lub usuniesz bibliotekę zależną albo gdy ktoś zmieni i zsynchronizuje jeden z projektów bibliotek zależnych.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Teraz foldery, które udostępniłeś, pojawią się w panelu *Assets* i będziesz mógł korzystać ze wszystkich zawartych tam zasobów. Każda zsynchronizowana zmiana w projekcie biblioteki będzie dostępna w Twoim projekcie.

![Library setup done](images/libraries/libraries_done.png)

## Edytowanie plików w zależnościach bibliotek

Plików w bibliotekach nie można zapisać. Możesz wprowadzać zmiany, a edytor będzie mógł budować projekt z uwzględnieniem tych zmian, co bywa przydatne podczas testów. Sam plik pozostanie jednak niezmieniony, a wszystkie modyfikacje zostaną odrzucone po jego zamknięciu.

Jeśli chcesz zmienić pliki biblioteki, utwórz własnego forka i wprowadź zmiany tam. Inną opcją jest skopiowanie całego folderu biblioteki do katalogu projektu i korzystanie z lokalnej kopii. W takim przypadku lokalny folder zasłoni oryginalną zależność, więc usuń wpis z `game.project` z listy zależności. Nie zapomnij potem wybrać <kbd>Project ▸ Fetch Libraries</kbd>.

`builtins` to także biblioteka dostarczana przez silnik. Jeśli chcesz edytować jej pliki, skopiuj je do projektu i używaj lokalnych kopii zamiast oryginalnych plików `builtins`. Na przykład, aby zmodyfikować `default.render_script`, skopiuj zarówno `/builtins/render/default.render`, jak i `/builtins/render/default.render_script` do folderu projektu jako `my_custom.render` i `my_custom.render_script`. Następnie zaktualizuj lokalny `my_custom.render`, aby odwoływał się do `my_custom.render_script` zamiast do wbudowanego pliku, a w ustawieniach Render w `game.project` ustaw swój `my_custom.render`.

Jeśli skopiujesz materiał i chcesz używać go we wszystkich komponentach danego typu, pomocne mogą być [szablony dla poszczególnych projektów](/manuals/editor/#creating-new-project-files).

## Zerwane odwołania

Udostępnianie bibliotek obejmuje tylko pliki znajdujące się w udostępnionych folderach. Jeśli utworzysz coś, co odwołuje się do zasobu poza tą hierarchią, ścieżki odwołań zostaną zerwane.

## Kolizja nazw

Ponieważ w ustawieniu projektu *dependencies* możesz podać kilka adresów URL projektów, może pojawić się kolizja nazw. Dzieje się tak wtedy, gdy dwa lub więcej projektów zależnych ma folder o tej samej nazwie w ustawieniu *`include_dirs`*.

Defold rozwiązuje kolizje nazw, ignorując wszystko poza ostatnim odwołaniem do folderu o danej nazwie w kolejności, w jakiej adresy URL pojawiają się na liście *dependencies*. Na przykład, jeśli na tej liście podasz trzy adresy URL projektów bibliotek i każdy z nich udostępnia folder *items*, tylko jeden folder *items* będzie widoczny---ten należący do projektu, który jest ostatni na liście URL-i.
