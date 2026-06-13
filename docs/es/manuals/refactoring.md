---
title: Refactorización
brief: Este manual explica cómo puedes cambiar fácilmente la estructura de tu proyecto con la ayuda de una refactorización potente.
---

# Refactorización

La refactorización se refiere al proceso de reestructurar código y recursos existentes. Durante el desarrollo de un proyecto, a menudo surge la necesidad de cambiar o mover elementos: los nombres necesitan cambiar para seguir convenciones de nomenclatura o mejorar la claridad, y los archivos de código o de recursos necesitan moverse a un lugar más lógico dentro de la jerarquía del proyecto.

Defold te ayuda a refactorizar de forma eficiente manteniendo un registro de cómo se usan los recursos. Actualiza automáticamente las referencias a los recursos que se renombran o se mueven. Como desarrollador, debes sentirte libre en tu trabajo. Tu proyecto es una estructura flexible que puedes cambiar a voluntad sin temer que todo se rompa y deje de funcionar.

::: important
La refactorización automática solo funcionará si los cambios se hacen desde dentro del editor. Si renombras o mueves un archivo fuera del editor, las referencias a este archivo no se cambiarán automáticamente.
:::

Sin embargo, si rompes una referencia, por ejemplo al eliminar un recurso, el editor no puede resolver el problema, pero proporcionará señales de error útiles. Por ejemplo, si eliminas una animación de un atlas y esa animación se usa en algún lugar, Defold señalará un error cuando intentes iniciar el juego. El editor también marcará dónde ocurren los errores para ayudarte a localizar rápidamente el problema:

![Refactoring error](images/workflow/delete_error.png)

Los errores de build aparecen en el panel *Build Errors* en la parte inferior del editor. Hacer <kbd>doble click</kbd> en un error te lleva a la ubicación del problema.
