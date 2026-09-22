---
title: Gestione dei contenuti Live Update tramite script
brief: Per usare i contenuti Live Update, devi scaricare e montare i dati nel gioco. Questo manuale spiega come usare Live Update tramite script.
---

# Utilizzo di Live Update tramite script {#scripting-live-update}

Il flusso di lavoro di base per il montaggio usa `liveupdate.add_mount()`, `liveupdate.remove_mount()` e `liveupdate.get_mounts()`. Consulta il [riferimento completo dell'API `liveupdate`](/ref/liveupdate/) per conoscere tutte le funzioni disponibili.

Usa `liveupdate.is_built_with_excluded_files()` quando il codice deve distinguere un bundle il cui manifest di build prevede contenuti Live Update esclusi:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Questa funzione restituisce soltanto i metadati del manifest di build. Non indica che un archivio sia attualmente montato o che una determinata risorsa sia disponibile. Usa `liveupdate.get_mounts()` per esaminare i punti di montaggio (mount) attivi e [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) per esaminare gli hash delle risorse registrati nel manifest per un proxy di collezione (collection proxy).

Il flusso di lavoro consigliato consiste nello scaricare e montare un archivio Zip completo usando un URI `zip:`.

## Ottenere i punti di montaggio {#get-mounts}

`liveupdate.get_mounts()` restituisce i punti di montaggio attivi nella sessione corrente. Ogni voce contiene una stringa `uri`, una `priority` numerica e un hash `name`. L'elenco contiene anche i punti di montaggio di base del motore, che hanno priorità inferiori a zero e non possono essere rimossi.

Il motore non ripristina i punti di montaggio dopo un riavvio. Se l'applicazione ha bisogno di contenuti scaricati in precedenza in una sessione successiva, deve conservare l'URI, il nome e la priorità del pacchetto nei propri dati di salvataggio e chiamare di nuovo `liveupdate.add_mount()` durante l'avvio.

Quando sono montati più pacchetti, è utile convalidare i relativi metadati definiti dall'applicazione. Poiché `mount.name` è un hash, usalo come chiave di una tabella o confrontalo con `hash("mount-name")`; non concatenarlo a un percorso di risorsa. L'esempio seguente associa a ciascun hash del nome un percorso univoco per la risorsa contenente i metadati:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- table with mounts
	local version_resources = {
		[hash("level-pack")] = "/version_level_pack.json",
		[hash("season-pack")] = "/version_season_pack.json",
	}

	for _, mount in ipairs(mounts) do
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- if it has no version file, it's likely an old/invalid archive
		end

		-- Ignore the engine's base mounts, which have negative priorities.
		if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
			liveupdate.remove_mount(mount.name)
		end
	end
end
```

Usa percorsi univoci per i metadati di pacchetti diversi. La ricerca delle risorse segue la priorità dei punti di montaggio, quindi l'uso dello stesso percorso in più pacchetti comporterebbe la lettura della copia dal punto di montaggio con la priorità più alta.

## Utilizzo dei proxy di collezione esclusi tramite script {#scripting-with-excluded-collection-proxies}

Un proxy di collezione escluso dalla creazione del bundle funziona come un normale proxy di collezione, con una differenza importante. Se gli invii un messaggio `load` mentre alcune delle sue risorse non sono ancora disponibili nello spazio di archiviazione del bundle, il caricamento fallisce.

Nel flusso di lavoro basato sugli archivi, in genere decidi in anticipo quali archivi servono a un proxy e li monti prima del caricamento. Per esaminare gli hash delle risorse registrati nel manifest per un proxy escluso noto, usa `collectionproxy.get_resources()`.

Dopo aver montato un pacchetto, puoi anche reindirizzare un proxy escluso e non caricato a un'altra collezione compilata con `collectionproxy.set_collection()`. Consulta [Modificare la collezione di un proxy escluso](/manuals/collection-proxy/#changing-an-excluded-proxys-collection) per le restrizioni e la sequenza di caricamento.

Per una build di archivio che pubblica contenuti Live Update, il manifest principale incluso nel bundle omette le voci Live Update escluse, mentre il manifest del pacchetto pubblicato le conserva. `collectionproxy.get_resources()` legge i metadati delle dipendenze del manifest; non verifica che ogni blocco di dati a cui fanno riferimento sia disponibile:

* Prima che venga montato un manifest di pacchetto contenente le voci escluse del proxy, `collectionproxy.get_resources("#proxy")` restituisce una tabella vuota `{}`.
* Dopo il montaggio del pacchetto corrispondente, restituisce una tabella non vuota di hash delle risorse per quel proxy, ad esempio:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 L'esempio di codice seguente presuppone che le risorse siano disponibili tramite l'URL specificato nell'impostazione `game.http_url`.

```lua

-- You'll need to track which archive contains which content
-- In this example, we only use a single liveupdate archive, containing all missing resource.
-- If you are using multiple archive, you need to structure the downloads accordingly
local lu_infos = {
    liveupdate = {
        name = "liveupdate",
        priority = 10,
    }
}

local function get_lu_info_for_level(level_name)
    if level_name == "level1" then
        return lu_infos['liveupdate']
    end
end

local function mount_zip(self, name, priority, path, callback)
    liveupdate.add_mount(name, "zip:" .. path, priority, function(_self, _name, _uri, _result) -- <1>
        callback(_name, _uri, _result)
    end)
end

local function has_mount(name)
    local name_hash = hash(name)
    for _, mount in ipairs(liveupdate.get_mounts()) do
        if mount.name == name_hash then
            return true
        end
    end
    return false
end

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_info_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local proxy_resources = collectionproxy.get_resources("#" .. message.level) -- <5>

        -- A build that publishes Live Update content omits excluded entries from the
        -- bundled manifest, so this table is empty until the relevant package manifest
        -- is mounted. After mounting, it contains the resource hashes for the proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Check if the archive already exists. If it does, try to mount it!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- try to load the level again
                else
                    os.remove(download_path)             -- remove and try to
                    msg.post("#", "load_level", message) -- download again
                end
            end)
        else
            -- Make the request. You can use credentials
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- try to load the level again
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- the level is loaded, and we can enable it
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` monta un singolo archivio usando un nome, una priorità e un file zip specificati. I dati sono quindi immediatamente disponibili per il caricamento (non è necessario riavviare il motore). Il punto di montaggio è attivo solo per la sessione corrente. Conserva il percorso del pacchetto scaricato e le impostazioni di montaggio desiderate nei tuoi dati di salvataggio e chiama di nuovo `liveupdate.add_mount()` dopo ogni riavvio.
2. Devi memorizzare l'archivio online (ad esempio su S3), da dove potrai scaricarlo.
3. Dato il nome di un proxy di collezione, devi determinare quali archivi scaricare e come montarli
4. All'avvio, proviamo a caricare il livello.
5. In questo flusso di lavoro che pubblica archivi, usa `collectionproxy.get_resources()` per esaminare i metadati dei contenuti esclusi del proxy. Restituisce `{}` finché non viene montato il manifest del pacchetto corrispondente e una tabella non vuota di hash delle risorse dopo il montaggio. Questi hash descrivono le dipendenze; il risultato in sé non verifica che ogni blocco di dati sia disponibile.
6. Se il proxy usa contenuti Live Update e l'archivio corrispondente non è ancora montato, lo scarichiamo e lo montiamo prima di caricare il proxy.
7. Esegui una richiesta HTTP e scarica l'archivio in `download_path`
8. I dati sono stati scaricati ed è il momento di montarli nel motore in esecuzione.


Una volta predisposto il codice di caricamento, possiamo testare l'applicazione. Tuttavia, eseguendola dall'editor non verrà scaricato nulla, perché Live Update è una funzionalità dei bundle. Durante l'esecuzione nell'ambiente dell'editor non vengono mai escluse risorse. Per assicurarci che tutto funzioni correttamente, dobbiamo creare un bundle.
