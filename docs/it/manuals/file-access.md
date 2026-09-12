---
title: Lavorare con i file
brief: Questo manuale spiega come salvare e caricare file ed eseguire altri tipi di operazioni sui file.
---

# Lavorare con i file {#working-with-files}
Esistono molti modi diversi per creare file e accedervi. I percorsi dei file e le modalità di accesso variano in base al tipo di file e alla sua posizione.

## Funzioni per l'accesso a file e cartelle {#functions-for-file-and-folder-access}
Defold offre diverse funzioni per lavorare con i file:

* Puoi usare le [funzioni standard `io.*`](https://defold.com/ref/stable/io/) per leggere e scrivere file. Queste funzioni offrono un controllo molto preciso sull'intero processo di I/O.

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

* Puoi usare [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) e [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) per rinominare ed eliminare file.

* Puoi usare [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) e [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) per leggere e scrivere tabelle Lua. Sono disponibili altre funzioni [`sys.*`](https://defold.com/ref/stable/sys/) che aiutano a risolvere i percorsi dei file in modo indipendente dalla piattaforma.

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

`sys.load()` restituisce una tabella vuota se il file non esiste. Se il file esiste ma non è stato creato da `sys.save()`, è danneggiato o usa un formato di tabella serializzata non supportato, `sys.load()` genera un errore Lua. Usa `pcall()` come nell'esempio precedente quando occorre poter gestire dati di salvataggio danneggiati o modificati dall'esterno.


## Posizioni di file e cartelle {#file-and-folder-locations}
Le posizioni di file e cartelle si possono suddividere in tre categorie:

* File specifici dell'applicazione creati dalla tua applicazione
* File e cartelle inclusi nel bundle della tua applicazione
* File specifici del sistema a cui accede la tua applicazione

### Come salvare e caricare file specifici dell'applicazione {#how-to-save-and-load-application-specific-files}
Quando salvi e carichi file specifici dell'applicazione, come punteggi migliori, impostazioni dell'utente e stato del gioco, è consigliabile usare una posizione fornita dal sistema operativo e destinata appositamente a questo scopo. Puoi usare [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) per ottenere il percorso assoluto di un file nella posizione prevista dal sistema operativo. Una volta ottenuto il percorso assoluto, puoi usare le funzioni `sys.*`, `io.*` e `os.*` (vedi sopra).

[Consulta l'esempio che mostra come usare `sys.save()` e `sys.load()`](/examples/file/sys_save_load/).

### Come accedere ai file inclusi nel bundle dell'applicazione {#how-to-access-files-bundled-with-the-application}
Puoi includere file nella tua applicazione usando risorse del bundle (bundle resources) e risorse personalizzate (custom resources).

#### Risorse personalizzate {#custom-resources}
:[Custom Resources](../shared/custom-resources.md)

Anche le estensioni possono fornire questi file tramite `ext.properties`. I loro percorsi vengono combinati con le risorse personalizzate del progetto sia nelle build dell'editor sia negli archivi di Bob. Consulta [Risorse personalizzate delle estensioni](/manuals/extensions/#custom-resources).

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

#### Risorse del bundle {#bundle-resources}
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
Per motivi di sicurezza, i browser (e di conseguenza qualsiasi codice JavaScript eseguito al loro interno) non possono accedere ai file di sistema. Le operazioni sui file nelle build HTML5 di Defold funzionano comunque, ma solo su un "file system virtuale" che usa l'API IndexedDB del browser. Questo significa che non è possibile accedere alle risorse del bundle tramite le funzioni `io.*` o `os.*`. Puoi però accedere alle risorse del bundle tramite `http.request()`.
:::


#### Risorse personalizzate e risorse del bundle - confronto {#custom-and-bundle-resources-comparison}

| Caratteristica              | Risorse personalizzate                          | Risorse del bundle                               |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Velocità di caricamento     | Maggiore - file caricati da un archivio binario | Minore - file caricati dal file system          |
| Caricamento parziale dei file | No - solo file interi                     | Sì - lettura di qualsiasi porzione di byte del file |
| Modifica dei file dopo la creazione del bundle | No - file memorizzati in un archivio binario | Sì - file memorizzati nel file system locale    |
| Supporto HTML5              | Sì                                        | Sì - ma con accesso tramite HTTP anziché I/O su file |


### Accesso ai file di sistema {#system-file-access}
Il sistema operativo può limitare l'accesso ai file di sistema per motivi di sicurezza. Puoi usare l'estensione nativa [`extension-directories`](https://defold.com/assets/extensiondirectories/) per ottenere il percorso assoluto di alcune directory di sistema comuni (ad esempio `documents`, `resource`, `temp`). Una volta ottenuto il percorso assoluto di questi file, puoi usare le funzioni `io.*` e `os.*` per accedervi (vedi sopra).

::: sidenote
Per motivi di sicurezza, i browser (e di conseguenza qualsiasi codice JavaScript eseguito al loro interno) non possono accedere ai file di sistema. Le operazioni sui file nelle build HTML5 di Defold funzionano comunque, ma solo su un "file system virtuale" che usa l'API IndexedDB del browser. Questo significa che non è possibile accedere ai file di sistema nelle build HTML5.
:::

## Estensioni {#extensions}
L'[Asset Portal](https://defold.com/assets/) contiene diversi asset per semplificare l'accesso a file e cartelle. Alcuni esempi:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Funzioni per lavorare con directory, autorizzazioni dei file, ecc.
* [DefSave](https://defold.com/assets/defsave/) - Un modulo che aiuta a salvare e caricare la configurazione e i dati del giocatore tra una sessione e l'altra.
