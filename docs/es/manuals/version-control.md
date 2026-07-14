---
title: Control de versiones
brief: Este manual explica cómo usar Git con proyectos Defold e inspeccionar los cambios locales en el editor.
---

# Control de versiones

Los proyectos Defold funcionan bien con [Git](https://git-scm.com), pero la sincronización se gestiona fuera del editor. Usa tu cliente Git preferido o la línea de comando para clonar, hacer fetch y pull, crear commits, hacer push, crear ramas y resolver conflictos.

## Archivos modificados

Cuando el directorio del proyecto es la raíz de un árbol de trabajo de Git con al menos un commit, Defold enumera en el panel del editor *Changed Files* los archivos no ignorados que se detectan como añadidos, modificados, eliminados o renombrados. Obtiene estas entradas comparando directamente los archivos del disco con el commit actual (`HEAD`), por lo que poner un cambio en staging no altera la lista. Resuelve los conflictos de merge en un cliente Git externo.

![archivos modificados](images/workflow/changed_files.png)

Selecciona exactamente un archivo modificado o renombrado y haz click en <kbd>Diff</kbd> para ver su diff de texto. Haz click en <kbd>Revert</kbd> para descartar los cambios seleccionados del árbol de trabajo y del índice. Los archivos con seguimiento se restauran a `HEAD`; los archivos ausentes de `HEAD` se eliminan, estén o no en staging como archivos añadidos; y los renombrados eliminan la ruta nueva y restauran la antigua. Esto no se puede deshacer en el editor, así que haz commit o crea una copia de seguridad del trabajo que puedas necesitar.

## Git

Git almacena de forma eficiente los archivos de proyecto de Defold basados en texto. Los assets binarios grandes que cambian con frecuencia, como archivos PSD o de producción de audio, pueden seguir haciendo crecer rápidamente el historial del repositorio. Considera usar Git LFS o una solución independiente de almacenamiento y copia de seguridad para los archivos de trabajo grandes.

El panel *Changed Files* solo proporciona operaciones locales de estado, diff y revert. No sabe si los commits se han enviado a un repositorio remoto y no realiza fetch, pull, commit ni push de cambios. Realiza esas operaciones en un cliente Git externo o desde la línea de comando. De forma predeterminada, Defold recarga los cambios externos y actualiza el panel cuando recupera el foco. Si *Load External Changes on App Focus* está desactivado, selecciona *File ▸ Load External Changes*.
