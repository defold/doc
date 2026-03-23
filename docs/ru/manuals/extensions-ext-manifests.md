---
title: Native extensions - manifests расширений
brief: В этом руководстве описывается manifest расширения и то, как он соотносится с manifest приложения и manifest движка.
---

# Файлы manifest расширения, приложения и движка

Manifest расширения — это конфигурационный файл с флагами и defines, используемыми при сборке одного расширения. Эта конфигурация объединяется с конфигурацией уровня приложения и базовой конфигурацией самого движка Defold.

## App Manifest

Manifest приложения (файл с расширением `.appmanifest`) — это конфигурация уровня приложения, описывающая, как собирать вашу игру на build-серверах. Manifest приложения позволяет удалять части движка, которые вы не используете. Если вам не нужен физический движок, его можно исключить из исполняемого файла, чтобы уменьшить размер. Узнайте, как исключать неиспользуемые возможности, [в руководстве по application manifest](/manuals/app-manifest).

## Engine manifest

У движка Defold есть manifest сборки (`build.yml`), который включен в каждый релиз движка и Defold SDK. Этот manifest управляет тем, какие версии SDK использовать, какие компиляторы, линкеры и другие инструменты запускать, а также какие build- и link-флаги по умолчанию передавать этим инструментам. Этот manifest можно найти в share/extender/build_input.yml [на GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Extension Manifest

Manifest расширения (`ext.manifest`), в свою очередь, представляет собой конфигурационный файл, относящийся непосредственно к расширению. Manifest расширения управляет тем, как компилируется и линкуется исходный код расширения, а также какие дополнительные библиотеки должны быть подключены.

Все три manifest-файла используют один и тот же синтаксис, чтобы их можно было объединять и полностью управлять тем, как собираются расширения и сама игра.

Для каждого расширения, которое собирается, manifests объединяются следующим образом:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Это позволяет пользователю переопределять поведение по умолчанию как у движка, так и у каждого расширения. А для финального этапа линковки app manifest объединяется с manifest Defold:

	manifest = merge(game.appmanifest, build.yml)


### Файл ext.manifest

Помимо имени расширения, manifest-файл может содержать платформо-зависимые compile flags, link flags, библиотеки и frameworks. Если файл *ext.manifest* не содержит секцию "platforms" или в списке отсутствует какая-то платформа, сборка для этой платформы все равно пройдет, но без каких-либо дополнительных флагов.

Пример:

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

#### Допустимые ключи

Допустимые ключи для платформо-зависимых compile flags:

* `frameworks` - Apple frameworks, которые нужно включить при сборке (iOS и macOS)
* `weakFrameworks` - Apple frameworks, которые при сборке нужно подключать опционально (iOS и macOS)
* `flags` - флаги, которые должны быть переданы компилятору
* `linkFlags` - флаги, которые должны быть переданы линкеру
* `libs` - дополнительные библиотеки, которые нужно подключить при линковке
* `defines` - defines, которые нужно установить при сборке
* `aaptExtraPackages` - имя дополнительного package, который должен быть сгенерирован (Android)
* `aaptExcludePackages` - regexp (или точные имена) пакетов, которые нужно исключить (Android)
* `aaptExcludeResourceDirs` - regexp (или точные имена) директорий ресурсов, которые нужно исключить (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - эти флаги используются для удаления сущностей, ранее определенных в platform context.

Для всех ключевых слов применяется white list-фильтр. Это сделано для того, чтобы избежать некорректной работы с путями и обращения к файлам вне папки, загружаемой для сборки.
