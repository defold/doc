---
title: Trabajar con proyectos de bibliotecas en Defold
brief: La funcionalidad Libraries te permite compartir recursos entre proyectos. Este manual explica cómo funciona.
---

# Bibliotecas

La funcionalidad Libraries te permite compartir recursos entre proyectos. Es un mecanismo simple pero muy potente que puedes usar en tu flujo de trabajo de varias maneras.

Las bibliotecas son útiles para los siguientes propósitos:

* Copiar recursos de un proyecto terminado a uno nuevo. Si estás creando una secuela de un juego anterior, esta es una forma sencilla de comenzar.
* Construir una biblioteca de plantillas que puedes copiar en tus proyectos y luego personalizar o especializar.
* Construir una o más bibliotecas de objetos o scripts listos para usar a los que puedes hacer referencia directamente. Esto es muy práctico para almacenar módulos de script comunes o para construir una biblioteca compartida de recursos de gráficos, sonido y animación.

## Configurar el uso compartido de bibliotecas

Supongamos que quieres construir una biblioteca que contenga sprites y tile sources compartidos. Empieza por [configurar un nuevo proyecto](/manuals/project-setup/). Decide qué carpetas quieres compartir desde el proyecto y agrega los nombres de esas carpetas a la propiedad *`include_dirs`* en la configuración del proyecto. Si quieres listar más de una carpeta, separa los nombres con espacios:

![Directorios incluidos](images/libraries/libraries_include_dirs.png)

Antes de poder agregar esta biblioteca a otro proyecto, necesitamos una forma de localizarla.

## URL de biblioteca

Las bibliotecas se referencian mediante una URL estándar. Para un proyecto alojado en GitHub, sería la URL de una release del proyecto:

![URL de biblioteca de GitHub](images/libraries/libraries_library_url_github.png)

::: important
Se recomienda depender siempre de una release específica de un proyecto de biblioteca en lugar de la rama master. De esta forma, tú como desarrollador decides cuándo incorporar cambios de un proyecto de biblioteca, en vez de obtener siempre los cambios más recientes (y potencialmente incompatibles) de la rama master de un proyecto de biblioteca.
:::

::: important
Se recomienda revisar siempre las bibliotecas de terceros antes de usarlas. Aprende más sobre [cómo proteger tu uso de software de terceros](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Autenticación de acceso básica

Es posible agregar un nombre de usuario y una contraseña/token a la URL de la biblioteca para realizar autenticación de acceso básica al usar bibliotecas que no están disponibles públicamente:

```
https://username:password@github.com/defold/private/archive/main.zip
```

Los campos `username` y `password` se extraerán y se agregarán como un encabezado de solicitud `Authorization`. Esto funciona con cualquier servidor que admita autorización de acceso básica.

::: important
Asegúrate de no compartir ni filtrar accidentalmente tu token de acceso personal generado o tu contraseña, ya que puede tener consecuencias graves si caen en las manos equivocadas.
:::

Para evitar filtrar accidentalmente credenciales al tenerlas en texto claro en la URL de la biblioteca, también es posible usar un patrón de reemplazo de string y almacenar las credenciales como variables de ambiente:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

En el ejemplo anterior, el nombre de usuario y el token se leerán desde las variables de ambiente del sistema `PRIVATE_USERNAME` y `PRIVATE_TOKEN`.

#### Autenticación de GitHub

Para obtener datos de un repositorio privado en GitHub, necesitas [generar un token de acceso personal](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) y usarlo como contraseña.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Autenticación de GitLab

Para obtener datos de un repositorio privado en GitLab, necesitas [generar un token de acceso personal](https://docs.gitlab.com/ee/security/token_overview.html) y enviarlo como parámetro de URL.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Autenticación de acceso avanzada

Al usar la autenticación de acceso básica, el token de acceso y el nombre de usuario de una persona se compartirán en cualquier repositorio usado para el proyecto. En un equipo de más de una persona, esto puede ser un problema. Para resolverlo, se debe usar un usuario de "solo lectura" para acceder al repositorio como biblioteca. En GitHub, esto requiere una organización, un equipo y un usuario que no necesite editar el repositorio (por lo tanto, de solo lectura).

Pasos en GitHub:

* [Crear una organización](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Crear un equipo dentro de la organización](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Transferir el repositorio privado deseado a tu organización](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Dar al equipo acceso de "solo lectura" al repositorio](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Crear o seleccionar un usuario para que forme parte de este equipo](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Usar la "autenticación de acceso básica" anterior para crear un token de acceso personal para este usuario

En este punto, los detalles de autenticación del nuevo usuario se pueden confirmar y enviar al repositorio. Esto permitirá que cualquiera que trabaje con tu repositorio privado pueda obtenerlo como biblioteca sin tener permisos de edición sobre la biblioteca en sí.

::: important
El token del usuario de solo lectura es completamente accesible para cualquiera que pueda acceder a los repositorios de juego que usan la biblioteca.
:::

Esta solución se propuso en el foro de Defold y [se discutió en este hilo](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Configurar dependencias de bibliotecas

Abre el proyecto desde el que quieres acceder a la biblioteca. En la configuración del proyecto, agrega la URL de biblioteca a la propiedad *dependencies*. Puedes especificar varios proyectos dependientes si quieres. Solo agrégalos uno por uno con el botón `+` y elimínalos con el botón `-`:

![Dependencias](images/libraries/libraries_dependencies.png)

Ahora selecciona <kbd>Project ▸ Fetch Libraries</kbd> para actualizar las dependencias de bibliotecas. Esto ocurre automáticamente cada vez que abres un proyecto, así que solo tendrás que hacerlo si las dependencias cambian sin volver a abrir el proyecto. Esto ocurre si agregas o eliminas bibliotecas de dependencia, o si uno de los proyectos de biblioteca dependientes es modificado y sincronizado por alguien.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Ahora las carpetas que compartiste aparecen en el panel *Assets* y puedes usar todo lo que compartiste. Cualquier cambio sincronizado realizado en el proyecto de biblioteca estará disponible en tu proyecto.

![Configuración de biblioteca completada](images/libraries/libraries_done.png)

## Editar archivos en dependencias de bibliotecas

Los archivos de las bibliotecas no se pueden guardar. Puedes hacer cambios, y el editor podrá crear una build con esos cambios, lo cual es útil para pruebas. Sin embargo, el archivo en sí permanece sin cambios, y todas las modificaciones se descartarán cuando se cierre el archivo.

Si quieres hacer cambios en archivos de biblioteca, asegúrate de crear tu propio fork de la biblioteca y hacer los cambios allí. Otra opción es copiar y pegar toda la carpeta de la biblioteca en el directorio de tu proyecto y usar la copia local. En este caso, tu carpeta local ocultará la dependencia original, y el enlace de dependencia debe eliminarse de `game.project` (no olvides elegir <kbd>Project ▸ Fetch Libraries</kbd> después).

`builtins` también es una biblioteca proporcionada por el motor. Si quieres editar archivos allí, asegúrate de copiarlos a tu proyecto y usar esos archivos en lugar de los archivos `builtins` originales. Por ejemplo, para modificar `default.render_script`, copia tanto `/builtins/render/default.render` como `/builtins/render/default.render_script` en la carpeta de tu proyecto como `my_custom.render` y `my_custom.render_script`. Luego actualiza tu `my_custom.render` local para que haga referencia a `my_custom.render_script` en lugar del integrado, y configura tu `my_custom.render` personalizado en `game.project`, en la opción Render.

Si copias y pegas un material y quieres usarlo en todos los componentes de un tipo determinado, puede ser útil usar [plantillas por proyecto](/manuals/editor/#creating-new-project-files).

## Referencias rotas

El uso compartido de bibliotecas solo incluye archivos ubicados bajo las carpetas compartidas. Si creas algo que referencia recursos ubicados fuera de la jerarquía compartida, las rutas de referencia se romperán.

## Colisiones de nombres

Como puedes listar varias URL de proyecto en la configuración de proyecto *dependencies*, podrías encontrar una colisión de nombres. Esto ocurre si dos o más de los proyectos dependientes comparten una carpeta con el mismo nombre en la configuración de proyecto *`include_dirs`*.

Defold resuelve las colisiones de nombres ignorando simplemente todas las referencias a carpetas con el mismo nombre excepto la última, según el orden en que se especifican las URL de proyecto en la lista *dependencies*. Por ejemplo, si listas 3 URL de proyectos de biblioteca en las dependencias y todas comparten una carpeta llamada *items*, solo aparecerá una carpeta *items*: la que pertenece al proyecto que está último en la lista de URL.
