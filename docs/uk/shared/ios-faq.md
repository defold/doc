#### П: Не вдається встановити гру Defold за допомогою безкоштовного облікового запису Apple Developer. {#q-i-am-unable-to-install-my-defold-game-using-a-free-apple-developer-account}
В: Переконайтеся, що ідентифікатор пакета у вашому проєкті Defold збігається з ідентифікатором у проєкті Xcode, який ви використовували для створення мобільного профілю підготовки.

#### П: Як перевірити права доступу пакета застосунку? {#q-how-can-i-check-the-entitlements-of-a-bundled-application}
В: Із розділу [«Перевірка прав доступу зібраного застосунку»](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

```sh
codesign -d --ent :- /path/to/the.app
```

#### П: Як перевірити права доступу профілю підготовки? {#q-how-can-i-check-the-entitlements-of-a-provisioning-profile}
В: Із розділу [«Перевірка прав доступу профілю»](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

```sh
security cms -D -i /path/to/iOSTeamProfile.mobileprovision
```