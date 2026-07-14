---
title: Scripting con contenido de Live Update
brief: Para usar el contenido de Live Update, necesitas descargar y montar los datos en tu juego. Aprende cómo usar scripts con Live Update en este manual.
---

# Scripting con Live Update

El flujo de montaje principal usa `liveupdate.add_mount()`, `liveupdate.remove_mount()` y `liveupdate.get_mounts()`. Consulta la [referencia completa de la API `liveupdate`](/ref/liveupdate/) para conocer todas las funciones disponibles.

Usa `liveupdate.is_built_with_excluded_files()` cuando el código necesite distinguir un bundle cuyo manifiesto de build espera contenido excluido de Live Update:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Esto solo informa sobre los metadatos del manifiesto de build. No significa que haya un archivo montado en ese momento ni que un recurso concreto esté disponible. Usa `liveupdate.get_mounts()` para inspeccionar los montajes activos y [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources) para inspeccionar los hashes de recursos registrados en el manifiesto de un proxy de colección.

El flujo recomendado consiste en descargar y montar un archivo Zip completo con una URI `zip:`.

## Obtener montajes

`liveupdate.get_mounts()` devuelve los montajes activos en la sesión actual. Cada entrada contiene una URI `mount.uri`, una prioridad numérica `mount.priority` y un hash `mount.name`. Los montajes no se restauran al reiniciar; la aplicación debe guardar los ajustes necesarios y volver a llamar a `liveupdate.add_mount()`.

Como `mount.name` es un hash, úsalo como clave de tabla o compáralo con `hash("nombre")`; no lo concatenes en una ruta. Asigna cada hash a una ruta de metadatos única:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- tabla con montajes
	local version_resources = {
		[hash("liveupdate")] = "/version_liveupdate.json",
	}

    -- Cada montaje tiene: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- Esto requiere que el nombre de archivo sea único, para que no obtengamos un archivo desde un archivo comprimido de Live Update diferente
        -- Estos datos los crea el desarrollador como forma de especificar metadatos para el archivo comprimido
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- si no tiene archivo de versión, es probable que sea un archivo comprimido antiguo/no válido
		end

        -- verificar la versión del archivo comprimido contra la versión soportada por el juego
        if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- no era válido, así que lo desmontamos!
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## Scripting con proxies de colección excluidos

Un proxy de colección (collection proxy) que se ha excluido del bundling funciona como un proxy de colección normal, con una diferencia importante. Enviarle un mensaje `load` mientras todavía tiene recursos que no están disponibles en el almacenamiento del bundle hará que falle.

En el flujo de trabajo basado en archivos comprimidos de Live Update, por lo general decides de antemano qué archivo comprimido o archivos comprimidos necesita un proxy y los montas antes de cargar. Para inspeccionar los hashes de recursos registrados en el manifiesto de un proxy excluido conocido, usa `collectionproxy.get_resources()`.

Después de montar un paquete, un proxy excluido y no cargado también puede redirigirse a otra colección compilada con `collectionproxy.set_collection()`. Consulta [Cambiar la colección de un proxy excluido](/manuals/collection-proxy/#changing-an-excluded-proxys-collection) para conocer las restricciones y la secuencia de carga.

En una build basada en archivos comprimidos que publica contenido de Live Update, el manifiesto principal incluido en el bundle omite las entradas excluidas de Live Update, mientras que el manifiesto del paquete publicado las conserva. `collectionproxy.get_resources()` lee los metadatos de dependencias del manifiesto; no comprueba que todos los blobs de datos referenciados estén disponibles:

* Antes de montar un manifiesto de paquete que contenga las entradas excluidas del proxy, `collectionproxy.get_resources("#proxy")` devuelve una tabla vacía `{}`.
* Después de montar el paquete correspondiente, devuelve una tabla no vacía de hashes de recursos para ese proxy, por ejemplo:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

El siguiente código de ejemplo asume que los recursos están disponibles mediante la URL especificada en la configuración `game.http_url`.

```lua

-- Necesitas llevar registro de qué archivo comprimido contiene qué contenido
-- En este ejemplo, usamos un único archivo comprimido de Live Update, que contiene todos los recursos que faltan.
-- Si usas varios archivos comprimidos, necesitas estructurar las descargas en consecuencia
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

        -- Una build que publica contenido de Live Update omite las entradas excluidas
        -- del manifiesto incluido en el bundle, por lo que esta tabla está vacía hasta
        -- que se monta el manifiesto del paquete correspondiente. Después de montarlo,
        -- contiene los hashes de recursos del proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Comprueba si el archivo ya existe. Si existe, intenta montarlo.
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- intenta cargar el nivel de nuevo
                else
                    os.remove(download_path)             -- elimínalo e intenta
                    msg.post("#", "load_level", message) -- descargarlo de nuevo
                end
            end)
        else
            -- Realiza la solicitud. Puedes usar credenciales
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- intenta cargar el nivel de nuevo
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- el nivel está cargado, y podemos habilitarlo
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` monta un solo archivo comprimido usando un nombre, una prioridad y un archivo ZIP especificados. Luego los datos quedan disponibles de inmediato para cargarse (no es necesario reiniciar el motor). El montaje solo permanece activo durante la sesión actual. Guarda la ruta del paquete descargado y los ajustes de montaje deseados en tus propios datos persistentes y vuelve a llamar a `liveupdate.add_mount()` después de cada reinicio.
2. Necesitas almacenar el archivo comprimido en línea (por ejemplo, en S3), desde donde puedas descargarlo.
3. Dado un nombre de proxy de colección, necesitas averiguar qué archivo comprimido o archivos comprimidos descargar y cómo montarlos.
4. Al iniciar, intentamos cargar el nivel.
5. En este flujo de publicación de archivos comprimidos, usa `collectionproxy.get_resources()` para inspeccionar los metadatos del contenido excluido del proxy. Devuelve `{}` hasta que se monta el manifiesto del paquete correspondiente, y una tabla no vacía de hashes de recursos después de montarlo. Estos hashes describen dependencias; el resultado no comprueba por sí mismo que todos los blobs de datos estén disponibles.
6. Si el proxy usa contenido de Live Update y el archivo comprimido correspondiente aún no está montado, lo descargamos y montamos antes de cargar el proxy.
7. Realiza una solicitud HTTP y descarga el archivo en `download_path`.
8. Los datos se descargaron, y es momento de montarlos en el motor en ejecución.


Con el código de carga en su lugar, podemos probar la aplicación. Sin embargo, ejecutarla desde el editor no descargará nada. Esto se debe a que Live Update es una funcionalidad de bundle. Cuando se ejecuta en el entorno del editor nunca se excluyen recursos. Para asegurarnos de que todo funciona bien, necesitamos crear un bundle.
