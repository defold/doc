---
title: Использование зависимостей CocoaPods в сборках для iOS и macOS
brief: В этом руководстве объясняется, как использовать CocoaPods для разрешения зависимостей в сборках для iOS и macOS.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) — это менеджер зависимостей для Cocoa-проектов на Swift и Objective-C. Обычно CocoaPods используется для управления и интеграции зависимостей в проектах Xcode. Defold не использует Xcode при сборке под iOS и macOS, но по-прежнему использует CocoaPods на сервере сборки для разрешения зависимостей.


## Разрешение зависимостей

Нативные расширения могут включать файл `Podfile` в каталогах `manifests/ios` и `manifests/osx`, чтобы указать зависимости расширения. Пример:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Сервер сборки соберет файлы `Podfile` из всех расширений, использует их для разрешения всех зависимостей и включит их при сборке нативного кода.

Примеры:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
