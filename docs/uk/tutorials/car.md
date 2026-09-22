---
title: Створення простого автомобіля в Defold.
brief: Якщо ви лише починаєте працювати з Defold, цей урок допоможе вам зорієнтуватися в редакторі. Він також пояснює основні ідеї та найуживаніші будівельні блоки Defold — ігрові об’єкти, колекції, скрипти та спрайти.
---

# Створення автомобіля {#building-a-car}

Якщо ви лише починаєте працювати з Defold, цей урок допоможе вам зорієнтуватися в редакторі. Він також пояснює основні ідеї та найуживаніші будівельні блоки Defold: ігрові об’єкти (game objects), колекції (collections), скрипти та спрайти.

Ми почнемо з порожнього проєкту й крок за кроком створимо зовсім невеликий застосунок, у який можна грати. Сподіваємося, наприкінці ви зрозумієте, як працює Defold, і будете готові перейти до докладнішого уроку або одразу заглибитися в посібники.

::: sidenote
У цьому уроці докладні описи понять і способів виконання окремих дій позначено так само, як цей абзац. Якщо ці розділи здаються вам надто докладними, пропускайте їх.
:::

## Створення нового проєкту {#creating-a-new-project}

![Новий проєкт](images/new_empty.png)

1. Запустіть Defold.
2. Виберіть *New Project* ліворуч.
3. Виберіть вкладку *From Template*.
4. Виберіть *Empty Project*
5. Виберіть розташування проєкту на локальному диску.
6. Натисніть *Create New Project*.

## Редактор {#the-editor}

Почніть зі створення [нового проєкту](/manuals/project-setup/) і відкрийте його в редакторі. Двічі клацніть файл *main/main.collection*, щоб відкрити його:

![Огляд редактора](../manuals/images/editor/editor2_overview.png)

Редактор складається з таких основних областей:

Assets pane
: Тут показано всі файли вашого проєкту. Різні типи файлів мають різні піктограми. Двічі клацніть файл, щоб відкрити його в редакторі для відповідного типу. Спеціальна тека *builtins*, доступна лише для читання, є спільною для всіх проєктів і містить корисні ресурси: стандартний скрипт рендерингу, шрифт, матеріали для рендерингу різних компонентів та інше.

Main Editor View
: Залежно від типу файлу, який ви редагуєте, у цій області показано відповідний редактор. Найчастіше використовується редактор сцен, який ви бачите тут. Кожен відкритий файл показано в окремій вкладці.

Changed Files
: Містить файли, які локально додано, змінено, перейменовано або видалено порівняно з поточним комітом Git. Тут можна переглядати текстові відмінності та скасовувати локальні зміни. Для синхронізації з віддаленим репозиторієм використовуйте зовнішній клієнт Git або командний рядок.

Outline
: Вміст поточного редагованого файлу в ієрархічному вигляді. У цій області можна додавати, видаляти, змінювати та вибирати об’єкти й компоненти.

Properties
: Властивості поточного вибраного об’єкта або компонента.

Console
: Коли гра працює, у цій області показано виведення ігрового рушія (журнал, помилки, налагоджувальну інформацію тощо), а також ваші налагоджувальні повідомлення `print()` і `pprint()` зі скриптів. Якщо застосунок або гра не запускається, насамперед перевірте консоль. За консоллю розташовано вкладки з інформацією про помилки та редактором кривих, який використовується для створення ефектів частинок.

## Запуск гри {#running-the-game}

Шаблон проєкту "Empty" справді зовсім порожній. Попри це, виберіть <kbd>Project ▸ Build</kbd>, щоб зібрати проєкт і запустити гру.

![Збирання](images/car/start_build_and_launch.png)

Чорний екран, можливо, не дуже захоплює, але це вже запущений ігровий застосунок Defold, і ми легко можемо перетворити його на щось цікавіше. Тож зробімо це.

::: sidenote
Редактор Defold працює з файлами. Двічі клацнувши файл на панелі *Assets pane*, ви відкриєте його у відповідному редакторі. Після цього можна працювати з вмістом файлу.

Завершивши редагування файлу, збережіть його. Виберіть <kbd>File ▸ Save</kbd> у головному меню. Редактор підказує, які файли містять незбережені зміни: додає зірочку '\*' до імені файлу на вкладці.

![Файл із незбереженими змінами](images/car/file_changed.png)
:::

## Складання автомобіля {#assembling-the-car}

Насамперед створімо нову колекцію. Колекція — це контейнер ігрових об’єктів, які ви додали та розташували. Найчастіше колекції використовуються для створення ігрових рівнів, але вони також корисні, коли потрібно повторно використовувати групи та/або ієрархії пов’язаних ігрових об’єктів. Колекції можна уявляти як різновид префабів.

Клацніть теку *main* на панелі *Assets pane*, потім клацніть правою кнопкою миші та виберіть <kbd>New ▸ Collection File</kbd>. Також можна вибрати <kbd>File ▸ New ▸ Collection File</kbd> у головному меню.

![Новий файл колекції](images/car/start_new_collection.png)

Назвіть новий файл колекції *car.collection* і відкрийте його. У цій новій порожній колекції ми складемо невеликий автомобіль із кількох ігрових об’єктів. Ігровий об’єкт — це контейнер компонентів (components), наприклад спрайтів, звуків, скриптів логіки тощо, з яких ви будуєте гру. Кожен ігровий об’єкт має у грі унікальний ідентифікатор. Ігрові об’єкти можуть взаємодіяти через передавання повідомлень, але про це — пізніше.

Також ігровий об’єкт можна створити на місці (in-place) у колекції, як ми зробили тут. У результаті виходить окремий об’єкт. Його можна скопіювати, але кожна копія буде незалежною — зміни в одній не впливатимуть на інші. Це означає, що якщо ви створите 10 копій ігрового об’єкта й вирішите змінити їх усі, вам доведеться відредагувати всі 10 екземплярів (instances) об’єкта. Тому ігрові об’єкти, створені на місці, варто використовувати, коли ви не плануєте робити багато їхніх копій.

Натомість ігровий об’єкт, збережений у _файлі_, працює як прототип (в інших рушіях також відомий як "prefabs" або "blueprints"). Коли ви розміщуєте в колекції екземпляри збереженого у файлі ігрового об’єкта, кожен об’єкт додається _за посиланням_ (by reference) — це клон на основі прототипу. Якщо ви вирішите змінити прототип, кожен розміщений ігровий об’єкт на його основі миттєво оновиться.

![Додавання ігрового об’єкта автомобіля](images/car/start_add_car_gameobject.png)

Виберіть кореневий вузол "Collection" на панелі *Outline*, клацніть правою кнопкою миші та виберіть <kbd>Add Game Object</kbd>. У колекції з’явиться новий ігровий об’єкт з ідентифікатором "go". Виберіть його та встановіть ідентифікатор "car" на панелі *Properties*. Поки що "car" зовсім не цікавий. Він порожній, не має ні візуального подання, ні логіки. Щоб додати візуальне подання, нам потрібен _компонент_ спрайта.

Компоненти надають ігровим об’єктам видиме або чутне подання (графіку, звук) і функціональність (фабрики для створення об’єктів, колізії, поведінку, задану скриптами). Компонент не може існувати сам по собі — він має бути всередині ігрового об’єкта. Зазвичай компоненти визначаються на місці в тому самому файлі, що й ігровий об’єкт. Проте для повторного використання компонент можна зберегти в окремому файлі (як і ігровий об’єкт) і додати за посиланням до будь-якого файлу ігрового об’єкта. Деякі типи компонентів (наприклад, скрипти Lua) обов’язково потрібно розміщувати в окремому файлі компонента, а потім додавати до об’єктів за посиланням.

Зауважте, що ви не керуєте компонентами безпосередньо — можна переміщувати, повертати, масштабувати й анімувати властивості ігрових об’єктів, які містять компоненти.

![Додавання компонента автомобіля](images/car/start_add_car_component.png)

Виберіть ігровий об’єкт "car", клацніть правою кнопкою миші та виберіть <kbd>Add Component</kbd>, потім виберіть *Sprite* і натисніть *Ok*. Якщо вибрати спрайт на панелі *Outline*, ви побачите кілька властивостей, які потрібно задати:

Image
: Тут потрібно вказати джерело зображення для спрайта. Створіть файл атласу зображень: виберіть "main" на панелі *Assets pane*, клацніть правою кнопкою миші та виберіть <kbd>New ▸ Atlas File</kbd>. Назвіть новий файл атласу *sprites.atlas* і двічі клацніть його, щоб відкрити в редакторі атласів. Збережіть наведені нижче два файли зображень на комп’ютері та перетягніть їх до *main* на панелі *Assets pane*. Тепер виберіть кореневий вузол Atlas у редакторі атласів, клацніть правою кнопкою миші та виберіть <kbd>Add Images</kbd>. Додайте до атласу зображення автомобіля й шини та збережіть його. Тепер можна вибрати *sprites.atlas* як джерело зображення для компонента спрайта в ігровому об’єкті "car" у колекції "car".

Зображення для нашої гри:

![Зображення автомобіля](images/car/start_car.png)
![Зображення шини](images/car/start_tire.png)

Додайте ці зображення до атласу:

![Атлас спрайтів](images/car/start_sprites_atlas.png)

![Властивості спрайта](images/car/start_sprite_properties.png)

Default Animation
: Встановіть значення "car" (або назву, яку ви дали зображенню автомобіля). Кожному спрайту потрібна стандартна анімація, яка відтворюється, коли він з’являється у грі. Для зручності, коли ви додаєте зображення до атласу, Defold створює для кожного файлу однокадрову (нерухому) анімацію.

## Завершення автомобіля {#completing-the-car}

Додайте до колекції ще два ігрові об’єкти. Назвіть їх "left_wheel" і "right_wheel" та додайте до кожного компонент спрайта із зображенням шини, яке ми додали до *sprites.atlas*. Потім перетягніть ігрові об’єкти коліс на "car", щоб зробити їх дочірніми об’єктами "car". Дочірні ігрові об’єкти переміщуються разом із батьківським об’єктом. Їх також можна переміщувати окремо, але всі переміщення відбуваються відносно батьківського об’єкта. Для шин це ідеально: вони мають залишатися прикріпленими до автомобіля, а під час керування ми лише трохи повертатимемо їх ліворуч і праворуч. Колекція може містити будь-яку кількість ігрових об’єктів, розташованих поруч, організованих у складні батьківсько-дочірні дерева або поєднаних обома способами.

Перемістіть ігрові об’єкти шин на потрібні місця: виберіть їх, а потім виберіть <kbd>Scene ▸ Move Tool</kbd>. Перетягніть стрілки маніпулятора або центральний зелений квадрат, щоб розмістити об’єкт. Насамкінець потрібно переконатися, що шини малюються під автомобілем. Для цього встановіть компоненту Z позиції в -0.5. Усі візуальні елементи гри малюються від заднього плану до переднього, у порядку їхніх значень Z. Об’єкт зі значенням Z, рівним 0, буде намальовано поверх об’єкта зі значенням Z, рівним -0.5. Оскільки стандартне значення Z ігрового об’єкта автомобіля — 0, нове значення для об’єктів шин розмістить їх під зображенням автомобіля.

![Готова колекція автомобіля](images/car/start_car_collection_complete.png)

## Скрипт автомобіля {#the-car-script}

Остання складова — _скрипт_ для керування автомобілем. Скрипт — це компонент із програмою, яка визначає поведінку ігрових об’єктів. За допомогою скриптів можна задавати правила гри й визначати, як об’єкти реагуватимуть на різні взаємодії — і з гравцем, і з іншими об’єктами. Усі скрипти пишуться мовою програмування Lua. Щоб працювати з Defold, вам або комусь із вашої команди потрібно навчитися програмувати на Lua.

Виберіть "main" на панелі *Assets pane*, клацніть правою кнопкою миші та виберіть <kbd>New ▸ Script File</kbd>. Назвіть новий файл *car.script*, а потім додайте його до ігрового об’єкта "car": виберіть "car" на панелі *Outline*, клацніть правою кнопкою миші та виберіть <kbd>Add Component File</kbd>. Виберіть *car.script* і натисніть *OK*. Збережіть файл колекції.

Двічі клацніть *car.script*, щоб відкрити його.

::: sidenote
Defold надає кілька функцій життєвого циклу для написання ігрової логіки. Докладніше про них читайте в [посібнику зі скриптів](/manuals/script).
:::

Спочатку видаліть функції `final`, `on_message` і `on_reload`, оскільки вони не знадобляться
в цьому уроці.

Далі додайте наведені нижче рядки коду перед початком функції `init`.

```lua
-- Constants
local turn_speed = 0.1                           									  -- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector from center of back and front wheel pairs

local acceleration = 100 																						-- The acceleration of the car

-- prehash the inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Ці зміни досить прості: ми лише додали до скрипту кілька констант (`constants`), які згодом використаємо для програмування автомобіля.

::: sidenote
Зверніть увагу, що ми заздалегідь зберігаємо хеші у змінних. Це корисна практика: вона робить код читабельнішим і швидшим.
:::

Далі відредагуйте функцію `init`, щоб вона містила таке:

```lua
function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Some variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end
```

Цікаво, що саме ми змінили? Ось пояснення.

1. Надсилаємо повідомлення скрипту рендерингу з проханням установити сірий колір тла. Скрипти рендерингу — це спеціальні скрипти Defold, які керують відображенням об’єктів на екрані.
2. Щоб отримувати дії введення в компоненті-скрипті або скрипті GUI, потрібно надіслати повідомлення `acquire_input_focus` ігровому об’єкту, що містить цей компонент. У нашому випадку ми надсилаємо повідомлення ігровому об’єкту зі скриптом автомобіля.
3. Потім оголошуємо кілька змінних, за допомогою яких відстежуватимемо поточний стан автомобіля.

Просто, чи не так? Продовжимо: відредагуйте функцію `update`, щоб вона містила таке:

```lua
function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

Це велика функція! Але не хвилюйтеся — ось як вона працює:

1. Спочатку задаємо вектор прискорення на основі вектора введення. Завдяки цьому автомобіль прискорюється в напрямку, заданому введенням.
2. Далі обчислюємо переміщення обох пар коліс за простим принципом: задні колеса автомобіля завжди рухаються вперед, а передні — у напрямку, в який вони повернуті.
3. На основі переміщення обох пар коліс обчислюємо новий напрямок руху автомобіля.
4. Тут додаємо обчислене прискорення до швидкості.
5. Далі оновлюємо позицію автомобіля на основі поточної швидкості.
6. Застосовуємо сферичну лінійну інтерполяцію до кута повороту коліс залежно від введення ліворуч або праворуч. Завдяки цьому колеса не повертаються ривком щоразу, коли введення змінюється.
7. Потім задаємо поворот коліс відповідно до поточного кута кермування автомобіля. Так само задаємо поворот автомобіля відповідно до поточного напрямку його руху.
8. Насамкінець скидаємо вектори прискорення та введення.

Нарешті час зробити так, щоб автомобіль реагував на введення. Оновіть функцію `on_input` так:

```lua
function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Ця функція насправді досить проста: ми лише приймаємо введення та задаємо відповідний вектор.

Не забудьте зберегти зміни.

## Введення {#input}

Дії введення ще не налаштовано, тож виправмо це. Відкрийте файл */input/game.input_bindings* і додайте прив’язки *key_trigger* для "accelerate", "brake", "left" і "right". Ми призначимо їм клавіші зі стрілками (KEY_LEFT, KEY_RIGHT, KEY_UP і KEY_DOWN):

![Прив’язки введення](images/car/start_input_bindings.png)

## Додавання автомобіля до гри {#adding-the-car-to-the-game}

Тепер автомобіль готовий до поїздки. Ми створили його в "car.collection", але у грі його ще немає. Це тому, що наразі рушій завантажує "main.collection" під час запуску. Щоб це виправити, потрібно лише додати *car.collection* до *main.collection*. Відкрийте *main.collection*, виберіть кореневий вузол "Collection" на панелі *Outline*, клацніть правою кнопкою миші та виберіть <kbd>Add Collection From File</kbd>, виберіть *car.collection* і натисніть *OK*. Тепер вміст *car.collection* буде розміщено в *main.collection* як нові екземпляри. Якщо змінити вміст *car.collection*, кожен екземпляр колекції автоматично оновиться під час збирання гри.

![Додавання колекції автомобіля](images/car/start_adding_car_collection.png)

Тепер виберіть <kbd>Project ▸ Build</kbd> і випробуйте свій новий автомобіль!
Ви побачите, що тепер можете керувати його рухом. Але дещо ще працює не так. Коли ви відпускаєте клавіші керування, автомобіль не зупиняється, хоча мав би. Час додати цю поведінку!

## Сила опору поспішає на допомогу {#drag-to-the-rescue}

Коли об’єкт рухається в реальному світі, проти його руху діє сила опору, яка сповільнює його. Ця сила приблизно пропорційна квадрату швидкості рухомого об’єкта, тому її можна описати як `D = k * |V| * V`, де `k` — константа, `V` — вектор швидкості, а `|V|` — його довжина (модуль швидкості). Додаймо її.

У розділі констант на початку скрипту додайте таку константу

```lua
local drag = 1.1	        --the drag constant <1>
```

Потім у функції `update`, безпосередньо перед цим рядком, додайте наведені нижче рядки й збережіть файл.

```lua
function update(self, dt)
	...
  -- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Speed is the magnitude of the velocity
	local speed = vmath.length_sqr(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Оголошуємо значення опору як константу.
2. Обчислюємо швидкість руху.
3. Застосовуємо опір до поточного прискорення за формулою
4. Зупиняємо автомобіль, якщо його швидкість уже достатньо мала.

## Повний скрипт автомобіля {#the-complete-car-script}

Після виконання наведених вище кроків ваш *car.script* має виглядати так:

```lua
local turn_speed = 0.1                           				          	-- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector from center of back and front wheel pairs

local acceleration = 100 		                      									-- The acceleration of the car
local drag = 1.1                                                  	-- the drag constant

function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")

	-- Some variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Speed is the magnitude of the velocity
	local speed = vmath.length(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Випробування готової гри {#trying-the-final-game}

Тепер виберіть <kbd>Project ▸ Build</kbd> у головному меню й випробуйте свій новий автомобіль!

На цьому вступний урок завершено. Ось кілька завдань, які ви можете виконати самостійно:

1. Наразі автомобіль рухається з однаковим прискоренням уперед і назад. Можна змінити це, щоб заднім ходом автомобіль рухався повільніше.
2. Зробіть деякі константи (наприклад, прискорення) властивостями (`properties`), щоб їх можна було змінювати для різних екземплярів автомобіля.
3. Додайте автомобілю звуки, щоб він заревів! ([Підказка](/manuals/sound/))

А тепер заглиблюйтеся в Defold. Ми підготували багато [посібників і уроків](/learn), які допоможуть вам, а якщо виникнуть труднощі — завітайте на [форум](//forum.defold.com).

Приємної роботи з Defold!
