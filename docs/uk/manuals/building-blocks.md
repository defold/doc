---
title: Будівельні блоки Defold
brief: Цей посібник вникає в деталі ігрових обʼєктів, компонентів та колецкцій.
---

# Будівельні блоки

В центрі архітектури Defold знаходяться кілька дуже важливих концепцій. Цей посібник пояснює з яких блоків складається Defold. Після того як прочитаєте цей посібник, переходьте до [посібника по адресації](/manuals/addressing) та [надсиланню повідомлень](/manuals/message-passing). А в редакторі є набір [уроків](/tutorials/getting-started) для швидкого старту.

![Будівельні блоки](images/building_blocks/building_blocks.png){srcset="images/building_blocks/building_blocks@2x.png 2x"}

Defold гра складається з блоків трьох головних типів:

Колекція (collection)
: Колекція - це файл, який використовується для структуризації вашої гри. В колекціях ви складаєте ієрархію з ігрових обʼєктів та інших колекцій. Зазвичай колекції використовують для створення структури ігрових рівнів, груп ворогів або персонажів, які складаються з декількох ігрових обʼєктів.

Ігровий обʼєкт (game object)
: Ігровий обʼєкт - це контейнер, що має ідентифікатор, позицію, поворот, та масштаб. Він містить в собі компоненти. Зазвичай ігрові обʼєкти використовуються для створення персонажів гравців, куль, систем ігрових правил, завантажувачів або розвантажувачів рівнів, тощо.

Компонент (component)
: Компоненти - це сутності, які можна додати до ігрових обʼєктів щоб надати їм графіку, звук або логіку в грі. Зазвичай вони використовуються щоб створювати спрайти (sprites) персонажів, файли сценаріїв, додавати звукові ефекти та частинки.

## Колекції (collections)

Колекції - це деревоподібні структури, які містять в собі ігрові обʼєкти та інші колекції. Вони завжди зберігаються у файлах.

Коли рушій Defold стартує, він завантажує єдину _стартову колекцію (bootstrap collection)_, яка вказана в файлі налаштувань проєкту *game.project*. Стартова колекція зазвичай називається "main.collection", але ви можете переіменувати її як завгодно.

Колекція може містити ігрові обʼєкти та інші колекції (через посилання на файл підколекції), скомпоновані як завгодно. Ось, наприклад, файл "main.collection". Він містить один ігровий обʼєкт (з ідентифікатором "can") та одну підколекію (з ідентифікатором "bean"). В свою чергу, підколекція містить два ігрові обʼєкти: "bean" та "shield".

![Колекція](images/building_blocks/collection.png){srcset="images/building_blocks/collection@2x.png 2x"}

Зверніть увагу, підколекція "bean" зберігається в своєму окремому файлі під назвою "/main/bean.collection" а "main.collection" на неї лише посилається:

![Колекція Bean](images/building_blocks/bean_collection.png){srcset="images/building_blocks/bean_collection@2x.png 2x"}

Самі колекції не можна адресувати, тому що під час виконання не існує обʼєктів, відповідних колекціям "main" та "bean". Однак, іноді вам доведеться використовувати ідентифікатор колекції як частину _шляху_ до ігрового обʼєкта (див. [посібник з адресації](/manuals/addressing)):

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

Колекція завжди додається до іншої колекції як посилання на файл:

Клацніть <kbd>правою кнопкою</kbd> на колекцію в вікні *Структура (Outline)* та оберіть <kbd>Add Collection File</kbd>.

## Ігрові обʼєкти (Game Objects)

Ігрові обʼєкти - це прості обʼєкти, кожен із своїм життєвим циклом під час виконання гри. В них є позиція, поворот та масштаб (position, rotation, scale), які можна змінювати та анімувати під час виконання.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Ігрові обʼєкти можна використовувати пустими (наприклад, в якості маркерів позиції), але зазвичай до них додаються різномаїтні компоненти: спрайти, звуки, сценарії, моделі, фабрики, та інші. Ігрові обʼєкти створюються в редакторі, додаються до колекцій, або генеруються динамічно під час виконання за допомогою компонентів _фабрик (factory)_.

Ігрові обʼєкти додаються до колекції на місці, або як посилання на файл ігрового обʼєкта:

Клацніть <kbd>правою кнопкою</kbd> на колекції в вікні *Структура (Outline)* та оберіть <kbd>Add Game Object</kbd> (додати на місці) або <kbd>Add Game Object File</kbd> (додати як посилання на файл).


## Компоненти (Components)

:[компоненти](../shared/components.md)

Див. [огляд компонентів](/manuals/components/) із переліком всіх доступних типів компонентів.

## Додавання обʼєктів на місці (in-place) або за посиланням (by reference)

Коли ви створюєте _файл_ колекції, ігрового обʼєкта або компонента, ви створюєте так званий прототип (також відомий як "prefab" або "blueprint" в інших рушіях). Такий файл лише додається до структури проєкту, нічого не буде додано до вашої гри під час виконання. Для того щоб створити екземпляр(instance) колекції, ігрового обʼєкта або компонента, його потрібно додати до файлу колекції.

Ви можете побачити файл, із якого створюється екземпляр, у вікні структури (outline). Файл "main.collection" містить три єкземпляри, що засновані на цих файлах:

1. Підколекція "bean".
2. Компонент-сценарій "bean", в ігровому обʼєкті "bean", в підколекції "bean".
3. Компонент-сценарій "can", в ігровому обʼєкті "can" .

![Екземпляр](images/building_blocks/instance.png){srcset="images/building_blocks/instance@2x.png 2x"}

Користь від створення файлів-прототипів стає очевидною коли ви маєте кілька екземплярів ігрового обʼєкта або колекції та бажаєте міняти їх всіх одразу:

![Екземпляри ІО](images/building_blocks/go_instance.png){srcset="images/building_blocks/go_instance@2x.png 2x"}

Після змін в файлі-прототипі, всі екземпляри, що використовують такий файл, будуть одразу ж оновлені.

![Зміна прототипу ІО](images/building_blocks/go_change_blueprint.png){srcset="images/building_blocks/go_change_blueprint@2x.png 2x"}

Наприклад, тут зображення спрайту було змінене в прототипі, і негайно всі екземпляри оновились:

![Оновлені екземпляри ІО](images/building_blocks/go_instance2.png){srcset="images/building_blocks/go_instance2@2x.png 2x"}

## Дочірні ігрові обʼєкти (childing)

У файлі колекції ви можете будувати ієрархії ігрових обʼєктів таким чином, щоб один або більше ігрових обʼєктів ставали дочірніми в межах одного батьківського обʼєкта. Просто <kbd>перетягніть</kbd> один обʼєкт на інший, і перетягнутий обʼєкт стане дочірнім:

![Дочірні ігрові обʼєкти](images/building_blocks/childing.png){srcset="images/building_blocks/childing@2x.png 2x"}

Ієрархія дочірніх обʼєктів - це динамічні відносини, вони впливають на те як обʼєкти реагують на трансформації. Будь-яка трансформація обʼєкта (пересування, поворот або масштаб) буде в свою чергу застосована до дочірніх обʼєктів, як у редакторі, так і під час виконання:

![Дочірня трансформація](images/building_blocks/child_transform.png){srcset="images/building_blocks/child_transform@2x.png 2x"}

І навпаки, трансформації дочірнії обʼєктів виконуються в локальному просторі батьківського обʼєкта. В редакторі ви можете обирати чи редагувати обʼєкт в батьківскьому просторі, чи в глобальному, обравши <kbd>Edit ▸ World Space</kbd> (за замовчуванням) або <kbd>Edit ▸ Local Space</kbd>.

Також, батька можна змінити під час виконання відправивши повідомлення `set_parent` обʼєкту.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Поширене непорозуміння що місце обʼєкта в колекції змінюється коли він стає частиною батьківських-дочірніх відносин. Однак, це різні речі. Ієрархія дочірніх обʼєктів динамічно змінює граф сцени, що дозволяю обʼєктам візуально приєднуватися одне до одного. Єдине, від чого залежить адрес обʼєкта, це його місце в ієрархії колекцій. Адреса залишиться статичною на весь час існування обʼєкта.
:::