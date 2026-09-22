---
title: Defold-Handbuch zu Compute-Programmen
brief: Dieses Handbuch erklärt den Umgang mit Compute-Programmen, Shader-Konstanten und Samplern.
---

# Compute-Programme {#compute-programs}

::: sidenote
Die Unterstützung für Compute-Shader in Defold befindet sich derzeit in der *technischen Vorschau*.
Das bedeutet, dass einige Funktionen fehlen und sich die API in Zukunft möglicherweise ändern kann.
:::

Compute-Shader (compute shaders) sind ein leistungsfähiges Werkzeug für allgemeine Berechnungen auf der GPU. Sie ermöglichen es dir, die parallele Rechenleistung der GPU für Aufgaben wie Physiksimulationen, Bildverarbeitung und mehr zu nutzen. Ein Compute-Shader arbeitet mit Daten, die in Puffern oder Texturen gespeichert sind, und führt Operationen parallel über viele GPU-Threads aus. Diese Parallelität macht Compute-Shader so leistungsfähig bei rechenintensiven Aufgaben.

* Weitere Informationen zur Rendering-Pipeline findest du in der [Rendering-Dokumentation](/manuals/render).
* Eine ausführliche Erklärung von Shader-Programmen findest du in der [Shader-Dokumentation](/manuals/shader).

## Was kann ich mit Compute-Shadern machen? {#what-can-i-do-with-compute-shaders}

Da Compute-Shader für allgemeine Berechnungen vorgesehen sind, gibt es praktisch keine Grenzen für ihre Einsatzmöglichkeiten. Hier sind einige Beispiele für typische Anwendungen von Compute-Shadern:

Bildverarbeitung
  - Bildfilterung: Weichzeichnung, Kantenerkennung, Schärfefilter und so weiter anwenden.
  - Farbkorrektur: Den Farbraum eines Bildes anpassen.

Physik
  - Partikelsysteme: Eine große Anzahl von Partikeln für Effekte wie Rauch, Feuer und Strömungsdynamik simulieren.
  - Physik verformbarer Körper: Verformbare Objekte wie Stoff und Gelee simulieren.
  - Aussondern von Geometrie (Culling): Aussondern verdeckter Geometrie (Occlusion Culling), Aussondern von Geometrie außerhalb des Sichtvolumens (Frustum Culling)

Prozedurale Erzeugung
  - Gelände erzeugen: Detailliertes Gelände mithilfe von Rauschfunktionen erstellen.
  - Vegetation und Blattwerk: Prozedural erzeugte Pflanzen und Bäume erstellen.

Rendering-Effekte
  - Globale Beleuchtung: Realistische Beleuchtung simulieren, indem die Ausbreitung von reflektiertem Licht in einer Szene angenähert wird.
  - Voxelisierung: Ein 3D-Voxelraster aus Mesh-Daten erstellen.

## Wie funktionieren Compute-Shader? {#how-does-compute-shaders-work}

Grundsätzlich teilen Compute-Shader eine Aufgabe in viele kleinere Aufgaben auf, die gleichzeitig ausgeführt werden können. Dafür werden die Konzepte der `Arbeitsgruppen` (work groups) und `Aufrufe` (invocations) verwendet:

Arbeitsgruppen
: Der Compute-Shader arbeitet mit einem Raster aus `Arbeitsgruppen`. Jede Arbeitsgruppe enthält eine feste Anzahl von Aufrufen (oder Threads). Die Größe der Arbeitsgruppen und die Anzahl der Aufrufe werden im Shader-Code definiert.

Aufrufe
: Jeder Aufruf (oder Thread) führt das Compute-Shader-Programm aus. Aufrufe innerhalb einer Arbeitsgruppe können Daten über gemeinsam genutzten Speicher austauschen. Das ermöglicht eine effiziente Kommunikation und Synchronisierung zwischen ihnen.

Die GPU führt den Compute-Shader aus, indem sie viele Aufrufe über mehrere Arbeitsgruppen hinweg parallel startet. Dadurch stellt sie erhebliche Rechenleistung für geeignete Aufgaben bereit.

## Ein Compute-Programm erstellen {#creating-a-compute-program}

Um ein Compute-Programm zu erstellen, führe einen <kbd>Rechtsklick</kbd> auf einen Zielordner im Browser *Assets* aus und wähle <kbd>New... ▸ Compute</kbd>. (Du kannst auch <kbd>File ▸ New...</kbd> im Menü und anschließend <kbd>Compute</kbd> wählen.) Gib der neuen Compute-Datei einen Namen und klicke auf <kbd>Ok</kbd>.

![Compute-Datei](images/compute/compute_file.png)

Die neue Compute-Datei wird im *Compute Editor* geöffnet.

![Compute-Editor](images/compute/compute.png)

Die Compute-Datei enthält die folgenden Informationen:

Compute Program
: Die zu verwendende Compute-Shader-Programmdatei (*`.cp`*). Der Shader arbeitet mit „abstrakten Arbeitselementen“. Das bedeutet, dass es keine feste Definition der Datentypen für Ein- und Ausgaben gibt. Du legst beim Programmieren fest, was der Compute-Shader erzeugen soll.

Constants
: Uniforms, die an das Compute-Shader-Programm übergeben werden. Eine Liste der verfügbaren Konstanten findest du weiter unten.

Samplers
: Du kannst optional bestimmte Sampler in der Materialdatei konfigurieren. Füge einen Sampler hinzu, gib ihm den im Shader-Programm verwendeten Namen und passe die Einstellungen für Texturadressierung und Filterung nach deinen Wünschen an.


## Das Compute-Programm in Defold verwenden {#using-the-compute-program-in-defold}

Im Gegensatz zu Materialien werden Compute-Programme keinen Komponenten (components) zugewiesen und sind nicht Teil des normalen Rendering-Ablaufs. Ein Compute-Programm muss in einem Render-Skript `gestartet` werden, um Arbeit auszuführen. Vor dem Start musst du jedoch sicherstellen, dass das Render-Skript eine Referenz auf das Compute-Programm besitzt. Derzeit kann ein Render-Skript nur auf das Compute-Programm zugreifen, wenn du es der Datei mit der Erweiterung .render hinzufügst, die die Referenz auf dein Render-Skript enthält:

![Render-Datei mit Compute-Programm](images/compute/compute_render_file.png)

Um das Compute-Programm zu verwenden, muss es zunächst an den Render-Kontext gebunden werden. Das geschieht auf die gleiche Weise wie bei Materialien:

```lua
render.set_compute("my_compute")
-- Do compute work here, call render.set_compute() to unbind
render.set_compute()
```

Die Compute-Konstanten werden beim Start des Programms automatisch angewendet. Es gibt jedoch keine Möglichkeit, Eingabe- oder Ausgaberessourcen (Texturen, Puffer und so weiter) über den Editor an ein Compute-Programm zu binden. Stattdessen musst du dies über Render-Skripte tun:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Um das Programm in dem von dir festgelegten Arbeitsraum auszuführen, musst du es starten:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute also accepts an options table as the last argument
-- you can use this argument table to pass in render constants to the dispatch call
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Daten aus Compute-Programmen schreiben {#writing-data-from-compute-programs}

Derzeit lassen sich Ausgaben jeglicher Art aus einem Compute-Programm nur über `Speichertexturen` (storage textures) erzeugen. Eine Speichertextur ähnelt einer „normalen Textur“, bietet aber mehr Funktionen und Konfigurationsmöglichkeiten. Speichertexturen können, wie der Name nahelegt, als allgemeiner Puffer verwendet werden, aus dem du in einem Compute-Programm Daten lesen und in den du Daten schreiben kannst. Anschließend kannst du denselben Puffer zum Lesen an ein anderes Shader-Programm binden.

Um eine Speichertextur in Defold zu erstellen, musst du eine reguläre `.script`-Datei verwenden. Render-Skripte bieten diese Funktion nicht, da dynamische Texturen über die `resource`-API erstellt werden müssen, die nur in regulären `.script`-Dateien verfügbar ist.

```lua
-- In a .script file:
function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- get the texture handle from the resource
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notify the renderer of the backing texture, so it can be bound with render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Alles zusammenfügen {#putting-it-all-together}

### Shader-Programm {#shader-program}

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// specify the input resources
uniform vec4 color;
uniform sampler2D texture_in;

// specify the output image
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // This isn't a particularly interesting shader, but it demonstrates
    // how to read from a texture and constant buffer and write to a storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Write the output value to the storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Skriptkomponente {#script-component}
```lua
-- In a .script file

-- Here we specify the input texture that we later will bind to the
-- compute program. We can assign this texture to a model component,
-- or enable it to the render context in the render script.
go.property("texture_in", resource.texture())

function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notify the renderer of the input and output textures
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Render-Skript {#render-script}
```lua
-- respond to the message "set_backing_texture"
-- to set the backing texture for the compute program
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- We can bind textures to specific named constants
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Dispatch the compute program as many times as we have pixels.
    -- This constitutes our "working group". The shader will be invoked
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- when we are done with the compute program, we need to unbind it
    render.set_compute()
end
```

## Kompatibilität {#compatibility}

Defold unterstützt Compute-Shader derzeit mit den folgenden Grafikadaptern:

- Vulkan
- Metal (über MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

Verwende `graphics.get_adapter_info()`, um zu prüfen, ob der aktive Grafikadapter Compute-Shader unterstützt. Das Feld `features` enthält ein Array der Kontextfunktionskonstanten, die der Adapter unterstützt:

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local compute_shaders_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_COMPUTE_SHADER
)
```

Das Array enthält nur unterstützte Funktionen; es ist keine Tabelle, deren Schlüssel die Funktionskonstanten sind. Führe diese Prüfung immer vor der Verwendung von Compute-Shadern durch, wenn das Spiel mit verschiedenen Grafikadaptern oder auf Geräten mit unterschiedlicher Treiberunterstützung laufen kann. Die Unterstützung durch OpenGL und OpenGL ES hängt von der API-Version und dem Treiber ab. Vulkan und Metal über MoltenVK unterstützen Compute-Shader ab Version 1.0. Verwende ein [Anwendungsmanifest](/manuals/app-manifest), um Vulkan auf Plattformen auszuwählen, auf denen es noch nicht das standardmäßige Grafik-Backend ist.
