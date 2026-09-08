---
title: Utiliser le contenu Live Update dans des scripts
brief: Pour utiliser le contenu Live Update, vous devez télécharger les données et les monter dans votre jeu. Ce manuel vous explique comment utiliser Live Update dans des scripts.
---

# Utiliser Live Update dans des scripts {#scripting-live-update}

Le flux de travail de montage repose sur `liveupdate.add_mount()`, `liveupdate.remove_mount()` et `liveupdate.get_mounts()`. Consultez la [référence complète de l'API `liveupdate`](/ref/liveupdate/) pour connaître toutes les fonctions disponibles.

Utilisez `liveupdate.is_built_with_excluded_files()` lorsque le code doit identifier un bundle dont le manifeste de build attend du contenu Live Update exclu :

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Le résultat reflète uniquement les métadonnées du manifeste de build. Cela ne signifie pas qu'une archive est actuellement montée ni qu'une ressource particulière est disponible. Utilisez `liveupdate.get_mounts()` pour inspecter les montages actifs et [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) pour inspecter les hachages de ressources enregistrés dans le manifeste pour un proxy de collection (collection proxy).

Le flux de travail recommandé consiste à télécharger et à monter une archive Zip complète à l'aide d'un URI `zip:`.

## Obtenir les montages {#get-mounts}

`liveupdate.get_mounts()` renvoie les montages actifs dans la session actuelle. Chaque entrée comporte une chaîne `uri`, une valeur numérique `priority` et une valeur hachée `name`. La liste contient également les montages de base du moteur, dont les priorités sont inférieures à zéro et qui ne peuvent pas être supprimés.

Le moteur ne rétablit pas les montages après un redémarrage. Si l'application a besoin de contenu précédemment téléchargé lors d'une session ultérieure, elle doit conserver l'URI, le nom et la priorité du paquet dans ses propres données de sauvegarde et rappeler `liveupdate.add_mount()` au démarrage.

Lorsque plusieurs paquets sont montés, il est utile de valider leurs métadonnées définies par l'application. Puisque `mount.name` est une valeur hachée, utilisez-la comme clé de table ou comparez-la à `hash("mount-name")` ; ne la concaténez pas dans un chemin de ressource. L'exemple suivant associe chaque nom haché à un chemin unique de ressource de métadonnées :

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

Utilisez des chemins de métadonnées uniques pour les différents paquets. La recherche de ressources suit la priorité des montages : utiliser le même chemin dans plusieurs paquets conduirait donc à lire la copie du montage ayant la priorité la plus élevée.

## Utiliser des proxys de collection exclus dans des scripts {#scripting-with-excluded-collection-proxies}

Un proxy de collection exclu de la création du bundle fonctionne comme un proxy de collection normal, avec une différence importante. Lui envoyer un message `load` alors que certaines de ses ressources sont encore indisponibles dans le stockage du bundle provoquera un échec.

Dans le flux de travail fondé sur les archives, vous déterminez généralement à l'avance la ou les archives dont un proxy a besoin et vous les montez avant le chargement. Pour inspecter les hachages de ressources enregistrés dans le manifeste pour un proxy exclu connu, utilisez `collectionproxy.get_resources()`.

Une fois un paquet monté, un proxy exclu et non chargé peut également être redirigé vers une autre collection compilée avec `collectionproxy.set_collection()`. Consultez [Changer la collection d'un proxy exclu](/manuals/collection-proxy/#changing-an-excluded-proxys-collection) pour connaître les restrictions et la séquence de chargement.

Pour un build d'archive qui publie du contenu Live Update, le manifeste principal inclus dans le bundle omet les entrées Live Update exclues, tandis que le manifeste du paquet publié les conserve. `collectionproxy.get_resources()` lit les métadonnées de dépendances du manifeste ; cette fonction ne vérifie pas que chaque bloc de données référencé est disponible :

* Avant le montage d'un manifeste de paquet contenant les entrées exclues du proxy, `collectionproxy.get_resources("#proxy")` renvoie une table vide `{}`.
* Une fois le paquet concerné monté, cette fonction renvoie une table non vide de hachages de ressources pour ce proxy, par exemple :

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 L'exemple de code suivant suppose que les ressources sont disponibles à l'URL indiquée dans le paramètre `game.http_url`.

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

1. La fonction `liveupdate.add_mount()` monte une seule archive à partir d'un nom, d'une priorité et d'un fichier zip spécifiés. Les données sont alors immédiatement disponibles pour le chargement (il n'est pas nécessaire de redémarrer le moteur). Le montage n'est actif que pour la session actuelle. Conservez le chemin du paquet téléchargé et les paramètres de montage souhaités dans vos propres données de sauvegarde, puis rappelez `liveupdate.add_mount()` après chaque redémarrage.
2. Vous devez stocker l'archive en ligne (par exemple sur S3), d'où vous pourrez la télécharger.
3. À partir du nom d'un proxy de collection, vous devez déterminer la ou les archives à télécharger et la manière de les monter
4. Au démarrage, nous essayons de charger le niveau.
5. Dans ce flux de travail de publication d'archives, utilisez `collectionproxy.get_resources()` pour inspecter les métadonnées du contenu exclu du proxy. Cette fonction renvoie `{}` tant que le manifeste du paquet concerné n'est pas monté, puis une table non vide de hachages de ressources après le montage. Ces hachages décrivent des dépendances ; le résultat ne vérifie pas à lui seul que chaque bloc de données est disponible.
6. Si le proxy utilise du contenu Live Update et que l'archive correspondante n'est pas encore montée, nous la téléchargeons et la montons avant de charger le proxy.
7. Effectuez une requête HTTP et téléchargez l'archive vers `download_path`
8. Les données sont téléchargées et il est temps de les monter dans le moteur en cours d'exécution.


Une fois le code de chargement en place, nous pouvons tester l'application. Cependant, son exécution depuis l'éditeur ne téléchargera rien. En effet, Live Update est une fonctionnalité des bundles. Lors de l'exécution dans l'environnement de l'éditeur, aucune ressource n'est jamais exclue. Pour vérifier que tout fonctionne correctement, nous devons créer un bundle.
