---
title: Trabajar con archivos
brief: Este manual explica cómo guardar y cargar archivos y realizar otros tipos de operaciones con archivos.
---

# Trabajar con archivos
Hay muchas maneras diferentes de crear y/o acceder a archivos. Las rutas de archivo y las formas en que accedes a estos archivos varían según el tipo de archivo y su ubicación.

## Funciones para acceder a archivos y carpetas
Defold proporciona varias funciones diferentes para trabajar con archivos:

* Puedes usar las funciones estándar [`io.*`](https://defold.com/ref/stable/io/) para leer y escribir archivos. Estas funciones te dan un control muy detallado sobre todo el proceso de E/S.

```lua
-- abrir myfile.txt para escritura en modo binario
-- devuelve nil más un mensaje de error si falla
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- escribir en el archivo, vaciarlo al disco y luego cerrar el archivo
f:write("Foobar")
f:flush()
f:close()

-- abrir myfile.txt para lectura en modo binario
-- devuelve nil más un mensaje de error si falla
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- leer el archivo completo como string
-- devuelve nil si falla
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* Puedes usar [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) y [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) para renombrar y eliminar archivos.

* Puedes usar [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) y [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) para leer y escribir tablas Lua. Existen funciones [`sys.*`](https://defold.com/ref/stable/sys/) adicionales para ayudar con la resolución de rutas de archivo independiente de la plataforma.

```lua
-- obtener una ruta independiente de la plataforma al archivo "highscore" para la aplicación "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- guardar una tabla Lua con algunos datos
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- cargar los datos
local data = sys.load(path)
print(data.highscore) -- 100
```


## Ubicaciones de archivos y carpetas
Las ubicaciones de archivos y carpetas se pueden dividir en tres categorías:

* Archivos específicos de la aplicación creados por tu aplicación
* Archivos y carpetas empaquetados con tu aplicación
* Archivos específicos del sistema a los que accede tu aplicación

### Cómo guardar y cargar archivos específicos de la aplicación
Al guardar y cargar archivos específicos de la aplicación, como puntuaciones altas, configuración de usuario y estado del juego, se recomienda hacerlo en una ubicación proporcionada por el sistema operativo y destinada específicamente a este propósito. Puedes usar [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) para obtener la ruta absoluta específica del sistema operativo a un archivo. Una vez que tengas la ruta absoluta, puedes usar las funciones `sys.*`, `io.*` y `os.*` (consulta arriba).

[Consulta el ejemplo que muestra cómo usar `sys.save()` y `sys.load()`](/examples/file/sys_save_load/).

### Cómo acceder a archivos empaquetados con la aplicación
Puedes incluir archivos con tu aplicación usando Custom Resources y Bundle Resources.

#### Recursos personalizados (Custom Resources)
:[Custom Resources](../shared/custom-resources.md)

```lua
-- Cargar los datos del nivel en un string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decodificar el string JSON a una tabla Lua
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Recursos de bundle (Bundle Resources)
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
Por motivos de seguridad, los navegadores (y por extensión cualquier JavaScript que se ejecute en un navegador) no pueden acceder a los archivos del sistema. Las operaciones de archivo en builds HTML5 en Defold aún funcionan, pero solo en un "sistema de archivos virtual" que usa la API IndexedDB en el navegador. Esto significa que no hay forma de acceder a recursos de bundle usando funciones `io.*` u `os.*`. Sin embargo, puedes acceder a recursos de bundle usando `http.request()`.
:::


#### Comparación de Custom Resources y Bundle Resources

| Característica              | Custom Resources                               | Bundle Resources                                       |
|-----------------------------|------------------------------------------------|--------------------------------------------------------|
| Velocidad de carga          | Más rápido: archivos cargados desde un archivo binario | Más lento: archivos cargados desde el sistema de archivos |
| Cargar archivos parciales   | No: solo archivos completos                    | Sí: leer bytes arbitrarios del archivo                 |
| Modificar archivos después de crear el bundle | No: archivos almacenados dentro de un archivo binario | Sí: archivos almacenados en el sistema de archivos local |
| Soporte HTML5               | Sí                                             | Sí: pero acceso a través de http y no de E/S de archivos |


### Acceso a archivos del sistema
El acceso a los archivos del sistema puede estar restringido por el sistema operativo por motivos de seguridad. Puedes usar la extensión nativa [`extension-directories`](https://defold.com/assets/extensiondirectories/) para obtener la ruta absoluta a algunos directorios comunes del sistema (por ejemplo, documents, resource, temp). Una vez que tengas la ruta absoluta, puedes usar las funciones `io.*` y `os.*` para acceder a los archivos (consulta arriba).

::: sidenote
Por motivos de seguridad, los navegadores (y por extensión cualquier JavaScript que se ejecute en un navegador) no pueden acceder a los archivos del sistema. Las operaciones de archivo en builds HTML5 en Defold aún funcionan, pero solo en un "sistema de archivos virtual" que usa la API IndexedDB en el navegador. Esto significa que no hay forma de acceder a archivos del sistema en builds HTML5.
:::

## Extensiones
El [Asset Portal](https://defold.com/assets/) contiene varios assets para simplificar el acceso a archivos y carpetas. Algunos ejemplos:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Funciones para trabajar con directorios, permisos de archivo, etc.
* [DefSave](https://defold.com/assets/defsave/) - Un módulo que te ayuda a guardar / cargar configuración y datos del jugador entre sesiones.
