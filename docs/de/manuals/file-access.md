---
title: Mit Dateien arbeiten
brief: Dieses Handbuch erklärt, wie du Dateien speicherst und lädst und andere Dateioperationen ausführst.
---

# Mit Dateien arbeiten {#working-with-files}
Es gibt viele verschiedene Möglichkeiten, Dateien zu erstellen und/oder auf sie zuzugreifen. Die Dateipfade und die Art des Zugriffs unterscheiden sich je nach Dateityp und Speicherort der Datei.

## Funktionen für den Zugriff auf Dateien und Ordner {#functions-for-file-and-folder-access}
Defold bietet verschiedene Funktionen für die Arbeit mit Dateien:

* Du kannst die standardmäßigen [`io.*`-Funktionen](https://defold.com/ref/stable/io/) verwenden, um Dateien zu lesen und zu schreiben. Mit diesen Funktionen kannst du den gesamten Ein-/Ausgabeprozess sehr genau steuern.

```lua
-- open myfile.txt for writing in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- write to the file, flush it to disk and then close the file
f:write("Foobar")
f:flush()
f:close()

-- open myfile.txt for reading in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- read the entire file as a string
-- returns nil on failure
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* Du kannst [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) und [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) verwenden, um Dateien umzubenennen und zu löschen.

* Du kannst [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) und [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) verwenden, um Lua-Tabellen zu lesen und zu schreiben. Weitere [`sys.*`](https://defold.com/ref/stable/sys/)-Funktionen helfen dabei, Dateipfade plattformunabhängig zu ermitteln.

```lua
-- get a platform independent path to the file "highscore" for application "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- save a Lua table with some data
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- load the data
local ok, data = pcall(sys.load, path)
if not ok then
	-- The file exists, but is corrupt, foreign, or uses an unsupported format.
	print("Failed to load save data:", data)
	data = {}
end
print(data.highscore) -- 100
```

`sys.load()` gibt eine leere Tabelle zurück, wenn die Datei nicht existiert. Wenn die Datei existiert, aber nicht mit `sys.save()` erstellt wurde, beschädigt ist oder ein nicht unterstütztes Format für serialisierte Tabellen verwendet, löst `sys.load()` einen Lua-Fehler aus. Verwende wie oben gezeigt `pcall()`, wenn die Anwendung Fehler durch beschädigte oder extern veränderte Speicherdaten abfangen können muss.


## Speicherorte von Dateien und Ordnern {#file-and-folder-locations}
Die Speicherorte von Dateien und Ordnern lassen sich in drei Kategorien einteilen:

* Anwendungsspezifische Dateien, die deine Anwendung erstellt
* Dateien und Ordner, die mit deiner Anwendung gebündelt werden
* Systemspezifische Dateien, auf die deine Anwendung zugreift

### Anwendungsspezifische Dateien speichern und laden {#how-to-save-and-load-application-specific-files}
Es wird empfohlen, anwendungsspezifische Dateien wie Höchstpunktzahlen, Benutzereinstellungen und den Spielzustand an einem Speicherort zu speichern und zu laden, den das Betriebssystem eigens für diesen Zweck bereitstellt. Mit [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) kannst du den betriebssystemspezifischen absoluten Pfad zu einer Datei ermitteln. Sobald du den absoluten Pfad hast, kannst du die Funktionen `sys.*`, `io.*` und `os.*` verwenden (siehe oben).

[Sieh dir das Beispiel zur Verwendung von `sys.save()` und `sys.load()` an](/examples/file/sys_save_load/).

### Auf Dateien zugreifen, die mit der Anwendung gebündelt sind {#how-to-access-files-bundled-with-the-application}
Mit Bundle-Ressourcen (bundle resources) und benutzerdefinierten Ressourcen (custom resources) kannst du Dateien in deine Anwendung aufnehmen.

#### Benutzerdefinierte Ressourcen {#custom-resources}
:[Custom Resources](../shared/custom-resources.md)

Erweiterungen können diese Dateien auch über `ext.properties` bereitstellen. Ihre Pfade werden sowohl bei Editor-Builds als auch bei Bob-Archiven mit den benutzerdefinierten Ressourcen des Projekts zusammengeführt. Siehe [benutzerdefinierte Ressourcen von Erweiterungen](/manuals/extensions/#custom-resources).

```lua
-- Load level data into a string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decode json string to a Lua table
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Bundle-Ressourcen {#bundle-resources}
:[Bundle Resources](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: sidenote
Aus Sicherheitsgründen dürfen Browser (und damit auch jeglicher JavaScript-Code, der in einem Browser ausgeführt wird) nicht auf Systemdateien zugreifen. Dateioperationen funktionieren in HTML5-Builds von Defold weiterhin, allerdings nur in einem „virtuellen Dateisystem“, das die IndexedDB-API des Browsers verwendet. Das bedeutet, dass du mit den Funktionen `io.*` oder `os.*` nicht auf Bundle-Ressourcen zugreifen kannst. Du kannst jedoch mit `http.request()` auf Bundle-Ressourcen zugreifen.
:::


#### Benutzerdefinierte Ressourcen und Bundle-Ressourcen – Vergleich {#custom-and-bundle-resources-comparison}

| Merkmal                     | Benutzerdefinierte Ressourcen             | Bundle-Ressourcen                              |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Ladegeschwindigkeit         | Schneller – Dateien werden aus einem Binärarchiv geladen | Langsamer – Dateien werden aus dem Dateisystem geladen |
| Dateien teilweise laden     | Nein – nur vollständige Dateien           | Ja – beliebige Bytes aus einer Datei lesen     |
| Dateien nach der Bundle-Erstellung ändern | Nein – Dateien sind in einem Binärarchiv gespeichert | Ja – Dateien sind im lokalen Dateisystem gespeichert |
| HTML5-Unterstützung         | Ja                                        | Ja – aber Zugriff über HTTP und nicht über Datei-Ein-/Ausgabe |


### Zugriff auf Systemdateien {#system-file-access}
Das Betriebssystem kann den Zugriff auf Systemdateien aus Sicherheitsgründen einschränken. Mit der nativen Erweiterung (native extension) [`extension-directories`](https://defold.com/assets/extensiondirectories/) kannst du den absoluten Pfad zu einigen gängigen Systemverzeichnissen ermitteln (z. B. `documents`, `resource`, `temp`). Sobald du den absoluten Pfad dieser Dateien hast, kannst du mit den Funktionen `io.*` und `os.*` auf die Dateien zugreifen (siehe oben).

::: sidenote
Aus Sicherheitsgründen dürfen Browser (und damit auch jeglicher JavaScript-Code, der in einem Browser ausgeführt wird) nicht auf Systemdateien zugreifen. Dateioperationen funktionieren in HTML5-Builds von Defold weiterhin, allerdings nur in einem „virtuellen Dateisystem“, das die IndexedDB-API des Browsers verwendet. Das bedeutet, dass du in HTML5-Builds nicht auf Systemdateien zugreifen kannst.
:::

## Erweiterungen {#extensions}
Das [Asset Portal](https://defold.com/assets/) enthält verschiedene Assets, die den Zugriff auf Dateien und Ordner vereinfachen. Einige Beispiele:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Funktionen für die Arbeit mit Verzeichnissen, Dateiberechtigungen usw.
* [DefSave](https://defold.com/assets/defsave/) - Ein Modul, mit dem du Konfigurations- und Spielerdaten über Sitzungen hinweg speichern und laden kannst.
