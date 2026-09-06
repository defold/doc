---
title: Маніфест застосунку
brief: У цьому посібнику описано, як за допомогою маніфеста застосунку виключати функції з рушія.
---

# Маніфест застосунку {#app-manifest}

Маніфест застосунку визначає, які функції та бекенди компонуються з рушієм. Невикористовувані функції рекомендовано виключати, оскільки це зменшує кінцевий розмір двійкового файлу гри. Маніфест застосунку також містить параметри збирання, як-от мінімальні підтримувані версії браузерів для HTML5 і налаштування пам’яті WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Застосування маніфеста {#applying-the-manifest}

У `game.project` призначте маніфест у `Native Extensions` -> `App Manifest`.

## Двовимірна фізика (Physics 2D) {#physics-2d}

Виберіть реалізацію Box2D, яку потрібно включити:

* **Box2D Version 3** — включити Box2D 3. Цю реалізацію потрібно вибрати явно; вона може давати інші результати симуляції, ніж попередня, тому в наявних проєктах може знадобитися повторне налаштування фізики.
* **Box2D (Legacy Defold version)** — включити попередню реалізацію Box2D у Defold. Використовується за замовчуванням.
* **None** — виключити двовимірну фізику.

Налаштування розв’язувача Box2D залежать від версії. Докладніше див. у [налаштуваннях проєкту для Box2D](/manuals/project-settings/#box2d).

## Тривимірна фізика (Physics 3D) {#physics-3d}

Включіть реалізацію тривимірної фізики Bullet. Її включено за замовчуванням; вимкніть цей параметр, щоб виключити тривимірну фізику.

## Риги й моделі (Rig + Model) {#rig-model}

Керуйте функціональністю ригів (rig) і моделей або виберіть None, щоб повністю виключити моделі й риги. (Див. документацію [`Model`](https://defold.com/manuals/model/#model-component)).


## Виключення запису відео (Exclude Record) {#exclude-record}

Виключіть із рушія можливість запису відео (див. документацію повідомлення [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Профайлер (Profiler) {#profiler}

Визначте, коли функціональність профайлера компонується з рушієм:

* **Debug Only** — включати профайлер лише до налагоджувальних збірок. Використовується за замовчуванням.
* **None** — виключити функціональність профайлера з усіх варіантів збірки.
* **Always** — включати профайлер до налагоджувальних збірок і збірок випуску.

Параметр маніфеста застосунку визначає, чи буде код профайлера включено до збірки під час компонування. Налаштування розділу `profiler` у *game.project* керують поведінкою профайлера під час виконання. Про використання доступних засобів читайте в [посібнику з профілювання](/manuals/profiling/).


## Звук (Sound) {#sound}

Налаштування звуку визначають, яка звукова система та які декодери компонуються з рушієм.

### Виключення звуку (Exclude Sound) {#exclude-sound}

Виключіть із рушія всі можливості відтворення звуку.

### Виключення декодера звуку WAV (Exclude Sound Decoder: WAV) {#exclude-sound-decoder-wav}

Виключіть підтримку звукових ресурсів WAV.

### Виключення декодера звуку OGG (Exclude Sound Decoder: OGG) {#exclude-sound-decoder-ogg}

Виключіть підтримку звукових ресурсів Ogg Vorbis.

### Включення декодера звуку Opus (Include Sound Decoder: Opus) {#include-sound-decoder-opus}

Включіть підтримку звукових ресурсів Ogg Opus. Декодер Opus за замовчуванням виключено, тому перед відтворенням ресурсів `.opus` потрібно ввімкнути цей параметр. Підтримувані формати наведено в [посібнику зі звуку](/manuals/sound/).


## Виключення введення (Exclude Input) {#exclude-input}

Виключіть із рушія всю обробку введення.


## Виключення Live Update (Exclude Live Update) {#exclude-live-update}

Виключіть із рушія [функціональність Live Update](/manuals/live-update).


## Виключення модуля image (Exclude Image) {#exclude-image}

Виключіть із рушія модуль скриптів `image` ([посилання](https://defold.com/ref/stable/image/)).


## Виключення модуля types (Exclude Types) {#exclude-types}

Виключіть із рушія модуль скриптів `types` ([посилання](https://defold.com/ref/stable/types/)).


## Виключення транскодера Basis (Exclude Basis Transcoder) {#exclude-basis-transcoder}

Виключіть із рушія [бібліотеку стиснення текстур](/manuals/texture-profiles) Basis Universal.


## Використання Android Support Library (Use Android Support Lib) {#use-android-support-lib}

Використовуйте застарілу Android Support Library замість Android X. [Докладніше](https://defold.com/manuals/android/#using-androidx).


## Графіка (Graphics) {#graphics}

Виберіть графічні бекенди, які потрібно включити для кожної платформи. Комбінований варіант включає обидва бекенди, щоб за недоступності пріоритетного можна було перейти на резервний.

| Поле | Платформи | Варіанти | За замовчуванням |
|---|---|---|---|
| **Graphics** | Windows і Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

У Linux ARM64 варіант **OpenGL** використовує бекенд OpenGL ES. Комбінований варіант для Android за замовчуванням використовує Vulkan, якщо він доступний, і переходить на OpenGL ES, якщо ні.

## Використання повної системи компонування тексту (Use full text layout system) {#use-full-text-layout-system}

Якщо ввімкнено (`true`), можна генерувати шрифти типу SDF під час виконання, коли в проєкті використовуються шрифти True Type (`.ttf`). Докладніше читайте в [посібнику зі шрифтів](https://defold.com/manuals/font/#enabling-runtime-fonts).


## Мінімальні версії браузерів {#minimum-browser-versions}

Поля YAML **`minSafariVersion`**, **`minFirefoxVersion`** і **`minChromeVersion`** задають мінімальні версії браузерів, на які орієнтується Emscripten. Поточні значення за замовчуванням і мінімальні підтримувані версії відрізняються для цілей без підтримки потоків і з підтримкою потоків:

| Ціль | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Задавайте перевизначення в контексті відповідної цілі. Для цілі з підтримкою потоків також діють додаткові [вимоги до хостингу](/manuals/html5/#creating-html5-bundle). Див. довідник налаштувань Emscripten для [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) і [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Початковий обсяг пам’яті (HTML5) {#initial-memory-html5}
Назва поля YAML: **`initialMemory`**
Значення за замовчуванням: **33554432**

Початковий обсяг пам’яті, виділеної для вебзастосунку, у байтах. Значення має бути кратним розміру сторінки WebAssembly (64 КіБ). Див. налаштування Emscripten [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory).

Цей параметр задає значення за замовчуванням під час компіляції. Значення [`html5.heap_size`](/manuals/html5/#heap-size) у *game.project* перевизначає його під час виконання.

## Розмір стека (HTML5) {#stack-size-html5}
Назва поля YAML: **`stackSize`**
Значення за замовчуванням: **5242880**

Розмір стека застосунку в байтах. Див. налаштування Emscripten [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size).
