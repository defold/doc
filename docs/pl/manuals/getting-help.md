---
title: Jak uzyskać pomoc?
brief: Instrukcja opisuje jak efektywnie i szybko uzyskać pomoc, jeśli napotkasz jakiekolwiek problemy z Defoldem.
---

# Jak uzyskać pomoc?

Jeśli napotkasz jakiekolwiek problemy z Defoldem, służymy pomocą! Postaramy się naprawić błędy i rozwiązać problemy lub pomóc Ci znaleźć inne rozwiązanie! Jest kilka sposobów na zgłoszenie i przedystkutowanie problemów. Wybierz takim który jest dla Ciebie najwygodniejszy:

## Zgłoś problem na forum

Dobrym sposobem na przedyskutowanie problemu jest zadanie pytania na naszym [forum](https://forum.defold.com). Zadaj pytanie w ogólnej kategorii: [Questions](https://forum.defold.com/c/questions) lub opisz błąd w kategorii: [Bugs](https://forum.defold.com/c/bugs). Pamiętaj też, że zawsze możesz spróbować przeszukać forum: [search](https://forum.defold.com/search) w poszukiwaniu odpowiedzi na nurtujące Cię pytania lub rozwiązania problemu, na który ktoś mógł już natrafić. (Forum jest anglojęzyczne, ale przykładowo na Discordzie Defolda możesz znaleźć polskojęzyczny kanał - przyp.tłum.)

Jeśli masz więcej niż jedno pytanie, utwórz dla każdego z nich osobny post dla zachowania porządku.

### Wymagane informacje
Nie będziemy mogli udzielić Ci pomocy jeśli nie podasz paru ważnych informacji:

**Tytuł**
Post musi mieć krótki i opisujący problem tytuł. Dobrymi przykładami są "How do I move a game object in the direction it is rotated?" lub "How do I fade out a sprite?". Złymi przykładami natomiast są "I need some help using Defold!" albo "My game is not working!".

**Opisz problem (WYMAGANE)**
Jasny i dokładny opis problemu.

**Odtworzenie problemu (WYMAGANE)**
Kroki, które trzeba wykonać, aby zreprodukować problem, np:
  1. Przejdź do '...'
  2. Kliknij na '...'
  3. Przewiń do '...'
  4. Zobaczysz błąd

(Oczywiście po angielsku np:
  1. Go to '...'
  2. Click on '....'
  3. Scroll down to '....'
  4. See error
)

**Oczekiwane zachowanie (WYMAGANE)**
Jasny i zwięzły opis czego oczekujesz po prawidłowym zachowaniu silnika/gry.

**Wersja Defolda (WYMAGANE):**
 - np: [Version 1.2.155]

**Sprzęt i system operacyjny (WYMAGANE):**
 - Platforms: [np. iOS, Android, Windows, macOS, Linux, HTML5]
 - OS: [np. iOS8.1, Windows 10, High Sierra]
 - Device: [np. iPhone6]

**Repro case - mały projekt z reprodukcją błędu (OPCJONALNIE):**
Możesz dołączyć mały, zrobiony na szybko projekt Defold, w którym podstawowe elementy są odtworzone w taki sposób, jak w Twoim głównym projekcie, przez co pojawia się ten sam błąd. Załączenie takiego projektu z pewnością znacząco ułatwi i przyspieszy jego rozwiązanie.

**Logi (OPCJONALNIE):**
Dołącz proszę ważne logi silnika, edytora lub serwera do budowania, które pojawiają się w konsoli lub są zapisywane do pliku: [tutaj](#log-files).

**Workaround - obejście problemu (OPCJONALNIE):**
Jeśli znasz jakikolwiek sposób na poradzenie sobie z problemem w inny, sprytny sposób, opisz go proszę w poście.

**Screenshots - zrzuty ekranu (OPCJONALNIE):**
Jeśli zdjęcia jasno pokazują problem, możesz śmiało zamieścić je w poście.

**Dodatkowy kontekst (OPCJONALNIE):**
Jeśli są jeszcze jakiekolwiek inne kwestie warte poruszenia, śmiało dopisz je.

## Zgłoś problem z poziomu Edytora Defold

Edytor umożliwia w łatwy sposób zgłosić problem. Wybierz <kbd>Help->Report Issue</kbd>.

![](images/getting_help/report_issue.png)

Wybranie tej opcji przeniesie Cię do strony ze śledzeniem zgłoszeń błędów na GitHubie. Dodaj [plik z logami](#log-files), informacje o Twoim sprzęcie i systemie operacyjnym, opisz kroki, które trzeba wykonać, aby zreprodukować problem, możliwe obejście itd.

::: sidenote
Musisz mieć konto na GitHubie, żeby zgłosić problem w ten sposób.
:::


## Przedysktuj problem na Slacku

W razie problemów możesz również zadać pytanie na oficjalnym [Slacku](https://www.defold.com/slack/), jednak pamiętaj, że zalecamy, aby skomplikowane kwestie i dogłębne dyskusje prowadzić na forum. Pamiętaj też, że nie przyjmujemy zgłoszeń bugów, problemów przez Slacka.


# Logi

Silnik, Edytor i serwer do budowania Defolda generują logi (informacje), które mogą być bardzo przydatne podczas rozwiązywania problemów. Zawsze dodawaj pliki z logami do zgłaszanego problemu, których lokalizację możesz sprawdzić poniżej:

* [Logi Silnika](/manuals/debugging-game-and-system-logs)
* Logi Edytora
  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
  * Linux: `~/.Defold`
* [Logi serwera do budowania](/manuals/extensions#build-server-logs)
