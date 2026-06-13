---
title: Trabajar sin conexión
brief: Este manual describe cómo trabajar sin conexión en proyectos que contienen dependencias y, en particular, extensiones nativas
---

# Trabajar sin conexión

Defold no requiere una conexión a internet para funcionar en la mayoría de los casos. Sin embargo, hay algunas situaciones en las que se necesita una conexión a internet:

* Actualizaciones automáticas
* Reportar problemas
* Obtener dependencias
* Compilar extensiones nativas


## Actualizaciones automáticas

Defold comprobará periódicamente si existen nuevas actualizaciones. Las comprobaciones de actualización de Defold se hacen en el [sitio oficial de descarga](https://d.defold.com). Si se detecta una actualización, se descargará automáticamente.

Si solo tienes conexión a internet durante periodos limitados y no quieres esperar a que se active la actualización automática, puedes descargar manualmente nuevas versiones de Defold desde el [sitio oficial de descarga](https://d.defold.com).


## Reportar problemas

Si se detecta un problema en el editor, se te ofrece la opción de reportar el problema al issue tracker de Defold. El issue tracker está [alojado en GitHub](https://www.github.com/defold/editor2-issues), lo que significa que necesitas una conexión a internet para reportar el problema.

Si encuentras un problema mientras estás sin conexión, puedes reportarlo manualmente más tarde usando la [opción Report Issue en el menú Help](/manuals/getting-help/#report-a-problem-from-the-editor) del editor.


## Obtener dependencias

Defold admite un sistema en el que los desarrolladores pueden compartir código y assets mediante algo llamado [Library Projects](/manuals/libraries/). Las bibliotecas son archivos zip que pueden alojarse en cualquier lugar en línea. Normalmente encontrarás proyectos de biblioteca de Defold en GitHub y otros repositorios de código fuente en línea.

Un proyecto puede añadir una biblioteca como [dependencia del proyecto en la configuración del proyecto](/manuals/project-settings/#dependencies). Las dependencias se descargan o actualizan cuando se abre el proyecto, o en cualquier momento en que se selecciona la opción *Fetch Libraries* desde el menú *Project*.

Si necesitas trabajar sin conexión y en varios proyectos, puedes descargar las dependencias por adelantado y luego compartirlas mediante un servidor local. Las dependencias en GitHub suelen estar disponibles desde la pestaña Releases del repositorio del proyecto:

![GitHub Library URL](images/libraries/libraries_library_url_github.png)

Puedes usar Python para crear fácilmente un servidor local:

    python -m SimpleHTTPServer

Esto creará un servidor en el directorio actual que sirve archivos en `localhost:8000`. Si el directorio actual contiene dependencias descargadas, puedes añadirlas a tu archivo *game.project*:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Compilar extensiones nativas

Defold admite un sistema en el que los desarrolladores pueden añadir código nativo para extender la funcionalidad del motor mediante un sistema llamado [Native Extensions](/manuals/extensions/). Defold proporciona un punto de entrada sin configuración a las extensiones nativas con una solución de build basada en la nube.

La primera vez que crees una build de un proyecto y el proyecto contenga una extensión nativa, el código nativo se compilará en un motor de juego Defold personalizado en los servidores de build de Defold y se enviará de vuelta a tu computadora. El motor personalizado se almacenará en caché en tu proyecto y se reutilizará en builds posteriores siempre que no añadas, elimines ni cambies ninguna extensión nativa, y siempre que no actualices el editor.

Si necesitas trabajar sin conexión y tu proyecto contiene extensiones nativas, debes asegurarte de crear una build correctamente al menos una vez para garantizar que tu proyecto contiene una copia en caché del motor personalizado.
