---
title: Нативні розширення — маніфести розширень
brief: У цьому посібнику описано маніфест розширення та його зв’язок із маніфестом застосунку й маніфестом рушія.
---

# Файли маніфестів розширення, застосунку та рушія {#extension-application-and-engine-manifest-files}

Маніфест розширення — це файл конфігурації з прапорцями та визначеннями препроцесора, які використовуються під час збирання окремого розширення. Ця конфігурація об’єднується з конфігурацією рівня застосунку та базовою конфігурацією самого рушія Defold.

## Маніфест застосунку {#app-manifest}

Маніфест застосунку (файл із розширенням `.appmanifest`) — це конфігурація рівня застосунку, яка визначає, як збирати вашу гру на серверах збирання. Маніфест застосунку дає змогу вилучити частини рушія, які ви не використовуєте. Якщо вам не потрібен фізичний рушій, його можна вилучити з виконуваного файлу, щоб зменшити розмір цього файлу. Дізнайтеся, як вилучити невикористовувані можливості, [у посібнику з маніфесту застосунку](/manuals/app-manifest).

## Маніфест рушія {#engine-manifest}

Рушій Defold має маніфест збирання (`build.yml`), який входить до кожного випуску рушія та Defold SDK. Маніфест визначає, які версії SDK використовувати, які компілятори, компонувальники та інші інструменти запускати, а також які типові прапорці збирання й компонування передавати цим інструментам. Маніфест можна знайти у файлі share/extender/build_input.yml [на GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Маніфест розширення {#extension-manifest}

Маніфест розширення (`ext.manifest`), своєю чергою, є файлом конфігурації саме для розширення. Маніфест розширення визначає, як компілюється та компонується вихідний код розширення і які додаткові бібліотеки слід включити.

Усі три файли маніфестів мають однаковий синтаксис, тож їх можна об’єднувати й повністю керувати збиранням розширень і гри.

Для кожного розширення, що збирається, маніфести об’єднуються так:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Це дає користувачеві змогу перевизначити типову поведінку рушія, а також кожного розширення. Для завершального етапу компонування ми об’єднуємо маніфест застосунку з маніфестом Defold:

	manifest = merge(game.appmanifest, build.yml)


### Файл ext.manifest {#the-extmanifest-file}

Окрім назви розширення, файл маніфесту може містити прапорці компіляції, прапорці компонування, бібліотеки та фреймворки для окремих платформ. Якщо файл *ext.manifest* не містить розділу "platforms" або певної платформи немає у списку, збирання для платформи, для якої ви створюєте пакет, усе одно відбудеться, але без додаткових прапорців.

Ось приклад:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Дозволені ключі {#allowed-keys}

Дозволені ключі для прапорців компіляції окремих платформ:

* `frameworks` — фреймворки Apple, які слід включити під час збирання (iOS і macOS)
* `weakFrameworks` — фреймворки Apple для необов’язкового включення під час збирання (iOS і macOS)
* `flags` — прапорці, які слід передати компілятору
* `linkFlags` — прапорці, які слід передати компонувальнику
* `libs` — додаткові бібліотеки, які слід включити під час компонування
* `defines` — визначення препроцесора, які слід задати під час збирання
* `aaptExtraPackages` — назва додаткового пакета, який слід згенерувати (Android)
* `aaptExcludePackages` — регулярний вираз (або точні назви) для пакетів, які слід вилучити (Android)
* `aaptExcludeResourceDirs` — регулярний вираз (або точні назви) для каталогів ресурсів, які слід вилучити (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` — ці прапорці використовуються для вилучення елементів, раніше визначених у контексті платформи.

Для всіх ключових слів ми застосовуємо фільтрацію за списком дозволених значень. Це запобігає неприпустимій обробці шляхів і доступу до файлів поза папкою, завантаженою для збирання.
