---
title: Повідомлення про колізії в Defold
brief: Коли два об’єкти стикаються, рушій викликає функцію зворотного виклику обробки подій або розсилає повідомлення.
---

# Повідомлення про колізії {#collision-messages}

Коли два об’єкти стикаються, рушій надсилає подію до функції зворотного виклику обробки подій або розсилає повідомлення обом об’єктам.

## Фільтрування подій {#event-filtering}

Типами подій, що генеруються, можна керувати за допомогою прапорців для кожного об’єкта:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

За замовчуванням усі вони мають значення `true`.
Коли два об’єкти колізій (collision objects) взаємодіють, рушій перевіряє, чи слід надсилати повідомлення користувачеві, зважаючи на ці прапорці.

Наприклад, для прапорців "Generate Contact Events":

Якщо використовується `physics.set_event_listener()`:

| Компонент A | Компонент B | Надсилати повідомлення |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | Так          |
| ❌          | ✅︎          | Так          |
| ✅︎          | ❌          | Так          |
| ❌          | ❌          | Ні           |

Якщо використовується обробник повідомлень за замовчуванням:

| Компонент A | Компонент B | Надсилати повідомлення   |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Так (A,B) + (B,A) |
| ❌          | ✅︎          | Так (B,A)         |
| ✅︎          | ❌          | Так (A,B)         |
| ❌          | ❌          | Ні                |

## Реакція на колізію {#collision-response}

Повідомлення `"collision_response"` надсилається, коли один з об’єктів, що стикаються, має тип "dynamic", "kinematic" або "static". У ньому задано такі поля:

`other_id`
: ідентифікатор екземпляра (instance), з яким зіткнувся об’єкт колізій (`hash`)

`other_position`
: позиція у світовому просторі екземпляра, з яким зіткнувся об’єкт колізій (`vector3`)

`other_group`
: група колізій іншого об’єкта колізій (`hash`)

`own_group`
: група колізій поточного об’єкта колізій (`hash`)

Повідомлення `collision_response` підходить лише для обробки колізій, коли не потрібні подробиці фактичного перетину об’єктів, наприклад, якщо ви хочете визначити, чи влучила куля у ворога. Для кожної пари об’єктів, що стикаються, за кадр надсилається лише одне таке повідомлення.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Реакція в точці контакту {#contact-point-response}

Повідомлення `"contact_point_response"` надсилається, коли один з об’єктів, що стикаються, має тип "dynamic" або "kinematic", а інший — "dynamic", "kinematic" або "static". У ньому задано такі поля:

`position`
: позиція точки контакту у світовому просторі (`vector3`).

`normal`
: нормаль у точці контакту у світовому просторі, спрямована від іншого об’єкта до поточного (`vector3`).

`relative_velocity`
: відносна швидкість об’єкта колізій з погляду іншого об’єкта (`vector3`).

`distance`
: глибина проникнення між об’єктами — невід’ємне значення (`number`).

`applied_impulse`
: імпульс, що виник унаслідок контакту (`number`).

`life_time`
: (*наразі не використовується!*) час існування контакту (`number`).

`mass`
: маса поточного об’єкта колізій у кг (`number`).

`other_mass`
: маса іншого об’єкта колізій у кг (`number`).

`other_id`
: ідентифікатор екземпляра, з яким контактує об’єкт колізій (`hash`).

`other_position`
: позиція іншого об’єкта колізій у світовому просторі (`vector3`).

`other_group`
: група колізій іншого об’єкта колізій (`hash`).

`own_group`
: група колізій поточного об’єкта колізій (`hash`).

Для гри чи застосунку, де потрібно повністю розділити об’єкти, повідомлення `"contact_point_response"` надає всю необхідну інформацію. Однак зауважте, що для кожної пари об’єктів, що стикаються, за кадр може надходити кілька повідомлень `"contact_point_response"` залежно від характеру колізії. Докладніше див. у [посібнику з розв’язання колізій](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Реакція тригера {#trigger-response}

Повідомлення `"trigger_response"` надсилається, коли один з об’єктів, що стикаються, має тип "trigger". Повідомлення надсилається один раз, коли колізію виявлено вперше, і ще раз, коли об’єкти більше не стикаються. Воно має такі поля:

`other_id`
: ідентифікатор екземпляра, з яким зіткнувся об’єкт колізій (`hash`).

`enter`
: `true`, якщо взаємодія була входом у тригер, `false`, якщо це був вихід. (`boolean`).

`other_group`
: група колізій іншого об’єкта колізій (`hash`).

`own_group`
: група колізій поточного об’єкта колізій (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
