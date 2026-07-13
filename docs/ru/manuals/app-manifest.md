---
title: App Manifest
brief: В этом руководстве описано, как использовать app manifest для исключения возможностей из движка.
---

# App Manifest

Манифест приложения определяет, какие функции и бэкенды компонуются с движком. Неиспользуемые функции рекомендуется исключать, поскольку это уменьшает итоговый размер бинарного файла игры. Манифест приложения также содержит параметры времени сборки, например минимальные поддерживаемые версии браузеров HTML5 и настройки памяти WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Применение манифеста

В `game.project` назначьте манифест в разделе `Native Extensions` -> `App Manifest`.

## Physics 2D

Выберите реализацию Box2D, которую нужно включить:

* **Box2D Version 3** — включить Box2D 3. Эта реализация включается явно и может давать иные результаты симуляции по сравнению с прежней, поэтому в существующих проектах может потребоваться перенастроить параметры физики.
* **Box2D (Legacy Defold version)** — включить прежнюю реализацию Box2D в Defold. Используется по умолчанию.
* **None** — исключить 2D-физику.

Параметры решателя Box2D зависят от версии. Подробнее см. в [настройках проекта Box2D](/manuals/project-settings/#box2d).

## Physics 3D

Включает реализацию 3D-физики Bullet. Она включена по умолчанию; отключите этот параметр, чтобы исключить 3D-физику.

## Rig + Model

Позволяет управлять функциональностью rig и model, либо выбрать None, чтобы полностью исключить модели и риги. См. [документацию по `Model`](https://defold.com/manuals/model/#model-component).

## Exclude Record

Исключает из движка возможность записи видео. См. документацию по сообщению [`start_record`](https://defold.com/ref/stable/sys/#start_record).

## Profiler

Определяет, когда функциональность профайлера компонуется с движком:

* **Debug Only** — включать профайлер только в отладочные сборки. Значение по умолчанию.
* **None** — исключить функциональность профайлера из всех вариантов сборки.
* **Always** — включать профайлер как в отладочные, так и в релизные сборки.

Параметр манифеста приложения определяет, будет ли код профайлера скомпонован со сборкой. Параметры раздела `profiler` в *game.project* управляют поведением профайлера во время выполнения. Доступные возможности описаны в [руководстве по профилированию](/manuals/profiling/).

## Sound

Параметры звука определяют, какая звуковая система и какие декодеры компонуются с движком.

### Exclude Sound

Исключает из движка всю функциональность воспроизведения звука.

### Exclude Sound Decoder: WAV

Исключает поддержку звуковых ресурсов WAV.

### Exclude Sound Decoder: OGG

Исключает поддержку звуковых ресурсов Ogg Vorbis.

### Include Sound Decoder: Opus

Включает поддержку звуковых ресурсов Ogg Opus. Декодер Opus по умолчанию исключён, поэтому перед воспроизведением ресурсов `.opus` этот параметр необходимо включить. Поддерживаемые форматы перечислены в [руководстве по звуку](/manuals/sound/).

## Exclude Input

Исключает из движка всю обработку ввода.

## Exclude Live Update

Исключает из движка [функциональность Live Update](/manuals/live-update).

## Exclude Image

Исключает из движка скриптовый модуль `image`: [документация](https://defold.com/ref/stable/image/).

## Exclude Types

Исключает из движка скриптовый модуль `types`: [документация](https://defold.com/ref/stable/types/).

## Exclude Basis Transcoder

Исключает из движка библиотеку сжатия текстур Basis Universal. Подробнее см. в [руководстве по профилям текстур](/manuals/texture-profiles).

## Use Android Support Lib

Использует устаревшую Android Support Library вместо Android X. [Подробнее](https://defold.com/manuals/android/#using-androidx).

## Graphics

Позволяет выбрать графические бэкенды, включаемые для каждой платформы. Комбинированный вариант включает оба бэкенда, чтобы при недоступности предпочтительного можно было использовать резервный.

| Поле | Платформы | Варианты | По умолчанию |
|---|---|---|---|
| **Graphics** | Windows и Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

В Linux ARM64 вариант **OpenGL** использует backend OpenGL ES. Комбинированный вариант Android по умолчанию предпочитает Vulkan, а если он недоступен, переходит на OpenGL ES.

## Use full text layout system

Если включено (`true`), это позволит использовать генерацию во время выполнения для шрифтов типа SDF при использовании в проекте шрифтов True Type (`.ttf`). Подробнее см. в [руководстве по шрифтам](https://defold.com/manuals/font/#enabling-runtime-fonts).

## Минимальные версии браузеров

Поля YAML **`minSafariVersion`**, **`minFirefoxVersion`** и **`minChromeVersion`** задают минимальные версии браузеров, на которые ориентируется Emscripten. Текущие значения по умолчанию и минимальные поддерживаемые версии различаются для однопоточной и многопоточной целей:

| Цель | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Указывайте переопределения в контексте соответствующей цели. Для многопоточной цели также действуют дополнительные [требования к хостингу](/manuals/html5/#creating-html5-bundle). См. справочник параметров Emscripten: [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) и [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Initial memory (HTML5)

Имя поля в YAML: **`initialMemory`**
Значение по умолчанию: **33554432**

Начальный объём памяти, выделяемой веб-приложению, в байтах. Значение должно быть кратно размеру страницы WebAssembly (64 КиБ). См. параметр Emscripten [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory).

Этот параметр задаёт значение по умолчанию во время компиляции. Значение [`html5.heap_size`](/manuals/html5/#heap-size) в *game.project* переопределяет его во время выполнения.

## Stack size (HTML5)

Имя поля в YAML: **`stackSize`**
Значение по умолчанию: **5242880**

Размер стека приложения в байтах. См. параметр Emscripten [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size).
