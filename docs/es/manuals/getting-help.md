---
title: Cómo obtener ayuda
brief: Este manual describe cómo obtener ayuda si encuentras un problema al usar Defold.
---

# Obtener ayuda {#getting-help}

Si encuentras un problema al usar Defold, nos gustaría saberlo para que podamos corregirlo y/o ayudarte a encontrar una solución alternativa. Hay varias formas de hablar sobre problemas y también de reportarlos. Elige la opción que funcione mejor para ti:

## Reportar un problema en el foro {#report-a-problem-on-the-forum}

Una buena forma de hablar sobre un problema y obtener ayuda es publicar una pregunta en nuestro [foro](https://forum.defold.com). Publica en la categoría [Questions](https://forum.defold.com/c/questions) o [Bugs](https://forum.defold.com/c/bugs), según el tipo de problema que tengas. Recuerda [buscar](https://forum.defold.com/search) tu pregunta o problema antes de preguntar, ya que puede que ya exista una solución para tu problema.

Si tienes varias preguntas, crea varias publicaciones. No hagas preguntas no relacionadas en la misma publicación.

### Información requerida {#required-information}
No podremos ofrecer soporte a menos que proporciones la información necesaria:

**Título**
Asegúrate de usar un título corto y descriptivo. Un buen título sería "¿Cómo muevo un objeto de juego en la dirección hacia la que está rotado?" o "¿Cómo hago que un sprite desaparezca gradualmente?". Un mal título sería "¡Necesito ayuda usando Defold!" o "¡Mi juego no funciona!".

**Describe el bug (REQUERIDO)**
Una descripción clara y concisa de cuál es el bug.

**Para reproducirlo (REQUERIDO)**
Pasos para reproducir el comportamiento:
1. Ve a '...'
2. Haz click en '....'
3. Desplázate hacia abajo hasta '....'
4. Observa el error

**Comportamiento esperado (REQUERIDO)**
Una descripción clara y concisa de lo que esperabas que ocurriera.

**Versión de Defold (REQUERIDO):**
  - Versión [p. ej. 1.2.155]

**Plataformas (REQUERIDO):**
 - Plataformas: [p. ej. iOS, Android, Windows, macOS, Linux, HTML5]
 - SO: [p. ej. iOS8.1, Windows 10, High Sierra]
 - Dispositivo: [p. ej. iPhone6]

**Proyecto mínimo de reproducción (OPCIONAL):**
Adjunta un proyecto mínimo donde se reproduzca el bug. Esto ayudará mucho a la persona que intente investigar y corregir el bug.

**Logs (OPCIONAL):**
Proporciona logs relevantes del motor, el editor o el servidor de build. Aprende dónde se almacenan los logs [aquí](#log-files).

**Solución alternativa (OPCIONAL):**
Si existe una solución alternativa, descríbela aquí.

**Capturas de pantalla (OPCIONAL):**
Si corresponde, agrega capturas de pantalla para ayudar a explicar tu problema.

**Contexto adicional (OPCIONAL):**
Agrega aquí cualquier otro contexto sobre el problema.


### Compartir código {#sharing-code}
Cuando compartas código, se recomienda compartirlo como texto, no como capturas de pantalla. Compartirlo como texto facilita buscar en él, resaltar errores, sugerir modificaciones y aplicarlas. Comparte código envolviéndolo en tres \`\`\` o indentándolo con 4 espacios.

Ejemplo:

\`\`\`
print("Hello code!")
\`\`\`

Resultado:

```
print("Hello code!")
```


## Reportar un problema desde el editor {#report-a-problem-from-the-editor}

El editor ofrece una forma cómoda de reportar problemas. Selecciona la opción de menú <kbd>Help->Report Issue</kbd> desde el editor para reportar un problema.

![](images/getting_help/report_issue.png)

Al seleccionar esta opción de menú irás a un issue tracker en GitHub. Proporciona [archivos de log](#log-files), información sobre tu sistema operativo, pasos para reproducir el problema, posibles soluciones alternativas, etc.

::: sidenote
Necesitas una cuenta de GitHub para enviar un reporte de bug de esta forma.
:::


## Hablar sobre un problema en Discord {#discuss-a-problem-on-discord}

Si encuentras un problema al usar Defold, puedes intentar hacer la pregunta en [Discord](https://www.defold.com/discord/). Sin embargo, recomendamos publicar en el foro las preguntas complejas y las conversaciones en profundidad. Ten en cuenta también que no aceptamos reportes de bugs enviados por Discord.


# Archivos de log {#log-files}

El motor, el editor y el servidor de build generan información de logging que puede ser muy valiosa al pedir ayuda y depurar un problema. Proporciona siempre archivos de log al reportar un problema:

* [Logs del motor](/manuals/debugging-game-and-system-logs)
* [Logs del editor](/manuals/editor#editor-logs)
* [Logs del servidor de build](/manuals/extensions#build-server-logs)
