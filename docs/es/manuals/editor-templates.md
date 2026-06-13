---
title: Plantillas del editor
brief: Puedes agregar tus propias plantillas de proyecto personalizadas a la ventana New Project.
---

# Plantillas del editor

Puedes agregar tus propias plantillas de proyecto personalizadas a la ventana New Project:

![plantillas de proyecto personalizadas](images/editor/custom_project_templates.png)

Para agregar una o más pestañas nuevas con plantillas de proyecto personalizadas, necesitas agregar un archivo `welcome.edn` en la carpeta `.defold` dentro del directorio home de tu usuario:

* Crea una carpeta llamada `.defold` en el directorio home de tu usuario.
  * En Windows `C:\Users\**Your Username**\.defold`
  * En macOS `/Users/**Your Username**/.defold`
  * En Linux `~/.defold`
* Crea un archivo `welcome.edn` en la carpeta `.defold`

El archivo `welcome.edn` usa el formato Extensible Data Notation. Ejemplo:

```
{:new-project
  {:categories [
    {:label "My Templates"
     :templates [
          {:name "My project"
           :description "My template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-project/archive/master.zip"
           :skip-root? true},
          {:name "My other project"
           :description "My other template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-other-project/archive/master.zip"
           :skip-root? true}]
    }]
  }
}
```

Esto creará la lista de plantillas que se ve en la captura de pantalla anterior.

::: sidenote
Solo puedes usar las imágenes de plantilla [incluidas con el editor](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images).
:::
