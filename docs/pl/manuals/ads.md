---
title: Wyświetlanie reklam w Defoldzie
brief: Wyświetlanie różnorodnych reklam hest powszechnym sposobem na zarabianie w grach mobilnych i webowych. Ta instrukcja pokazuje jest używać róznych rodzajów reklam do monetyzacji Twojej gry lub aplikacji.
---

# Reklamy

Reklamy stały się bardzo powszechnym sposobem na zarabianie w grach mobilnych i webowych tworząc dochodowy biznes. Jako deweloper gry z reklamami otrzymujesz pieniądze w zależności od liczby osób oglądających reklamy w Twojej grze. Zazwyczaj większa liczba graczy oznacza większe dochody z reklam, ale oczywiście istnieją też inne czynniki wpływające na zarobki:

* Jakość reklam - reklamy odpowiadające użytkownikowi przykuwają ich uwagę i zwiększają szansę na interakcję.
* Format reklam - reklamy banerowe (zasłaniające część ekranu) zazwyczaj są mniej opłacane niż pełnoekranowe, szczególnie odtwarzane od początku do końca.
* Sieć reklamodawcza - sieci reklamodawcze różnią się między sobą ofertami, a co za tym idzie możliwymi zarobkami.

::: sidenote
CPM = Cost per mille - wysokość pieniędzy, jaką reklamodawca wypłaca za tysiąc wyświetleń danej reklamy. Wartości te różnią się między formatami reklam i sieciami reklamodawczymi.
:::

## Format reklam

Jest wiele formatów reklam, które można używać w grach. Najpopularniejsze to banery, reklamy między przejściami (interstitial) i nagradzane (reward):

### Reklamy banerowe

Banery to tekstowe, obrazkowe lub filmowe reklamy zasłaniające relatywnie małą część ekranu, zazwyczaj na górze lub dole ekranu. Są one bardzo łatwe w implementacji i pasują do typowych gier z jednym ekranem, gdzie łatwo jest zarezerwować fragment obszaru ekranu na reklamę. Banery są najlepiej wykorzystane, gdy gracze grają bez przerywania (np. ładowania i przechodzenia między ekranami).

### Reklamy między przejściami (interstitial)

Reklamy typu "interstitial" to pełnoekranowe reklamy z animacją lub video, a czasem nawet z interaktywnymi mediami. Są zazwyczaj wyświetlane między poziomami, podczas ładowania lub między sesjami gry jako naturalnie odbierana przerwa w rozgrywce. Zazwyczaj samych wyświetleń takich reklam jest mniej niż banerowych (ze względu na charakter momentu wyświetlenia), ale CPM jest zdecydowanie wyższe niż w przypadku banerów, co wiąże się w oczywisty sposób z większymi dochodami.

### Reklamy nagradzane (reward)

Reklamy nagradzane (znane też jako motywacyjne) są opcjonalne, przez co i mniej agresywne niż pozostałe. Zazwyczaj są pełnoekranowe, więc skupiają całą uwagę gracza. Użytkownik w nagrodę może wybrać sobie korzyść za obejrzenie reklamy - przykładowo daną ilość growej waluty, przedmioty, dodatkowe życia, dodatkowy czas (lub wręcz przeciwnie - skrócenie czasu oczekiwania na coś) czy jakikolwiek benefit czy walutę pasującą do gry. Reklamy nagradzane mają zazwyczaj większe CPM, ale ilość wyświetleń jest stricte związana z chęciami użytkowników. Reklamy te wygenerują więc spory dochód, jeśli nagrody będą wystarczająco wartościowe, aby zachęcić użytkownika do ich obejrzenia i oferowane powinny być w najlepszym dogodnym czasie.


## Sieci reklamodawców

[Defold Asset Portal](/tags/stars/ads/) posiada wiele rozszerzeń umożliwiających integrację z różnymi dostawcami reklam:

* [AdMob](https://defold.com/assets/admob/) - Google ad network.
* [Enhance](https://defold.com/assets/enhance/) - Różne sieci. Wymaga dodatkowego kroku po zbudowaniu, w celu dołączenia danych sieci.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Reklamy w grach Facebook Instant.
* [IronSource](https://defold.com/assets/ironsource/) - IronSource Ad network.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Unity Ads network.


# Jak zintegrować reklamy do Twojej gry?

Jeśli wybrałeś już dostawcę reklam i ich format postępuj zgodnie z krokami instalacyjnymi i instrukcjami użytkowania dla danych rozszerzeń. W większości przypadków dodajesz bibliotekę do projektu określając tzw. [project dependency](/manuals/libraries/#setting-up-library-dependencies). Kiedy masz zaimportowaną bilbiotekę do Twojego projektu możesz kontynuować integrację i wywoływać w kodzie funckje specyficzne dla danego modułu umożliwiające ładowanie i wyświetlanie reklam.


# Łączenie reklam i zakupów wewnątrz aplikacji

Popularnym rozwiązaniem jest umożliwienie wyłączenia reklam po uiszczeniu opłaty poprzez zakup wewnątrz aplikacji, czyli [In-app purchase](/manuals/iap).


## Więcej

Jest wiele źródeł, z których można dowiedzieć się więcej na temat reklam i optymalizacji zysków (w języku angielskim):

* Google AdMob [Monetize mobile games with ads](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Popular ad formats and how to use them](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Ad serving in games: 10 expert tips](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
