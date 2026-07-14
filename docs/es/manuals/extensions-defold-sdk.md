---
title: Extensiones nativas - Defold SDK
brief: Este manual describe cómo trabajar con el Defold SDK al crear extensiones nativas.
---

# El Defold SDK

El Defold SDK contiene la funcionalidad necesaria para declarar una extensión nativa, así como para interactuar con la capa nativa de bajo nivel de la plataforma en la que se ejecuta la aplicación y con la capa Lua de alto nivel en la que se crea la lógica del juego.

## Uso

Las extensiones C++ pueden incluir el encabezado agregado `dmsdk/sdk.h`:

```cpp
#include <dmsdk/sdk.h>
```

El encabezado agregado incluye declaraciones de C++ y no se puede incluir desde un archivo fuente C. Los archivos fuente C deben incluir los encabezados `.h` individuales compatibles con C que necesiten, por ejemplo:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Actualmente solo una parte de dmSDK tiene una interfaz C pura; no todos los subsistemas de C++ tienen un equivalente en C. Las funciones y los tipos disponibles se documentan en la [descripción general de la API C](/ref/overview_defoldc/) y la [descripción general de la API C++](/ref/overview_defoldcpp/). Los archivos de encabezado del Defold SDK se incluyen como un archivo separado `defoldsdk_headers.zip` para cada [release de Defold en GitHub](https://github.com/defold/defold/releases). Puedes usar estos archivos para el autocompletado de código en el editor de tu elección.
