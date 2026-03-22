---
title: Samouczek platformówki w Defold
brief: W tym artykule przejdziesz przez implementację prostej dwuwymiarowej platformówki opartej na kafelkach w Defold. Poznasz ruch w lewo i w prawo, skakanie oraz spadanie.
---

# Platformówka

W tym artykule przejdziemy przez implementację prostej dwuwymiarowej platformówki opartej na kafelkach w Defold. Poznasz ruch w lewo i w prawo, skakanie oraz spadanie.

Istnieje wiele różnych sposobów tworzenia platformówki. Rodrigo Monteiro napisał na ten temat bardzo obszerną analizę i więcej znajdziesz [tutaj](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Zdecydowanie polecamy przeczytanie jej, jeśli dopiero zaczynasz tworzyć platformówki, ponieważ zawiera wiele cennych informacji. W tym artykule omówimy nieco bardziej szczegółowo kilka opisanych metod oraz to, jak zaimplementować je w Defold. Wszystko powinno jednak być łatwe do przeniesienia na inne platformy i języki (w Defold używamy Lua).

Zakładamy, że znasz choć trochę matematykę wektorową (algebrę liniową). Jeśli nie, warto się z nią zapoznać, bo jest niesamowicie przydatna w tworzeniu gier. David Rosen z Wolfire napisał bardzo dobrą serię na ten temat [tutaj](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/).

Jeśli już używasz Defold, możesz utworzyć nowy projekt oparty na szablonie projektu _Platformer_ i poeksperymentować z nim podczas czytania tego artykułu.

::: sidenote
Niektórzy czytelnicy zwrócili uwagę, że proponowana przez nas metoda nie jest możliwa przy domyślnej implementacji Box2D. Wprowadziliśmy kilka modyfikacji do Box2D, aby to zadziałało:

Kolizje między obiektami kinematycznymi i statycznymi są ignorowane. Zmień sprawdzenia w `b2Body::ShouldCollide` i `b2ContactManager::Collide`.

Również odległość kontaktu (nazywana separation w Box2D) nie jest przekazywana do funkcji zwrotnej.
Dodaj pole distance do `b2ManifoldPoint` i upewnij się, że jest aktualizowane w funkcjach `b2Collide*`.
:::

## Wykrywanie kolizji

Wykrywanie kolizji jest potrzebne, aby gracz nie przechodził przez geometrię poziomu.
Istnieje wiele sposobów rozwiązania tego problemu, zależnie od gry i jej konkretnych wymagań.
Jednym z najprostszych rozwiązań, jeśli to możliwe, jest powierzenie tego silnikowi fizycznemu.
W Defold używamy silnika fizycznego [Box2D](http://box2d.org/) do gier 2D.
Domyślna implementacja Box2D nie ma wszystkich potrzebnych funkcji, więc na końcu tego artykułu opisujemy, jak ją zmodyfikowaliśmy.

Silnik fizyczny przechowuje stany obiektów fizycznych wraz z ich kształtami, aby symulować zachowanie fizyczne. Podczas symulacji raportuje też kolizje, dzięki czemu gra może reagować na nie w momencie ich wystąpienia. W większości silników fizycznych istnieją trzy typy obiektów: _statyczne_, _dynamiczne_ i _kinematyczne_ (nazwy te mogą się różnić w innych silnikach fizycznych). Istnieją też inne typy obiektów, ale na razie je pomińmy.

- *statyczny* obiekt nigdy się nie porusza (np. geometria poziomu).
- *dynamiczny* obiekt jest poddawany działaniu sił i momentów obrotowych, które podczas symulacji są zamieniane na prędkości.
- *kinematyczny* obiekt jest kontrolowany przez logikę aplikacji, ale nadal wpływa na inne obiekty dynamiczne.

W takiej grze chcemy uzyskać coś przypominającego fizyczne zachowanie z prawdziwego świata, ale znacznie ważniejsze są responsywne sterowanie i dobrze wyważone mechaniki. Skok, który daje dobre wrażenie, nie musi być fizycznie dokładny ani zachowywać się zgodnie z rzeczywistą grawitacją. [Ta](http://hypertextbook.com/facts/2007/mariogravity.shtml) analiza pokazuje jednak, że grawitacja w grach z Mario zbliża się do 9,8 m/s<sup>2</sup> w każdej wersji. :-)

Ważne jest, abyśmy mieli pełną kontrolę nad tym, co się dzieje, dzięki czemu możemy projektować i dostrajać mechaniki tak, aby osiągnąć zamierzony efekt. Dlatego modelujemy postać gracza jako obiekt kinematyczny. Dzięki temu możemy swobodnie poruszać postacią gracza, bez konieczności radzenia sobie z siłami fizycznymi. Oznacza to, że separację między postacią a geometrią poziomu będziemy musieli rozwiązać samodzielnie (więcej o tym później), ale jest to kompromis, który jesteśmy gotowi zaakceptować. Postać gracza będziemy reprezentować w świecie fizyki przez kształt pudełka.

## Ruch

Skoro zdecydowaliśmy, że postać gracza będzie reprezentowana przez obiekt kinematyczny, możemy swobodnie przemieszczać ją, ustawiając pozycję. Zacznijmy od ruchu w lewo i w prawo.

Ruch będzie oparty na przyspieszeniu, aby nadać postaci pewien ciężar. Podobnie jak w przypadku zwykłego pojazdu przyspieszenie określa, jak szybko postać gracza może osiągnąć maksymalną prędkość i zmienić kierunek. Przyspieszenie działa w czasie kroku klatki - zwykle przekazywanym w parametrze `dt` (delta-`t`) - a następnie jest dodawane do prędkości. Analogicznie, prędkość działa w trakcie klatki, a wynikowe przemieszczenie jest dodawane do pozycji. W matematyce nazywa się to [całkowaniem w czasie](http://en.wikipedia.org/wiki/Integral).

![Przybliżone całkowanie prędkości](images/platformer/integration.png)

Dwie pionowe linie oznaczają początek i koniec klatki. Wysokość linii to prędkość, jaką postać gracza ma w tych dwóch punktach czasu. Nazwijmy te prędkości `v0` i `v1`. `v1` otrzymujemy, stosując przyspieszenie (nachylenie krzywej) dla kroku czasowego `dt`:

![Równanie prędkości](images/platformer/equationofvelocity.png)

Pomarańczowy obszar to przemieszczenie, które powinniśmy zastosować do postaci gracza w bieżącej klatce. Geometrycznie możemy przybliżyć ten obszar jako:

![Równanie przemieszczenia](images/platformer/equationoftranslation.png)

W ten sposób całkujemy przyspieszenie i prędkość, aby poruszać postacią w pętli aktualizacji:

1. Określ docelową prędkość na podstawie wejścia.
2. Oblicz różnicę między aktualną prędkością a prędkością docelową.
3. Ustaw przyspieszenie tak, aby działało w kierunku tej różnicy.
4. Oblicz zmianę prędkości w tej klatce (`dv` to skrót od delta-velocity), jak wyżej:

    ```lua
    local dv = acceleration * dt
    ```

5. Sprawdź, czy `dv` nie przekracza zamierzonej różnicy prędkości, i w razie potrzeby ogranicz ją.
6. Zapisz bieżącą prędkość do późniejszego użycia (`self.velocity`, czyli aktualnie prędkość użyta w poprzedniej klatce):

    ```lua
    local v0 = self.velocity
    ```

7. Oblicz nową prędkość, dodając zmianę prędkości:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Oblicz przemieszczenie w osi x dla tej klatki, całkując prędkość, jak wyżej:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Zastosuj je do postaci gracza.

Jeśli nie wiesz, jak obsługiwać wejście w Defold, znajdziesz o tym poradnik [tutaj](/manuals/input).

Na tym etapie możemy poruszać postacią w lewo i w prawo, a sterowanie ma przyjemne, płynne odczucie z wyczuwalnym ciężarem. Teraz dodajmy grawitację!

Grawitacja także jest przyspieszeniem, ale działa na postać wzdłuż osi y. Oznacza to, że będzie stosowana w taki sam sposób jak opisane wyżej przyspieszenie ruchu. Jeśli po prostu zamienimy powyższe obliczenia na wektory i dopilnujemy, aby w kroku 3) uwzględnić grawitację w składowej y przyspieszenia, wszystko po prostu zadziała. Kochamy matematykę wektorową! :-)

## Reakcja na kolizje

Teraz nasza postać może się poruszać i spadać, więc czas przyjrzeć się reakcji na kolizje.
Oczywiście musimy móc lądować na geometrii poziomu i przemieszczać się po niej. Użyjemy punktów kontaktu dostarczanych przez silnik fizyczny, aby mieć pewność, że nigdy niczego nie nakładamy.

Punkt kontaktu zawiera _normalną_ kontaktu (wskazującą na zewnątrz obiektu, z którym się zderzamy, choć w innych silnikach może to wyglądać inaczej) oraz _odległość_, która mierzy, jak głęboko wniknęliśmy w drugi obiekt. To wszystko, czego potrzebujemy, aby oddzielić postać gracza od geometrii poziomu.
Ponieważ używamy pudełka, możemy w jednej klatce otrzymać wiele punktów kontaktu. Dzieje się tak na przykład wtedy, gdy dwa rogi pudełka przecinają się z poziomym podłożem albo gdy gracz porusza się w stronę narożnika.

![Normalne kontaktów działające na postać gracza](images/platformer/collision.png)

Aby nie wykonywać tej samej korekty wielokrotnie, sumujemy korekty w wektorze, żeby nie skompensować zbyt mocno. W przeciwnym razie znaleźlibyśmy się za daleko od obiektu, z którym doszło do kolizji. Na powyższym obrazku widać, że mamy obecnie dwa punkty kontaktu, pokazane przez dwie strzałki (normalne). Odległość penetracji jest taka sama dla obu kontaktów, więc gdybyśmy bezrefleksyjnie stosowali ją za każdym razem, przesunęlibyśmy postać dwa razy bardziej, niż zamierzaliśmy.

::: sidenote
Ważne jest, aby wyzerować skumulowane korekty w każdej klatce do wektora 0.
Na końcu funkcji `update()` umieść coś takiego:
`self.corrections = vmath.vector3()`
:::

Zakładając, że istnieje funkcja zwrotna wywoływana dla każdego punktu kontaktu, tak wygląda oddzielanie obiektów w tej funkcji:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Rzutuj wektor korekty na normalną kontaktu (dla pierwszego punktu kontaktu wektor korekty jest wektorem 0).
2. Oblicz kompensację, którą musimy zastosować dla tego punktu kontaktu.
3. Dodaj ją do wektora korekty.
4. Zastosuj kompensację do postaci gracza.

Musimy też wyzerować tę część prędkości gracza, która kieruje się w stronę punktu kontaktu:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Rzutuj prędkość na normalną.
2. Jeśli rzut jest ujemny, oznacza to, że część prędkości jest skierowana w stronę punktu kontaktu; w takim przypadku usuń ten składnik.

## Skakanie

Skoro możemy już biegać po geometrii poziomu i spadać, czas skakać! Skakanie w platformówkach można zrealizować na wiele różnych sposobów. W tej grze celujemy w coś podobnego do Super Mario Bros i Super Meat Boy. Podczas skoku postać gracza jest wypychana w górę impulsem, który jest w zasadzie stałą prędkością.

Grawitacja będzie nieustannie ściągać postać z powrotem w dół, tworząc przyjemną parabolę skoku. Będąc w powietrzu, gracz nadal może sterować postacią. Jeśli gracz puści przycisk skoku przed osiągnięciem szczytu paraboli, prędkość wznoszenia zostanie zmniejszona, aby przerwać skok wcześniej.

1. Gdy wejście zostanie wciśnięte, wykonaj:

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Należy to zrobić tylko wtedy, gdy wejście jest _wciśnięte_, a nie w każdej klatce, gdy pozostaje _przytrzymane_.

2. Gdy wejście zostanie zwolnione, wykonaj:

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike przygotował kilka ciekawych wykresów trajektorii skoku w [Super Mario Bros 3](http://meyermike.com/wp/?p=175) i [Super Meat Boy](http://meyermike.com/wp/?p=160), które warto zobaczyć.

## Geometria poziomu

Geometria poziomu to kształty kolizyjne otoczenia, z którymi zderza się postać gracza (i ewentualnie inne obiekty). W Defold istnieją dwa sposoby tworzenia takiej geometrii.

Możesz albo tworzyć osobne kształty kolizji na wierzchu budowanych poziomów. Ta metoda jest bardzo elastyczna i pozwala precyzyjnie pozycjonować grafikę. Jest szczególnie przydatna, jeśli chcesz mieć łagodne nachylenia.
Gra [Braid](http://braid-game.com/) używała takiego sposobu budowania poziomów i tak samo zbudowano poziom przykładowy w tym samouczku. Tak to wygląda w edytorze Defold:

![Edytor Defold z geometrią poziomu i umieszczoną w świecie postacią gracza](images/platformer/editor.png)

Inną opcją jest budowanie poziomów z kafelków i pozwolenie edytorowi na automatyczne generowanie kształtów fizycznych na podstawie grafiki kafelków. Oznacza to, że geometria poziomu będzie aktualizowana automatycznie, gdy zmieniasz poziomy, co może być niezwykle przydatne.

Ułożone kafelki zostaną automatycznie połączone w jeden kształt, jeśli ich krawędzie będą do siebie pasować.
Eliminuje to szczeliny, przez które postać gracza mogłaby się zatrzymywać lub podskakiwać podczas ślizgania się po kilku poziomych kafelkach. Osiąga się to przez zamianę wielokątów kafelków na kształty krawędzi w Box2D podczas wczytywania.

![Wiele wielokątów opartych na kafelkach połączonych w jeden](images/platformer/stitching.png)

Powyżej znajduje się przykład, w którym utworzyliśmy pięć sąsiadujących kafelków z fragmentu grafiki platformówki. Na obrazku widać, jak ułożone kafelki (u góry) odpowiadają jednemu kształtowi, który został połączony w jeden (na dole, szary kontur).

Więcej informacji znajdziesz w naszych poradnikach o [fizyce](/manuals/physics) i [kafelkach](/manuals/2dgraphics).

## Podsumowanie

Jeśli chcesz dowiedzieć się więcej o mechanice platformówek, tutaj znajdziesz imponująco dużą ilość informacji o fizyce w [Sonicu](http://info.sonicretro.org/Sonic_Physics_Guide).

Jeśli wypróbujesz nasz projekt szablonowy na urządzeniu z iOS lub przy użyciu myszy, skok może wydawać się bardzo niezręczny.
To tylko nasza nieśmiała próba zaimplementowania platformowania z użyciem wejścia jednoprzyciskowego. :-)

Nie wspomnieliśmy o tym, jak obsłużyliśmy animacje w tej grze. Możesz zobaczyć, jak to działa, sprawdzając poniższy plik *player.script* i szukając funkcji `update_animations()`.

Mamy nadzieję, że te informacje były przydatne!
Stwórzcie świetną platformówkę, żebyśmy wszyscy mogli w nią zagrać! <3

## Kod

Oto zawartość pliku *player.script*:

```lua
-- player.script

-- these are the tweaks for the mechanics, feel free to change them for a different feeling
-- the acceleration to move right/left
local move_acceleration = 3500
-- acceleration factor to use when air-borne
local air_acceleration_factor = 0.8
-- max speed right/left
local max_speed = 450
-- gravity pulling the player down in pixel units
local gravity = -1000
-- take-off speed when jumping in pixel units
local jump_takeoff_speed = 550
-- time within a double tap must occur to be considered a jump (only used for mouse/touch controls)
local touch_jump_timeout = 0.2

-- prehashing ids improves performance
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- this lets us handle input in this script
    msg.post(".", "acquire_input_focus")

    -- initial player velocity
    self.velocity = vmath.vector3(0, 0, 0)
    -- support variable to keep track of collisions and separation
    self.correction = vmath.vector3()
    -- if the player stands on ground or not
    self.ground_contact = false
    -- movement input in the range [-1,1]
    self.move_input = 0
    -- the currently playing animation
    self.anim = nil
    -- timer that controls the jump-window when using mouse/touch
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- only play animations which are not already playing
    if self.anim ~= anim then
        -- tell the sprite to play the animation
        sprite.play_flipbook("#sprite", anim)
        -- remember which animation is playing
        self.anim = anim
    end
end

local function update_animations(self)
    -- make sure the player character faces the right way
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- make sure the right animation is playing
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determine the target speed based on input
    local target_speed = self.move_input * max_speed
    -- calculate the difference between our current speed and the target speed
    local speed_diff = target_speed - self.velocity.x
    -- the complete acceleration to integrate over this frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- set the acceleration to work in the direction of the difference
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- decrease the acceleration when air-borne to give a slower feel
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calculate the velocity change this frame (dv is short for delta-velocity)
    local dv = acceleration * dt
    -- check if dv exceeds the intended speed difference, clamp it in that case
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- save the current velocity for later use
    -- (self.velocity, which right now is the velocity used the previous frame)
    local v0 = self.velocity
    -- calculate the new velocity by adding the velocity change
    self.velocity = self.velocity + dv
    -- calculate the translation this frame by integrating the velocity
    local dp = (v0 + self.velocity) * dt * 0.5
    -- apply it to the player character
    go.set_position(go.get_position() + dp)

    -- update the jump timer
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- check if we received a contact point message
    if message_id == msg_contact_point_response then
        -- check that the object is something we consider an obstacle
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    -- (extend this with a counter to do things like double-jumps)
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
        -- play animation
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- move towards the touch-point
        local diff = action.x - go.get_position().x
        -- only give input when far away (more than 10 pixels)
        if math.abs(diff) > 10 then
            -- slow down when less than 100 pixels away
            self.move_input = diff / 100
            -- clamp input to [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- start timing the last release to see if we are about to jump
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- jump on double tap
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
