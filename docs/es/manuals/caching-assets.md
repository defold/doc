---
title: Caché de assets
brief: Este manual explica cómo usar la caché de assets para acelerar las builds.
---

# Caché de assets

Los juegos creados con Defold normalmente se compilan en cuestión de segundos, pero a medida que un proyecto crece también aumenta la cantidad de assets. Compilar fuentes y comprimir texturas puede llevar una cantidad significativa de tiempo en un proyecto grande, y la caché de assets existe para acelerar las builds recompilando solo los assets que han cambiado y usando assets ya compilados desde la caché para los assets que no han cambiado.

Defold usa una caché de tres niveles:

1. Caché del proyecto
2. Caché local
3. Caché remota


## Caché del proyecto

Por defecto, Defold guarda los assets compilados en caché en la carpeta `build/default` de un proyecto Defold. La caché del proyecto acelera las builds posteriores porque solo se deben recompilar los assets modificados, mientras que los assets sin cambios se usan desde la caché del proyecto. Esta caché siempre está activada y la usan tanto el editor como las herramientas de línea de comando.

La caché del proyecto se puede eliminar manualmente borrando los archivos en `build/default` o ejecutando el comando `clean` desde la [herramienta de build de línea de comando Bob](/manuals/bob).


## Caché local

La caché local es una segunda caché opcional donde los assets compilados se almacenan en una ubicación externa del sistema de archivos en la misma máquina o en una unidad de red. Gracias a su ubicación externa, el contenido de la caché sobrevive a una limpieza de la caché del proyecto. También puede ser compartida por varios desarrolladores que trabajan en el mismo proyecto. Actualmente, la caché solo está disponible al crear builds con las herramientas de línea de comando. Se activa mediante la opción `resource-cache-local`:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Se accede a los assets compilados desde la caché local según un checksum calculado que tiene en cuenta la versión del motor Defold, los nombres y el contenido de los assets de origen, así como las opciones de build del proyecto. Esto garantiza que los assets en caché sean únicos y que la caché se pueda compartir entre varias versiones de Defold.

::: sidenote
Los archivos almacenados en la caché local se conservan indefinidamente. Corresponde al desarrollador eliminar manualmente los archivos antiguos o sin usar.
:::


## Caché remota

La caché remota es una tercera caché opcional donde los assets compilados se almacenan en un servidor y se accede a ellos mediante solicitudes HTTP. Actualmente, la caché solo está disponible al crear builds con las herramientas de línea de comando. Se activa mediante la opción `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Al igual que con la caché local, se accede a todos los assets desde la caché remota según un checksum calculado. Se accede a los assets en caché mediante los métodos de solicitud HTTP GET, PUT y HEAD. Defold no proporciona el servidor de caché remota. Corresponde a cada desarrollador configurarlo. Puedes ver un ejemplo de [un servidor Python básico aquí](https://github.com/britzl/httpserver-python).
