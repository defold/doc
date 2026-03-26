#### P: Dlaczego węzły GUI typu box bez tekstury są przezroczyste w edytorze, ale po zbudowaniu i uruchomieniu wyglądają poprawnie?

O: Ten błąd może występować na [komputerach z kartami graficznymi AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Upewnij się, że masz zaktualizowane sterowniki graficzne.

#### P: Dlaczego podczas otwierania atlasu lub widoku sceny pojawia się błąd `com.sun.jna.Native.open.class java.lang.Error: Access is denied`?

O: Spróbuj uruchomić Defold jako administrator. Kliknij plik wykonywalny Defold prawym przyciskiem myszy i wybierz <kbd>Run as Administrator</kbd>.

#### P: Dlaczego moja gra nie renderuje się poprawnie w Windows na zintegrowanym układzie Intel UHD, choć wersja HTML5 działa?

O: Upewnij się, że sterownik jest zaktualizowany do wersji nie niższej niż 27.20.100.8280. Sprawdź to za pomocą narzędzia [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Dodatkowe informacje znajdziesz w [tym wpisie na forum](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### P: Edytor Defold się zawiesza, a w logu widzę `AWTError: Assistive Technology not found`

Jeśli edytor ulega awarii, a w logu pojawia się wpis `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, wykonaj następujące kroki:

* Przejdź do `C:\Users\<username>`
* Otwórz plik `.accessibility.properties` w zwykłym edytorze tekstu (Notatnik też wystarczy)
* Znajdź w konfiguracji następujące linie:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Dodaj przed tymi liniami znak hash (`#`)
* Zapisz zmiany w pliku i uruchom Defold ponownie
