---
title: Live-Update-Inhalte per Skript verwenden
brief: Um Live-Update-Inhalte zu verwenden, musst du die Daten herunterladen und in dein Spiel einbinden. In diesem Handbuch erfährst du, wie du Live Update in Skripten verwendest.
---

# Live Update per Skript verwenden {#scripting-live-update}

Der grundlegende Arbeitsablauf für Einbindungen (mounts) verwendet `liveupdate.add_mount()`, `liveupdate.remove_mount()` und `liveupdate.get_mounts()`. Alle verfügbaren Funktionen findest du in der vollständigen [API-Referenz zu `liveupdate`](/ref/liveupdate/).

Verwende `liveupdate.is_built_with_excluded_files()`, wenn dein Code ein Bundle erkennen muss, dessen Build-Manifest ausgeschlossene Live-Update-Inhalte erwartet:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Dies gibt nur Metadaten des Build-Manifests zurück. Es bedeutet nicht, dass derzeit ein Archiv eingebunden ist oder eine bestimmte Ressource verfügbar ist. Verwende `liveupdate.get_mounts()`, um aktive Einbindungen zu untersuchen, und [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources), um die im Manifest verzeichneten Ressourcen-Hashwerte für einen Sammlungs-Proxy (collection proxy) zu untersuchen.

Der empfohlene Arbeitsablauf besteht darin, ein vollständiges ZIP-Archiv herunterzuladen und über eine URI mit `zip:` einzubinden.

## Einbindungen abrufen {#get-mounts}

`liveupdate.get_mounts()` gibt die Einbindungen zurück, die in der aktuellen Sitzung aktiv sind. Jeder Eintrag hat eine Zeichenfolge `uri`, einen numerischen Wert `priority` und einen Hashwert `name`. Die Liste enthält auch die Basiseinbindungen der Engine, deren Prioritäten unter null liegen und die nicht entfernt werden können.

Die Engine stellt Einbindungen nach einem Neustart nicht wieder her. Wenn die Anwendung zuvor heruntergeladene Inhalte in einer späteren Sitzung benötigt, muss sie die URI, den Namen und die Priorität des Pakets in ihren eigenen Speicherdaten dauerhaft speichern und beim Start erneut `liveupdate.add_mount()` aufrufen.

Wenn mehrere Pakete eingebunden sind, ist es sinnvoll, ihre von der Anwendung definierten Metadaten zu validieren. Da `mount.name` ein Hashwert ist, verwende ihn als Tabellenschlüssel oder vergleiche ihn mit `hash("mount-name")`; füge ihn nicht durch Verkettung in einen Ressourcenpfad ein. Das folgende Beispiel ordnet jedem Namens-Hashwert einen eindeutigen Pfad zu einer Metadatenressource zu:

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

Verwende für verschiedene Pakete eindeutige Metadatenpfade. Die Ressourcensuche folgt der Priorität der Einbindungen. Wenn du denselben Pfad in mehreren Paketen verwendest, wird daher die Kopie aus der Einbindung mit der höchsten Priorität gelesen.

## Skripte mit ausgeschlossenen Sammlungs-Proxys {#scripting-with-excluded-collection-proxies}

Ein Sammlungs-Proxy, der von der Bundle-Erstellung ausgeschlossen wurde, funktioniert wie ein normaler Sammlungs-Proxy, mit einem wichtigen Unterschied. Wenn du ihm eine `load`-Nachricht sendest, während noch Ressourcen im Bundle-Speicher fehlen, schlägt das Laden fehl.

Beim Arbeitsablauf mit Archiven legst du in der Regel im Voraus fest, welche Archive ein Proxy benötigt, und bindest sie vor dem Laden ein. Um die im Manifest verzeichneten Ressourcen-Hashwerte für einen bekannten ausgeschlossenen Proxy zu untersuchen, verwende `collectionproxy.get_resources()`.

Nachdem ein Paket eingebunden wurde, kann ein ausgeschlossener und entladener Proxy mit `collectionproxy.set_collection()` auch auf eine andere kompilierte Sammlung (collection) umgeleitet werden. Die Einschränkungen und die Ladereihenfolge findest du unter [Die Sammlung eines ausgeschlossenen Proxys ändern](/manuals/collection-proxy/#changing-an-excluded-proxys-collection).

Bei einem Archiv-Build, der Live-Update-Inhalte veröffentlicht, lässt das im Bundle enthaltene Hauptmanifest ausgeschlossene Live-Update-Einträge aus, während das veröffentlichte Paketmanifest sie beibehält. `collectionproxy.get_resources()` liest die Abhängigkeitsmetadaten des Manifests; es überprüft nicht, ob jeder referenzierte Datenblock verfügbar ist:

* Bevor ein Paketmanifest mit den ausgeschlossenen Einträgen des Proxys eingebunden wird, gibt `collectionproxy.get_resources("#proxy")` eine leere Tabelle `{}` zurück.
* Nachdem das entsprechende Paket eingebunden wurde, gibt die Funktion eine nicht leere Tabelle mit Ressourcen-Hashwerten für diesen Proxy zurück, zum Beispiel:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 Der folgende Beispielcode setzt voraus, dass die Ressourcen über die URL verfügbar sind, die in der Einstellung `game.http_url` angegeben ist.

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

1. `liveupdate.add_mount()` bindet ein einzelnes Archiv mit einem angegebenen Namen, einer Priorität und einer ZIP-Datei ein. Die Daten stehen dann sofort zum Laden bereit (die Engine muss nicht neu gestartet werden). Die Einbindung ist nur für die aktuelle Sitzung aktiv. Speichere den Pfad des heruntergeladenen Pakets und die gewünschten Einstellungen für die Einbindung dauerhaft in deinen eigenen Speicherdaten und rufe nach jedem Neustart erneut `liveupdate.add_mount()` auf.
2. Du musst das Archiv online speichern (z. B. auf S3), damit du es von dort herunterladen kannst.
3. Ausgehend vom Namen eines Sammlungs-Proxys musst du ermitteln, welche Archive heruntergeladen werden müssen und wie sie einzubinden sind.
4. Beim Start versuchen wir, das Level zu laden.
5. Verwende in diesem Arbeitsablauf zur Veröffentlichung von Archiven `collectionproxy.get_resources()`, um die Metadaten zu den ausgeschlossenen Inhalten des Proxys zu untersuchen. Die Funktion gibt `{}` zurück, bis das entsprechende Paketmanifest eingebunden ist, und danach eine nicht leere Tabelle mit Ressourcen-Hashwerten. Diese Hashwerte beschreiben Abhängigkeiten; das Ergebnis selbst bestätigt nicht, dass jeder Datenblock verfügbar ist.
6. Wenn der Proxy Live-Update-Inhalte verwendet und das passende Archiv noch nicht eingebunden ist, laden wir es herunter und binden es ein, bevor wir den Proxy laden.
7. Sende eine HTTP-Anfrage und lade das Archiv nach `download_path` herunter.
8. Die Daten sind heruntergeladen, und jetzt können wir sie in die laufende Engine einbinden.


Mit dem Code zum Laden können wir die Anwendung testen. Wenn du sie aus dem Editor heraus ausführst, wird allerdings nichts heruntergeladen. Der Grund dafür ist, dass Live Update eine Bundle-Funktion ist. Bei der Ausführung in der Editorumgebung werden niemals Ressourcen ausgeschlossen. Um sicherzustellen, dass alles richtig funktioniert, müssen wir ein Bundle erstellen.
