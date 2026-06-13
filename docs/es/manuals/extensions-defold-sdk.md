---
title: Extensiones nativas - Defold SDK
brief: Este manual describe cómo trabajar con el Defold SDK al crear extensiones nativas.
---

# El Defold SDK

El Defold SDK contiene la funcionalidad necesaria para declarar una extensión nativa, así como para interactuar con la capa nativa de bajo nivel de la plataforma en la que se ejecuta la aplicación y con la capa Lua de alto nivel en la que se crea la lógica del juego.

## Uso

Usas el Defold SDK incluyendo el archivo de encabezado `dmsdk/sdk.h`:

    #include <dmsdk/sdk.h>

Las funciones y namespaces disponibles del SDK están documentados en nuestra [referencia de la API](/ref/overview_cpp). Los archivos de encabezado del Defold SDK se incluyen como un archivo separado `defoldsdk_headers.zip` para cada [release de Defold en GitHub](https://github.com/defold/defold/releases). Puedes usar estos archivos para el autocompletado de código en el editor de tu elección.
