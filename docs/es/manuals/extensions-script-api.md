---
title: Agregar autocompletado del editor a extensiones nativas
brief: Este manual explica cómo crear una definición de API de script para que el editor Defold pueda proporcionar autocompletado a los usuarios de una extensión.
---

# Autocompletado para extensiones nativas

El editor Defold proporciona sugerencias de autocompletado para todas las funciones de la API de Defold y genera sugerencias para los módulos Lua requeridos por tus scripts. Sin embargo, el editor no puede proporcionar automáticamente sugerencias de autocompletado para la funcionalidad expuesta por extensiones nativas. Una extensión nativa puede proporcionar una definición de API en un archivo separado para habilitar sugerencias de autocompletado también para la API de la extensión.


## Crear una definición de API de script

Un archivo de definición de API de script tiene la extensión `.script_api`. Debe estar en [formato YAML](https://yaml.org/) y ubicado junto con los archivos de la extensión. El formato esperado para una definición de API de script es:

```yml
- name: Nombre de la extensión
  type: table
  desc: Descripción de la extensión
  members:
  - name: Nombre del primer miembro
    type: Tipo del miembro
    desc: Descripción del miembro
    # si el tipo del miembro es "function"
    parameters:
    - name: Nombre del primer parámetro
      type: Tipo del parámetro
      desc: Descripción del parámetro
    - name: Nombre del segundo parámetro
      type: Tipo del parámetro
      desc: Descripción del parámetro
    # si el tipo del miembro es "function"
    returns:
    - name: Nombre del primer valor de retorno
      type: Tipo del valor de retorno
      desc: Descripción del valor de retorno
    examples:
    - desc: Primer ejemplo de uso del miembro
    - desc: Segundo ejemplo de uso del miembro

  - name: Nombre del segundo miembro
    ...
```

Los tipos pueden ser cualquiera de `table, string , boolean, number, function`. Si un valor puede tener varios tipos, se escribe como `[type1, type2, type3]`.
::: sidenote
Los tipos actualmente no se muestran en el editor. Se recomienda proporcionarlos de todos modos para que estén disponibles cuando el editor tenga soporte para mostrar información de tipos.
:::

## Ejemplos

Consulta los siguientes proyectos para ver ejemplos de uso reales:

* [Extensión de Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Extensión de WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
