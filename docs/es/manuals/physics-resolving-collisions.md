---
title: Resolver colisiones cinemáticas en Defold
brief: Este manual explica cómo resolver colisiones de físicas cinemáticas.
---

# Resolver colisiones cinemáticas

Usar objetos de colisión cinemáticos requiere que resuelvas las colisiones tú mismo y muevas los objetos como reacción. Una implementación ingenua para separar dos objetos que colisionan se ve así:

```lua
function on_message(self, message_id, message, sender)
  -- Manejar la colisión
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Este código separará tu objeto cinemático de otro objeto físico en el que haya penetrado, pero la separación suele excederse y en muchos casos verás vibración. Para entender mejor el problema, considera el siguiente caso en el que un personaje jugador ha colisionado con dos objetos, *A* y *B*:

![Colisión de físicas](images/physics/collision_multi.png)

El motor de físicas enviará varios mensajes `"contact_point_response"`, uno para el objeto *A* y otro para el objeto *B*, en el frame en que ocurre la colisión. Si mueves el personaje en respuesta a cada penetración, como en el código ingenuo anterior, la separación resultante sería:

- Mover el personaje fuera del objeto *A* según su distancia de penetración (la flecha negra)
- Mover el personaje fuera del objeto *B* según su distancia de penetración (la flecha negra)

El orden de estas operaciones es arbitrario, pero el resultado es el mismo en cualquier caso: una separación total que es la *suma de los vectores de penetración individuales*:

![Separación de físicas ingenua](images/physics/separation_naive.png)

Para separar correctamente el personaje de los objetos *A* y *B*, necesitas manejar la distancia de penetración de cada punto de contacto y comprobar si alguna separación previa ya resolvió la separación, total o parcialmente.

Supón que el primer mensaje de punto de contacto viene del objeto *A* y que mueves el personaje hacia fuera con el vector de penetración de *A*:

![Separación de físicas paso 1](images/physics/separation_step1.png)

Entonces el personaje ya se ha separado parcialmente de *B*. La compensación final necesaria para realizar la separación completa del objeto *B* se indica con la flecha negra de arriba. La longitud del vector de compensación se puede calcular proyectando el vector de penetración de *A* sobre el vector de penetración de *B*:

![Proyección](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

El vector de compensación se puede encontrar reduciendo la longitud de *B* en *l*. Para calcular esto para un número arbitrario de penetraciones, puedes acumular la corrección necesaria en un vector, para cada punto de contacto, comenzando con un vector de corrección de longitud cero:

1. Proyecta la corrección actual contra el vector de penetración del contacto.
2. Calcula qué compensación queda del vector de penetración (según la fórmula anterior).
3. Mueve el objeto por el vector de compensación.
4. Agrega la compensación a la corrección acumulada.

Una implementación completa se ve así:

```lua
function init(self)
  -- vector de corrección
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reiniciar la corrección
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Manejar la colisión
  if message_id == hash("contact_point_response") then
    -- Obtener la información necesaria para salir de la colisión. Podríamos
    -- recibir varios puntos de contacto y tener que calcular
    -- cómo salir de todos ellos acumulando un
    -- vector de corrección para este frame:
    if message.distance > 0 then
      -- Primero, proyecta la corrección acumulada sobre
      -- el vector de penetración
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Solo considera proyecciones que no se pasen.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Aplicar compensación
        go.set_position(go.get_position() + comp)
        -- Acumular la corrección realizada
        self.correction = self.correction + comp
      end
    end
  end
end
```
