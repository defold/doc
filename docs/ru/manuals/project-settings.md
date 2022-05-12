---
title: Настройки проекта
brief: Данное руководство описывает настройки, специфичные для проекта Defold.
---

# Настройки проекта

Файл *game.project* содержит все настройки проекта. Он должен находиться в корневой папке проекта и называться *game.project*. Первое, что делает движок при старте и запуске игры, это ищет данный файл.

Каждая настройка в файле относится к определенной категории. При открытии файла Defold представляет все настройки, сгруппированные по категориям.

![Project settings](images/project-settings/settings.jpg)

Ниже приведены все доступные настройки, упорядоченные по секциям. Некоторые параметры на данный момент не отображаются в редакторе настроек (они помечены ниже как "скрытые настройки"), но их можно настроить вручную, кликнув правой кнопкой мыши на "game.project" и выбрав <kbd>Open With ▸ Text Editor</kbd>.

## Project

#### Title
Название приложения.

#### Version
Версия приложения.

#### Write Log
Если опция отмечена, движок будет записывать файл журнала *log.txt* в корень проекта. При запуске на iOS доступ к файлу журнала можно получить через iTunes, вкладка *Apps* раздел *File Sharing*. На Android файл хранится во внешнем хранилище приложения. При запуске приложения разработки *dmengine* журнал можно просмотреть с помощью:

```bash
$ adb shell cat /mnt/sdcard/Android/data/com.defold.dmengine/files/log.txt
```

#### Compress Archive
Включает сжатие архивов при упаковке в бандл. Стоит отметить, что в настоящее время это относится ко всем платформам, кроме Android, где apk содержит все данные в уже сжатом виде.

#### Dependencies
Список URL на *Library URL* проекта. За подробностями обращайтесь к [руководству по библиотекам](/manuals/libraries/).

#### Custom Resources
Список ресурсов, разделенных запятыми, которые будут включены в проект. Если указаны каталоги, рекурсивно включаются все файлы и каталоги в этом каталоге. Ресурсы могут быть загружены с помощью [`sys.load_resource()`](/ref/sys/#sys.load_resource).

#### Bundle Resources
Список директорий, разделенных запятыми и содержащих файлы ресурсов и директории, которые должны быть скопированы как есть в результирующий бандл. Директории должны быть указаны с абсолютным путем от корня проекта, например `/res`. Директория ресурсов должна содержать вложенные папки с именами `platform` или `architecure-platform`.

  Поддерживаемые платформы: `ios`, `android`, `osx`, `win32`, `linux`, `web`.

  Также допускается наличие подпапки с именем `common`, содержащей файлы ресурсов, общие для всех платформ.

#### Bundle Exclude Resources
Список ресурсов, разделенных запятыми, которые не должны быть включены в бандл.

## Bootstrap

#### Main Collection
Ссылка на файл коллекции, используемой для запуска приложения, по умолчанию `/logic/main.collection`.

#### Render
Файл, используемый для настройки и определения пайплайна рендеринга, по умолчанию `/builtins/render/default.render`.

## Library

#### Include Dirs
Список директорий, разделенных пробелами, которые должны быть доступны из проекта через общий доступ к библиотеке.

## Script

#### Shared State
Если опция отмечена, скрипты всех типов будут выполнятся в едином Lua-контексте. По умолчанию опция отключена.

## Engine

#### Run While Iconified
Позволяет движку продолжать выполнение, пока окно приложения свернуто (только для настольных платформ), по умолчанию опция отключена (`false`).

## Display

#### Width
Ширина окна приложения в пикселях, по умолчанию `960`.

#### Height
Высота окна приложения в пикселях, по умолчанию `640`.

#### High Dpi
Создает вторичный буфер высокого разрешения (high dpi back buffer) для мониторов с его поддержкой. При этом, игра будет рендериться в двойном разрешении по сравнению с тем, что установлено в настройках *Width* и *Height* и которое по прежнему будет логическим разрешением, используемым в скриптах и свойствах.

#### Samples
Количество сэмплов, используемых при избыточной выборке сглаживания (SSAA). Задает для окна инструкцию GLFW_FSAA_SAMPLES. По умолчанию `0`, что означает, что сглаживание отключено.

#### Fullscreen
Если опция отмечена, приложение будет запускаться в полноэкранном режиме, иначе --- в оконном.

#### Frame Cap
If `Vsync` checked, snaps to the closest matching swap interval for the set frame cap if a monitor is detected. Otherwise uses timers to respect the set value, 0 means no cap. This setting maps to `display.update_frequency`.

#### Vsync
Vertical sync, rely on hardware vsync for frame timing. Can be overridden depending on graphics driver and platform specifics.

#### Display Profiles
Используемый файл профилей отображения, по умолчанию `/builtins/render/default.display_profilesc`. За подробностями обращайтесь к [руководству по GUI-компоновкам](/manuals/gui-layouts/#creating-display-profiles).

#### Dynamic Orientation
Если опция отмечена, приложение будет динамически переключаться между книжной и альбомной ориентациями при повороте устройства. Следует отметить, что в настоящее время в приложении для разработчиков данная настройка не предусмотрена.

## Render

#### Clear Color Red
Clear color red channel, используется рендер скриптом и при создании окна. Добавлено в 1.2.167.

#### Clear Color Green
Clear color green channel, используется рендер скриптом и при создании окна. Добавлено в 1.2.167.

#### Clear Color Blue
Clear color blue channel, используется рендер скриптом и при создании окна. Добавлено в 1.2.167.

#### Clear Color Alpha
Clear color alpha channel, используется рендер скриптом и при создании окна. Добавлено в 1.2.167.

## Physics

#### Type
Используемый тип физики, `2D` (по умолчанию) или `3D`.

#### Gravity Y
Мировая гравитация по оси Y. По умолчанию`-10`, что соответствует естественному значению.

#### Debug
Если опция отмечена, физика будет визуализироваться в целях отладки.

#### Debug Alpha
Значение компонента альфа для визуализируемой физики, `0`--`1`. По умолчанию `0.9`.

#### World Count
Максимальное количество одновременных физических пространств, по умолчанию `4`. Если загружать более 4 пространств одновременно через прокси коллекции, необходимо увеличить это значение. Следует помнить, что для каждого физического пространства выделяется значительный объем памяти.

#### Gravity X
Мировая гравитация по оси X. По умолчанию `0`.

#### Gravity Z
Мировая гравитация по оси Z. По умолчанию `0`.

#### Scale
Указывает физическому движку, как масштабировать физические пространства по отношению к игровому миру для числовой точности, `0.01`--`1.0`. Если значение установлено в `0.02`, это означает, что физический движок будет воспринимать 50 единиц как 1 метр ($1 / 0.02$). По умолчанию используется значение `1.0`.

#### Allow Dynamic Transforms
Если опция отмечена, физический движок будет масштабировать объекты столкновения, используя масштаб игровых объектов, к которым они относятся. По умолчанию `true`.

#### Debug Scale
Указывает, насколько большими рисовать отдельные объекты в физике, такие как триады и нормали. По умолчанию `30`.

#### Max Collisions
Количество коллизий, о которых будет сообщено скриптам, по умолчанию `64`.

#### Max Contacts
Количество точек контакта, о которых будет сообщено скриптам, по умолчанию `128`.

#### Contact Impulse Limit
Игнорировать импульсы контактов со значениями меньше этого, по умолчанию `0.0`.

#### Ray Cast Limit 2d
Максимальное количество запросов 2d-рейкастинга в кадре. По умолчанию `64`.

#### Ray Cast Limit 3d
Максимальное количество запросов 3d-рейкастинга в кадре. По умолчанию `128`.

#### Trigger Overlap Capacity
Максимальное количество накладывающихся (overlapping) физических триггеров. По умолчанию `16`.

## Graphics

#### Default Texture Min Filter
Указывает, какую фильтрацию использовать при уменьшающей фильтрации, `linear` (по умолчанию) или `nearest`.

#### Default Texture Mag Filter
Указывает, какую фильтрацию использовать при увеличивающей фильтрации, `linear` (по умолчанию) или `nearest`.

#### Max Draw Calls
Максимальное количество вызовов рендеринга, по умолчанию `1024`.

#### Max Characters:
Количество символов, предварительно распределенных в буфере рендеринга текста, то есть количество символов, которое может быть отображено в каждом кадре, по умолчанию `8192`.

#### Max Debug Vertices
Максимальное количество отладочных вершин. Используется, в частности, для физического рендеринга форм, по умолчанию `10000`.

#### Texture Profiles
Файл профилей текстур, используемый для данного проекта, по умолчанию `/builtins/graphics/default.texture_profiles`.

## Input

#### Repeat Delay
Секунды ожидания перед тем, как удерживаемый ввод начнет повторяться, по умолчанию `0.5`.

#### Repeat Interval
Секунды ожидания между каждым повторением удерживаемого ввода, по умолчанию `0.2`.

#### Gamepads
Ссылка на файл конфигурации геймпадов, который сопоставляет сигналы геймпадов с ОС. По умолчанию `/builtins/input/default.gamepads`.

#### Game Binding
Ссылка на файл конфигурации ввода, который сопоставляет аппаратный ввод с действиями. По умолчанию `/input/game.input_binding`.

#### Use Accelerometer
Если опция отмечена, движок будет получать ввод событий акселерометра каждый кадр. Отключение ввода акселерометра может дать некоторый выигрыш в производительности. По умолчанию опция включена.

## Resource

#### Http Cache
Если опция отмечена, будет включен кэш HTTP, что позволит запущенному на устройстве движку быстрее загружать ресурсы по сети. По умолчанию опция отключена.

#### Uri
Место поиска данных о сборке проекта, в формате URI.

#### Max Resources
Максимальное количество ресурсов, которые могут быть загружены одновременно, по умолчанию `1024`.

## Network

#### Http Timeout
Время ожидания (timeout) HTTP в секундах. По умолчанию `0`, что соответствует отключению таймаута.

## Collection

#### Max Instances
Максимальное количество экземпляров игровых объектов в коллекции, по умолчанию `1024`.

## Sound

#### Gain
Глобальное усиление (громкость), `0`--`1`, По умолчанию `1`.

#### Max Sound Data
Максимальное количество звуковых ресурсов, то есть количество уникальных звуковых файлов во время выполнения. По умолчанию `128`.

#### Max Sound Buffers
(В настоящее время не используется) Максимальное количество одновременно существующих буферов звука. По умолчанию `32`.

#### Max Sound Sources
(В настоящее время не используется) Максимальное количество одновременно воспроизводимых звуков. По умолчанию `16`.

#### Max Sound Instances
Максимальное количество одновременно существующих экземпляров звука, то есть фактических звуков, воспроизводимых в одно и то же время. По умолчанию `256`.

#### Use Thread
Если опция отмечена, звуковая система будет использовать потоки для воспроизведения звука, чтобы снизить риск запинания при высокой нагрузке на основной поток. По умолчанию включено.

## Sprite

#### Max Count
Максимальное количество спрайтов на коллекцию. По умолчанию `128`.

#### Subpixels
Если опция отмечены, спрайтам разрешается отображаться невыровненными по отношению к пикселям, по умолчанию опция отмечена.

## Tilemap

#### Max Count
Максимальное количество тайловых карт на коллекцию. По умолчанию `16`.

#### Max Tile Count
Максимальное количество одновременно видимых тайлов на коллекцию. По умолчанию `2048`.

## Spine

#### Max Count
Максимальное количество Spine-моделей. По умолчанию `128`.

## Mesh

#### Max Count
Максимальное количество компонентов Mesh на коллекцию. По умолчанию `128`.

## Model

#### Max Count
Максимальное количество компонентов Model на коллекцию. По умолчанию `128`.

## GUI

#### Max Count
Максимальное количество компонентов GUI. По умолчанию `64`.

#### Max Particlefx Count
Максимальное количество одновременно существующих. По умолчанию `64`.

#### Max Particle Count
Максимальное количество одновременно существующих частиц. По умолчанию `1024`.

## Label

#### Max Count
Максимальное компонентов Label. По умолчанию `64`.

#### Subpixels
Если опция отмечена, Label будут отображаться невыровненными по отношению к пикселям. По умолчанию включено.

## Particle FX

#### Max Count
Максимальное количество одновременно существующих эмиттеров. По умолчанию `64`.

#### Max Particle Count
Максимальное количество одновременно существующих частиц. По умолчанию `1024`.

## Collection proxy

#### Max Count
Максимальное количество прокси-коллекций. По умолчанию `8`.

## Collection factory

#### Max Count
Максимальное количество фабрик коллекций. По умолчанию `128`.

## Factory

#### Max Count
Максимальное количество фабрик игровых объектов. По умолчанию `128`.

## iOS

#### App Icon 57x57--180x180
Файл изображения (.png), используемый в качестве иконки приложения при заданных значениях ширины и высоты --- `W` &times; `H`.

#### Launch Screen
Файл раскадровки (.storyboard). О том, как его создать читайте в [руководстве по iOS](/manuals/ios/#creating-a-storyboard).

#### Pre Rendered Icons
(iOS 6 and earlier) Check if your icons are pre-rendered. If this is unchecked the icons will get a glossy highlight added automatically.

#### Bundle Identifier
Идентификатор бандла, позволяющий iOS распознавать любые обновления к вашему приложению. ID бандла должен быть зарегистрирован в Apple и быть уникальным для приложения. Невозможно использовать один и тот же идентификатор для iOS и macOS приложений.

#### Info.plist
Если задано, этот файл info.plist используется при сборке бандла приложения.

#### Custom Entitlements
If specified, the entitlements in the supplied provisioning profile (.entitlements, .xcent, .plist) will be merged with the entitlements from the provisioning profile supplied when bundling the application.

#### Override Entitlements
If checked the Custom Entitlements will replace the ones in the provisioning profile when bundling. Must be used in combination with the Custom Entitlements setting above.

#### Default Language
Язык, используемый приложением, если в списке `Localizations` отсутствует предпочитаемый пользователем язык (см. [CFBundleDevelopmentRegion](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Используйте двухбуквенный стандарт ISO 639-1, если предпочитаемый язык в нем доступен, или трехбуквенный ISO 639-2.

#### Localizations
Данное поле содержит разделенные запятыми строки, идентифицирующие названия языков или ISO-обозначения языков поддерживаемых локализаций (см. [CFBundleLocalizations](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

## Android

#### App Icon 36x36--192x192
Файл изображения (.png), используемый в качестве иконки приложения при заданных значениях ширины и высоты --- `W` &times; `H`.

#### Push Icon Small--LargeXxxhdpi
Файлы изображений (.png) для использования в качестве пользовательских иконок push-уведомлений на Android. Иконки будут автоматически использоваться как для локальных, так и для удаленных push-уведомлений. Если они не заданы, по умолчанию будет использоваться иконка приложения.

#### Push Field Title
Specifies which payload JSON field should be used as notification title. Leaving this setting empty makes the pushes default to the application name as title.

#### Push Field Text
Specifies which payload JSON field should be used as notification text. If left empty, the text in the field `alert` is used, just as on iOS.

#### Version Code
Целочисленное значение, указывающее на версию приложения. Увеличивайте для каждого последующего обновления.

#### Package
Идентификатор пакета.

#### Gcm Sender Id
Идентификатор отправителя Google Cloud Messaging. Задайте здесь строку, назначенную Google для включения push-уведомлений.

#### Manifest
Если задано, при упаковке бандла будет использоваться указанный XML-файл манифеста Android.

#### Iap Provider
Используемый магазин. Возможные варианты: `Amazon` и `GooglePlay`. По умолчанию используется `GooglePlay`.

#### Input Method
Метод получения ввода с клавиатуры на Android устройствах. Возможные варианты: `KeyEvent` (старый метод) и `HiddenInputField` (новый). По умолчанию `KeyEvent`.

#### Immersive Mode
Если опция отмечена, панель навигации и строка состояния скроются и приложение будет перехватывать все события касаний экрана.

#### Debuggable
Включает или отключает возможность отлаживать приложение с помощью таких инструментов, как [GAPID](https://github.com/google/gapid) или [Android Studio](https://developer.android.com/studio/profile/android-profiler). Опция устанавливает флаг `android:debuggable` в манифесте Android.

## macOS

#### App Icon
Файл изображения (.png), используемый в качестве иконки приложения на macOS.

#### Info.plist
Если задано, указанный файл info.plist будет использоваться при сборке бандла.

#### Bundle Identifier
Идентификатор бандла позволяет macOS распознавать обновления для вашего приложения. ID бандла должен быть зарегистрирован в Apple и быть уникальным для приложения. Невозможно использовать один и тот же идентификатор для приложений iOS и macOS.

#### Default Language
Язык, используемый приложением, если в списке `Localizations` отсутствует предпочитаемый пользователем язык (см. [CFBundleDevelopmentRegion](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Используйте двухбуквенный стандарт ISO 639-1, если предпочитаемый язык в нем доступен, или трехбуквенный ISO 639-2.

#### Localizations
Данное поле содержит разделенные запятыми строки, идентифицирующие названия языков или ISO-обозначения языков поддерживаемых локализаций (см. [CFBundleLocalizations](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

## Windows

#### App Icon
Файл изображения (.ico), используемый в качестве иконки приложения в Windows. О том, как создать файл .ico, читайте в [руководстве по Windows](/manuals/windows).

#### Iap Provider
Используемый магазин. Возможные варианты: `None` и `Gameroom`. По умолчанию `None`.

## HTML5

#### Heap Size
Размер кучи (количество мегабайт) для использования компилятором Emscripten. По умолчанию 256 МБ.

#### .html Shell
HTML файл-шаблон, используемый при сборке бандла. По умолчанию `/builtins/manifests/web/engine_template.html`.

#### Custom .css
CSS файл темы, используемый при сборке бандла. По умолчанию `/builtins/manifests/web/light_theme.css`.

#### Splash Image
Если опция отмечена, то при запуске при комплектации вместо логотипа Defold будет использоваться указанный сплешскрин.

#### Archive Location Prefix
При сборке бандла для HTML5 игровые данные разбиваются на один или несколько архивных файлов. Когда движок запускает игру, эти архивные файлы считываются в память. Данный параметр используется для указания расположения этих данных. По умолчанию `archive`.

#### Archive Location Suffix
Суффикс, который будет добавляться к архивным файлам. Полезно, например, для принудительного получения некэшированного содержимого из CDN (`?version2`, например).

#### Engine Arguments
Список аргументов, передаваемых движку.

#### Show Fullscreen Button
Включает кнопку Fullscreen в файле `index.html`. По умолчанию `true`.

#### Show Made With Defold
Включает ссылку Made With Defold в файле `index.html` file. По умолчанию `true`.

#### Scale Mode
Метод масштабирования игрового холста. По умолчанию `Downscale Fit`.

## IAP

#### Auto Finish Transactions
Если опция отмечена, IAP транзакции будут завершаться автоматически. В противном случае необходимо явно вызывать `iap.finish()` после успешной транзакции. По умолчанию опция включена.

## Live update

#### Private Key
If set, use the specified private key file when bundling live update content. If no key file is set, a key is generated.

#### Public Key
If set, use the specified public key file when bundling live update content. If no key file is set, a key is generated.

## Native extension

#### _App Manifest_
If set, use the app manifest to customize the engine build. This allows you to remove unneeded parts from the engine making it possible to decrease the final binary size. Note that this feature is in alpha state. Please visit [the forum](https://forum.defold.com/t/native-extensions/4946/142) for information on how to proceed.

## Profiler

#### Track Cpu
Если опция отмечена, профилирование CPU в релизных версиях сборок будет включено. Как правило, информация о профилировании доступна только в отладочных сборках.

## Формат файла

Формат файла настроек представляет собой простой текст (формат INI) и может быть отредактирован любым стандартным текстовым редактором. Формат выглядит следующим образом:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Наглядный пример:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

что означает, что настройка *main_collection* относится к категории *bootstrap*.
Во всех случаях, когда используется ссылка на файл, как в примере выше, путь должен быть дополнен символом 'c'. Это означает, что вы ссылаетесь на скомпилированную версию файла.
Также следует учитывать, что папка, содержащая файл *game.project*, будет корнем проекта, поэтому в пути установки присутствует начальный символ '/'.

## Установка конфигурационных значений при запуске движка

При запуске движка из командной строки можно указать конфигурационные значения, переопределяющие настройки *game.project*:

```bash
# Указать коллекцию начальной загрузки
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Установить два пользовательских конфигурационных значения
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=1234
```

Пользовательские значения, как и любое другое значение конфигурации, могут быть считаны с помощью [`sys.get_config()`](/ref/sys/#sys.get_config):

```lua
local my_value = tonumber(sys.get_config("test.my_value"))
```

## Vsync, frame cap, and swap interval
The first thing of note is that on desktop platforms vsync can be controlled globally by graphics card settings. If for example vsync is force-enabled in the graphics control panel it is not user controllable, e.g. the setting cannot be accessed or modified from Defold. Most mobile devices also has vsync enabled by default.

With `Vsync` checked in `game.project` the engine relies on hardware vsync and uses a fixed time step `dt` based on any detected monitor refresh rate. This is the default setting. With `Vsync` checked and `Frame cap` > 0, the rate will be clamped to a swap interval that matches any detected main monitor refresh rate. With `Vsync` unchecked and `Frame cap` 0, the time step is not fixed but instead uses actual elapsed time difference for `dt`. With `Vsync` unchecked and `Frame cap` > 0, timers are used to respect the set frame cap value. There is no guarantee that the frame cap will be achieved depending on platform specifics and hardware settings.

Swap interval is the interval with which to swap the front and back buffers in sync with vertical blanks (v-blank), the hardware event where the screen image is updated with data from the front buffer. A value of 1 swaps the buffers at every v-blank, a value of 2 swaps the buffers every other v-blank and so on. A value of 0 disables waiting for v-blank before swapping the buffers\*. Setting `swap_interval` is done by calling the [```set_vsync_swap_interval```](/ref/sys/#sys.set_vsync_swap_interval:swap_interval) function.

### Caveat
Currently, Defold queries for monitor refresh rate at init and uses that as a basis for picking a fixed `dt`. If you want to support monitors using variable refresh rate (GSync or FreeSync for example) or other scenarios where the refresh rate might not be trivial to query, uncheck `Vsync`to let the engine measure actual `dt` each frame instead of relying on a fixed time step.


### Vsync and frame cap in Defold

<table>
  <tr>
    <th></th>
    <th><b>Frame cap 0 (default)</b></th>
    <th><b>Frame cap > 0</b></th>
  </tr>
  <tr>
    <td><b>Vsync checked (default)</b></td>
    <td>Relies on hardware vsync. Fixed <code>dt</code> of <code>1/(detected monitor refresh rate)</code>.</td>
    <td>Fixed <code>dt</code> of <code>(swap interval)/(detected monitor refresh rate)</code> where swap interval is clamped to the closest matching monitor refresh rate frame cap multiple.</td>
  </tr>
  <tr>
    <td><b>Vsync unchecked</b></td>
    <td>Calculates <code>dt</code> each frame based on elapsed system time. Vsync might still be enabled in driver settings.</td>
    <td>Uses a fixed <code>dt</code> of <code>1 / (Frame cap)</code>. Uses timers and sleeps to respect the set frame cap.</td>
  </tr>
</table>
