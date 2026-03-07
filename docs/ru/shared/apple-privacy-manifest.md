
## Apple Privacy Manifest

Privacy manifest — это список свойств, в котором фиксируются типы данных, собираемых вашим приложением или сторонним SDK, а также причины использования required reasons API вашим приложением или сторонним SDK. Для каждого типа данных, который собирает приложение или сторонний SDK, и для каждой категории required reasons API, которую оно использует, причины должны быть указаны в bundled privacy manifest file.

Defold предоставляет privacy manifest по умолчанию через поле Privacy Manifest в файле *game.project*. При создании application bundle privacy manifest будет объединён с любыми privacy manifests из зависимостей проекта и включён в application bundle.

Подробнее о privacy manifests читайте в [официальной документации Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).
