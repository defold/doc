---
title: Manipulation des fichiers
brief: Ce manuel explique comment enregistrer et charger des fichiers, ainsi que réaliser d'autres types d'opérations sur les fichiers.
---

# Manipulation des fichiers {#working-with-files}
Il existe de nombreuses façons de créer des fichiers et/ou d'y accéder. Les chemins des fichiers et les façons d'y accéder varient selon leur type et leur emplacement.

## Fonctions d'accès aux fichiers et aux dossiers {#functions-for-file-and-folder-access}
Defold propose plusieurs fonctions pour manipuler les fichiers :

* Vous pouvez utiliser les [fonctions standard `io.*`](https://defold.com/ref/stable/io/) pour lire et écrire des fichiers. Ces fonctions vous offrent un contrôle très précis sur l'ensemble du processus d'entrée/sortie.

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

* Vous pouvez utiliser [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) et [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) pour renommer et supprimer des fichiers.

* Vous pouvez utiliser [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) et [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) pour lire et écrire des tables Lua. Des fonctions [`sys.*`](https://defold.com/ref/stable/sys/) supplémentaires facilitent la résolution des chemins de fichiers indépendamment de la plateforme.

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

`sys.load()` renvoie une table vide si le fichier n'existe pas. Si le fichier existe, mais n'a pas été créé par `sys.save()`, est corrompu ou utilise un format de table sérialisée non pris en charge, `sys.load()` déclenche une erreur Lua. Utilisez `pcall()` comme ci-dessus lorsque les données de sauvegarde endommagées ou modifiées en dehors de l'application doivent pouvoir être récupérées.


## Emplacements des fichiers et des dossiers {#file-and-folder-locations}
Les emplacements des fichiers et des dossiers peuvent être répartis en trois catégories :

* Fichiers propres à votre application, créés par celle-ci
* Fichiers et dossiers inclus dans le bundle de votre application
* Fichiers propres au système auxquels votre application accède

### Comment enregistrer et charger des fichiers propres à l'application {#how-to-save-and-load-application-specific-files}
Pour enregistrer et charger des fichiers propres à l'application, comme les meilleurs scores, les paramètres utilisateur et l'état du jeu, il est recommandé d'utiliser un emplacement fourni par le système d'exploitation et spécifiquement destiné à cet usage. Vous pouvez utiliser [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) pour obtenir le chemin absolu d'un fichier adapté au système d'exploitation. Une fois ce chemin absolu obtenu, vous pouvez utiliser les fonctions `sys.*`, `io.*` et `os.*` (voir ci-dessus).

[Consultez l'exemple qui montre comment utiliser `sys.save()` et `sys.load()`](/examples/file/sys_save_load/).

### Comment accéder aux fichiers inclus dans le bundle de l'application {#how-to-access-files-bundled-with-the-application}
Vous pouvez inclure des fichiers dans votre application à l'aide de ressources de bundle et de ressources personnalisées.

#### Ressources personnalisées {#custom-resources}
:[Custom Resources](../shared/custom-resources.md)

Les extensions peuvent également fournir ces fichiers via `ext.properties`. Leurs chemins sont combinés aux ressources personnalisées du projet dans les builds de l'éditeur comme dans les archives de Bob. Consultez [Ressources personnalisées des extensions](/manuals/extensions/#custom-resources).

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

#### Ressources de bundle {#bundle-resources}
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
Pour des raisons de sécurité, les navigateurs (et, par extension, tout code JavaScript exécuté dans un navigateur) ne peuvent pas accéder aux fichiers système. Les opérations sur les fichiers fonctionnent tout de même dans les builds HTML5 de Defold, mais uniquement sur un « système de fichiers virtuel » utilisant l'API IndexedDB du navigateur. Cela signifie qu'il est impossible d'accéder aux ressources de bundle avec les fonctions `io.*` ou `os.*`. Vous pouvez cependant y accéder avec `http.request()`.
:::


#### Comparaison des ressources personnalisées et des ressources de bundle {#custom-and-bundle-resources-comparison}

| Caractéristique             | Ressources personnalisées                 | Ressources de bundle                           |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Vitesse de chargement       | Plus rapide - fichiers chargés depuis une archive binaire | Plus lente - fichiers chargés depuis le système de fichiers |
| Chargement partiel des fichiers | Non - uniquement les fichiers entiers   | Oui - lecture de n'importe quels octets du fichier |
| Modification des fichiers après la création du bundle | Non - fichiers stockés dans une archive binaire | Oui - fichiers stockés sur le système de fichiers local |
| Prise en charge HTML5       | Oui                                       | Oui - mais accès via HTTP et non par les entrées/sorties sur les fichiers |


### Accès aux fichiers système {#system-file-access}
L'accès aux fichiers système peut être limité par le système d'exploitation pour des raisons de sécurité. Vous pouvez utiliser l'extension native [`extension-directories`](https://defold.com/assets/extensiondirectories/) pour obtenir le chemin absolu de certains répertoires système courants (à savoir `documents`, `resource`, `temp`). Une fois le chemin absolu de ces fichiers obtenu, vous pouvez utiliser les fonctions `io.*` et `os.*` pour y accéder (voir ci-dessus).

::: sidenote
Pour des raisons de sécurité, les navigateurs (et, par extension, tout code JavaScript exécuté dans un navigateur) ne peuvent pas accéder aux fichiers système. Les opérations sur les fichiers fonctionnent tout de même dans les builds HTML5 de Defold, mais uniquement sur un « système de fichiers virtuel » utilisant l'API IndexedDB du navigateur. Cela signifie qu'il est impossible d'accéder aux fichiers système dans les builds HTML5.
:::

## Extensions {#extensions}
L'[Asset Portal](https://defold.com/assets/) contient plusieurs ressources qui simplifient l'accès aux fichiers et aux dossiers. Quelques exemples :

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Fonctions pour manipuler les répertoires, les autorisations des fichiers, etc.
* [DefSave](https://defold.com/assets/defsave/) - Un module qui facilite l'enregistrement et le chargement de la configuration et des données du joueur entre les sessions.
