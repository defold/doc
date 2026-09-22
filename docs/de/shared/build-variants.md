## Build-Varianten {#build-variants}

Wenn du ein Bundle für ein Spiel erstellst, musst du auswählen, welche Art von Engine du verwenden möchtest. Du hast drei grundlegende Optionen:

  * Debug
  * Release
  * Headless

Diese verschiedenen Versionen werden auch als `Build-Varianten` (Build variants) bezeichnet.

::: sidenote
Wenn du <kbd>Project ▸ Build</kbd> wählst, erhältst du immer die Debug-Version.
:::


### Debug

Diese Art von ausführbarer Datei wird üblicherweise während der Entwicklung eines Spiels verwendet, da sie mehrere nützliche Debugging-Funktionen enthält:

* Profiler - Dient zum Erfassen von Leistungs- und Nutzungszählern. Wie du den Profiler verwendest, erfährst du im [Profiling-Handbuch](/manuals/profiling/).
* Protokollierung - Die Engine protokolliert Systeminformationen, Warnungen und Fehler, wenn die Protokollierung aktiviert ist. Die Engine gibt außerdem Protokollmeldungen der Lua-Funktion `print()` sowie von nativen Erweiterungen (native extensions) aus, die mit `dmLogInfo()`, `dmLogError()` und ähnlichen Funktionen protokollieren. Wie du diese Protokolle liest, erfährst du im [Handbuch zu Spiel- und Systemprotokollen](https://defold.com/manuals/debugging-game-and-system-logs/).
* Hot Reload - Hot Reload ist eine leistungsfähige Funktion, mit der du während der Entwicklung Ressourcen (resources) neu laden kannst, während das Spiel läuft. Wie du diese Funktion verwendest, erfährst du im [Hot-Reload-Handbuch](https://defold.com/manuals/hot-reload/).
* Engine-Dienste - Du kannst über verschiedene offene TCP-Ports und Dienste eine Verbindung zu einer Debug-Version eines Spiels herstellen und mit ihr interagieren. Zu diesen Diensten gehören die Hot-Reload-Funktion, der Fernzugriff auf Protokolle und der oben erwähnte Profiler, aber auch weitere Dienste zur Ferninteraktion mit der Engine. Mehr über die Engine-Dienste erfährst du [in der Entwicklerdokumentation](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release

Bei dieser Variante sind die Debugging-Funktionen deaktiviert. Du solltest diese Option wählen, wenn das Spiel zur Veröffentlichung im App Store oder zur Weitergabe an Spieler auf anderem Wege bereit ist. Aus mehreren Gründen wird davon abgeraten, ein Spiel mit aktivierten Debugging-Funktionen zu veröffentlichen:

* Die Debugging-Funktionen beanspruchen etwas Platz in der Binärdatei, und [es ist bewährte Praxis, die Binärdatei eines veröffentlichten Spiels so klein wie möglich zu halten](https://defold.com/manuals/optimization/#optimize-application-size).
* Die Debugging-Funktionen beanspruchen auch etwas CPU-Zeit. Das kann die Leistung des Spiels beeinträchtigen, wenn ein Nutzer leistungsschwache Hardware verwendet. Auf Mobiltelefonen trägt die erhöhte CPU-Auslastung außerdem zur Erwärmung und zum Akkuverbrauch bei.
* Die Debugging-Funktionen können Informationen über das Spiel offenlegen, die nicht für die Augen der Spieler bestimmt sind, sei es im Hinblick auf Sicherheit, Schummeln oder Betrug.


### Headless

Diese ausführbare Datei läuft ohne Grafik und Ton. Das bedeutet, dass du die Unit- und Smoke-Tests des Spiels auf einem CI-Server ausführen oder das Spiel sogar als Spielserver in der Cloud betreiben kannst.
