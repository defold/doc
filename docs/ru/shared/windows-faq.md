#### Q: Почему GUI box nodes без текстуры прозрачны в редакторе, но отображаются как ожидается после сборки и запуска?

A: Эта ошибка может возникать на [компьютерах с GPU AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Убедитесь, что у вас обновлены графические драйверы.

#### Q: Почему при открытии атласа или scene view я получаю `com.sun.jna.Native.open.class java.lang.Error: Access is denied`?

A: Попробуйте запустить Defold от имени администратора. Щёлкните правой кнопкой мыши по исполняемому файлу Defold и выберите "Run as Administrator".

#### Q: Почему моя игра неправильно рендерится на Windows с интегрированным GPU Intel UHD, хотя HTML5-сборка работает?

A: Убедитесь, что у вас установлена версия драйвера не ниже 27.20.100.8280. Проверьте это через [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Дополнительную информацию можно найти [в этом сообщении на форуме](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### Q: Редактор Defold падает, и в логе показано `AWTError: Assistive Technology not found`

Если редактор падает, а в логе есть строка `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, выполните следующие шаги:

* Перейдите в `C:\Users\<username>`
* Откройте файл `.accessibility.properties` обычным текстовым редактором (подойдёт Notepad)
* Найдите в конфиге следующие строки:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Добавьте символ решётки (`#``) перед этими строками
* Сохраните изменения в файле и перезапустите Defold
