---
title: Właściwości komponentu skryptu
brief: Ta instrukcja wyjaśnia, jak dodawać niestandardowe właściwości do komponentów skryptu i jak uzyskiwać do nich dostęp z edytora oraz skryptów uruchamianych podczas działania gry.
---

# Właściwości skryptów

Właściwości skryptów dostarczają prosty i potężny sposób definiowania i eksponowania niestandardowych właściwości dla określonej instancji obiektu gry. Właściwości skryptów można edytować bezpośrednio w edytorze na określonych instancjach, a ich ustawienia można używać w kodzie do zmiany zachowania obiektu gry. Istnieje wiele przypadków, w których właściwości skryptów są bardzo przydatne:

* Kiedy chcesz zastąpić wartości dla określonych instancji w edytorze, zwiększając tym samym ponowne wykorzystanie skryptu.
* Kiedy chcesz utworzyć obiekt gry z wartościami początkowymi.
* Kiedy chcesz animować wartości właściwości.
* Kiedy chcesz uzyskać dostęp do danych stanu w jednym skrypcie z innego. (Należy pamiętać, że jeśli często uzyskujesz dostęp do właściwości między obiektami, lepiej jest przenieść dane do wspólnej pamięci.)

Powszechnymi przypadkami użycia są ustawianie zdrowia lub prędkości określonego przeciwnika AI, koloru odbierania przedmiotu, atlasu sprite'a lub wiadomości, którą obiekt przycisku ma wysłać po naciśnięciu - i/lub dokąd ma ją wysłać.

## Definicja właściwości skryptu

Właściwości skryptu są dodawane do komponentu skryptu poprzez ich zdefiniowanie za pomocą specjalnej funkcji `go.property()`. Funkcję tę należy używać na najwyższym poziomie - poza jakimikolwiek funkcjami wywoływanymi, takimi jak `init()` i `update()`. Domyślna wartość podana dla właściwości decyduje o rodzaju właściwości: `number`, `boolean`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` oraz `resource` (patrz niżej).

```lua
-- can.script
-- Definiowanie właściwości skryptu dla zdrowia i celu ataku
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- przechowaj początkową pozycję celu.
  -- self.target to url odnoszący się do innego obiektu.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- zmniejsz wartość właściwości health
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```
Dowolna instancja komponentu skryptu utworzona z tego skryptu może następnie ustawiać wartości właściwości.

![Component with properties](images/script-properties/component.png)

Wybierz komponent skryptu w widoku *Outline* w Edytorze, a właściwości pojawią się w widoku *Properties*, pozwalając na ich edycję:

![Properties](images/script-properties/properties.png)

Każda właściwość, która zostanie zastąpiona nową wartością określoną dla danej instancji, jest oznaczana kolorem niebieskim. Kliknij przycisk resetowania obok nazwy właściwości, aby przywrócić wartość domyślną (ustawioną w skrypcie).

## Dostęp do właściwości skryptu

Każda zdefiniowana właściwość skryptu jest dostępna jako przechowywana zmienna w `self`, odniesieniu do instancji skryptu:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- Odczyt i zapis właściwości
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

Niestandardowe właściwości skryptu można również uzyskać poprzez funkcje pozyskiwania, ustawiania i animowania, w ten sam sposób, co dowolna inna właściwość:

```lua
-- another.script

-- zwiększenie "my_property" w "myobject#script" o 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- animowanie "my_property" w "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Obiekty utworzone przez fabryki

Jeśli używasz fabryki do tworzenia obiektu gry, możesz ustawić właściwości skryptu podczas tworzenia:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Dostęp do właściwości skryptu utworzonych przez fabrykę
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Podczas tworzenia hierarchii obiektów gry przez `collectionfactory.create()` musisz zestawić identyfikatory obiektów z tabelami właściwości. Są one zbierane w jednej tabeli i przekazywane do funkcji `create()`:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

Wartości właściwości dostarczane za pomocą `factory.create()` i `collectionfactory.create()` zastępują wartość ustawioną w pliku prototypu, a także wartości domyślne w skrypcie.

Jeśli kilka komponentów skryptu przyczepionych do obiektu gry definiuje tę samą właściwość, każdy komponent zostanie zainicjowany wartością dostarczoną za pomocą `factory.create()` lub `collectionfactory.create()`.

## Właściwości zasobów

Właściwości zasobów definiuje się dokładnie tak samo jak właściwości skryptu dla podstawowych typów danych:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Gdy właściwość zasobu jest zdefiniowana, pojawia się w widoku *Properties* tak samo jak każda inna właściwość skryptu, ale jako pole przeglądarki plików/zasobów:

![Resource Properties](images/script-properties/resource-properties.png)

Dostęp i użycie właściwości zasobu odbywa się za pomocą funkcji `go.get()` lub poprzez odniesienie do instancji skryptu `self` i używając `go.set()`:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
