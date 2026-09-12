---
title: Написання нативних розширень для Defold
brief: Цей посібник пояснює, як написати нативне розширення для ігрового рушія Defold і скомпілювати його за допомогою хмарних засобів збирання, що не потребують налаштування.
---

# Нативні розширення {#native-extensions}

Якщо вам потрібна власна взаємодія із зовнішнім програмним або апаратним забезпеченням на низькому рівні, де можливостей Lua недостатньо, Defold SDK дає змогу писати розширення рушія мовами C, C++, C#, Objective-C, Java або JavaScript залежно від цільової платформи. Типові випадки використання нативних розширень (native extensions):

- Взаємодія з певним апаратним забезпеченням, наприклад із камерою мобільного телефона.
- Взаємодія із зовнішніми низькорівневими API, наприклад API рекламних мереж, які не підтримують взаємодію через мережеві API, де можна було б використати Luasocket.
- Високопродуктивні обчислення й обробка даних.

::: sidenote
Підтримка C# є експериментальною й призначена для нативних розширень, а не для компонентів-скриптів (script components) Defold. Вона використовує .NET 9 NativeAOT для створення статичної бібліотеки; додайте файли вихідного коду `.cs` до папки `src` розширення, і сервіс збирання згенерує файл проєкту. Підтримка цільових платформ залежить від поточних можливостей NativeAOT і сервісу збирання. Актуальний порядок роботи й перевірену конфігурацію наведено в офіційному [прикладі мов для нативних розширень](https://github.com/defold/example-languages).
:::

## Сервер збирання {#the-build-server}

Defold дає змогу почати роботу з нативними розширеннями без налаштування завдяки хмарному збиранню. Будь-яке нативне розширення, розроблене й додане до ігрового проєкту безпосередньо або через [бібліотечний проєкт](/manuals/libraries/), стає частиною звичайного вмісту проєкту. Не потрібно збирати спеціальні версії рушія й розповсюджувати їх серед учасників команди: це відбувається автоматично — кожен учасник команди, який збирає та запускає проєкт, отримає виконуваний файл рушія для цього проєкту з усіма вбудованими нативними розширеннями.

![Хмарне збирання](images/extensions/cloud_build.png)

Defold надає хмарний сервер збирання безкоштовно й без обмежень використання. Сервер розміщено в Європі, а URL, на який надсилається нативний код, налаштовується у [вікні Editor Preferences](/manuals/editor-preferences/#extensions) або за допомогою параметра командного рядка `--build-server` для [bob](/manuals/bob/#usage). Якщо ви хочете налаштувати власний сервер, [дотримуйтеся цих інструкцій](/manuals/extender-local-setup).

## Структура проєкту {#project-layout}

Щоб створити нове розширення, створіть папку в корені проєкту. Ця папка міститиме всі налаштування, вихідний код, бібліотеки й ресурси, пов’язані з розширенням. Засіб збирання розширень розпізнає структуру папок і збирає всі файли вихідного коду та бібліотеки.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: Папка розширення _обов’язково_ має містити файл *ext.manifest*. Це файл конфігурації з прапорцями й макровизначеннями, які використовуються під час збирання окремого розширення. Опис формату файлу наведено в [посібнику з маніфесту розширення](https://defold.com/manuals/extensions-ext-manifests/).

*src*
: Ця папка має містити всі файли вихідного коду.

*include*
: Ця необов’язкова папка містить файли для включення.

*lib*
: Ця необов’язкова папка містить скомпільовані бібліотеки, від яких залежить розширення. Файли бібліотек слід розміщувати в підпапках із назвами у форматі `platform` або `architecture-platform`, залежно від того, які архітектури підтримують ваші бібліотеки.

  :[Платформи](../shared/platforms.md)

*manifests*
: Ця необов’язкова папка містить додаткові файли, що використовуються під час збирання або пакування. Докладніше див. нижче.

*res*
: Ця необов’язкова папка містить додаткові ресурси, від яких залежить розширення. Файли ресурсів слід розміщувати в підпапках із назвами у форматі `platform` або `architecture-platform`, як і підпапки `lib`. Також допускається підпапка `common`, яка містить файли ресурсів, спільні для всіх платформ.

### Файли маніфестів {#manifest-files}

Необов’язкова папка *manifests* розширення містить додаткові файли, що використовуються під час збирання й пакування. Файли слід розміщувати в підпапках із назвами у форматі `platform`:

* `android` — у цій папці можна розмістити файл фрагмента маніфесту, який буде об’єднано з маніфестом основного застосунку ([як описано тут](/manuals/extensions-manifest-merge-tool)).
  * Папка також може містити файл `build.gradle` із залежностями, які [оброблятиме Gradle](/manuals/extensions-gradle).
  * Розширення з кодом Java мають містити [файл правил збереження R8](#r8-keep-rules-for-android) (`.keep`) для класів, потрібних їм під час виконання.
* `ios` — у цій папці можна розмістити файл фрагмента маніфесту, який буде об’єднано з маніфестом основного застосунку ([як описано тут](/manuals/extensions-manifest-merge-tool)).
  * Папка також може містити файл `Podfile` із залежностями, які [оброблятиме Cocoapods](/manuals/extensions-cocoapods).
* `osx` — у цій папці можна розмістити файл фрагмента маніфесту, який буде об’єднано з маніфестом основного застосунку ([як описано тут](/manuals/extensions-manifest-merge-tool)).
* `web` — у цій папці можна розмістити файл фрагмента маніфесту, який буде об’єднано з маніфестом основного застосунку ([як описано тут](/manuals/extensions-manifest-merge-tool)).


### Правила збереження R8 для Android {#r8-keep-rules-for-android}

Додайте файл `.keep` до каталогу `manifests/android` розширення, поряд із `build.gradle`. Наприклад, `/myextension/manifests/android/myextension.keep` може зберігати класи Java розширення за допомогою такого правила:

```proguard
-keep,allowoptimization class com.example.myextension.** { *; }
```

Замініть `com.example.myextension` пакетом, що містить класи Java вашого розширення. Це правило зберігає класи та їхні члени, водночас даючи R8 змогу оптимізувати їхній код. Додайте правила для інших класів, доступ до яких відбувається через Java Native Interface (JNI) або рефлексію, оскільки R8 може не виявити таке використання автоматично.

Якщо розширення використовує анотації під час виконання, також додайте:

```proguard
-keepattributes *Annotation*
```

Ці правила об’єднуються з вибраним файлом збереження проєкту, коли [ввімкнено R8](/manuals/android/#enabling-r8).


## Користувацькі ресурси {#custom-resources}

Розширення може включати дані до архіву гри, оголосивши користувацькі ресурси у файлі `ext.properties` поряд із `ext.manifest`:

```ini
[project]
custom_resources.default = /myextension/data
```

Наприклад, розмістіть файл JSON за шляхом `/myextension/data/settings.json`. Шлях задається від кореня проєкту й включає папку розширення. Коли ви поширюєте розширення як бібліотеку, додайте `myextension` до [Include Dirs](/manuals/libraries/#setting-up-library-sharing) бібліотеки, щоб проєкти, які її використовують, отримали розширення разом із даними.

Ці шляхи об’єднуються з `project.custom_resources` із *game.project* і внесками інших розширень. Налаштування користувацьких ресурсів у проєкті не замінює внески розширень. Файли включаються як до збірок редактора, так і до архівів Bob, і їх можна завантажувати під час виконання:

```lua
local data, err = sys.load_resource("/myextension/data/settings.json")
if data then
    local settings = json.decode(data)
    pprint(settings)
else
    print(err)
end
```

Про відмінності між користувацькими ресурсами й ресурсами пакета читайте в розділі [Доступ до файлів](/manuals/file-access/#custom-resources).

## Поширення розширення {#sharing-an-extension}

Розширення обробляються так само, як будь-які інші ресурси проєкту, і їх можна поширювати так само. Якщо папку нативного розширення додано як папку бібліотеки, нею можна поділитися, щоб інші могли використовувати її як залежність проєкту. Докладніше див. у [посібнику з бібліотечних проєктів](/manuals/libraries/).


## Простий приклад розширення {#a-simple-example-extension}

Створімо дуже просте розширення. Спочатку створимо папку *`myextension`* у корені проєкту й додамо файл *`ext.manifest`* із назвою розширення `MyExtension`. Зауважте, що назва є символом C++ і має збігатися з першим аргументом `DM_DECLARE_EXTENSION` (див. нижче).

![Маніфест](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

Розширення складається з одного файлу C++, *`myextension.cpp`*, який створюється в папці `src`.

![Файл C++](images/extensions/cppfile.png)

Файл вихідного коду розширення містить такий код:

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Зверніть увагу на макрос `DM_DECLARE_EXTENSION`, який використовується для оголошення різних точок входу в код розширення. Перший аргумент `symbol` має збігатися з назвою, зазначеною в *ext.manifest*. У цьому простому прикладі точки входу `update` і `on_event` не потрібні, тому у відповідні аргументи макросу передається `0`.

Тепер залишається лише зібрати проєкт (<kbd>Project ▸ Build</kbd>). Розширення буде надіслано до засобу збирання розширень, який створить власну версію рушія з новим розширенням. Якщо під час збирання виникнуть помилки, з’явиться діалогове вікно з помилками збирання.

Щоб перевірити розширення, створіть ігровий об’єкт (game object) і додайте компонент-скрипт із тестовим кодом:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

Ось і все! Ми створили повністю працездатне нативне розширення.


## Життєвий цикл розширення {#extension-lifecycle}

Як ми бачили вище, макрос `DM_DECLARE_EXTENSION` використовується для оголошення різних точок входу в код розширення:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

Точки входу дають змогу виконувати код на різних етапах життєвого циклу розширення:

* Запуск рушія
  * Запускаються системи рушія
  * `app_init` розширення
  * `init` розширення — усі API Defold уже ініціалізовано. Це рекомендований етап життєвого циклу розширення для створення прив’язок Lua до коду розширення.
  * Ініціалізація скриптів — викликається функція `init()` файлів скриптів.
* Цикл рушія
  * Оновлення рушія
    * `update` розширення
    * Оновлення скриптів — викликається функція `update()` файлів скриптів.
  * Події рушія (згортання та розгортання вікна тощо)
    * `on_event` розширення
* Завершення роботи рушія (або перезапуск)
  * Завершення роботи скриптів — викликається функція `final()` файлів скриптів.
  * `final` розширення
  * `app_final` розширення

## Визначені ідентифікатори платформ {#defined-platform-identifiers}

Засіб збирання визначає такі ідентифікатори на відповідних платформах:

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Журнали сервера збирання {#build-server-logs}

Журнали сервера збирання доступні, коли проєкт використовує нативні розширення. Під час збирання проєкту журнал сервера збирання (`log.txt`) завантажується разом із власною версією рушія та зберігається у файлі `.internal/%platform%/build.zip`, а також розпаковується до папки збирання вашого проєкту.

## Приклади розширень {#example-extensions}

* [Базовий приклад розширення](https://github.com/defold/template-native-extension) (розширення з цього посібника)
* [Приклад розширення для Android](https://github.com/defold/extension-android)
* [Приклад розширення для HTML5](https://github.com/defold/extension-html5)
* [Розширення відеопрогравача для macOS, iOS та Android](https://github.com/defold/extension-videoplayer)
* [Розширення камери для macOS та iOS](https://github.com/defold/extension-camera)
* [Розширення покупок у застосунку для iOS та Android](https://github.com/defold/extension-iap)
* [Розширення Firebase Analytics для iOS та Android](https://github.com/defold/extension-firebase-analytics)

[Портал ресурсів Defold](https://www.defold.com/assets/) також містить кілька нативних розширень.
