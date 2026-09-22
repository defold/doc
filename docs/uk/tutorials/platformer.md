---
title: Урок зі створення платформера в Defold
brief: У цій статті ви розглянете реалізацію простого двовимірного платформера на основі плиток у Defold. Ви опануєте такі механіки, як рух ліворуч і праворуч, стрибки та падіння.
---

# Платформер {#platformer}

У цій статті ми розглянемо реалізацію простого двовимірного платформера на основі плиток у Defold. Ми опануємо такі механіки, як рух ліворуч і праворуч, стрибки та падіння.

Створити платформер можна багатьма різними способами. Rodrigo Monteiro написав вичерпний огляд цієї теми й не тільки — його можна прочитати [тут](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Наполегливо радимо прочитати його, якщо ви лише починаєте створювати платформери: він містить чимало цінної інформації. Ми докладніше розглянемо кілька описаних методів і те, як реалізувати їх у Defold. Утім, усе це має бути нескладно перенести на інші платформи й мови (у Defold ми використовуємо Lua).

Ми припускаємо, що ви трохи знайомі з векторною математикою (лінійною алгеброю). Якщо ні, варто з нею ознайомитися, адже вона надзвичайно корисна для розробки ігор. David Rosen із Wolfire написав дуже хорошу серію статей на цю тему — її можна знайти [тут](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/).

Якщо ви вже користуєтеся Defold, можете створити новий проєкт на основі шаблону _Platformer_ і поекспериментувати з ним під час читання цієї статті.

::: sidenote
Деякі читачі зауважили, що запропонований нами метод неможливо застосувати зі стандартною реалізацією Box2D. Щоб він запрацював, ми внесли кілька змін до Box2D:

Колізії між кінематичними й статичними об’єктами ігноруються. Змініть перевірки в `b2Body::ShouldCollide` і `b2ContactManager::Collide`.

Крім того, відстань контакту (у Box2D вона називається separation) не передається до функції зворотного виклику.
Додайте поле відстані до `b2ManifoldPoint` і переконайтеся, що воно оновлюється у функціях `b2Collide*`.
:::

## Виявлення колізій {#collision-detection}

Виявлення колізій потрібне, щоб персонаж гравця не проходив крізь геометрію рівня.
Залежно від вашої гри та її вимог це можна реалізувати кількома способами.
Один із найпростіших, якщо це можливо, — доручити це фізичному рушію.
У Defold для двовимірних ігор ми використовуємо фізичний рушій [Box2D](http://box2d.org/).
Стандартна реалізація Box2D не має всіх потрібних можливостей; про внесені нами зміни читайте внизу цієї статті.

Фізичний рушій зберігає стани фізичних об’єктів разом із їхніми формами, щоб моделювати фізичну поведінку. Під час моделювання він також повідомляє про колізії, тож гра може реагувати на них у міру виникнення. У більшості фізичних рушіїв є три типи об’єктів: _статичні_, _динамічні_ й _кінематичні_ (в інших фізичних рушіях назви можуть відрізнятися). Є й інші типи об’єктів, але поки що ми їх не розглядатимемо.

- *Статичний* об’єкт ніколи не рухається (наприклад, геометрія рівня).
- На *динамічний* об’єкт діють сили й обертальні моменти, які під час моделювання перетворюються на швидкості.
- *Кінематичним* об’єктом керує логіка застосунку, але він усе одно впливає на інші динамічні об’єкти.

У такій грі нам потрібна поведінка, що нагадує фізику реального світу, але чутливе керування та збалансовані механіки значно важливіші. Приємний для гравця стрибок не обов’язково має бути фізично точним чи відбуватися під дією реальної гравітації. Утім, [цей](http://hypertextbook.com/facts/2007/mariogravity.shtml) аналіз показує, що з кожною версією ігор про Маріо гравітація в них наближається до 9,8 м/с<sup>2</sup>. :-)

Важливо повністю контролювати те, що відбувається, щоб розробляти й налаштовувати механіки для бажаних вражень від гри. Саме тому ми вирішили представити персонажа гравця кінематичним об’єктом. Так ми зможемо рухати персонажа як завгодно, не маючи справи з фізичними силами. Це означає, що нам доведеться самостійно усувати перетини між персонажем і геометрією рівня (про це докладніше згодом), але з цим недоліком ми готові змиритися. У фізичному світі персонаж матиме форму прямокутника.

## Рух {#movement}

Тепер, коли ми вирішили представити персонажа гравця кінематичним об’єктом, можемо вільно рухати його, задаючи позицію. Почнімо з руху ліворуч і праворуч.

Рух ґрунтуватиметься на прискоренні, щоб передати відчуття ваги персонажа. Як і для звичайного транспортного засобу, прискорення визначає, як швидко персонаж може досягти максимальної швидкості та змінити напрямок. Прискорення діє протягом часового кроку кадру — зазвичай переданого в параметрі `dt` (дельта-`t`), — а отримана зміна додається до швидкості. Так само швидкість діє протягом кадру, а отримане переміщення додається до позиції. У математиці це називається [інтегруванням за часом](http://en.wikipedia.org/wiki/Integral).

![Наближене інтегрування швидкості](images/platformer/integration.png)

Дві вертикальні лінії позначають початок і кінець кадру. Їхня висота відповідає швидкості персонажа в ці два моменти часу. Назвімо ці швидкості `v0` і `v1`. `v1` отримуємо, застосувавши прискорення (нахил кривої) протягом часового кроку `dt`:

![Рівняння швидкості](images/platformer/equationofvelocity.png)

Помаранчева площа відповідає переміщенню, яке потрібно застосувати до персонажа протягом поточного кадру. Геометрично цю площу можна наближено обчислити так:

![Рівняння переміщення](images/platformer/equationoftranslation.png)

Ось як ми інтегруємо прискорення та швидкість, щоб рухати персонажа в циклі оновлення:

1. Визначте цільову швидкість на основі введення
2. Обчисліть різницю між поточною та цільовою швидкостями
3. Спрямуйте прискорення в напрямку цієї різниці
4. Обчисліть зміну швидкості в цьому кадрі (`dv` — скорочення від дельта-швидкості), як показано вище:

    ```lua
    local dv = acceleration * dt
    ```

5. Перевірте, чи перевищує `dv` потрібну різницю швидкостей, і якщо так — обмежте її
6. Збережіть поточну швидкість для подальшого використання (`self.velocity`, яка зараз містить швидкість попереднього кадру):

    ```lua
    local v0 = self.velocity
    ```

7. Обчисліть нову швидкість, додавши зміну швидкості:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Обчисліть переміщення вздовж осі x в цьому кадрі, проінтегрувавши швидкість, як показано вище:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Застосуйте його до персонажа гравця

Якщо ви не впевнені, як обробляти введення в Defold, відповідний посібник можна знайти [тут](/manuals/input).

На цьому етапі ми можемо рухати персонажа ліворуч і праворуч, а керування відчувається плавним і передає його вагу. Тепер додаймо гравітацію!

Гравітація — це теж прискорення, але вона діє на персонажа вздовж осі y. Тому ми застосуємо її так само, як описане вище прискорення руху. Якщо просто перейти у наведених вище обчисленнях до векторів і на кроці 3) врахувати гравітацію в компоненті y прискорення, усе запрацює. Як же не любити векторну математику! :-)

## Реакція на колізії {#collision-response}

Тепер наш персонаж може рухатися й падати, тож час розглянути реакцію на колізії.
Звісно, нам потрібно приземлятися на геометрію рівня й рухатися вздовж неї. Щоб персонаж ніколи ні з чим не перетинався, ми використовуватимемо точки контакту, які надає фізичний рушій.

Точка контакту містить _нормаль_ контакту (спрямовану назовні від об’єкта, з яким ми зіткнулися, хоча в інших рушіях це може бути інакше), а також _відстань_, що показує, наскільки глибоко ми проникли в інший об’єкт. Цього достатньо, щоб усунути перетин персонажа з геометрією рівня.
Оскільки ми використовуємо прямокутник, протягом одного кадру може виникнути кілька точок контакту. Це трапляється, наприклад, коли два кути прямокутника перетинають горизонтальну поверхню землі або коли персонаж рухається в кут.

![Нормалі контактів, що діють на персонажа гравця](images/platformer/collision.png)

Щоб не застосовувати ту саму корекцію кілька разів, ми накопичуємо корекції у векторі й таким чином уникаємо надмірної компенсації. Інакше персонаж опинився б надто далеко від об’єкта, з яким зіткнувся. На зображенні вище видно дві поточні точки контакту, позначені двома стрілками (нормалями). Глибина проникнення однакова для обох контактів, і якби ми щоразу сліпо використовували її, то перемістили б персонажа вдвічі далі, ніж потрібно.

::: sidenote
Важливо кожного кадру скидати накопичені корекції до нульового вектора.
Додайте щось подібне наприкінці функції `update()`:
`self.corrections = vmath.vector3()`
:::

Якщо є функція зворотного виклику, що викликається для кожної точки контакту, ось як у ній можна усунути перетин:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Спроєктуйте вектор корекції на нормаль контакту (для першої точки контакту вектор корекції є нульовим)
2. Обчисліть компенсацію, потрібну для цієї точки контакту
3. Додайте її до вектора корекції
4. Застосуйте компенсацію до персонажа гравця

Також потрібно прибрати ту частину швидкості персонажа, яка спрямована до точки контакту:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Спроєктуйте швидкість на нормаль
2. Якщо проєкція від’ємна, це означає, що частина швидкості спрямована до точки контакту; у такому разі приберіть цю складову

## Стрибки {#jumping}

Тепер, коли ми можемо бігати по геометрії рівня й падати, час стрибати! Стрибки у платформерах можна реалізувати багатьма способами. У цій грі ми прагнемо отримати щось схоже на Super Mario Bros і Super Meat Boy. Під час стрибка імпульс штовхає персонажа вгору, фактично задаючи йому фіксовану швидкість.

Гравітація безперервно тягнутиме персонажа назад униз, утворюючи гарну дугу стрибка. Перебуваючи в повітрі, гравець усе ще може керувати персонажем. Якщо гравець відпустить кнопку стрибка до вершини дуги, швидкість руху вгору зменшиться, щоб передчасно припинити підйом.

1. Коли кнопку натиснуто, виконайте:

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Це слід робити лише в момент _натискання_ кнопки, а не кожного кадру, поки її _утримують натиснутою_.

2. Коли кнопку відпущено, виконайте:

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike створив чудові графіки дуг стрибків у [Super Mario Bros 3](http://meyermike.com/wp/?p=175) і [Super Meat Boy](http://meyermike.com/wp/?p=160), з якими варто ознайомитися.

## Геометрія рівня {#level-geometry}

Геометрія рівня — це форми колізій оточення, з якими стикається персонаж гравця (і, можливо, інші об’єкти). У Defold є два способи створити цю геометрію.

Перший — створювати окремі форми колізій поверх побудованих рівнів. Цей метод дуже гнучкий і дає змогу точно розміщувати графіку. Він особливо корисний, якщо вам потрібні пологі схили.
Цей спосіб побудови рівнів використовувався у грі [Braid](http://braid-game.com/), і саме так побудовано приклад рівня в цьому уроці. Ось який вигляд він має в редакторі Defold:

![Редактор Defold із геометрією рівня та персонажем, розміщеними у світі](images/platformer/editor.png)

Інший варіант — будувати рівні з плиток і доручити редактору автоматично генерувати фізичні форми на основі графіки плиток. Це означає, що геометрія рівня автоматично оновлюватиметься після змін у рівнях, що може бути надзвичайно корисним.

Фізичні форми розміщених плиток автоматично об’єднуються в одну, якщо вони прилягають одна до одної.
Це усуває проміжки, через які персонаж може зупинятися або підстрибувати, ковзаючи по кількох горизонтальних плитках. Для цього під час завантаження полігони плиток у Box2D замінюються реберними формами.

![Кілька полігонів на основі плиток, зшитих в один](images/platformer/stitching.png)

Вище наведено приклад, у якому ми створили п’ять сусідніх плиток із фрагмента графіки платформера. На зображенні видно, як розміщені плитки (вгорі) відповідають єдиній зшитій формі (сірий контур унизу).

Докладніше читайте в наших посібниках про [фізику](/manuals/physics) та [плитки](/manuals/2dgraphics).

## На завершення {#final-words}

Якщо вас цікавить більше інформації про механіки платформерів, тут зібрано напрочуд великий обсяг відомостей про фізику в [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide).

Якщо ви спробуєте наш шаблонний проєкт на пристрої iOS або з мишею, стрибок може здатися дуже незручним.
Це лише наша невдала спроба зробити платформер із керуванням одним дотиком. :-)

Ми не розповіли, як працюємо з анімаціями в цій грі. Ви можете зрозуміти це, переглянувши наведений нижче *player.script*: знайдіть функцію `update_animations()`.

Сподіваємося, ця інформація була для вас корисною!
Створіть чудовий платформер, щоб ми всі могли в нього пограти! <3

## Код {#code}

Ось вміст *player.script*:

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
