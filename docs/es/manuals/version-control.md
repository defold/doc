---
title: Control de versiones
brief: Este manual explica cómo trabajar con el sistema integrado de control de versiones.
---

# Control de versiones

Defold está pensado para equipos pequeños que colaboran intensamente para crear juegos. Los miembros del equipo pueden trabajar en paralelo sobre el mismo contenido con muy poca fricción. Defold tiene soporte integrado para control de versiones mediante [Git](https://git-scm.com). Git está diseñado para el trabajo colaborativo distribuido y es una herramienta extremadamente potente que permite una amplia variedad de flujos de trabajo.

## Archivos modificados

Cuando guardas cambios en tu copia de trabajo local, Defold registra todos los cambios en el panel del editor *Changed Files*, donde enumera cada archivo que se ha añadido, eliminado o modificado.

![archivos modificados](images/workflow/changed_files.png)

Selecciona un archivo en la lista y haz click en <kbd>Diff</kbd> para ver los cambios que has hecho en el archivo, o en <kbd>Revert</kbd> para deshacer todos los cambios y restaurar el archivo al estado que tenía después de la última sincronización.

## Git

Git está diseñado principalmente para manejar código fuente y archivos de texto, y almacena esos tipos de archivos de forma muy eficiente. Solo se almacenan los cambios entre cada versión, lo que significa que puedes conservar un historial amplio de cambios de todos los archivos del proyecto con un costo relativamente bajo. Sin embargo, los archivos binarios, como archivos de imagen o sonido, no se benefician del esquema de almacenamiento de Git. Cada nueva versión que registras y sincronizas ocupa aproximadamente el mismo espacio. Por lo general, esto no es un problema importante con los assets finales del proyecto (imágenes JPEG o PNG, archivos de sonido OGG, etc.), pero puede convertirse rápidamente en un problema con los archivos de trabajo del proyecto (archivos PSD, proyectos Protools, etc.). Estos tipos de archivos suelen crecer mucho, ya que normalmente trabajas con una resolución mucho más alta que la de los assets objetivo. En general, se considera mejor evitar poner archivos de trabajo grandes bajo el control de Git y usar en su lugar una solución independiente de almacenamiento y copia de seguridad para ellos.

Hay muchas maneras de usar Git en un flujo de trabajo de equipo. La que usa Defold es la siguiente. Cuando sincronizas, ocurre lo siguiente:

1. Cualquier cambio local se guarda en stash para poder restaurarlo si algo falla más adelante en el proceso de sincronización.
2. Se traen los cambios del servidor.
3. Se aplica el stash (se restauran los cambios locales); esto puede producir conflictos de merge que deben resolverse.
4. El usuario recibe la opción de hacer commit de cualquier cambio en archivos locales.
5. Si hay commits locales, el usuario puede elegir hacer push de estos al servidor. De nuevo, es posible que esto provoque conflictos que deban resolverse.

Si prefieres un flujo de trabajo diferente, puedes ejecutar Git desde la línea de comando o mediante una aplicación de terceros para hacer pulls, pushes, commits y merges, trabajar en varias ramas, etc.
