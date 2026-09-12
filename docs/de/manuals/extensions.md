---
title: Native Erweiterungen für Defold schreiben
brief: Dieses Handbuch erklärt, wie du eine native Erweiterung für die Defold-Game-Engine schreibst und sie mit den Cloud-Build-Diensten ohne Einrichtungsaufwand kompilierst.
---

# Native Erweiterungen {#native-extensions}

Wenn du eine angepasste Interaktion mit externer Software oder Hardware auf niedriger Ebene benötigst, für die Lua nicht ausreicht, kannst du mit dem Defold-SDK native Erweiterungen (native extensions) für die Engine in C, C++, C#, Objective-C, Java oder JavaScript schreiben, abhängig von der Zielplattform. Typische Anwendungsfälle für native Erweiterungen sind:

- Interaktion mit bestimmter Hardware, beispielsweise der Kamera von Mobiltelefonen.
- Interaktion mit externen APIs auf niedriger Ebene, beispielsweise APIs von Werbenetzwerken, die keine Interaktion über Netzwerk-APIs zulassen, bei denen Luasocket verwendet werden könnte.
- Berechnungen und Datenverarbeitung mit hoher Leistung.

::: sidenote
Die Unterstützung für C# ist experimentell und für native Erweiterungen vorgesehen, nicht für Skriptkomponenten (script components) von Defold. Sie verwendet .NET 9 NativeAOT, um eine statische Bibliothek zu erzeugen. Füge `.cs`-Quelldateien zum Ordner `src` einer Erweiterung hinzu; der Build-Dienst erzeugt die Projektdatei. Die Unterstützung von Zielplattformen richtet sich nach den aktuellen Möglichkeiten von NativeAOT und des Build-Dienstes. Den aktuellen Arbeitsablauf und die getestete Einrichtung findest du im offiziellen [Sprachbeispiel für native Erweiterungen](https://github.com/defold/example-languages).
:::

## Der Build-Server {#the-build-server}

Defold bietet mit einer cloudbasierten Build-Lösung einen Einstieg in native Erweiterungen ohne Einrichtungsaufwand. Jede native Erweiterung, die entwickelt und einem Spielprojekt entweder direkt oder über ein [Bibliotheksprojekt](/manuals/libraries/) hinzugefügt wird, wird Teil des gewöhnlichen Projektinhalts. Du musst keine speziellen Versionen der Engine erstellen und an Teammitglieder verteilen. Das geschieht automatisch---jedes Teammitglied, das einen Build des Projekts erstellt und ausführt, erhält eine projektspezifische ausführbare Engine-Datei mit allen eingebundenen nativen Erweiterungen.

![Cloud-Build](images/extensions/cloud_build.png)

Defold stellt den Cloud-Build-Server kostenlos und ohne Nutzungsbeschränkungen bereit. Der Server wird in Europa gehostet. Die URL, an die nativer Code gesendet wird, wird im [Fenster für die Editoreinstellungen](/manuals/editor-preferences/#extensions) oder über die Befehlszeilenoption `--build-server` von [bob](/manuals/bob/#usage) konfiguriert. Wenn du deinen eigenen Server einrichten möchtest, [folge dieser Anleitung](/manuals/extender-local-setup).

## Projektstruktur {#project-layout}

Um eine neue Erweiterung zu erstellen, lege einen Ordner im Stammverzeichnis des Projekts an. Dieser Ordner enthält alle Einstellungen, den Quellcode, die Bibliotheken und die Ressourcen der Erweiterung. Der Build-Dienst für Erweiterungen erkennt die Ordnerstruktur und sammelt alle Quelldateien und Bibliotheken.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: Der Erweiterungsordner _muss_ eine Datei *ext.manifest* enthalten. Diese Konfigurationsdatei enthält Flags und Defines, die beim Erstellen eines Builds einer einzelnen Erweiterung verwendet werden. Die Definition des Dateiformats findest du im [Handbuch zum Erweiterungsmanifest](https://defold.com/manuals/extensions-ext-manifests/).

*src*
: Dieser Ordner sollte alle Quellcodedateien enthalten.

*include*
: Dieser optionale Ordner enthält Include-Dateien.

*lib*
: Dieser optionale Ordner enthält kompilierte Bibliotheken, von denen die Erweiterung abhängt. Bibliotheksdateien sollten in Unterordnern mit Namen nach dem Schema `platform` oder `architecture-platform` abgelegt werden, je nachdem, welche Architekturen deine Bibliotheken unterstützen.

  :[platforms](../shared/platforms.md)

*manifests*
: Dieser optionale Ordner enthält zusätzliche Dateien, die beim Build-Vorgang oder bei der Bundle-Erstellung verwendet werden. Einzelheiten findest du weiter unten.

*res*
: Dieser optionale Ordner enthält zusätzliche Ressourcen, von denen die Erweiterung abhängt. Ressourcendateien sollten in Unterordnern mit Namen nach dem Schema `platform` oder `architecture-platform` abgelegt werden, genauso wie im Ordner `lib`. Ein Unterordner `common` ist ebenfalls zulässig. Er enthält Ressourcendateien, die allen Plattformen gemeinsam sind.

### Manifestdateien {#manifest-files}

Der optionale Ordner *manifests* einer Erweiterung enthält zusätzliche Dateien, die beim Build-Vorgang und bei der Bundle-Erstellung verwendet werden. Dateien sollten in Unterordnern mit Namen nach dem Schema `platform` abgelegt werden:

* `android` - Dieser Ordner nimmt eine Manifest-Teildatei auf, die mit dem Manifest der Hauptanwendung zusammengeführt wird ([wie hier beschrieben](/manuals/extensions-manifest-merge-tool)).
  * Der Ordner kann auch eine Datei `build.gradle` mit Abhängigkeiten enthalten, die [von Gradle aufgelöst werden](/manuals/extensions-gradle).
  * Erweiterungen mit Java-Code sollten eine [Datei mit R8-Keep-Regeln](#r8-keep-rules-for-android) (`.keep`) für die Klassen enthalten, die sie zur Laufzeit benötigen.
* `ios` - Dieser Ordner nimmt eine Manifest-Teildatei auf, die mit dem Manifest der Hauptanwendung zusammengeführt wird ([wie hier beschrieben](/manuals/extensions-manifest-merge-tool)).
  * Der Ordner kann auch eine Datei `Podfile` mit Abhängigkeiten enthalten, die [von Cocoapods aufgelöst werden](/manuals/extensions-cocoapods).
* `osx` - Dieser Ordner nimmt eine Manifest-Teildatei auf, die mit dem Manifest der Hauptanwendung zusammengeführt wird ([wie hier beschrieben](/manuals/extensions-manifest-merge-tool)).
* `web` - Dieser Ordner nimmt eine Manifest-Teildatei auf, die mit dem Manifest der Hauptanwendung zusammengeführt wird ([wie hier beschrieben](/manuals/extensions-manifest-merge-tool)).


### R8-Keep-Regeln für Android {#r8-keep-rules-for-android}

Füge im Verzeichnis `manifests/android` der Erweiterung neben `build.gradle` eine Datei mit der Endung `.keep` hinzu. Beispielsweise kann `/myextension/manifests/android/myextension.keep` die Java-Klassen der Erweiterung mit folgender Regel erhalten:

```proguard
-keep,allowoptimization class com.example.myextension.** { *; }
```

Ersetze `com.example.myextension` durch das Paket, das die Java-Klassen deiner Erweiterung enthält. Diese Regel erhält die Klassen und ihre Mitglieder, erlaubt R8 aber, ihren Code zu optimieren. Füge Regeln für weitere Klassen hinzu, auf die über das Java Native Interface (JNI) oder Reflexion zugegriffen wird, da R8 diese Verwendungen möglicherweise nicht automatisch erkennt.

Wenn die Erweiterung zur Laufzeit auf Annotationen angewiesen ist, füge außerdem Folgendes hinzu:

```proguard
-keepattributes *Annotation*
```

Diese Regeln werden mit der ausgewählten Keep-Datei des Projekts kombiniert, wenn [R8 aktiviert ist](/manuals/android/#enabling-r8).


## Benutzerdefinierte Ressourcen {#custom-resources}

Eine Erweiterung kann Daten in das Spielarchiv aufnehmen, indem sie benutzerdefinierte Ressourcen in einer Datei `ext.properties` neben ihrer Datei `ext.manifest` deklariert:

```ini
[project]
custom_resources.default = /myextension/data
```

Lege beispielsweise eine JSON-Datei unter `/myextension/data/settings.json` ab. Der Pfad ist relativ zum Stammverzeichnis des Projekts und enthält den Erweiterungsordner. Wenn du die Erweiterung als Bibliothek teilst, nimm `myextension` in die [Include Dirs](/manuals/libraries/#setting-up-library-sharing) der Bibliothek auf, damit Projekte, die sie verwenden, die Erweiterung und ihre Daten erhalten.

Diese Pfade werden mit `project.custom_resources` aus *game.project* und den Einträgen anderer Erweiterungen kombiniert. Das Festlegen benutzerdefinierter Ressourcen im Projekt ersetzt die Einträge der Erweiterungen nicht. Sowohl Editor-Builds als auch Bob-Archive enthalten die Dateien, die zur Laufzeit geladen werden können:

```lua
local data, err = sys.load_resource("/myextension/data/settings.json")
if data then
    local settings = json.decode(data)
    pprint(settings)
else
    print(err)
end
```

Unter [Dateizugriff](/manuals/file-access/#custom-resources) erfährst du, wie sich benutzerdefinierte Ressourcen von Bundle-Ressourcen unterscheiden.

## Eine Erweiterung teilen {#sharing-an-extension}

Erweiterungen werden genauso behandelt wie alle anderen Assets in deinem Projekt und können auf dieselbe Weise geteilt werden. Wenn ein Ordner mit einer nativen Erweiterung als Bibliotheksordner hinzugefügt wird, kann er geteilt und von anderen als Projektabhängigkeit verwendet werden. Weitere Informationen findest du im [Handbuch zu Bibliotheksprojekten](/manuals/libraries/).


## Eine einfache Beispielerweiterung {#a-simple-example-extension}

Erstellen wir eine sehr einfache Erweiterung. Zuerst legen wir einen neuen Ordner *`myextension`* im Stammverzeichnis an und fügen eine Datei *`ext.manifest`* hinzu, die den Namen der Erweiterung „`MyExtension`“ enthält. Beachte, dass der Name ein C++-Symbol ist und mit dem ersten Argument von `DM_DECLARE_EXTENSION` übereinstimmen muss (siehe unten).

![Manifest](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

Die Erweiterung besteht aus einer einzigen C++-Datei, *`myextension.cpp`*, die im Ordner „`src`“ erstellt wird.

![C++-Datei](images/extensions/cppfile.png)

Die Quelldatei der Erweiterung enthält den folgenden Code:

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Beachte das Makro `DM_DECLARE_EXTENSION`, mit dem die verschiedenen Einstiegspunkte in den Code der Erweiterung deklariert werden. Das erste Argument `symbol` muss mit dem in *ext.manifest* angegebenen Namen übereinstimmen. Für dieses einfache Beispiel sind keine Einstiegspunkte für `update` oder `on_event` nötig. Daher wird dem Makro an diesen Stellen `0` übergeben.

Jetzt musst du nur noch einen Build des Projekts erstellen (<kbd>Project ▸ Build</kbd>). Dadurch wird die Erweiterung zum Build-Dienst für Erweiterungen hochgeladen, der eine angepasste Engine mit der neuen Erweiterung erzeugt. Falls der Build-Dienst Fehler feststellt, erscheint ein Dialogfeld mit den Build-Fehlern.

Um die Erweiterung zu testen, erstelle ein Spielobjekt (game object) und füge eine Skriptkomponente mit etwas Testcode hinzu:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

Das war's! Wir haben eine vollständig funktionsfähige native Erweiterung erstellt.


## Lebenszyklus einer Erweiterung {#extension-lifecycle}

Wie oben gezeigt, wird das Makro `DM_DECLARE_EXTENSION` verwendet, um die verschiedenen Einstiegspunkte in den Code der Erweiterung zu deklarieren:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

Über die Einstiegspunkte kannst du Code zu verschiedenen Zeitpunkten im Lebenszyklus einer Erweiterung ausführen:

* Start der Engine
  * Die Systeme der Engine starten
  * `app_init` der Erweiterung
  * `init` der Erweiterung - Alle Defold-APIs wurden initialisiert. Dies ist der empfohlene Zeitpunkt im Lebenszyklus der Erweiterung, um Lua-Anbindungen an den Code der Erweiterung zu erstellen.
  * Initialisierung der Skripte - Die Funktion `init()` der Skriptdateien wird aufgerufen.
* Engine-Schleife
  * Aktualisierung der Engine
    * `update` der Erweiterung
    * Aktualisierung der Skripte - Die Funktion `update()` der Skriptdateien wird aufgerufen.
  * Engine-Ereignisse (Fenster minimieren/maximieren usw.)
    * `on_event` der Erweiterung
* Beenden der Engine (oder Neustart)
  * Finalisierung der Skripte - Die Funktion `final()` der Skriptdateien wird aufgerufen.
  * `final` der Erweiterung
  * `app_final` der Erweiterung

## Definierte Plattformbezeichner {#defined-platform-identifiers}

Die folgenden Bezeichner werden vom Build-Dienst auf der jeweiligen Plattform definiert:

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Protokolle des Build-Servers {#build-server-logs}

Protokolle des Build-Servers sind verfügbar, wenn das Projekt native Erweiterungen verwendet. Das Protokoll des Build-Servers (`log.txt`) wird beim Erstellen eines Builds des Projekts zusammen mit der angepassten Engine heruntergeladen, in der Datei `.internal/%platform%/build.zip` gespeichert und außerdem in den Build-Ordner deines Projekts entpackt.

## Beispielerweiterungen {#example-extensions}

* [Einfaches Erweiterungsbeispiel](https://github.com/defold/template-native-extension) (die Erweiterung aus diesem Handbuch)
* [Beispiel für eine Android-Erweiterung](https://github.com/defold/extension-android)
* [Beispiel für eine HTML5-Erweiterung](https://github.com/defold/extension-html5)
* [Videoplayer-Erweiterung für macOS, iOS und Android](https://github.com/defold/extension-videoplayer)
* [Kamera-Erweiterung für macOS und iOS](https://github.com/defold/extension-camera)
* [Erweiterung für In-App-Käufe unter iOS und Android](https://github.com/defold/extension-iap)
* [Firebase-Analytics-Erweiterung für iOS und Android](https://github.com/defold/extension-firebase-analytics)

Das [Defold Asset Portal](https://www.defold.com/assets/) enthält ebenfalls mehrere native Erweiterungen.
