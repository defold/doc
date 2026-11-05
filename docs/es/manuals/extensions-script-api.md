---
title: Agregar autocompletado del editor a extensiones nativas
brief: Este manual explica cómo crear una definición de API de script para que el editor Defold pueda proporcionar autocompletado a los usuarios de una extensión.
---

# Autocompletado para extensiones nativas

El editor Defold proporciona sugerencias de autocompletado para todas las funciones de la API de Defold y genera sugerencias para los módulos Lua requeridos por tus scripts. Sin embargo, el editor no puede proporcionar automáticamente sugerencias de autocompletado para la funcionalidad expuesta por extensiones nativas. Una extensión nativa puede proporcionar una definición de API en un archivo separado para habilitar sugerencias de autocompletado también para la API de la extensión.


## Crear una definición de API de script

Un archivo de definición de API de script tiene la extensión `.script_api`. Debe estar en [formato YAML](https://yaml.org/) y ubicado junto con los archivos de la extensión. El formato esperado para una definición de API de script es:

```yml
- name: The name of the extension
  type: table
  desc: Extension description
  members:
  - name: Name of the first member
    type: Member type
    desc: Member description
    # if member type is "function"
    parameters:
    - name: Name of the first parameter
      type: Parameter type
      desc: Parameter description
    - name: Name of the second parameter
      type: Parameter type
      desc: Parameter description
    # if member type is "function"
    returns:
    - name: Name of first return value
      type: Return value type
      desc: Return value description
    examples:
    - desc: First example of member usage
    - desc: Second example of member usage

  - name: Name of the second member
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
