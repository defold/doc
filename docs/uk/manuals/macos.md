---
title: Розробка в Defold для платформи macOS
brief: Цей посібник описує, як збирати й запускати застосунки Defold у macOS
---

# Розробка для macOS {#macos-development}

Розробка застосунків Defold для платформи macOS — простий процес, під час якого потрібно врахувати лише кілька особливостей.

## Налаштування проєкту {#project-settings}

Параметри застосунку, специфічні для macOS, задають у [розділі macOS](/manuals/project-settings/#macos) файлу налаштувань *game.project*.

## Піктограма застосунку {#application-icon}

Піктограма застосунку для гри на macOS має бути у форматі .`icns`. Ви можете легко створити файл `.icns` із набору файлів `.png`, зібраних у `.iconset`. Дотримуйтеся [офіційних інструкцій зі створення файлу `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Стислий опис потрібних кроків:

* Створіть папку для піктограм, наприклад `game.iconset`
* Скопіюйте файли піктограм у створену папку:

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

* Перетворіть папку `.iconset` на файл `.icns` за допомогою засобу командного рядка `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Публікація застосунку {#publishing-your-application}
Ви можете опублікувати застосунок у Mac App Store, у сторонньому магазині чи на порталі, наприклад Steam або itch.io, або самостійно через вебсайт. Перед публікацією застосунок потрібно підготувати до подання. Наведені нижче кроки обов’язкові незалежно від того, як ви плануєте розповсюджувати застосунок:

1. Додайте дозволи на виконання, щоб будь-хто міг запустити вашу гру (за замовчуванням дозвіл на виконання має лише власник файлу):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. Створіть файл дозволів (entitlements), у якому вкажіть дозволи, потрібні вашій грі. Для більшості ігор достатньо таких дозволів:

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

  * `com.apple.security.cs.allow-jit` — визначає, чи може застосунок створювати пам’ять із дозволами на запис і виконання, використовуючи прапорець MAP_JIT
  * `com.apple.security.cs.allow-unsigned-executable-memory` — визначає, чи може застосунок створювати пам’ять із дозволами на запис і виконання без обмежень, які накладає використання прапорця MAP_JIT
  * `com.apple.security.cs.allow-dyld-environment-variables` — визначає, чи можуть на застосунок впливати змінні середовища динамічного компонувальника, які можна використовувати для впровадження коду в процес застосунку

Деяким застосункам також можуть знадобитися додаткові дозволи. Розширенню Steamworks потрібен такий додатковий дозвіл:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

  * `com.apple.security.cs.disable-library-validation` — визначає, чи може застосунок завантажувати довільні плагіни або фреймворки без вимоги підписування коду.

Усі дозволи, які можна надати застосунку, перелічено в офіційній [документації Apple для розробників](https://developer.apple.com/documentation/bundleresources/entitlements).

3. Підпишіть гру за допомогою `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Публікація поза Mac App Store {#publishing-outside-the-mac-app-store}
Apple вимагає, щоб усе програмне забезпечення, яке розповсюджується поза Mac App Store, пройшло нотаризацію в Apple, щоб воно запускалося за замовчуванням у macOS Catalina. Зверніться до [офіційної документації](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow), щоб дізнатися, як додати нотаризацію до середовища збирання, автоматизованого за допомогою скриптів, поза Xcode. Стислий опис потрібних кроків:

1. Виконайте описані вище кроки з додавання дозволів і підписування застосунку.

2. Запакуйте гру в ZIP-архів і завантажте її для нотаризації за допомогою `altool`.

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

3. Перевірте статус подання, використовуючи UUID запиту, повернений викликом `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. Зачекайте, доки статус стане `success`, і прикріпіть квиток нотаризації до гри:

```
$ xcrun stapler staple "Game.app"
```

5. Тепер ваша гра готова до розповсюдження.

## Публікація в Mac App Store {#publishing-to-the-mac-app-store}
Процес публікації в Mac App Store докладно описано в [документації Apple для розробників](https://developer.apple.com/macos/submit/). Перед поданням обов’язково додайте дозволи й підпишіть застосунок за допомогою `codesign`, як описано вище.

Примітка: під час публікації в Mac App Store гра не потребує нотаризації.

:[Маніфест конфіденційності Apple](../shared/apple-privacy-manifest.md)
