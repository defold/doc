---
title: Jak uzyskać pomoc
brief: Ta instrukcja opisuje, jak uzyskać pomoc, jeśli napotkasz problem podczas korzystania z Defold.
---

# Jak uzyskać pomoc

Jeśli napotkasz problem podczas korzystania z Defold, chcemy o tym wiedzieć, żeby móc naprawić błąd lub pomóc Ci obejść problem. Istnieje kilka sposobów, by omówić problem i zgłosić go dalej. Wybierz opcję, która najlepiej Ci odpowiada:

## Zgłoś problem na forum

Dobrym sposobem na omówienie problemu i uzyskanie pomocy jest zadanie pytania na naszym [forum](https://forum.defold.com). Opublikuj wpis w kategorii [Questions](https://forum.defold.com/c/questions) albo [Bugs](https://forum.defold.com/c/bugs), zależnie od rodzaju problemu. Pamiętaj, aby [wyszukać](https://forum.defold.com/search) swoje pytanie lub zgłoszenie, zanim je opublikujesz, bo możliwe, że rozwiązanie już istnieje.

Jeśli masz kilka pytań, utwórz osobne wpisy. Nie zadawaj niezwiązanych pytań w jednym wpisie.

### Wymagane informacje
Nie będziemy w stanie udzielić pomocy, jeśli nie podasz potrzebnych informacji:

**Tytuł**
Użyj krótkiego i jasno opisującego problem tytułu. Dobry tytuł to na przykład „How do I move a game object in the direction it is rotated?” albo „How do I fade out a sprite?”. Zły tytuł to „I need some help using Defold!” albo „My game is not working!”.

**Opisz błąd (WYMAGANE)**
Jasny i zwięzły opis tego, na czym polega błąd.

**Odtworzenie problemu (WYMAGANE)**
Kroki prowadzące do odtworzenia zachowania:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Oczekiwane zachowanie (WYMAGANE)**
Jasny i zwięzły opis tego, czego się spodziewałeś.

**Wersja Defold (WYMAGANE):**
  - Version [e.g. 1.2.155]

**Platformy (WYMAGANE):**
 - Platforms: [e.g. iOS, Android, Windows, macOS, Linux, HTML5]
 - OS: [e.g. iOS8.1, Windows 10, High Sierra]
 - Device: [e.g. iPhone6]

**Minimal reproduction case project (OPCJONALNIE):**
Dołącz minimalny projekt, w którym da się odtworzyć błąd. Bardzo to pomaga osobie, która będzie badać i naprawiać problem.

**Logi (OPCJONALNIE):**
Dodaj odpowiednie logi z silnika, edytora lub serwera budowania. Informacje o tym, gdzie są przechowywane, znajdziesz [tutaj](#log-files).

**Workaround (OPCJONALNIE):**
Jeśli istnieje obejście problemu, opisz je tutaj.

**Screenshots (OPCJONALNIE):**
Jeśli to pomoże wyjaśnić problem, dołącz zrzuty ekranu.

**Additional context (OPCJONALNIE):**
Dodaj tutaj każdy dodatkowy kontekst związany z problemem.

### Udostępnianie kodu
Kiedy udostępniasz kod, zalecamy umieszczenie go jako tekstu, a nie jako zrzutu ekranu. Dzięki temu łatwiej go wyszukać, wskazać błędy i zaproponować poprawki. Wstaw kod między trzy backticki (\`\`\`) albo wcięty o 4 spacje.

Przykład:

\`\`\`
print("Hello code!")
\`\`\`

Efekt:

```
print("Hello code!")
```

## Zgłoś problem z poziomu edytora

Edytor udostępnia wygodny sposób zgłaszania problemów. Wybierz z poziomu edytora <kbd>Help->Report Issue</kbd>, aby zgłosić błąd.

![](images/getting_help/report_issue.png)

Wybranie tej opcji przeniesie Cię do systemu zgłoszeń na GitHubie. Dołącz [pliki z logami](#log-files), informacje o systemie operacyjnym, kroki odtworzenia problemu, możliwe obejścia i tym podobne szczegóły.

::: sidenote
Do przesłania zgłoszenia w ten sposób potrzebujesz konta GitHub.
:::


## Przedyskutuj problem na Discord

Jeśli napotkasz problem podczas korzystania z Defold, możesz spróbować zadać pytanie na [Discord](https://www.defold.com/discord/). Zalecamy jednak, aby złożone pytania i bardziej szczegółowe dyskusje prowadzić na forum. Nie przyjmujemy zgłoszeń błędów przesyłanych przez Discord.


# Pliki z logami

Silnik, edytor i serwer budowania generują informacje do logów, które mogą być bardzo pomocne podczas proszenia o pomoc i diagnozowania problemu. Zawsze dołączaj pliki z logami, gdy zgłaszasz problem:

* [Engine logs](/manuals/debugging-game-and-system-logs)
* [Editor logs](/manuals/editor#editor-logs)
* [Build server logs](/manuals/extensions#build-server-logs)
