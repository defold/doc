---
title: Comunicación entre aplicaciones en Defold
brief: La comunicación entre aplicaciones permite obtener los argumentos de lanzamiento usados al iniciar tu aplicación. Este manual explica la API de Defold disponible para esta funcionalidad.
---

# Comunicación entre aplicaciones

En la mayoría de los sistemas operativos, las aplicaciones pueden iniciarse de varias maneras:

* Desde la lista de aplicaciones instaladas
* Desde un enlace específico de la aplicación
* Desde una notificación push
* Como paso final de un proceso de instalación.

Cuando la aplicación se inicia desde un enlace, una notificación o al instalarse, es posible pasar argumentos adicionales, como un install referrer durante la instalación o un deep-link al iniciarla desde un enlace específico de la aplicación o una notificación. Defold proporciona una forma unificada de obtener información sobre cómo se invocó la aplicación usando una extensión nativa.

## Instalar la extensión

Para empezar a usar la extensión de comunicación entre aplicaciones (Inter-app communication), debes agregarla como dependencia a tu archivo *game.project*. La última versión estable está disponible con la URL de dependencia:
```
https://github.com/defold/extension-iac/archive/master.zip
```

Recomendamos usar un enlace a un archivo ZIP de una [versión específica](https://github.com/defold/extension-iac/releases).

## Usar la extensión

La API es muy fácil de usar. Proporcionas a la extensión una función listener y reaccionas a los callbacks del listener.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- Esto fue una invocación
         print(payload.origin) -- origin puede ser un string vacío si no se pudo resolver
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

La documentación completa de la API está disponible en la [página de GitHub de la extensión](https://defold.github.io/extension-iac/).
