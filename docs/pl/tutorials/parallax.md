---
title: Przykład kodu paralaksy
brief: W tym przykładzie nauczysz się, jak używać efektu paralaksy do symulowania głębi w świecie gry.
---
# Paralaksa - projekt przykładowy

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>

W tym przykładowym projekcie, który możesz [otworzyć w edytorze](/manuals/project-setup/) albo [pobrać z GitHub](https://github.com/defold/sample-parallax), pokazujemy, jak używać efektu paralaksy do symulowania głębi w świecie gry.
Są tu dwie warstwy chmur, z których jedna sprawia wrażenie, jakby znajdowała się dalej niż druga. Dla urozmaicenia dodano też animowany spodek.

Warstwy chmur są zbudowane z dwóch osobnych obiektów gry, z których każdy zawiera komponent *Tile Map* i *Script*.
Warstwy poruszają się z różnymi prędkościami, aby uzyskać efekt paralaksy. Odpowiadają za to funkcje `update()` w plikach *background1.script* i *background2.script* poniżej.

```lua
-- plik: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- tło jest mapą kafelków w obiekcie gry
-- przesuwamy obiekt gry, aby uzyskać efekt paralaksy

function update(self, dt)
    -- zmniejszaj pozycję x o 1 jednostkę na klatkę, aby uzyskać efekt paralaksy
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- plik: background2.script

-- tło jest mapą kafelków w obiekcie gry
-- przesuwamy obiekt gry, aby uzyskać efekt paralaksy

function update(self, dt)
    -- zmniejszaj pozycję x o 0.5 jednostki na klatkę, aby uzyskać efekt paralaksy
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

Spodek jest osobnym obiektem gry, zawierającym komponent *Sprite* i *Script*.
Porusza się w lewo ze stałą prędkością. Ruch góra-dół uzyskuje się przez animowanie składowej y wokół stałej wartości za pomocą funkcji sinus w Lua (`math.sin()`). Odpowiada za to `update()` w pliku *spaceship.script*.


```lua
-- plik: spaceship.script

function init(self)
    -- zapamiętaj początkową pozycję y,
    -- aby można było przesuwać spodek bez zmiany skryptu
    self.start_y = go.get_position().y
    -- ustaw licznik na zero; będzie używany przez ruch sinusoidalny poniżej
    self.counter = 0
end

function update(self, dt)
    -- zmniejszaj pozycję x o 2 jednostki na klatkę
    local p = go.get_position()
    p.x = p.x - 2

    -- poruszaj pozycją y wokół wartości początkowej
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- zaktualizuj pozycję
    go.set_position(p)

    -- usuń spodek, gdy znajdzie się poza ekranem
    if p.x < - 32 then
        go.delete()
    end

    -- zwiększ licznik
    self.counter = self.counter + 1
end
```
