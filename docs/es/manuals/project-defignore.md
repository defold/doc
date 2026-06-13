---
title: Ignorados de proyecto Defold
brief: Este manual describe cómo ignorar archivos y carpetas en Defold.
---

# Ignorar archivos

Es posible configurar el editor Defold y las herramientas para que ignoren archivos y carpetas en un proyecto. Esto puede ser útil si el proyecto contiene archivos con extensiones que entran en conflicto con las extensiones usadas por Defold. Un ejemplo son los archivos del lenguaje Go con la extensión de archivo `.go`, que es la misma que usa el editor para los archivos de objeto de juego.

## El archivo `.defignore`
Los archivos y carpetas que se excluirán se definen en un archivo llamado `.defignore` en la raíz del proyecto. El archivo debe listar los archivos y carpetas que se excluirán, uno por línea. Ejemplo:

```
/path/to/file.png
/otherpath
```

Esto excluirá el archivo `/path/to/file.png` y todo lo que esté en la ruta `/otherpath`.

## El archivo `.defunload`

En ciertos proyectos grandes que contienen varios módulos independientes, puede que quieras excluir partes del proceso de carga para reducir el uso de memoria y los tiempos de carga en el editor. Para conseguirlo, puedes listar las rutas que se excluirán de la carga en un archivo `.defunload` bajo el directorio del proyecto.

En pocas palabras, el archivo `.defunload` te permite ocultar partes del proyecto al editor sin convertir en un error de build las referencias a los recursos ocultos.

Los patrones en `.defunload` usan las mismas reglas que el archivo `.defignore`. Las colecciones (Collections) y los objetos de juego (Game Objects) descargados se comportarán como si estuvieran vacíos cuando sean referenciados por recursos cargados. Otros recursos que coincidan con patrones de `.defunload` estarán en estado descargado y no se podrán ver en el editor. Sin embargo, si un recurso cargado depende de ellos, los recursos descargados y sus dependencias se cargan automáticamente.

Por ejemplo, si un Sprite depende de imágenes en un Atlas, tenemos que cargar el Atlas, o la imagen faltante se informará como un error. Si esto ocurre, una notificación advertirá al usuario sobre la situación y proporcionará información sobre qué recurso descargado fue referenciado y desde dónde.

El editor impedirá que el usuario agregue referencias a recursos `.defunloaded` desde recursos cargados, así que esta situación solo ocurre cuando los recursos se leen desde el disco.

A diferencia del archivo `.defignore`, necesitas reiniciar el editor después de editar el archivo `.defunload` para ver los cambios aplicados.
