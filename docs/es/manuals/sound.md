---
title: Sonido en Defold
brief: Este manual explica cómo incorporar sonidos en tu proyecto Defold, reproducirlos y controlarlos.
---

# Sonido

La implementación de sonido de Defold es simple pero potente. Solo hay dos conceptos que debes conocer:

Componentes de sonido
: Estos componentes contienen el sonido real que se debe reproducir y pueden reproducirlo.

Grupos de sonido
: Cada componente Sound puede designarse para pertenecer a un _grupo_. Los grupos ofrecen una forma sencilla de gestionar sonidos relacionados entre sí de manera intuitiva. Por ejemplo, se puede configurar un grupo "sound_fx" y cualquier sonido que pertenezca a ese grupo se puede atenuar con una simple llamada a una función.

## Crear un componente Sound

Los componentes Sound solo se pueden instanciar en el lugar dentro de un objeto de juego. Crea un nuevo objeto de juego, haz click derecho sobre él, selecciona <kbd>Add Component ▸ Sound</kbd> y presiona *OK*.

![Seleccionar componente](images/sound/sound_add_component.jpg)

El componente creado tiene un conjunto de propiedades que se deben definir:

![Seleccionar componente](images/sound/sound_properties.png)

*Sound*
: Se debe definir con un archivo de sonido de tu proyecto. El archivo debe estar en formato _Wave_, _Ogg Vorbis_ o _Ogg Opus_. Defold admite archivos Wave PCM de 8 y 16 bits. La reproducción de Ogg Opus es opcional y requiere activar **Include Sound Decoder: Opus** en el [manifiesto de la aplicación](/manuals/app-manifest/#sound); el decodificador Opus no se incluye de forma predeterminada.

*Looping*
: Si está marcada, el sonido se reproducirá _Loopcount_ veces o hasta que se detenga explícitamente.

*Loopcount*
: El número de veces que un sonido en loop se reproducirá antes de detenerse (0 significa que el sonido debe repetirse hasta que se detenga explícitamente).

*Group*
: El nombre del grupo de sonido al que debe pertenecer el sonido. Si esta propiedad se deja vacía, el sonido se asignará al grupo integrado "master".

*Gain*
: Puedes definir la ganancia del sonido directamente en el componente. Esto permite ajustar fácilmente la ganancia de un sonido sin volver a tu programa de sonido y reexportarlo. Consulta más abajo los detalles sobre cómo se calcula la ganancia.

*Pan*
: Puedes definir el valor de pan del sonido directamente en el componente. El pan debe ser un valor entre -1 (-45 grados a la izquierda) y 1 (45 grados a la derecha).

*Speed*
: Puedes definir el valor de velocidad del sonido directamente en el componente. Un valor de 1.0 es la velocidad normal, 0.5 es media velocidad y 2.0 es el doble de velocidad.


## Reproducir el sonido

Cuando tienes un componente Sound configurado correctamente, puedes hacer que reproduzca su sonido llamando a [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]):

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Un sonido seguirá reproduciéndose incluso si se elimina el objeto de juego al que pertenecía el componente Sound. Puedes llamar a [`sound.stop()`](/ref/sound/#sound.stop:url) para detener el sonido (ver más abajo).
:::
Cada mensaje enviado a un componente hará que reproduzca otra instancia del sonido, hasta que el buffer de sonido disponible esté lleno y el motor imprima errores en la consola. Se recomienda implementar algún tipo de mecanismo de compuerta y agrupación de sonidos.

## Detener el sonido

Si quieres detener la reproducción de un sonido, puedes llamar a [`sound.stop()`](/ref/sound/#sound.stop:url):

```lua
sound.stop("go#sound")
```

## Ganancia

![Ganancia](images/sound/sound_gain.png)

El sistema de sonido tiene 4 niveles de ganancia:

- La ganancia definida en el componente Sound.
- La ganancia definida al iniciar el sonido mediante una llamada a `sound.play()` o al cambiar la ganancia de la voz mediante una llamada a `sound.set_gain()`.
- La ganancia definida en el grupo mediante una llamada a la función [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain).
- La ganancia definida en el grupo "master". Esto se puede modificar con `sound.set_group_gain(hash("master"), gain)`.

Cuando **Use Linear Gain** está activado en las [opciones de proyecto de Sound](/manuals/project-settings/#sound) (el valor predeterminado), la ganancia de salida es el resultado de multiplicar estas cuatro ganancias. Una ganancia de `1.0` es la ganancia unitaria (0 dB). Cuando la ganancia lineal está desactivada, Defold aplica una curva no lineal durante la mezcla, por lo que la multiplicación directa de los cuatro valores y la conversión a decibelios que se muestra a continuación no describen el nivel de salida resultante.

## Grupos de sonido

Cualquier componente Sound con un nombre de grupo de sonido especificado se colocará en un grupo de sonido con ese nombre. Si no especificas un grupo, el sonido se asignará al grupo "master". También puedes definir explícitamente el grupo de un componente Sound como "master", lo que tiene el mismo efecto.

Hay algunas funciones disponibles para obtener todos los grupos disponibles, obtener el nombre como string, obtener y definir la ganancia, RMS (ver http://en.wikipedia.org/wiki/Root_mean_square) y la ganancia pico. También hay una función que permite comprobar si el reproductor de música del dispositivo objetivo está en ejecución:

```lua
-- Si se reproduce sonido en este dispositivo iPhone/Android, silencia todo
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

Los grupos se identifican con un valor hash. El nombre como string se puede recuperar con [`sound.get_group_name()`](/ref/sound#sound.get_group_name), que se puede usar para mostrar nombres de grupos en herramientas de desarrollo, por ejemplo un mezclador para probar los niveles de los grupos.

![Mezclador de grupos de sonido](images/sound/sound_mixer.png)

::: important
No debes escribir código que dependa del valor string de un grupo de sonido, ya que no están disponibles en builds release.
:::

Con **Use Linear Gain** activado, convierte un valor de ganancia positivo a decibelios con la fórmula estándar:

```math
db = 20 \times \log \left( gain \right)
```

```lua
for i, group_hash in ipairs(sound.get_groups()) do
    -- El string del nombre solo está disponible en debug. Devuelve "unknown_*" en release.
    local name = sound.get_group_name(group_hash)
    local gain = sound.get_group_gain(group_hash)

    -- Convierte a decibelios.
    local db = 20 * math.log10(gain)

    -- Obtiene RMS (ganancia Root Mean Square). Canales izquierdo y derecho por separado.
    local left_rms, right_rms = sound.get_rms(group_hash, 2048 / 65536.0)
    left_rmsdb = 20 * math.log10(left_rms)
    right_rmsdb = 20 * math.log10(right_rms)

    -- Obtiene la ganancia pico. Izquierda y derecha por separado.
    left_peak, right_peak = sound.get_peak(group_hash, 2048 * 10 / 65536.0)
    left_peakdb = 20 * math.log10(left_peak)
    right_peakdb = 20 * math.log10(right_peak)
end

-- Define la ganancia master en +6 dB (math.pow(10, 6/20)).
sound.set_group_gain("master", 1.995)
```

Defold 1.10.2 corrigió una atenuación de aproximadamente 3 dB que llevaba mucho tiempo presente en el mezclador de sonido. Si la mezcla de un proyecto antiguo compensaba esa atenuación y suena más fuerte después de actualizar, reajusta la opción global **Sound ▸ Gain** o las ganancias de los grupos afectados.

## Compuerta de sonidos

Si tu juego reproduce el mismo sonido en un evento y ese evento se dispara con frecuencia, corres el riesgo de reproducir el mismo sonido dos veces o más casi al mismo tiempo. Si eso ocurre, los sonidos quedarán _desfasados_, lo que puede provocar artefactos muy notorios.

![Desfase](images/sound/sound_phase_shift.png)

La forma más sencilla de manejar este problema es crear una compuerta que filtre los mensajes de sonido y no permita que el mismo sonido se reproduzca más de una vez dentro de un intervalo definido:

```lua
-- No permitas que el mismo sonido se reproduzca dentro del intervalo "gate_time".
local gate_time = 0.3

function init(self)
    -- Almacena los temporizadores de sonidos reproducidos en una tabla y descuéntalos cada frame
    -- hasta que hayan estado en la tabla durante "gate_time" segundos. Luego elimínalos.
    self.sounds = {}
end

function update(self, dt)
    -- Descuenta los temporizadores almacenados
    for k,_ in pairs(self.sounds) do
        self.sounds[k] = self.sounds[k] - dt
        if self.sounds[k] < 0 then
            self.sounds[k] = nil
        end
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("play_gated_sound") then
        -- Solo reproduce sonidos que no estén actualmente en la tabla de compuerta.
        if self.sounds[message.soundcomponent] == nil then
            -- Almacena el temporizador de sonido en la tabla
            self.sounds[message.soundcomponent] = gate_time
            -- Reproduce el sonido
            sound.play(message.soundcomponent, { gain = message.gain })
        else
            -- Se filtró un intento de reproducir un sonido
            print("gated " .. message.soundcomponent)
        end
    end
end
```

Para usar la compuerta, simplemente envíale un mensaje `play_gated_sound` y especifica el componente Sound objetivo y la ganancia del sonido. La compuerta llamará a `sound.play()` con el componente Sound objetivo si la compuerta está abierta:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
No funciona hacer que la compuerta escuche mensajes `play_sound`, ya que ese nombre está reservado por el motor Defold. Obtendrás un comportamiento inesperado si usas nombres de mensajes reservados.
:::


## Manipulación en tiempo de ejecución
Puedes manipular sonidos en tiempo de ejecución mediante varias propiedades diferentes (consulta la [documentación de la API para el uso](/ref/sound/)). Las siguientes propiedades se pueden manipular con `go.get()` y `go.set()`:

`gain`
: La ganancia del componente Sound (`number`).

`pan`
: El pan del componente Sound (`number`). El pan debe ser un valor entre -1 (-45 grados a la izquierda) y 1 (45 grados a la derecha).

`speed`
: La velocidad del componente Sound (`number`). Un valor de 1.0 es la velocidad normal, 0.5 es media velocidad y 2.0 es el doble de velocidad.

`sound`
: La ruta de recurso al sonido (`hash`). Puedes usar la ruta de recurso para cambiar el sonido con `resource.set_sound(path, buffer)`. Ejemplo:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Configuración del proyecto

El archivo *game.project* tiene algunas [opciones del proyecto](/manuals/project-settings#sound) relacionadas con los componentes Sound.

## Streaming de sonido

También es posible admitir [sonidos en streaming](/manuals/sound-streaming)
