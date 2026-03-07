---
title: Разработка на Defold для платформы macOS
brief: В этом руководстве описывается, как собирать и запускать приложения Defold на macOS
---

# Разработка для macOS

Разработка приложений Defold для платформы macOS представляет собой довольно простой процесс, требующий лишь небольшого количества дополнительных действий.

## Настройки проекта

Специфичная для macOS конфигурация приложения настраивается в [разделе macOS](/manuals/project-settings/#macos) файла настроек *game.project*.

## Иконка приложения

Иконка приложения для игры на macOS должна быть в формате `.icns`. Вы можете легко создать файл `.icns` из набора файлов `.png`, собранных в `.iconset`. Следуйте [официальной инструкции по созданию файла `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Кратко процесс выглядит так:

* Создайте папку для иконок, например `game.iconset`
* Скопируйте файлы иконок в созданную папку:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Преобразуйте папку `.iconset` в файл `.icns` с помощью инструмента командной строки `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Публикация приложения

Вы можете публиковать приложение в Mac App Store, через сторонний магазин или портал, такой как Steam или itch.io, либо самостоятельно через веб-сайт. Перед публикацией приложение нужно подготовить к отправке. Следующие шаги обязательны вне зависимости от того, как вы собираетесь распространять приложение:

* 1) Убедитесь, что любой пользователь сможет запустить игру, добавив права на выполнение файла (по умолчанию право выполнения есть только у владельца файла):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* 2) Создайте файл entitlements, указывающий разрешения, необходимые вашей игре. Для большинства игр достаточно следующих разрешений:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - указывает, может ли приложение создавать память с правами на запись и выполнение с использованием флага `MAP_JIT`
  * `com.apple.security.cs.allow-unsigned-executable-memory` - указывает, может ли приложение создавать память с правами на запись и выполнение без ограничений, накладываемых использованием флага `MAP_JIT`
  * `com.apple.security.cs.allow-dyld-environment-variables` - указывает, может ли на приложение влиять набор переменных окружения динамического линковщика, которые можно использовать для внедрения кода в процесс приложения

Некоторым приложениям могут потребоваться дополнительные entitlements. Расширению Steamworks нужен следующий дополнительный entitlement:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - указывает, может ли приложение загружать произвольные плагины или фреймворки без обязательной проверки подписи кода.

Полный список entitlements, которые могут быть выданы приложению, приведён в официальной [документации Apple для разработчиков](https://developer.apple.com/documentation/bundleresources/entitlements).

* 3) Подпишите игру с помощью `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Публикация вне Mac App Store

Apple требует, чтобы всё ПО, распространяемое вне Mac App Store, было нотариально заверено Apple, чтобы оно запускалось по умолчанию на macOS Catalina. Обратитесь к [официальной документации](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow), чтобы узнать, как добавить нотариальное заверение в автоматизированную среду сборки вне Xcode. Кратко процесс выглядит так:

* 1) Выполните описанные выше шаги по добавлению разрешений и подписи приложения.

* 2) Заархивируйте и отправьте игру на нотариальное заверение с помощью `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

* 3) Проверьте статус отправки, используя возвращённый request UUID из вызова `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

* 4) Дождитесь, пока статус не станет `success`, и прикрепите тикет нотариального заверения к игре:

```
$ xcrun stapler staple "Game.app"
```

* 5) Теперь игра готова к распространению.

## Публикация в Mac App Store

Процесс публикации в Mac App Store хорошо описан в [документации Apple Developer](https://developer.apple.com/macos/submit/). Перед отправкой обязательно добавьте разрешения и подпишите приложение, как описано выше.

Примечание: при публикации в Mac App Store игру не нужно нотариально заверять.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
