## Warianty budowania

Gdy tworzysz pakiet gry, musisz wybrać, którego wariantu silnika chcesz użyć. Masz trzy podstawowe opcje:

  * Debug
  * Release
  * Headless

Te różne wersje są też określane jako `Build variants`.

::: sidenote
Gdy wybierzesz <kbd>Project ▸ Build</kbd>, zawsze otrzymasz wersję debug.
:::


### Debug

Ten typ pliku wykonywalnego jest zwykle używany podczas tworzenia gry, ponieważ zawiera kilka przydatnych funkcji debugowania:

* Profiler - Służy do zbierania liczników wydajności i użycia. Dowiedz się, jak korzystać z profilera w [podręczniku profilowania](/manuals/profiling/).
* Logowanie - Silnik będzie zapisywał informacje systemowe, ostrzeżenia i błędy, gdy logowanie jest włączone. Będzie też wypisywać logi z funkcji Lua `print()` oraz z natywnych rozszerzeń korzystających z `dmLogInfo()`, `dmLogError()` i podobnych. Dowiedz się, jak czytać te logi w [podręczniku logów gry i systemu](https://defold.com/manuals/debugging-game-and-system-logs/).
* Szybkie przeładowanie (Hot reload) - To potężna funkcja, która pozwala deweloperowi przeładowywać zasoby, gdy gra jest uruchomiona. Dowiedz się, jak z niej korzystać w [instrukcji o szybkim przeładowaniu](https://defold.com/manuals/hot-reload/).
* Usługi silnika (Engine services) - Można połączyć się z debugową wersją gry i komunikować się z nią przez kilka różnych otwartych portów TCP i usług. Obejmują one funkcję hot reload, zdalny dostęp do logów i wspomniany wyżej profiler, ale także inne mechanizmy zdalnej interakcji z silnikiem. Więcej informacji o usługach silnika znajdziesz [w dokumentacji deweloperskiej](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release

Ten wariant ma wyłączone funkcje debugowania. Tę opcję należy wybrać, gdy gra jest gotowa do publikacji w sklepie z aplikacjami lub udostępnienia graczom w inny sposób. Nie zaleca się wydawania gry z włączonymi funkcjami debugowania z kilku powodów:

* Funkcje debugowania zajmują trochę miejsca w pliku binarnym, a [to dobra praktyka, aby starać się utrzymać rozmiar pliku binarnego wydanej gry tak mały, jak to możliwe](https://defold.com/manuals/optimization/#optimize-application-size).
* Funkcje debugowania zużywają też trochę czasu CPU. Może to wpłynąć na wydajność gry, jeśli użytkownik ma słabszy sprzęt. Na telefonach komórkowych zwiększone użycie CPU będzie też przyczyniać się do nagrzewania urządzenia i szybszego rozładowywania baterii.
* Funkcje debugowania mogą ujawniać informacje o grze, które nie powinny trafić do graczy, zarówno z perspektywy bezpieczeństwa, jak i oszustw czy nadużyć.


### Headless

Ten plik wykonywalny działa bez grafiki i dźwięku. Oznacza to, że możesz uruchamiać testy jednostkowe i smoke testy gry na serwerze CI, a nawet używać go jako serwera gry w chmurze.
