---
title: Wytyczne dotyczące portowania i wydania
brief: Ta instrukcja zwraca uwagę na kwestie, które warto rozważyć podczas portowania gry na nową platformę lub przy jej pierwszym wydaniu.
---

# Wytyczne dotyczące portowania i wydania

Ta strona zawiera przydatny przewodnik i listę kontrolną rzeczy, które warto wziąć pod uwagę podczas wydawania gry albo portowania jej na nową platformę.

Portowanie gry Defold na nową platformę lub pierwsze wydanie zwykle jest prostym procesem. W teorii wystarczy upewnić się, że odpowiednie sekcje są skonfigurowane w pliku *game.project*, ale aby w pełni wykorzystać możliwości każdej platformy, zaleca się dostosowanie gry do jej specyfiki.

## Wejście
Upewnij się, że gra jest dostosowana do metod wprowadzania danych dostępnych na danej platformie. Rozważ dodanie obsługi [gamepadów](/manuals/input-gamepads), jeśli platforma je wspiera. Upewnij się też, że gra obsługuje menu pauzy - jeśli kontroler nagle się odłączy, gra powinna zostać wstrzymana.

## Lokalizacja
Przetłumacz cały tekst występujący w grze. Przy wydaniu w Europie i obu Amerykach rozważ tłumaczenie przynajmniej na EFIGS (ang. English, French, Italian, German and Spanish, czyli angielski, francuski, włoski, niemiecki i hiszpański). Upewnij się, że można łatwo przełączać języki w samej grze, na przykład z poziomu menu pauzy.

::: important
Tylko iOS - Upewnij się, że w `game.project` określisz [Localizations](/manuals/project-settings/#localizations), ponieważ `sys.get_info()` nigdy nie zwróci języka, którego nie ma na tej liście.
:::

Przetłumacz też tekst widoczny na stronie sklepu, ponieważ pozytywnie wpływa to na sprzedaż. Niektóre platformy wymagają, aby tekst na stronie sklepu był przetłumaczony na język każdego kraju, w którym gra jest dostępna.

## Materiały sklepowe

### Ikona aplikacji
Upewnij się, że Twoja gra wyróżnia się na tle konkurencji. Ikona często jest pierwszym punktem kontaktu z potencjalnymi graczami. Powinna być łatwa do znalezienia na stronie pełnej ikon gier.

### Banery i grafiki sklepu
Użyj wyrazistej, przyciągającej wzrok oprawy graficznej. Warto rozważyć wydanie pieniędzy na współpracę z grafikiem, który przygotuje ilustracje przyciągające graczy.

## Zapisy gry

### Zapisy gry na desktopie, urządzeniach mobilnych i w sieci
Zapisy gry i inny zapisany stan można przechowywać za pomocą funkcji API w Defold `sys.save(filename, data)` i wczytywać funkcją `sys.load(filename)`. Funkcja `sys.get_save_file(application_id, name)` pozwala uzyskać ścieżkę do lokalizacji zależnej od systemu operacyjnego, w której można zapisywać pliki, zwykle w folderze domowym zalogowanego użytkownika.

### Zapisy gry na konsoli
Używanie `sys.get_save_file()` i `sys.save()` działa dobrze na większości platform, ale na konsolach zaleca się inne podejście. Platformy konsolowe zwykle przypisują użytkownika do każdego podłączonego kontrolera, więc zapisy gry, osiągnięcia i inne funkcje powinny być powiązane z odpowiednim użytkownikiem.

Zdarzenia wejściowe z gamepada będą zawierały identyfikator użytkownika, który można wykorzystać do powiązania działań kontrolera z użytkownikiem na konsoli.

Platformy konsolowe i ich rozszerzenia natywne udostępniają platformowo zależne funkcje API do zapisywania i wczytywania danych powiązanych z konkretnym użytkownikiem. Korzystaj z tych interfejsów podczas zapisywania i wczytywania na konsoli.

Interfejsy API platform konsolowych do operacji na plikach są zwykle asynchroniczne. Podczas tworzenia gry wieloplatformowej, przeznaczonej na konsole, zaleca się zaprojektowanie gry tak, aby wszystkie operacje na plikach były asynchroniczne, niezależnie od platformy. Przykład:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```

## Artefakty budowania

Upewnij się, że [wygenerujesz symbole debugowania](/manuals/debugging-native-code/#symbolicate-a-callstack) dla każdej wydanej wersji, aby móc debugować awarie. Przechowuj je razem z pakietem aplikacji.

## Optymalizacje aplikacji

Przeczytaj [instrukcję optymalizacji](/manuals/optimization), aby dowiedzieć się, jak optymalizować aplikację pod kątem wydajności, rozmiaru, zużycia pamięci i energii baterii.

## Wydajność
Zawsze testuj na docelowym sprzęcie. Sprawdź wydajność gry i zoptymalizuj ją, jeśli to potrzebne. Użyj [profilera](/manuals/profiling), aby znaleźć wąskie gardła w kodzie.

## Rozdzielczość ekranu i częstotliwość odświeżania
W przypadku platform o stałej orientacji i stałej rozdzielczości ekranu sprawdź, czy gra działa poprawnie przy docelowej rozdzielczości i proporcjach obrazu. W przypadku platform o zmiennej rozdzielczości i zmiennych proporcjach obrazu sprawdź, czy gra działa poprawnie przy różnych rozdzielczościach i proporcjach. Weź też pod uwagę, jaki rodzaj [projekcji widoku](/manuals/render/#default-view-projection) jest używany w skryptach do renderowania i kamerze.

Na platformach mobilnych albo zablokuj orientację ekranu w *game.project*, albo upewnij się, że gra działa zarówno w trybie poziomym, jak i pionowym.

* **Rozmiary wyświetlacza** - Czy wszystko wygląda dobrze na ekranie większym lub mniejszym niż domyślna szerokość i wysokość ustawione w *game.project*?
  * Projekcja używana w skrypcie renderowania i układy używane w GUI mają tutaj znaczenie.
* **Proporcje obrazu** - Czy wszystko wygląda dobrze na ekranie o innych proporcjach niż domyślne proporcje wynikające z szerokości i wysokości ustawionych w *game.project*?
  * Projekcja używana w skrypcie renderowania i układy używane w GUI mają tutaj znaczenie.
* **Częstotliwość odświeżania** - Czy gra działa dobrze na ekranie o częstotliwości odświeżania większej niż 60 Hz?
  * Vsync i swap interval w sekcji Display pliku *game.project*.

## Telefony komórkowe oraz kamery z wycięciem i otworem w ekranie
Coraz popularniejsze staje się stosowanie niewielkiego wycięcia w ekranie na przednią kamerę i czujniki, nazywanego też notchem albo hole punch camera. Podczas portowania gry na urządzenia mobilne zadbaj, aby ważne informacje mieściły się w bezpiecznym obszarze platformy.

Defold ma wbudowaną obsługę bezpiecznego obszaru w Androidzie i iOS. Ustaw `gui.safe_area_mode` w pliku *game.project*, aby określić, które przeciwległe marginesy bezpiecznego obszaru wpływają na dostosowanie GUI. `none` jest ustawieniem domyślnym i ignoruje marginesy; `long` stosuje lewy i prawy w orientacji poziomej oraz górny i dolny w pionowej; `short` stosuje przeciwną parę; a `both` stosuje wszystkie cztery krawędzie. Skrypt GUI może zastąpić tryb całego projektu dla swojej sceny za pomocą [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). Dla własnej logiki GUI lub renderowania funkcja [`window.get_safe_area()`](/ref/window/#window.get_safe_area) zwraca bezpieczny prostokąt i marginesy poszczególnych krawędzi. Platformy bez wbudowanych marginesów bezpiecznego obszaru zwracają całe okno i zerowe marginesy.

[Rozszerzenie Safe Area](/extension-safearea) pozostaje alternatywą dla starszych projektów lub przepływów pracy wymagających zachowania wykraczającego poza wbudowane API; nie jest wymagane do standardowej obsługi bezpiecznego obszaru w Androidzie i iOS.

## Wytyczne specyficzne dla platform

### Android
Upewnij się, że przechowujesz [keystore](/manuals/android/#creating-a-keystore) w bezpiecznym miejscu, aby móc później zaktualizować grę.

### Konsole
Zachowuj kompletny pakiet dla każdej wersji. Te pliki będą potrzebne, jeśli będziesz chciał załatać grę.

### Nintendo Switch
Zintegruj kod specyficzny dla platformy - dla Nintendo Switch istnieje osobne rozszerzenie z dodatkowymi funkcjami pomocniczymi, na przykład do wyboru użytkownika.

Wersja Defold dla Nintendo Switch używa Vulkana jako backendu graficznego - upewnij się, że przetestujesz grę z użyciem [backendu graficznego Vulkan](https://github.com/defold/extension-vulkan).

### PlayStation®4
Zintegruj kod specyficzny dla platformy - dla PlayStation®4 istnieje osobne rozszerzenie z dodatkowymi funkcjami pomocniczymi, na przykład do wyboru użytkownika.

### HTML5
Granie w gry webowe na telefonach komórkowych staje się coraz popularniejsze - postaraj się też, aby gra działała dobrze w mobilnej przeglądarce. Ważne jest również, aby pamiętać, że od gier webowych oczekuje się szybkiego ładowania. Upewnij się, że gra jest zoptymalizowana pod kątem rozmiaru. Weź też pod uwagę ogólne wrażenia z ładowania, aby nie tracić graczy niepotrzebnie.

W 2018 roku przeglądarki wprowadziły politykę automatycznego odtwarzania dźwięku, która uniemożliwia grom i innym treściom webowym odtwarzanie dźwięku, dopóki nie nastąpi zdarzenie interakcji użytkownika, takie jak dotknięcie, kliknięcie przycisku czy użycie gamepada. Podczas portowania do HTML5 trzeba to uwzględnić i rozpoczynać odtwarzanie dźwięków oraz muzyki dopiero po pierwszej interakcji użytkownika. Próby odtwarzania dźwięku przed jakąkolwiek interakcją użytkownika zostaną zapisane jako błąd w konsoli deweloperskiej przeglądarki, ale nie wpłyną na działanie gry.

Upewnij się też, że wstrzymasz wszystkie odtwarzane dźwięki, jeśli w grze są wyświetlane reklamy.
