#### Q: ¿Cuáles son los requisitos del sistema para el editor?
A: El editor utilizará el 75% de tu memoria disponible en el sistema. Una computadora con 4GB de RAM debe ser suficiente para proyectos menores de Defold. Para proyectos de tamaño medio o grandes es recomendado 6GB de RAM o más.


#### Q: ¿Las versiones beta de Defold se actualizan automáticamente?
A: Sí. El editor beta de Defold verifica por una actualización al inicio, tal como la versión estable de Defold.


#### Q: ¿Por qué obtengo un error diciendo "java.awt.AWTError: Assistive Technology not found" cuando lanzo el editor?
A: Este error está relacionado a problemas con Java assistive technology como el [NVDA screen reader](https://www.nvaccess.org/download/). Probablemente tienes un archivo `.accessibility.properties` en tu carpeta home. Remueve el archivo y trata de lanzar el editor de nuevo. (Nota: Si utilizas cualquier tecnología de asistencia y requieres que el archivo esté presente entonces por favor escríbenos a info@defold.se para discutir soluciones alternativas).

Se ha discutido [aquí en el foro de Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q: ¿Por qué el editor no inicia o abre mi proyecto?
A: Verifica si hay espacios en la ruta de la aplicación Defold. Por ejemplo, si pones la carpeta *Defold-macosx* que contiene la versión macOS del editor en tu carpeta de *Applications*, entonces debes estar bien. Si renombraste la carpeta a *Defold macosx* el editor puede que no inicie. En windows, poner Defold bajo *C:\\Program Files\\* puede ocasionar este problema. Esto es debido a un bug conocido en el framework de Eclipse.


#### Q: ¿Por qué estoy obteniendo un error diciendo "sun.security.validator.ValidatorException: PKIX path building failed" cuando lanzo el editor?
A: Esta excepción ocurre cuando el editor trata de hacer una conexión https pero la cadena de certificado provisto por el servidor no puede ser verificado.

Mira [este link](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md) para más detalles en este error.
