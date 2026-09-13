---
title: Lichtkomponente in Defold
brief: Dieses Handbuch erklärt, wie du Umgebungslichter, gerichtete Lichter, Punktlichter und Spotlichter verwendest und in Shadern auf Lichtdaten zugreifst.
---

# Lichtkomponente {#light-component}

Die Lichtkomponente (light component) stellt eine Lichtquelle in einer Sammlung (collection) dar. Defold unterstützt derzeit vier Typen von Lichtressourcen:

- Umgebungslicht (ambient light) (`.ambient_light`)
- Gerichtetes Licht (directional light) (`.directional_light`)
- Punktlicht (point light) (`.point_light`)
- Spotlicht (spot light) (`.spot_light`)

Lichtressourcen werden Spielobjekten (game objects) wie andere Komponentenressourcen hinzugefügt. Du kannst Lichtkomponenten entweder direkt unter einem Spielobjekt erstellen oder eine Lichtressource im Browser *Assets* erstellen und sie anschließend einem Spielobjekt in der Ansicht *Outline* als Komponente hinzufügen.

Defold wendet Beleuchtung nicht automatisch auf jedes Material an. Die Engine erfasst die Lichter und stellt sie Shadern über den integrierten Lichtpuffer zur Verfügung. Der Shader deines Materials entscheidet, wie er die Lichtdaten verwendet.

Die folgenden Beispiele verwenden dieselbe Szene, um zu zeigen, wie sich die verschiedenen Lichttypen auf das Endergebnis auswirken:

![Szene ohne Lichter](images/light/no_light.png)

## Lichteigenschaften {#light-properties}

Alle Lichtfarben sind RGB-Werte. Lichtressourcen verwenden den Alphakanal nicht.

### Umgebungslicht {#ambient-light}

Umgebungslichter fügen der Szene konstantes Licht hinzu. Position, Drehung und Skalierung des Spielobjekts wirken sich nicht auf sie aus. Sie können beispielsweise für eine allgemeine Hintergrundbeleuchtung verwendet werden oder um Objekte unbeleuchtet erscheinen zu lassen.

Die Umgebungslichtkomponente wird im Editor durch ein Symbol mit zur Mitte gerichteten Pfeilen dargestellt. Die Farbe des Symbols entspricht seiner Eigenschaft `color`. 

![Umgebungslicht mit geringerer Intensität](images/light/ambient_light_less_intensity.png)

Eigenschaften:

`color`
: Die RGB-Farbe des Umgebungslichts.

`intensity`
: Multipliziert die Farbe des Umgebungslichts.

![Umgebungslicht mit höherer Intensität](images/light/ambient_light_full_intensity.png)

Umgebungslichter werden im Lichtpuffer des Shaders zu einer einzigen Umgebungslichtfarbe `light_info.xyz` aufsummiert. Sie belegen keine Einträge im Array `lights[]`. Mehrere Umgebungslichtkomponenten in der Szene ergeben nur eine Ausgabefarbe, die aus allen diesen Lichtern gemischt wird.

### Gerichtetes Licht {#directional-light}

Gerichtete Lichter stellen Licht dar, das aus einer Richtung kommt, etwa Sonnenlicht. Sie verwenden weder die Position noch die Skalierung des Spielobjekts. Die Lichtrichtung wird jedoch aus der Drehung des Spielobjekts im Weltkoordinatensystem abgeleitet, die auf die lokale Vorwärtsrichtung `(0, 0, -1)` angewendet wird.

Die Komponente für gerichtetes Licht wird im Editor durch ein farbiges Sonnensymbol mit einem 3D-Pfeil dargestellt, der ihre Richtung angibt.

![Gerichtetes Licht](images/light/directional_light.png)

Eigenschaften:

`color`
: Die RGB-Farbe des gerichteten Lichts.

`intensity`
: Multipliziert die Farbe des gerichteten Lichts.


Gerichtete Lichter werden oft mit Umgebungslicht kombiniert, damit Oberflächen, die vom gerichteten Licht abgewandt sind, nicht vollständig dunkel werden.

![Gerichtetes Licht und Umgebungslicht](images/light/directional_and_ambient_light.png)

### Punktlicht {#point-light}

Punktlichter strahlen von der Position des Spielobjekts im Weltkoordinatensystem nach außen. Die Position des Punktlichts ergibt sich aus der Position des Spielobjekts im Weltkoordinatensystem.

Die Punktlichtkomponente wird im Editor durch einen Punkt mit nach außen verlaufenden Strahlen dargestellt. Seine Farbe entspricht der Eigenschaft `color`, und ein Kreis stellt die Reichweite `range` dar.

![Punktlicht](images/light/point_light.png)

Eigenschaften:

`color`
: Die RGB-Farbe des Punktlichts.

`intensity`
: Multipliziert die Farbe des Punktlichts.

`range`
: Der Lichtradius in Welteinheiten.

Die wirksame Reichweite wird mit dem kleinsten Betrag der Achsenskalierungsfaktoren des Spielobjekts im Weltkoordinatensystem multipliziert.

![Reichweite des Punktlichts](images/light/point_light_range.png)

Eine Änderung der Lichtfarbe färbt den Beleuchtungsbeitrag des Punktlichts ein, während die Reichweite steuert, wie weit das Licht von der Quelle aus reicht.

![Reichweite des Punktlichts mit grüner Farbe](images/light/point_ight_range_green_color.png)

### Spotlicht {#spot-light}

Spotlichter strahlen von der Position des Spielobjekts im Weltkoordinatensystem in einem Kegel ab. Die Richtung wird aus der Drehung des Spielobjekts im Weltkoordinatensystem abgeleitet, die auf `(0, 0, -1)` angewendet wird.

Die Spotlichtkomponente wird im Editor durch ein farbiges Lampensymbol und Hilfslinien dargestellt, die den äußeren und inneren Kegel zeigen.

![Spotlicht](images/light/spot_light.png)

Eigenschaften:

`color`
: Die RGB-Farbe des Spotlichts.

`intensity`
: Multipliziert die Farbe des Spotlichts.

`range`
: Der Lichtradius in Welteinheiten.

`inner_cone_angle`
: Der innere Kegelwinkel in Grad im Editor. Pixel innerhalb dieses Kegels erhalten den vollen Beleuchtungsbeitrag des Spotlichts.

`outer_cone_angle`
: Der äußere Kegelwinkel in Grad im Editor. Das Licht nimmt zwischen dem inneren und dem äußeren Kegel ab.

Die wirksame Reichweite wird mit dem kleinsten Betrag der Achsenskalierungsfaktoren des Spielobjekts im Weltkoordinatensystem multipliziert. Kegelwinkel werden in Grad bearbeitet und in der kompilierten Lichtressource ins Bogenmaß umgerechnet.

![Bearbeitungshilfen für Spotlichter](images/light/spot_light_gizmos.png)

## Validierung {#validation}

Die Build-Pipeline validiert und normalisiert die Daten der Lichtressourcen:

- `color` muss genau drei Zahlen enthalten.
- `intensity` wird auf mindestens `0` begrenzt.
- `range` wird für Punktlichter und Spotlichter auf mindestens `0` begrenzt.
- Die Kegelwinkel von Spotlichtern werden auf `0..180` Grad begrenzt.
- `inner_cone_angle` wird so begrenzt, dass der Wert niemals `outer_cone_angle` überschreitet.

## Projektgrenze {#project-limit}

Die maximale Anzahl der Lichtkomponenten wird durch die Projekteinstellung `light.max_count` gesteuert. Der Standardwert ist `64`.

Umgebungslichter belegen keine Einträge im Shader-Array `lights[]`, sind aber weiterhin Lichtkomponenten und zählen für `light.max_count` mit. Gerichtete Lichter, Punktlichter und Spotlichter belegen Einträge in `lights[]`, solange sie aktiv sind.

Wenn die Anzahl der Lichtkomponenten `light.max_count` überschreitet, meldet die Engine einen Fehler wegen eines vollen Komponentenpuffers.

## Lichtpuffer in Shadern {#light-buffer-in-shaders}

Ein Shader kann auf aktive Lichter zugreifen, indem er einen Uniform-Block namens `LightBuffer` mit dem integrierten Layout deklariert. Die Engine erkennt diesen Block und bindet die Lichtdaten automatisch für Materialien und Compute-Programme, die ihn verwenden.

![Shader mit Lichtpuffer](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: world position, w: unused
    vec4 color;           // rgb: color, a: unused
    vec4 direction_range; // xyz: normalized world direction, w: range
    vec4 params;          // x: type, y: intensity, z: inner cone, w: outer cone
};

uniform LightBuffer
{
    // xyz: accumulated ambient color, w: active non-ambient light count
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

Der Lichttyp wird in `lights[i].params.x` gespeichert:

| Typ | Wert |
|------|-------|
| Gerichtetes Licht | `0` |
| Punktlicht | `1` |
| Spotlicht | `2` |

Der Shader darf ein kleineres Array `lights[]` als `light.max_count` deklarieren, aber kein größeres. Begrenze Schleifen über Lichter immer auf die deklarierte Arraygröße:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // Directional
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // Point
        {
            result += light_color;
        }
        else if (type == 2) // Spot
        {
            result += light_color;
        }
    }

    return result;
}
```

Das obige Beispiel zeigt das Muster für den Pufferzugriff. Ein tatsächlicher Shader für Punktlichter oder Spotlichter sollte außerdem den Vektor vom zu schattierenden Punkt zu `lights[i].position.xyz` berechnen, mithilfe von `lights[i].direction_range.w` eine entfernungsabhängige Abschwächung anwenden und für Spotlichter `lights[i].params.z` und `lights[i].params.w` als Kegelwinkel im Bogenmaß verwenden.

## Integrierte Beleuchtungshilfe {#built-in-lighting-helper}

Defold enthält unter `/builtins/materials/lighting.glsl` eine Shader-Hilfsdatei. Definiere `MAX_LIGHT_COUNT`, stelle die von der Hilfsdatei erwarteten Varyings bereit und binde sie dann aus deinem Fragment-Shader ein:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

Die Hilfsdatei definiert die Konstanten `LIGHT_DIRECTIONAL`, `LIGHT_POINT` und `LIGHT_SPOT`, stellt `ambient_light()` bereit und bietet Funktionen für die diffuse Beleuchtung nach Lambert für die Lichter im Puffer.

## Siehe auch {#see-also}

- [Shader-Handbuch](/manuals/shader)
- [Material-Handbuch](/manuals/material)
- [Rendering-Handbuch](/manuals/render)
