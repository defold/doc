#### Запитання: Чому вузли Box у GUI без текстури прозорі в редакторі, але відображаються як очікується після збирання й запуску? {#q-why-are-gui-box-nodes-without-a-texture-transparent-in-the-editor-but-show-up-as-expected-when-i-build-and-run}

Відповідь: Ця помилка може виникати на [комп’ютерах із графічними процесорами AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Обов’язково оновіть графічні драйвери.

#### Запитання: Чому під час відкриття атласу або вікна сцени з’являється помилка `com.sun.jna.Native.open.class java.lang.Error: Access is denied`? {#q-why-am-i-getting-comsunjnanativeopenclass-javalangerror-access-is-denied-when-opening-an-atlas-or-a-scene-view}

Відповідь: Спробуйте запустити Defold від імені адміністратора. Клацніть виконуваний файл Defold правою кнопкою миші та виберіть «Run as Administrator».

#### Запитання: Чому моя гра неправильно відображається у Windows із вбудованим графічним процесором Intel UHD, хоча збірка HTML5 працює? {#q-why-is-my-game-not-rendering-properly-on-windows-using-an-intel-uhd-integrated-gpu-but-my-html5-build-works}

Відповідь: Обов’язково оновіть драйвер до версії 27.20.100.8280 або новішої. Перевірте його за допомогою [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Додаткову інформацію наведено в [цьому дописі на форумі](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### Запитання: Редактор Defold аварійно завершує роботу, а в журналі є повідомлення `AWTError: Assistive Technology not found` {#q-the-defold-editor-is-crashing-and-the-log-shows-awterror-assistive-technology-not-found}

Якщо редактор аварійно завершує роботу, а в журналі згадано `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, виконайте такі кроки:

* Перейдіть до `C:\Users\<username>`
* Відкрийте файл `.accessibility.properties` у звичайному текстовому редакторі (підійде Notepad)
* Знайдіть у конфігурації такі рядки:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Додайте знак решітки (`#`) на початку цих рядків
* Збережіть зміни у файлі та перезапустіть Defold
