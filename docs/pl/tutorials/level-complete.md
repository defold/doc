---
title: Przykładowy kod ukończenia poziomu
brief: W tym przykładowym projekcie poznasz efekty pokazujące zliczanie wyniku po ukończeniu poziomu.
---
# Ukończenie poziomu - przykładowy projekt

<iframe width="560" height="315" src="https://www.youtube.com/embed/tSdTSvku1o8" frameborder="0" allowfullscreen></iframe>

W tym przykładowym projekcie, który możesz [otworzyć w edytorze](/manuals/project-setup/) albo [pobrać z GitHub](https://github.com/defold/sample-levelcomplete), pokazujemy efekty służące do prezentowania zliczania wyniku po ukończeniu poziomu. Łączny wynik jest stopniowo zwiększany, a po osiągnięciu kolejnych progów pojawiają się trzy gwiazdki. Przykład korzysta też z funkcji szybkiego przeładowania, żeby przyspieszyć iterowanie podczas dostrajania wartości.

Scena jest uruchamiana wiadomością z gry.
Wiadomość zawiera uzyskany łączny wynik oraz poziomy, przy których powinny pojawić się trzy gwiazdki.
Gdy to się dzieje, tekst nagłówka ("Level completed!") zaczyna stopniowo się pojawiać, jednocześnie zmniejszając się do normalnego rozmiaru (100%). Dzieje się to w `on_message()` poniżej.

Po zakończeniu animacji nagłówka zaczyna się zliczanie całkowitego wyniku. Za każdym razem bieżący wynik jest zwiększany o niewielki krok. Potem sprawdzamy, czy został przekroczony któryś z poziomów gwiazdek; jeśli tak, uruchamia się animacja gwiazdki (patrz niżej). Dopóki nie osiągniemy wyniku docelowego, całkowity wynik jest animowany z efektem odbicia.
Im bliżej wyniku docelowego, tym jego skala rośnie aż do wartości maksymalnej. W podobny sposób kolor stopniowo zmienia się z białego na zielony. Dzieje się to w `inc_score()`.

Za każdym razem, gdy pojawia się gwiazdka, najpierw stopniowo się pokazuje, a potem zmniejsza do normalnego rozmiaru. To dzieje się w `animate_star()`.

Gdy animacja gwiazdki dobiegnie końca, wokół większej gwiazdki pojawiają się mniejsze gwiazdki rozmieszczone po okręgu. Dzieje się to w `spawn_small_stars()`.

Następnie są animowane tak, aby losowo wystrzeliły z gwiazdki. Ich prędkość i skala są losowane podczas rozszerzania się na zewnątrz. Potem stopniowo zanikają i ostatecznie są usuwane. Dzieje się to w `animate_small_star()` i `delete_small_star()`.

Gdy wynik osiągnie wartość docelową, odcisk high score stopniowo się pojawia i wraca na swoje miejsce. Jest to uruchamiane na końcu `inc_score()` i wykonywane w `animate_imprint()`.

Funkcja `setup()` dba o to, aby węzły miały poprawne wartości początkowe. Wywołując `setup()` z `on_reload()`, upewniamy się, że wszystko zostanie poprawnie skonfigurowane przy każdym przeładowaniu skryptu z Defold Editor.

```lua
-- plik: level_complete.gui_script

-- jak szybko wynik zwiększa się w ciągu sekundy
local score_inc_speed = 51100
-- jak długi jest odstęp między kolejnymi aktualizacjami wyniku
local dt = 0.03
-- skala wyniku na początku zliczania
local score_start_scale = 0.7
-- skala wyniku po osiągnięciu wartości docelowej
local score_end_scale = 1.0
-- jak mocno wynik "odbija" przy każdym zwiększeniu
local score_bounce_factor = 1.1
-- ile małych gwiazdek utworzyć dla każdej dużej gwiazdki
local small_star_count = 16

local function setup(self)
    -- ustaw kolor nagłówka jako przezroczysty
    local c = gui.get_color(self.heading)
    c.w = 0
    gui.set_color(self.heading, c)
    -- ustaw cień nagłówka jako przezroczysty
    c = gui.get_shadow(self.heading)
    c.w = 0
    gui.set_shadow(self.heading, c)
    -- początkowo ustaw skalę nagłówka na dwukrotną
    local s = 2
    gui.set_scale(self.heading, vmath.vector3(s, s, s))
    -- ustaw początkowy wynik (0)
    gui.set_text(self.score, "0")
    -- ustaw kolor wyniku na nieprzezroczystą biel
    gui.set_color(self.score, vmath.vector4(1, 1, 1, 1))
    -- ustaw skalę tak, aby wynik mógł rosnąć podczas zliczania
    gui.set_scale(self.score, vmath.vector4(score_start_scale, score_start_scale, 1, 0))

    -- ustaw wszystkie duże gwiazdki jako przezroczyste
    for i=1,#self.stars do
        gui.set_color(self.stars[i], vmath.vector4(1, 1, 1, 0))
    end
    -- ustaw imprint jako przezroczysty
    gui.set_color(self.imprint, vmath.vector4(1, 1, 1, 0))
    -- wynik aktualnie wyświetlany na ekranie
    self.current_score = 0
    -- docelowy wynik podczas zliczania
    self.target_score = 0
end

function init(self)
    -- pobierz węzły dla wygodniejszego dostępu
    self.heading = gui.get_node("heading")
    self.stars = {gui.get_node("star_left"), gui.get_node("star_mid"), gui.get_node("star_right")}
    self.score = gui.get_node("score")
    self.imprint = gui.get_node("imprint")
    -- kolor początkowy wyniku
    self.score_start_color = vmath.vector4(1, 1, 1, 1)
    -- zapisz końcowy kolor wyniku, do którego będziemy później animować
    self.score_end_color = gui.get_color(self.score)
    setup(self)
end

-- usuń małą gwiazdkę, gdy zakończy animację
local function delete_small_star(self, small_star)
    gui.delete_node(small_star)
end

-- animuj małą gwiazdkę zgodnie z podaną pozycją początkową i kątem
local function animate_small_star(self, pos, angle)
    -- kierunek ruchu małej gwiazdki
    local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0, 0)
    -- utwórz małą gwiazdkę
    local small_star = gui.new_box_node(pos + dir * 20, vmath.vector3(64, 64, 0))
    -- ustaw jej teksturę
    gui.set_texture(small_star, "small_star")
    -- ustaw jej kolor na pełną biel
    gui.set_color(small_star, vmath.vector4(1, 1, 1, 1))
    -- ustaw małą skalę początkową
    local start_s = 0.3
    gui.set_scale(small_star, vmath.vector3(start_s, start_s, 1))
    -- zróżnicowanie skali każdej małej gwiazdki
    local end_s_var = 1
    -- faktyczna końcowa skala tej gwiazdki
    local end_s = 0.5 + math.random() * end_s_var
    gui.animate(small_star, gui.PROP_SCALE, vmath.vector4(end_s, end_s, 1, 0), gui.EASING_NONE, 0.5)
    -- zróżnicowanie pokonanego dystansu, czyli w praktyce prędkości gwiazdki
    local dist_var = 300
    -- faktyczny dystans, jaki pokona gwiazdka
    local dist = 400 + math.random() * dist_var
    gui.animate(small_star, gui.PROP_POSITION, pos + dir * dist, gui.EASING_NONE, 0.5)
    gui.animate(small_star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_OUT, 0.3, 0.2, delete_small_star)
end

-- utwórz określoną liczbę małych gwiazdek
local function spawn_small_stars(self, star)
    -- pozycja dużej gwiazdki, wokół której pojawią się małe gwiazdki
    local p = gui.get_position(star)
    for i = 1,small_star_count do
        -- oblicz kąt dla konkretnej małej gwiazdki
        local angle = 2 * math.pi * i/small_star_count
        -- a także jej pozycję
        local pos = vmath.vector3(p.x, p.y, 0)
        -- utwórz i animuj małą gwiazdkę
        animate_small_star(self, pos, angle)
    end
end

-- rozpocznij animację pojawiania się dużej gwiazdki
local function animate_star(self, star)
    -- czas płynnego pojawiania się
    local fade_in = 0.2
    -- ustaw przezroczystość
    gui.set_color(star, vmath.vector4(1, 1, 1, 0))
    -- pokaż płynnie
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in)
    -- skala początkowa
    local scale = 5
    gui.set_scale(star, vmath.vector3(scale, scale, 1))
    -- zmniejsz z powrotem do właściwego rozmiaru
    gui.animate(star, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, 0, spawn_small_stars)
end

-- rozpocznij animację pojawiania się imprint
local function animate_imprint(self)
    -- chwilę odczekaj, zanim pojawi się imprint
    local delay = 0.8
    -- czas płynnego pojawiania się
    local fade_in = 0.2
    -- skala początkowa
    local scale = 4
    gui.set_scale(self.imprint, vmath.vector4(scale, scale, 1, 0))
    -- zmniejsz z powrotem do właściwego rozmiaru
    gui.animate(self.imprint, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, delay)
    -- jednocześnie pokazuj płynnie
    gui.animate(self.imprint, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in, delay)
end

-- zwiększ wynik o jeden krok w stronę wartości docelowej
local function inc_score(self, node)
    -- o ile wynik zwiększa się w tym kroku
    local score_inc = score_inc_speed * dt
    -- nowy wynik po zwiększeniu
    local new_score = self.current_score + score_inc
    for i = 1,#self.stars do
        -- uruchom animację dużej gwiazdki, jeśli przekroczymy próg jej pojawienia się
        if self.current_score < self.star_levels[i] and new_score >= self.star_levels[i] then
            animate_star(self, self.stars[i])
        end
    end
    -- zaktualizuj wynik, ale ogranicz go do wartości docelowej
    self.current_score = math.min(new_score, self.target_score)
    -- zaktualizuj wynik na ekranie
    gui.set_text(self.score, tostring(self.current_score))
    -- jeśli to jeszcze nie koniec, kontynuuj animację i zwiększanie
    if self.current_score < self.target_score then
        -- określ, jak blisko jesteśmy celu
        local f = self.current_score / self.target_score
        -- mieszaj kolor, aby uzyskać powolne przejście
        local c = vmath.lerp(f, self.score_start_color, self.score_end_color)
        gui.animate(self.score, gui.PROP_COLOR, c, gui.EASING_NONE, dt, 0, inc_score)
        -- nowa skala dla tego kroku
        local s = vmath.lerp(f, score_start_scale, score_end_scale)
        -- zwiększ skalę o współczynnik odbicia
        local sp = s * score_bounce_factor
        -- animuj od powiększonej skali z powrotem do właściwej
        gui.set_scale(self.score, vmath.vector4(sp, sp, 1, 0))
        gui.animate(self.score, gui.PROP_SCALE, vmath.vector4(s, s, 1, 0), gui.EASING_NONE, dt)
    else
        -- gotowe, pokaż płynnie imprint
        -- UWAGA! w prawdziwym przypadku należałoby to sprawdzić względem faktycznie zapisanego rekordu
        animate_imprint(self)
    end
end

function on_message(self, message_id, message, sender)
    -- ktoś informuje nas, że trzeba wyświetlić ekran ukończenia poziomu
    if message_id == hash("level_completed") then
        -- pobierz uzyskany wynik oraz progi punktowe dla wyświetlenia gwiazdek
        self.target_score = message.score
        self.star_levels = message.star_levels
        -- pokaż płynnie nagłówek ("Level completed!")
        local c = gui.get_color(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_COLOR, c, gui.EASING_IN, dt, 0.0, inc_score)
        c = gui.get_shadow(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_SHADOW, c, gui.EASING_IN, dt, 0.0)
        -- zmniejsz go do właściwego rozmiaru
        gui.animate(self.heading, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, 0.2, 0.0)
    end
end

-- ta funkcja jest wywoływana przy przeładowaniu skryptu
-- ustawiając scenę i symulując ukończenie poziomu, uzyskujemy bardzo szybki przebieg pracy do strojenia
function on_reload(self)
    -- dopilnuj, by uwzględnić wszelkie zmiany w konfiguracji
    setup(self)
    -- zasymuluj ukończenie poziomu
    msg.post("#gui", "level_completed", {score = 102000, star_levels = {40000, 70000, 100000}})
end
```
