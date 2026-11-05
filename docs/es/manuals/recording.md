---
title: Grabación de video en Defold
brief: Este manual explica cómo grabar la ventana del juego en MP4 mediante Lua o el servicio HTTP del motor.
---

# Grabación de video {#video-recording}

Defold puede grabar la ventana del juego como video H.264 en un archivo MP4 mediante el [módulo Lua `recorder`](/ref/recorder/) o el [servicio HTTP del motor](/manuals/engine-service/#recording-endpoints). Ambas interfaces comparten un único grabador, por lo que solo una grabación puede estar iniciándose, en curso o finalizándose a la vez.

## Disponibilidad {#availability}

La grabación se incluye en los motores **debug** de escritorio. Se omite en builds release, headless, móviles y web. Activar **Exclude Record** en un [App Manifest](/manuals/app-manifest/#exclude-record) también elimina el módulo Lua y las rutas HTTP.

| Plataforma | Requisitos de video | Audio de la aplicación |
| --- | --- | --- |
| macOS | macOS 15 o posterior, mediante ScreenCaptureKit | Compatible |
| Windows | Windows 10 versión 1903 o posterior, mediante Windows Graphics Capture y Media Foundation | Compatible a partir de Windows build 20348 |
| Linux | OpenGL, OpenGL ES o Vulkan, mediante captura del framebuffer | No compatible |

La compatibilidad con video y audio se comprueba por separado. Los clientes HTTP pueden inspeccionar `/recording/capabilities`; las llamadas Lua reciben un error si la captura solicitada no se admite. Los permisos del sistema operativo y los fallos del dispositivo de captura también pueden causar un error asíncrono después de aceptar una solicitud de inicio.

El grabador captura el contenido de la ventana del juego a su tamaño nativo en píxeles físicos. Puede recortar una fila o columna para que las dimensiones del video sean pares. Redimensionar la ventana o cambiar su densidad de píxeles detiene y finaliza la grabación. La frecuencia de captura es de 1–60 frames por segundo, con un valor predeterminado de 30.

## Grabar desde Lua {#recording-from-lua}

Usa [`recorder.start()`](/ref/recorder/#recorder.start) con una ruta de salida con permiso de escritura y un callback. El directorio padre debe existir; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) proporciona una ruta adecuada para guardar datos de la aplicación. Un archivo de salida existente puede sobrescribirse. Las grabaciones Lua pertenecen a quien las inicia y permanecen en disco después de salir del motor.

Las rutas usan la página de códigos ANSI de Windows en Windows y UTF-8 en las demás plataformas, igual que las operaciones de archivos de Lua. El `result.path` del callback conserva la ruta que se pasó a `recorder.start()`.

Este ejemplo `.script` graba durante cinco segundos a partir del inicio de la captura:

```lua
local function on_recording_event(self, event, result)
    if event == recorder.EVENT_STARTED then
        self.recording = true
        timer.delay(5, false, function(self)
            if self.recording then
                local ok, err = recorder.stop()
                if not ok then
                    print("Could not stop recording:", err)
                end
            end
        end)
    elseif event == recorder.EVENT_STOPPED then
        self.recording = false
        print("MP4 ready:", result.path)
    elseif event == recorder.EVENT_ERROR then
        self.recording = false
        print("Recording failed:", result.error)
    end
end

function init(self)
    self.recording = false
    if not recorder then
        print("Recording is not included in this engine build")
        return
    end

    local ok, err = recorder.start({
        path = sys.get_save_file("recording_example", "capture.mp4"),
        fps = 30,
        audio = false,
    }, on_recording_event)
    if not ok then
        print("Could not start recording:", err)
    end
end
```

`recorder.start()` y [`recorder.stop()`](/ref/recorder/#recorder.stop) devuelven `true` si se aceptan, o `nil, error` si se rechazan. La aceptación no significa que la captura o la finalización del archivo hayan terminado. Las opciones no válidas generan errores Lua.

Los callbacks se ejecutan durante las actualizaciones del motor:

| Evento | Significado |
| --- | --- |
| `recorder.EVENT_STARTED` | La captura está activa y ya puede detenerse. |
| `recorder.EVENT_STOPPED` | El MP4 se ha finalizado y está listo para leerse. También ocurre tras una detención automática por redimensionado. |
| `recorder.EVENT_ERROR` | La captura falló; inspecciona `result.error`. Un fallo de inicio puede generar este evento sin `EVENT_STARTED`. |

El resultado también contiene `path`, `width`, `height`, `fps` y `audio`. Lee o sube el archivo de salida únicamente después de `EVENT_STOPPED`. Mantén vivo el script que inició la captura para recibir el callback: eliminarlo descarta los callbacks sin detener la captura. Al cerrarse el motor, la captura se finaliza sin invocar callbacks Lua.

El audio está **desactivado de forma predeterminada en Lua**. Establece `audio = true` para solicitar audio de la aplicación en una plataforma compatible. Solicitar audio no compatible devuelve un error.

### Compartir el grabador con clientes HTTP {#sharing-the-recorder-with-http-clients}

`recorder.stop()` actúa sobre la grabación compartida actual, incluida una iniciada por HTTP. Devuelve un error mientras haya una operación pendiente o si no hay ninguna grabación activa. Si un cliente HTTP detiene una grabación Lua, el callback Lua original sigue recibiendo su evento de finalización. Iniciar por HTTP no crea un callback Lua; usa el estado HTTP para observar su finalización.

El estado HTTP puede describir una grabación Lua, pero su campo `file` es `null`: el servicio solo prepara descargas para grabaciones iniciadas por HTTP. Lee una grabación Lua desde `result.path` después de `EVENT_STOPPED`.

## Grabar mediante HTTP {#recording-through-http}

Las rutas de grabación usan el puerto del servicio del motor indicado en el log del juego. Descúbrelas mediante `/openapi.json`, como se describe en el [manual del servicio del motor](/manuals/engine-service/#discovering-operations-through-openapi). Un motor headless o release no las expone.

Los siguientes comandos usan una shell POSIX, `curl` y `jq`; la verificación de la descarga también usa Python 3. Ejecútalos en la misma shell y sustituye `<port>` por el puerto del motor en ejecución. Primero consulta las capacidades y conserva la identidad del servicio:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Continúa solo si `supported` es `true`; de lo contrario, inspecciona `unsupported_reason` y `minimum_platform_version`. El campo `audio` indica la compatibilidad con audio. A diferencia de Lua, **la grabación HTTP activa el audio de forma predeterminada cuando el backend lo admite**. El ejemplo siguiente lo desactiva explícitamente.

### Iniciar e inspeccionar la grabación {#start-and-inspect-the-recording}

Inicia con un objeto JSON opcional que contenga `fps` y/o `audio`. El servicio elige el archivo de salida; no acepta una ruta, ancho, alto ni escala.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 significa que la solicitud se ha aceptado. Vuelve a ejecutar el siguiente comando de estado hasta que `pending` sea `false` y `active` sea `true`. La comprobación rechaza respuestas de otra operación y notifica fallos de captura o preparación del archivo. Si una detención automática ya ha finalizado la grabación, continúa con la [finalización](#stop-and-wait-for-finalization) antes de descargarla.

```sh
STATUS=$(curl -fsS \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL/recording/status")
printf '%s\n' "$STATUS" | jq -e --argjson id "$OPERATION_ID" '
    if .operation_id != $id then error("Recording operation changed")
    elif .state == "failed" then error(.failure)
    elif .file.state == "failed" then error("Recording file preparation failed")
    else . end'
```

Deja que el juego se ejecute durante el tiempo que quieras capturar y solicita después la detención. Si la ventana cambió de tamaño y la grabación ya terminó, omite la solicitud de detención y continúa con la finalización descrita a continuación.

### Detener y esperar a la finalización {#stop-and-wait-for-finalization}

Detén la operación cuyo ID conservaste de la respuesta de inicio:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 solo acepta la solicitud de detención. Repite el comando de estado hasta que `pending` sea `false`, `finalized` sea `true` y `file.state` sea `complete`. El servicio prepara el tamaño del archivo y su SHA-256 después de terminar la captura nativa, por lo que `state: "complete"` y `finalized: true` por sí solos no significan que la descarga esté lista. Deja de esperar si `state` o `file.state` pasan a `failed`; no descargues un archivo cuyo estado sea `pending` o `failed`.

Un cliente automatizado debe consultar el estado con una pausa entre solicitudes y un tiempo límite, comprobando el ID de operación conservado en cada respuesta. Permite que el motor siga actualizándose mientras esperas a la captura y la finalización.

### Descargar y liberar el archivo {#download-and-release-the-file}

Usa la URL relativa del archivo completado que aparece en la respuesta de estado. La comprobación siguiente también garantiza que la respuesta sigue perteneciendo a tu operación:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Conserva el comprobante del estado completado en `capture.json` junto con el MP4. `/recording/status` describe la operación actual, por lo que una grabación posterior reemplaza la respuesta de estado aunque los archivos HTTP anteriores sigan disponibles.

Verifica el tamaño en bytes y el SHA-256 del archivo descargado antes de usarlo o eliminar la copia del servicio:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path("capture.json").read_text(encoding="utf-8"))
capture = Path("capture.mp4")
if capture.stat().st_size != receipt["file"]["size"]:
    raise SystemExit("Recording download size mismatch")

digest = hashlib.sha256()
with capture.open("rb") as stream:
    for chunk in iter(lambda: stream.read(65536), b""):
        digest.update(chunk)
if digest.hexdigest() != receipt["file"]["sha256"]:
    raise SystemExit("Recording download SHA-256 mismatch")
print("Verified capture.mp4")
PY
```

Un GET sin cabecera `Range` descarga el MP4 completo. El servicio también admite rangos cerrados de bytes, como `Range: bytes=0-1023`, si un cliente necesita descargas parciales. Verifica el archivo ensamblado con el mismo comprobante.

Después de descargar y verificar el archivo, puedes liberar la copia que conserva el servicio:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

Los archivos de grabación HTTP siguen disponibles hasta que se eliminan explícitamente o el motor se cierra o reinicia. Descárgalos antes de cerrar el motor. El servicio conserva como máximo 128 archivos; elimina los completados que hayas guardado para dejar espacio a nuevas grabaciones.

### Mantener juntas las identidades de las operaciones {#keeping-operation-identities-together}

Cada POST y DELETE requiere `X-Recording-Instance`. Los ejemplos también lo envían en las solicitudes de estado y descarga para rechazar respuestas de un motor que haya reemplazado al anterior. Mantén juntos `instance_id`, `operation_id` y la información del archivo: la identidad del servicio cambia al reiniciar, y un proceso nuevo puede reutilizar números de operación.

La falta de identidad devuelve HTTP 400. Una identidad obsoleta, una operación de detención obsoleta o un archivo eliminado devuelven HTTP 410. No obtengas una identidad nueva para reintentar con ella una operación antigua. Descubre el nuevo servicio e inicia una grabación nueva.

### Gestionar fallos HTTP {#handling-http-failures}

Las solicitudes rechazadas devuelven JSON con `error.code` y `error.message`. Para resolver problemas, ejecuta la solicitud `curl` individual con `-i` y sin `-f` para ver el estado HTTP y el cuerpo del error.

| Estado HTTP | Qué comprobar |
| --- | --- |
| 409 | Hay otra grabación activa o pendiente, la grabación actual aún no puede detenerse o el archivo sigue preparándose. Consulta el estado antes de reintentarlo. |
| 500 | Falló el inicio de la grabación, la inicialización del almacenamiento o la preparación/lectura del archivo. Inspecciona el mensaje de error; una captura fallida también indica `failure` en el estado. |
| 501 | El video o el audio solicitado no se admiten. Inspecciona las capacidades; usa `audio: false` si solo el audio no está disponible. |
| 507 | Se alcanzó el límite de archivos conservados por el servicio. Descarga y elimina archivos completados antes de iniciar otra grabación. |
