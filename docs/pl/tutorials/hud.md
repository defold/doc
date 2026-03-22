---
title: Przykład kodu HUD
brief: W tym przykładowym projekcie poznasz efekty zliczania punktów.
---
# HUD - przykładowy projekt

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

W tym przykładowym projekcie, który możesz [otworzyć z poziomu edytora](/manuals/project-setup/) albo [pobrać z GitHub](https://github.com/defold/sample-hud), pokazujemy efekty zliczania punktów. Punkty pojawiają się losowo na ekranie, symulując grę, w której gracz zdobywa punkty w różnych pozycjach.

Po pojawieniu się punkty unoszą się przez chwilę. Aby to osiągnąć, ustawiamy punkty jako przezroczyste, a następnie płynnie zwiększamy krycie ich koloru. Animujemy je również do góry. Jest to zrobione poniżej w `on_message()`.

Następnie przemieszczają się do sumy punktów na górze ekranu, gdzie są dodawane do całości.
Podczas ruchu lekko zanikają. Jest to zrobione w `float_done()`.

Gdy dotrą do wyniku u góry, ich wartości są dodawane do docelowego wyniku, do którego dąży licznik całkowitego wyniku. Jest to zrobione w `swoosh_done()`.

Podczas aktualizacji skrypt sprawdza, czy docelowy wynik został zwiększony i czy całkowity wynik trzeba podliczyć. Jeśli tak, całkowity wynik jest zwiększany mniejszym krokiem.
Następnie skala całkowitego wyniku jest animowana, aby uzyskać efekt odbicia. Jest to zrobione w `update()`.

Za każdym razem, gdy suma jest zwiększana, tworzymy pewną liczbę mniejszych gwiazdek i animujemy je od całkowitego wyniku na zewnątrz. Gwiazdki są tworzone, animowane i usuwane w `spawn_stars()`, `fade_out_star()` i `delete_star()`.

```lua
-- plik: hud.gui_script
-- jak szybko wynik narasta w ciągu sekundy
local score_inc_speed = 1000

function init(self)
    -- docelowy wynik odpowiada aktualnemu wynikowi w grze
    self.target_score = 0
    -- aktualny wynik, który rośnie w kierunku wyniku docelowego
    self.current_score = 0
    -- wynik wyświetlany w HUD-zie
    self.displayed_score = 0
    -- zachowaj odwołanie do węzła wyświetlającego wynik do późniejszego użycia
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- gwiazdka zakończyła animację, usuń ją
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- wygaszaj gwiazdkę przed usunięciem
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- pozycja węzła wyniku, używana do rozmieszczania gwiazdek
    local p = gui.get_position(self.score_node)
    -- odległość od miejsca, w którym pojawia się gwiazdka
    local start_distance = 0
    -- odległość, na której gwiazdka się zatrzymuje
    local end_distance = 240
    -- odstęp kątowy między gwiazdkami w okręgu
    local angle_step = 2 * math.pi / amount
    -- wylosuj kąt początkowy
    local angle = angle_step * math.random()
    for i=1,amount do
        -- zwiększ kąt o krok, aby równomiernie rozłożyć gwiazdki
        angle = angle + angle_step
        -- kierunek ruchu gwiazdki
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- pozycje początkowa i końcowa gwiazdki
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- utwórz węzeł gwiazdki
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- ustaw jej teksturę
        gui.set_texture(star, "star")
        -- ustaw pełną przezroczystość
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- pokaż płynnie
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- animuj pozycję
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- sprawdź, czy wynik wymaga aktualizacji
    if self.current_score < self.target_score then
        -- zwiększ wynik w tym kroku czasu, aby zbliżał się do wyniku docelowego
        self.current_score = self.current_score + score_inc_speed * dt
        -- ogranicz wynik, aby nie przekroczył wartości docelowej
        self.current_score = math.min(self.current_score, self.target_score)
        -- zaokrąglij w dół, aby wyświetlać wynik bez miejsc po przecinku
        local floored_score = math.floor(self.current_score)
        -- sprawdź, czy trzeba zaktualizować wyświetlany wynik
        if self.displayed_score ~= floored_score then
            -- zaktualizuj wyświetlany wynik
            self.displayed_score = floored_score
            -- zaktualizuj tekst węzła wyniku
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- ustaw skalę węzła wyniku na nieco większą niż zwykle
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- potem animuj skalę z powrotem do wartości początkowej
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- utwórz gwiazdki
            spawn_stars(self, 4)
        end
    end
end

-- ta funkcja zapisuje dodany wynik, aby wyświetlany wynik mógł narastać w `update()`
local function swoosh_done(self, node)
    -- pobierz wynik z węzła
    local amount = tonumber(gui.get_text(node))
    -- zwiększ wynik docelowy; sposób aktualizacji do tej wartości opisuje funkcja `update()`
    self.target_score = self.target_score + amount
    -- usuń tymczasowy wynik
    gui.delete_node(node)
end

-- ta funkcja animuje węzeł od fazy unoszenia do szybkiego przelotu w stronę łącznego wyniku
local function float_done(self, node)
    local duration = 0.2
    -- przesuń szybko w stronę wyświetlanego wyniku
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- dodatkowo częściowo wygaszaj podczas przelotu
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- zarejestruj dodany wynik; tę wiadomość może wysłać każdy, kto chce zwiększyć wynik
    if message_id == hash("add_score") then
        -- utwórz nowy tymczasowy węzeł wyniku
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- użyj dla niego małej czcionki
        gui.set_font(node, "small_score")
        -- początkowo ustaw przezroczystość
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- pokaż płynnie
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- unoś
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

W `main.script` pobieramy wejście dotyku/myszy, a następnie wysyłamy wiadomość do skryptu GUI, tworząc nowe wyniki z użyciem pozycji dotknięcia.

```lua
-- Po kliknięciu lub dotknięciu pobierz pozycję i wyślij ją wraz z liczbą punktów do skryptu GUI HUD-u.

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- użyj `action.x` i `action.y` jako współrzędnych x i y dotknięcia
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```
