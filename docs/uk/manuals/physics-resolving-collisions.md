---
title: Розв’язання кінематичних колізій у Defold
brief: Цей посібник пояснює, як розв’язувати кінематичні фізичні колізії.
---

# Розв’язання кінематичних колізій {#resolving-kinematic-collisions}

Коли ви використовуєте кінематичні об’єкти колізій (kinematic collision objects), вам потрібно самостійно розв’язувати колізії та переміщувати об’єкти у відповідь на них. Найпростіша реалізація розділення двох об’єктів, що зіткнулися, має такий вигляд:

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Цей код відокремить ваш кінематичний об’єкт від іншого фізичного об’єкта, у який він проникає, але розділення часто виявляється надмірним, і в багатьох випадках ви побачите тремтіння. Щоб краще зрозуміти проблему, розгляньте такий випадок, у якому персонаж гравця зіткнувся з двома об’єктами, *A* і *B*:

![Фізична колізія](images/physics/collision_multi.png)

У кадрі, у якому виникає колізія, фізичний рушій надішле кілька повідомлень `"contact_point_response"`: одне для об’єкта *A* й одне для об’єкта *B*. Якщо ви переміщуватимете персонажа у відповідь на кожне проникнення, як у найпростішому коді вище, розділення відбуватиметься так:

- Перемістіть персонажа за межі об’єкта *A* відповідно до глибини проникнення в нього (чорна стрілка)
- Перемістіть персонажа за межі об’єкта *B* відповідно до глибини проникнення в нього (чорна стрілка)

Порядок цих дій довільний, але результат у будь-якому разі однаковий: загальне розділення, що є *сумою окремих векторів проникнення*:

![Найпростіше фізичне розділення](images/physics/separation_naive.png)

Щоб правильно відокремити персонажа від об’єктів *A* і *B*, потрібно обробити глибину проникнення для кожної точки контакту та перевірити, чи попередні розділення вже не забезпечили потрібного розділення повністю або частково.

Припустімо, що перше повідомлення про точку контакту надходить від об’єкта *A* і ви переміщуєте персонажа назовні на вектор проникнення *A*:

![Фізичне розділення, крок 1](images/physics/separation_step1.png)

Тоді персонаж уже частково відокремлений від *B*. Остаточну компенсацію, необхідну для повного відокремлення від об’єкта *B*, показано чорною стрілкою вище. Довжину вектора компенсації можна обчислити, спроєктувавши вектор проникнення *A* на вектор проникнення *B*:

![Проєкція](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

Вектор компенсації можна знайти, зменшивши довжину *B* на *l*. Щоб виконати це обчислення для довільної кількості проникнень, можна накопичувати потрібну корекцію у векторі. Почніть із вектора корекції нульової довжини та для кожної точки контакту виконайте такі дії:

1. Спроєктуйте поточну корекцію на вектор проникнення контакту.
2. Обчисліть, яка компенсація ще потрібна для вектора проникнення (за наведеною вище формулою).
3. Перемістіть об’єкт на вектор компенсації.
4. Додайте компенсацію до накопиченої корекції.

Повна реалізація має такий вигляд:

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```
