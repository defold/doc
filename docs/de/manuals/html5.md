---
title: Entwicklung mit Defold für die HTML5-Plattform
brief: Dieses Handbuch beschreibt die Erstellung eines HTML5-Spiels sowie bekannte Probleme und Einschränkungen.
---

# HTML5-Entwicklung {#html5-development}

Defold unterstützt die Erstellung von Spielen für die HTML5-Plattform über das reguläre Menü zur Bundle-Erstellung, ebenso wie für andere Plattformen. Das daraus entstehende Spiel wird außerdem in eine normale HTML-Seite eingebettet, die sich über ein einfaches Vorlagensystem gestalten lässt.

Die Datei *game.project* enthält die HTML5-spezifischen Einstellungen:

![Projekteinstellungen](images/html5/html5_project_settings.png)

## Heap-Größe {#heap-size}

Defolds Unterstützung für HTML5 basiert auf Emscripten (siehe http://en.wikipedia.org/wiki/Emscripten). Vereinfacht gesagt erstellt es einen abgeschirmten Speicherbereich für den Heap, in dem die Anwendung ausgeführt wird. Standardmäßig reserviert die Engine großzügig bemessenen Speicher (256 MB). Das sollte für ein typisches Spiel mehr als ausreichen. Im Rahmen der Optimierung kannst du einen kleineren Wert wählen. Gehe dazu wie folgt vor:

1. Setze *heap_size* auf den gewünschten Wert. Er sollte in Megabyte angegeben werden.
2. Erstelle dein HTML5-Bundle (siehe unten)

## Einen HTML5-Build testen {#testing-html5-build}

Zum Testen benötigt ein HTML5-Build einen HTTP-Server. Defold erstellt einen für dich, wenn du <kbd>Project ▸ Build HTML5</kbd> wählst.

![Build HTML5](images/html5/html5_build_launch.png)

Wenn du dein Bundle testen möchtest, lade es auf deinen entfernten HTTP-Server hoch oder erstelle einen lokalen Server, beispielsweise mit Python im Bundle-Ordner.
Python 2:

```sh
python -m SimpleHTTPServer
```

Python 3:

```sh
python -m http.server
```

oder

```sh
python3 -m http.server
```

::: important
Du kannst das HTML5-Bundle nicht testen, indem du die Datei `index.html` in einem Browser öffnest. Dafür ist ein HTTP-Server erforderlich.
:::

::: important
Wenn in der Konsole der Fehler `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."` erscheint, musst du sicherstellen, dass dein Server den MIME-Typ `application/wasm` für `.wasm`-Dateien verwendet.
:::

## Ein HTML5-Bundle erstellen {#creating-html5-bundle}

HTML5-Inhalte mit Defold zu erstellen ist einfach und folgt demselben Muster wie bei allen anderen unterstützten Plattformen: Wähle im Menü <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd>:

![Ein HTML5-Bundle erstellen](images/html5/html5_bundle.png)

HTML5-Bundles unterstützen zwei WebAssembly-Architekturen:

* `wasm-web` - die reguläre WebAssembly-Engine ohne Thread-Unterstützung.
* `wasm_pthread-web` - eine WebAssembly-Engine, die Threads verwenden kann.

Du kannst eine der beiden Architekturen oder beide einbinden. Wenn beide enthalten sind, wählt der Loader `wasm_pthread-web`, sofern der Browser und die Hosting-Umgebung dies unterstützen, und greift andernfalls auf `wasm-web` zurück. Die kanonischen Zielnamen findest du im [Bob-Handbuch](/manuals/bob/#usage).

::: important
Die Engine mit Thread-Unterstützung benötigt `SharedArrayBuffer` auf einer sicheren Seite mit [ursprungsübergreifender Isolation](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated). Stelle das Bundle über HTTPS (oder localhost) bereit und konfiguriere den Server mit kompatiblen Headern zur ursprungsübergreifenden Isolation, üblicherweise:

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Ressourcen anderer Ursprünge, die die Seite lädt, müssen ebenfalls kompatible CORS- oder Cross-Origin-Resource-Policy-Header verwenden. Ein Bundle, das nur `wasm_pthread-web` enthält, kann nicht ausgeführt werden, wenn diese Voraussetzungen nicht erfüllt sind. Binde `wasm-web` als Ausweichoption ein, wenn das Spiel möglicherweise auf einer Website gehostet wird, die keine ursprungsübergreifende Isolation unterstützt.
:::

HTML5-Bundles von Defold benötigen einen modernen Browser mit WebAssembly-Unterstützung. Internet Explorer 11 wird nicht unterstützt.

Wenn du auf die Schaltfläche <kbd>Create bundle</kbd> klickst, wirst du aufgefordert, einen Ordner auszuwählen, in dem deine Anwendung erstellt werden soll. Nach Abschluss des Exports findest du dort alle Dateien, die zum Ausführen der Anwendung benötigt werden.

## WebGL-Kontextversion {#webgl-context-version}

Wähle den angeforderten Grafikkontext über [`graphics.webgl_version_hint`](/manuals/project-settings/#webgl-version-hint). Der Standardwert ist WebGL 2. Fordere WebGL 1 an, um diesen Kontext in Browsern, die beide Versionen unterstützen, zu testen oder als Ziel zu verwenden.

## Downloads überprüfen {#download-verification}

Der HTML5-Loader prüft standardmäßig die Größen heruntergeladener Engine- und Archivdateien. Bei fehlgeschlagenen Prüfungen werden Downloads erneut versucht, bevor der Loader einen Fehler meldet:

* Bei Netzwerkfehlern, HTTP-Fehlerstatuscodes und Größenabweichungen beim Download der JavaScript- oder WebAssembly-Datei der Engine gilt die in `html5.retry_count` festgelegte Obergrenze für erneute Versuche.
* Die Überprüfung von Archivdateien hat eine eigene Obergrenze für erneute Versuche bei Größen- oder SHA-1-Abweichungen. Bei jeder erneuten Überprüfung werden die Teile der Datei erneut heruntergeladen, wobei für jeden Download die üblichen erneuten Versuche bei Netzwerkfehlern zur Verfügung stehen.

Die Einstellung `html5.retry_time` steuert in beiden Fällen die Wartezeit zwischen erneuten Versuchen.

Wenn dein Server, Proxy oder CDN bereitgestellte Dateien absichtlich umschreibt und dadurch ihre Größe verändert, deaktiviere die Größenprüfung in *game.project*:

```ini
[html5]
verify_downloaded_file_size = 0
```

Wenn du **Verify Downloaded File Size** deaktivierst, bleibt eine im Bundle enthaltene SHA-1-Überprüfung weiterhin aktiviert. Siehe die [HTML5-Projekteinstellungen](/manuals/project-settings/#verify-downloaded-file-size).

## Bekannte Probleme und Einschränkungen {#known-issues-and-limitations}

* Hot Reload - Hot Reload funktioniert in HTML5-Builds nicht. Defold-Anwendungen müssen einen eigenen kleinen Webserver betreiben, um Aktualisierungen vom Editor zu empfangen. Das ist in einem HTML5-Build nicht möglich.
* Chrome
  * Langsame Debug-Builds - In Debug-Builds für HTML5 überprüfen wir alle WebGL-Grafikaufrufe, um Fehler zu erkennen. Beim Testen in Chrome ist das leider sehr langsam. Du kannst dies deaktivieren, indem du das Feld *Engine Arguments* in *game.project* auf `--verify-graphics-calls=false` setzt.
* Gamepad-Unterstützung - [Die Gamepad-Dokumentation](/manuals/input-gamepads/#gamepads-in-html5) beschreibt Besonderheiten und Schritte, die du bei HTML5 möglicherweise beachten oder durchführen musst.

## Ein HTML5-Bundle anpassen {#customizing-html5-bundle}

Beim Erstellen einer HTML5-Version deines Spiels stellt Defold eine Standardwebseite bereit. Sie verweist auf Stil- und Skriptressourcen, die bestimmen, wie dein Spiel dargestellt wird.

Bei jedem Export der Anwendung werden diese Inhalte neu erstellt. Wenn du eines dieser Elemente anpassen möchtest, musst du deine Projekteinstellungen ändern. Öffne dazu *game.project* im Defold-Editor und scrolle zum Abschnitt *html5*:

![HTML5-Abschnitt](images/html5/html5_section.png)

Weitere Informationen zu jeder Option findest du im [Handbuch zu den Projekteinstellungen](/manuals/project-settings/#html5).

::: important
Du kannst die Dateien der standardmäßigen HTML-/CSS-Vorlage im Ordner `builtins` nicht ändern. Um deine Änderungen anzuwenden, kopiere die benötigte Datei aus `builtins`, füge sie in dein Projekt ein und lege diese Datei in *game.project* fest.
:::

::: important
Die Zeichenfläche sollte weder mit einem Rahmen noch mit einem Innenabstand gestaltet werden. Andernfalls sind die Koordinaten der Mauseingabe falsch.
:::

In *game.project* kannst du die Schaltfläche `Fullscreen` und den Link `Made with Defold` deaktivieren.
Defold stellt ein dunkles und ein helles Design für `index.html` bereit. Standardmäßig ist das helle Design eingestellt, du kannst es aber durch Ändern der Datei `Custom CSS` wechseln. Im Feld `Scale Mode` stehen außerdem vier vordefinierte Skalierungsmodi zur Auswahl.

::: important
Die Berechnungen für alle Skalierungsmodi berücksichtigen den aktuellen DPI-Wert des Bildschirms, wenn du die Option `High Dpi` in *game.project* (Abschnitt `Display`) aktivierst.
:::

### Downscale Fit und Fit {#downscale-fit-and-fit}

Im Modus `Fit` wird die Größe der Zeichenfläche so angepasst, dass die gesamte Zeichenfläche des Spiels mit ihren ursprünglichen Proportionen auf dem Bildschirm zu sehen ist. Der einzige Unterschied bei `Downscale Fit` besteht darin, dass die Größe nur geändert wird, wenn der Innenbereich der Webseite kleiner als die ursprüngliche Zeichenfläche des Spiels ist. Ist die Webseite größer als die ursprüngliche Zeichenfläche des Spiels, wird diese nicht vergrößert.

![HTML5-Abschnitt](images/html5/html5_fit.png)

### Stretch

Im Modus `Stretch` wird die Größe der Zeichenfläche so angepasst, dass sie den Innenbereich der Webseite vollständig ausfüllt.

![HTML5-Abschnitt](images/html5/html5_stretch.png)

### No Scale
Im Modus `No Scale` entspricht die Größe der Zeichenfläche genau dem Wert, den du in der Datei *game.project* im Abschnitt `[display]` festgelegt hast.

![HTML5-Abschnitt](images/html5/html5_no_scale.png)

## Tokens

Wir verwenden die [Vorlagensprache Mustache](https://mustache.github.io/mustache.5.html) zum Erstellen der Datei `index.html`. Wenn du einen Build oder ein Bundle erstellst, werden die HTML- und CSS-Dateien durch einen Compiler verarbeitet, der bestimmte Tokens durch Werte ersetzen kann, die von deinen Projekteinstellungen abhängen. Diese Tokens stehen immer in doppelten oder dreifachen geschweiften Klammern (`{{TOKEN}}` oder `{{{TOKEN}}}`), je nachdem, ob Zeichenfolgen maskiert werden sollen oder nicht. Diese Funktion kann nützlich sein, wenn du häufig deine Projekteinstellungen änderst oder Material in anderen Projekten wiederverwenden möchtest.

::: sidenote
Weitere Informationen zur Vorlagensprache Mustache findest du im [Handbuch](https://mustache.github.io/mustache.5.html).
:::

Jeder Wert in *game.project* kann als Token dienen. Wenn du beispielsweise den Wert von `Width` aus dem Abschnitt `Display` verwenden möchtest:

![Abschnitt Display](images/html5/html5_display.png)

Öffne *game.project* als Text und prüfe `[section_name]` sowie den Namen des Felds, das du verwenden möchtest. Anschließend kannst du es als Token verwenden: `{{section_name.field}}` oder `{{{section_name.field}}}`.

![Abschnitt Display](images/html5/html5_game_project.png)

Zum Beispiel in JavaScript innerhalb der HTML-Vorlage:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

Außerdem gibt es die folgenden benutzerdefinierten Tokens:

DEFOLD_SPLASH_IMAGE
: Gibt den Dateinamen des Startbilds oder `false` aus, wenn `html5.splash_image` in *game.project* leer ist.


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: Der Projektname ohne unzulässige Zeichen.

DEFOLD_ARCHIVE_LOCATION_PREFIX
: Das aufgelöste Präfix des Archivpfads, das der Loader verwendet, basierend auf `html5.archive_location_prefix`.

DEFOLD_ARCHIVE_LOCATION_SUFFIX
: Das aufgelöste Suffix, das an Archiv-URLs angehängt wird, basierend auf `html5.archive_location_suffix`.

DEFOLD_HAS_ARCHIVE_ORIGIN
: `true`, wenn das Archivpräfix einen HTTP- oder HTTPS-Ursprung angibt, einschließlich einer protokollrelativen URL wie `//cdn.example.com/archive`. Bei relativen Archivpräfixen ist der Wert `false`. Verfügbar seit Defold 1.13.2.

DEFOLD_ARCHIVE_ORIGIN
: Der Ursprung des Archivs einschließlich Schema, Host und optionalem Port oder eine leere Zeichenfolge, wenn kein Ursprung angegeben ist. Ein protokollrelatives Präfix erzeugt einen protokollrelativen Ursprung. Wird für den Preconnect-Hinweis verwendet und ist seit Defold 1.13.2 verfügbar.

DEFOLD_HAS_WASM_ENGINE
: `true`, wenn das Bundle eine WebAssembly-Engine enthält, entweder `wasm-web` oder `wasm_pthread-web`.

DEFOLD_HAS_WASM_PTHREAD_ENGINE
: `true`, wenn das Bundle `wasm_pthread-web` enthält. Verwende dieses Token, um das Vorladen der falschen Engine-Variante zu vermeiden, wenn der Loader die Architektur zur Laufzeit auswählt.


DEFOLD_CUSTOM_CSS_INLINE
: An dieser Stelle wird der Inhalt der CSS-Datei direkt eingefügt, die in deinen *game.project*-Einstellungen angegeben ist.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
Dieser direkt eingefügte Block muss vor dem Laden des Hauptskripts der Anwendung stehen. Da er HTML-Tags enthält, sollte dieses Makro in dreifachen geschweiften Klammern `{{{TOKEN}}}` stehen, damit Zeichenfolgen nicht maskiert werden.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: Dieses Token ist `true`, wenn `html5.scale_mode` auf `Downscale Fit` gesetzt ist.

DEFOLD_SCALE_MODE_IS_FIT
: Dieses Token ist `true`, wenn `html5.scale_mode` auf `Fit` gesetzt ist.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: Dieses Token ist `true`, wenn `html5.scale_mode` auf `No Scale` gesetzt ist.

DEFOLD_SCALE_MODE_IS_STRETCH
: Dieses Token ist `true`, wenn `html5.scale_mode` auf `Stretch` gesetzt ist.

DEFOLD_HEAP_SIZE
: Die in *game.project* unter `html5.heap_size` angegebene Heap-Größe, umgerechnet in Bytes.

DEFOLD_ENGINE_ARGUMENTS
: Die in *game.project* unter `html5.engine_arguments` angegebenen Engine-Argumente, getrennt durch das Zeichen `,`.

build-timestamp
: Der aktuelle Build-Zeitstempel in Sekunden.


## Zusätzliche Parameter {#extra-parameters}

Wenn du eine eigene Vorlage erstellst, kannst du Parameter für den Engine-Loader ändern, indem du Werte im globalen Objekt `CUSTOM_PARAMETERS` zuweist. Die integrierte Vorlage stellt für diese Anpassungen einen bewusst leeren Block `<script id="engine-setup">` bereit.
::: important
Der Block `engine-setup` muss nach dem Skript stehen, das `dmloader.js` lädt, und vor dem Block `engine-start`, der `EngineLoader.load()` aufruft.
:::
Zum Beispiel:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS` kann unter anderem die folgenden Felder enthalten:

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## Dateioperationen in HTML5 {#file-operations-in-html5}

HTML5-Builds unterstützen Dateioperationen wie `sys.save()`, `sys.load()` und `io.open()`, aber die interne Verarbeitung dieser Operationen unterscheidet sich von anderen Plattformen. Wenn JavaScript in einem Browser ausgeführt wird, gibt es kein eigentliches Dateisystemkonzept, und der Zugriff auf lokale Dateien ist aus Sicherheitsgründen gesperrt. Stattdessen verwendet Emscripten (und damit auch Defold) [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), eine Datenbank im Browser zur dauerhaften Speicherung von Daten, um ein virtuelles Dateisystem im Browser zu erstellen. Der wesentliche Unterschied zum Dateisystemzugriff auf anderen Plattformen besteht darin, dass zwischen dem Schreiben in eine Datei und dem tatsächlichen Speichern der Änderung in der Datenbank eine kurze Verzögerung auftreten kann. Über die Entwicklerkonsole des Browsers kannst du in der Regel den Inhalt der IndexedDB untersuchen.


## Argumente an ein HTML5-Spiel übergeben {#passing-arguments-to-an-html5-game}

Manchmal ist es notwendig, einem Spiel vor oder während des Starts zusätzliche Argumente zu übergeben. Das können beispielsweise eine Nutzer-ID, ein Sitzungstoken oder die Angabe des Levels sein, das beim Spielstart geladen werden soll. Dies lässt sich auf verschiedene Arten erreichen, von denen einige hier beschrieben werden.

### Engine-Argumente {#engine-arguments}

Du kannst beim Konfigurieren und Laden der Engine zusätzliche Engine-Argumente angeben. Diese zusätzlichen Engine-Argumente lassen sich zur Laufzeit mit `sys.get_config_string()` abrufen. Weise die Argumente direkt `CUSTOM_PARAMETERS.engine_arguments` im Block `engine-setup` von `index.html` zu:


```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

Wenn du ein neues Array zuweist, ersetzt es alle in *game.project* konfigurierten Engine-Argumente. Um diese Argumente beizubehalten und ein weiteres hinzuzufügen, verwende stattdessen `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")`.

Du kannst auch `--config=example.foo1=bar1, --config=example.foo2=bar2` im Feld *Engine Arguments* im HTML5-Abschnitt von *game.project* eintragen. Die durch Kommas getrennten Werte werden `CUSTOM_PARAMETERS.engine_arguments` in der erzeugten Datei `dmloader.js` hinzugefügt.

Zur Laufzeit rufst du die Werte folgendermaßen ab:

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### Abfrageargumente in der URL {#query-arguments-in-the-url}

Du kannst Argumente als Teil der Abfrageparameter in der Seiten-URL übergeben und sie zur Laufzeit auslesen:

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Eine vollständige Hilfsfunktion, um alle Abfrageparameter als Lua-Tabelle abzurufen:

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- get the query part of the url (the bit after ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- iterate over all key value pairs
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Optimierungen {#optimizations}
Für HTML5-Spiele gelten in der Regel strenge Anforderungen an die anfängliche Downloadgröße, die Startzeit und den Speicherverbrauch, damit Spiele auch auf leistungsschwachen Geräten und bei langsamen Internetverbindungen schnell laden und gut laufen. Um ein HTML5-Spiel zu optimieren, empfiehlt es sich, auf die folgenden Bereiche zu achten:

* [Speicherverbrauch](/manuals/optimization-memory)
* [Engine-Größe](/manuals/optimization-size)
* [Spielgröße](/manuals/optimization-size)

## FAQ
:[HTML5 FAQ](../shared/html5-faq.md)
