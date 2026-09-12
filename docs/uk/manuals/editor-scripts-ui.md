---
title: "Скрипти редактора: UI"
brief: Цей посібник пояснює, як створювати елементи UI в редакторі за допомогою Lua
---

# Скрипти редактора та UI {#editor-scripts-and-ui}

Цей посібник пояснює, як створювати інтерактивні діалогові вікна й відкривати ресурси в редакторі за допомогою скриптів редактора, написаних мовою Lua. Щоб почати працювати зі скриптами редактора, дивіться [посібник зі скриптів редактора](/manuals/editor-scripts). Повний довідник API редактора доступний [тут](/ref/stable/editor-lua/).

## Привіт, світе {#hello-world}

Усі функції, пов’язані з UI, містяться в модулі `editor.ui`. Ось найпростіший приклад скрипту редактора з власним UI, з якого можна почати:
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

Цей фрагмент коду визначає команду **View → Do with confirmation**. Після її виконання ви побачите таке діалогове вікно:

![Діалогове вікно «Привіт, світе»](images/editor_scripts/perform_action_dialog.png)

Зрештою, після натискання <kbd>Enter</kbd> (або кнопки `Perform`) у консолі редактора з’явиться такий рядок:
```
Perform action:	true
```

## Відкриття ресурсів {#opening-resources}

Викличте `editor.ui.open_resource()` із функції `run` команди, щоб відкрити ресурс проєкту. Шлях починається з `/`. Якщо не вказати подання, буде вибрано основне подання ресурсу:

```lua
editor.ui.open_resource("/main/main.script")
```

Подання `code` і `text` приймають позицію курсора або виділення як третій аргумент. Номери рядків і стовпців починаються з `1`; якщо стовпець не вказано, використовується `1`. Коли передаєте ці аргументи, обов’язково вказуйте подання:

```lua
editor.ui.open_resource("/main/main.script", "code", { line = 10 })
editor.ui.open_resource("/main/main.script", "code", { line = 10, column = 5 })
```

Щоб виділити діапазон, натомість задайте позиції курсора `from` і `to`:

```lua
editor.ui.open_resource("/main/main.script", "code", {
    from = { line = 10, column = 1 },
    to = { line = 12, column = 1 }
})
```

Налаштоване подання ресурсу може відкриватися в редакторі або зовнішньому застосунку. Вбудовані подання Code і Text підтримують аргументи курсора й виділення. Підтримувані назви подань наведено в [`editor.ui.open_resource()`](/ref/beta/editor/#editor.ui.open_resource:resource_path-view-args).

## Основні поняття {#basic-concepts}

### Компоненти {#components}

Редактор надає різні **компоненти** (components) UI, які можна поєднувати для створення потрібного інтерфейсу. За домовленістю всі компоненти налаштовуються за допомогою однієї таблиці, яка називається **props**. Самі компоненти — це не таблиці, а **незмінні значення userdata**, які редактор використовує для створення UI.

### Властивості props {#props}

**Props** — це таблиці, які визначають вхідні дані компонентів. Вважайте props незмінними: змінення таблиці props на місці не спричинить повторного рендерингу компонента, а використання іншої таблиці — спричинить. UI оновлюється, коли екземпляр (instance) компонента отримує таблицю props, яка не дорівнює попередній за поверхневого порівняння.

### Вирівнювання {#alignment}

Коли компоненту виділяють певну область у UI, він займає весь її простір, але це не означає, що його видима частина розтягнеться. Видима частина займає стільки місця, скільки їй потрібно, а потім вирівнюється в межах виділеної області. Тому більшість вбудованих компонентів визначають властивість `alignment`.

Наприклад, розгляньте цей компонент текстової мітки:
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
Видима частина — це текст `Hello`, який вирівнюється в межах виділеної компоненту області:

![Вирівнювання](images/editor_scripts/alignment.png)

## Вбудовані компоненти {#built-in-components}

Редактор визначає різні вбудовані компоненти, які можна використовувати разом для створення UI. Компоненти можна приблизно поділити на 3 категорії: компонування, подання даних і введення.

### Компоненти компонування {#layout-components}

Компоненти компонування використовуються для розміщення інших компонентів поруч. Основні компоненти компонування — **`horizontal`**, **`vertical`** і **`grid`**. Вони також визначають такі властивості, як **padding** і **spacing**: padding — це порожній простір від краю виділеної області до вмісту, а spacing — порожній простір між дочірніми компонентами:

![Внутрішні відступи та проміжки](images/editor_scripts/padding_and_spacing.png)

Редактор визначає константи `small`, `medium` і `large` для внутрішніх відступів і проміжків. Для проміжків `small` призначено для відстані між складовими окремого елемента UI, `medium` — між окремими елементами UI, а `large` — між групами елементів. Типовий проміжок — `medium`. Для внутрішніх відступів значення `large` означає відступ від країв вікна до вмісту, `medium` — від країв великого елемента UI, а `small` — від країв невеликих елементів UI, як-от контекстні меню та спливні підказки (ще не реалізовано).

Контейнер **`horizontal`** розміщує дочірні компоненти один за одним по горизонталі, завжди розтягуючи висоту кожного з них на весь доступний простір. Типово ширина кожного дочірнього компонента залишається мінімальною, але можна надати йому якомога більше місця, установивши для нього властивість `grow` у `true`.

Контейнер **`vertical`** подібний до горизонтального, але його осі поміняно місцями.

Нарешті, **`grid`** — це компонент-контейнер, який розміщує дочірні компоненти у двовимірній сітці, як у таблиці. Налаштування `grow` у сітці застосовується до рядків або стовпців, тому його задають не для дочірнього компонента, а в таблиці налаштувань стовпця. Крім того, за допомогою властивостей `row_span` і `column_span` дочірні компоненти в сітці можна налаштувати так, щоб вони займали кілька рядків або стовпців. Сітки корисні для створення форм із кількома полями введення:
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- add padding around dialog edges
    columns = {{}, {grow = true}}, -- make 2nd column grow
    children = {
        {
            editor.ui.label({ 
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({ 
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
Наведений вище код створить таку форму діалогового вікна:

![Діалогове вікно створення рівня](images/editor_scripts/new_level_dialog.png)

### Компоненти подання даних {#data-presentation-components}

Редактор визначає такі компоненти подання даних:

- **`label`** — текстова мітка для використання з полями введення у формах.
- **`icon`** — піктограма; наразі компонент може показувати лише невеликий набір заздалегідь визначених піктограм, але в майбутньому ми плануємо розширити цей набір.
- **`image`** — зображення, завантажене за шляхом ресурсу проєкту, який починається з `/`, або із зовнішнього URL. Необов’язкові властивості `width` і `height` вписують зображення в задані розміри зі збереженням його пропорцій.
- **`heading`** — текстовий елемент для відображення рядка заголовка, наприклад у формі чи діалоговому вікні. Перелічуваний тип `editor.ui.HEADING_STYLE` визначає різні стилі заголовків, зокрема заголовки HTML `H1`-`H6`, а також специфічні для редактора `DIALOG` і `FORM`.
- **`paragraph`** — текстовий елемент для відображення абзацу тексту. Основна відмінність від `label` полягає в тому, що абзац підтримує перенесення слів: якщо виділена область надто вузька, текст переноситиметься на наступні рядки й, можливо, скорочуватиметься за допомогою `"..."`, якщо не вміститься в області відображення.

Наприклад, UI може показувати як зображення з проєкту, так і зображення з інтернету:

```lua
editor.ui.vertical({
    children = {
        editor.ui.image({
            image = "/builtins/assets/images/logo/logo_256.png",
            width = 64,
            height = 64
        }),
        editor.ui.image({
            image = "https://defold.com/images/assets/monarch-hero.jpg"
        })
    }
})
```

### Компоненти введення {#input-components}

Компоненти введення призначено для взаємодії користувача з UI. Усі компоненти введення підтримують властивість `enabled`, яка керує доступністю взаємодії, і визначають різні властивості зі зворотними викликами, які сповіщають скрипт редактора про взаємодію.

Якщо ви створюєте статичний UI, достатньо визначити зворотні виклики, які просто змінюють локальні змінні. Про динамічні UI та складніші взаємодії дивіться в розділі [«Реактивність»](#reactivity).

Наприклад, просте статичне діалогове вікно New File можна створити так:
```lua
-- initial file name, will be replaced by the dialog
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- Typing callback:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
Ось перелік вбудованих компонентів введення:
- **`string_field`**, **`integer_field`** і **`number_field`** — різновиди однорядкового текстового поля, у яких можна редагувати рядки, цілі числа та числа.
- **`select_box`** використовується для вибору варіанта із заздалегідь визначеного масиву за допомогою розкривного списку.
- **`check_box`** — булеве поле введення зі зворотним викликом `on_value_changed`
- **`button`** зі зворотним викликом `on_press`, який виконується після натискання кнопки.
- **`external_file_field`** — компонент для вибору шляху до файлу на комп’ютері. Він складається з текстового поля та кнопки, яка відкриває діалогове вікно вибору файлу.
- **`resource_field`** — компонент для вибору ресурсу в проєкті.

Для всіх компонентів, окрім кнопок, можна задати властивість `issue`, яка відображає пов’язану з компонентом проблему (`editor.ui.ISSUE_SEVERITY.ERROR` або `editor.ui.ISSUE_SEVERITY.WARNING`), наприклад:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
Коли проблему задано, вигляд компонента введення змінюється, а також додається спливна підказка з повідомленням про проблему.

Ось демонстрація всіх компонентів введення з їхніми варіантами відображення проблем:

![Компоненти введення](images/editor_scripts/inputs_demo.png)

### Компоненти діалогових вікон {#dialog-related-components}

Щоб показати діалогове вікно, скористайтеся функцією `editor.ui.show_dialog`. Вона очікує компонент **`dialog`**, який визначає основну структуру діалогових вікон Defold: `title`, `header`, `content` і `buttons`. Компонент діалогового вікна має особливість: його не можна використовувати як дочірній компонент іншого компонента, оскільки він представляє вікно, а не елемент UI. Натомість `header` і `content` — звичайні компоненти.

Кнопки діалогового вікна також особливі: їх створюють за допомогою компонента **`dialog_button`**. На відміну від звичайних кнопок, кнопки діалогового вікна не мають зворотного виклику `on_pressed`. Натомість вони визначають властивість `result` зі значенням, яке функція `editor.ui.show_dialog` поверне після закриття діалогового вікна. Кнопки діалогового вікна також визначають булеві властивості `cancel` і `default`: кнопка з властивістю `cancel` спрацьовує, коли користувач натискає <kbd>Escape</kbd> або закриває діалогове вікно кнопкою закриття операційної системи, а кнопка `default` — коли користувач натискає <kbd>Enter</kbd>. Для кнопки діалогового вікна можна одночасно встановити обидві властивості `cancel` і `default` у `true`.

### Допоміжні компоненти {#utility-components}

Крім того, редактор визначає кілька допоміжних компонентів: 
- **`separator`** — тонка лінія для розділення блоків вмісту
- **`scroll`** — компонент-обгортка, який показує смуги прокручування, коли вкладений компонент не вміщується у виділеному просторі

## Реактивність {#reactivity}

Оскільки компоненти — це **незмінні значення userdata**, їх неможливо змінити після створення. Як тоді зробити так, щоб UI змінювався з часом? Відповідь: **реактивні компоненти**. 

::: sidenote
UI скриптів редактора створено під впливом бібліотеки [React](https://react.dev/), тому знання реактивних UI та хуків React стануть у пригоді. 
:::

Якщо пояснити найпростіше, реактивний компонент — це компонент із функцією Lua, яка отримує дані (props) і повертає подання (інший компонент). Функція реактивного компонента може використовувати **хуки** (hooks): спеціальні функції модуля `editor.ui`, які додають компонентам реактивні можливості. За домовленістю назви всіх хуків починаються з `use_`.

Щоб створити реактивний компонент, скористайтеся функцією `editor.ui.component()`. 

Розгляньмо цей приклад — діалогове вікно New File, у якому можна створити файл лише тоді, коли введене ім’я файлу не порожнє:

```lua
-- 1. dialog is a reactive component
local dialog = editor.ui.component(function(props)
    -- 2. the component defines a local state (file name) that defaults to empty string
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. typing + Enter updates the local state
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Cancel", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Create File",
                -- 4. creation is enabled when the name exists
                enabled = name ~= "",
                default = true,
                -- 5. result is the name
                result = name
            })
        }
    })
end)

-- 6. show_dialog will either return non-empty file name or nil on cancel
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

Коли ви виконаєте команду меню, яка запускає цей код, редактор покаже діалогове вікно, у якому кнопка `"Create File"` спочатку неактивна, але стане активною після введення імені та натискання <kbd>Enter</kbd>:

![Діалогове вікно створення файлу](images/editor_scripts/reactive_new_file_dialog.png)

Як це працює? Під час першого рендерингу хук `use_state` створює локальний стан, пов’язаний із компонентом, і повертає його разом із функцією встановлення стану. Виклик цієї функції планує повторний рендеринг компонента. Під час наступних рендерингів функція компонента викликається знову, а `use_state` повертає оновлений стан. Потім новий компонент подання, повернений функцією компонента, порівнюється з попереднім, і UI оновлюється там, де виявлено зміни.

Цей реактивний підхід значно спрощує створення інтерактивних UI та підтримання їх узгодженості: замість явного оновлення всіх зачеплених компонентів UI після введення користувача подання визначається як чиста функція від вхідних даних (props і локального стану), а редактор сам виконує всі оновлення.

### Правила реактивності {#rules-of-reactivity}

Щоб реактивні функціональні компоненти працювали, редактор очікує від них дотримання таких правил:

1. Функції компонентів мають бути чистими. Немає гарантій щодо того, коли та як часто викликатиметься функція компонента. Усі побічні ефекти мають відбуватися поза рендерингом, наприклад у зворотних викликах
2. Props і локальний стан мають бути незмінними. Не змінюйте props. Якщо локальний стан — це таблиця, не змінюйте її на місці: коли стан має змінитися, створіть нову таблицю та передайте її функції встановлення стану.
3. Функції компонентів мають викликати ті самі хуки в тому самому порядку під час кожного виклику. Не викликайте хуки всередині циклів, в умовних блоках, після дострокового повернення з функції тощо. Рекомендовано викликати хуки на початку функції компонента, перед будь-яким іншим кодом.
4. Викликайте хуки лише з функцій компонентів. Хуки працюють у контексті реактивного компонента, тому викликати їх можна лише у функції компонента (або в іншій функції, яку безпосередньо викликає функція компонента).

### Хуки {#hooks}

::: sidenote
Якщо ви знайомі з [React](https://react.dev/), то помітите, що семантика хуків у редакторі дещо відрізняється в частині залежностей хуків.
:::

Редактор визначає 2 хуки: **`use_memo`** і **`use_state`**.

### **`use_state`**

Локальний стан можна створити 2 способами: із типовим значенням або з функцією ініціалізації:
```lua
-- default value
local enabled, set_enabled = editor.ui.use_state(true)
-- initializer function + args
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
Так само функцію встановлення стану можна викликати з новим значенням або з функцією оновлення:
```lua
-- updater function
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)
    
    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

Нарешті, стан може бути **скинуто**. Стан скидається, коли змінюється будь-який з аргументів `editor.ui.use_state()`, що перевіряється за допомогою `==`. Тому не використовуйте літерали таблиць або функцій ініціалізації як аргументи хука `use_state`: це призведе до скидання стану під час кожного повторного рендерингу. Наприклад:
```lua
-- ❌ BAD: literal table initializer causes state reset on every re-render
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ GOOD: use initializer function outside of component function to create table state
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...later, in component function:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ BAD: literal initializer function causes state reset on every re-render
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ GOOD: use referenced initializer function to create the state
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

Хук `use_memo` можна використовувати для підвищення продуктивності. У функціях рендерингу часто виконують певні обчислення, наприклад перевіряють коректність введення користувача. Хук `use_memo` можна застосовувати тоді, коли перевірка, чи змінилися аргументи функції обчислення, потребує менше ресурсів, ніж виклик самої функції. Хук викличе функцію обчислення під час першого рендерингу та повторно використовуватиме обчислене значення під час наступних рендерингів, якщо всі аргументи `use_memo` залишаються незмінними:
```lua
-- validation function outside of component function
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...later, in component function
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
У цьому прикладі перевірка пароля виконуватиметься після кожної його зміни (наприклад, під час введення в поле пароля), але не після зміни імені користувача.

Ще один випадок використання `use_memo` — створення зворотних викликів для компонентів введення або використання локально створеної функції як значення властивості іншого компонента. Це запобігає зайвим повторним рендерингам.
