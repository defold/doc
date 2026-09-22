#### Запитання: Які системні вимоги редактора? {#q-what-are-the-system-requirements-for-the-editor}
Відповідь: Редактор використовуватиме до 75% доступної системної пам’яті. На комп’ютері з 4 ГБ оперативної пам’яті цього має вистачити для невеликих проєктів Defold. Для середніх і великих проєктів рекомендовано 6 ГБ оперативної пам’яті або більше.


#### Запитання: Чи оновлюються бета-версії Defold автоматично? {#q-are-defold-beta-versions-auto-updating}
Відповідь: Так. Бета-версія редактора Defold перевіряє наявність оновлень під час запуску, як і стабільна версія Defold.


#### Запитання: Чому під час запуску редактора з’являється помилка `java.awt.AWTError: Assistive Technology not found`? {#q-why-am-i-getting-an-error-saying-javaawtawterror-assistive-technology-not-found-when-launching-the-editor}
Відповідь: Ця помилка пов’язана з проблемами допоміжних технологій Java, як-от [засобу читання з екрана NVDA](https://www.nvaccess.org/download/). Імовірно, у вашій домашній папці є файл `.accessibility.properties`. Видаліть його та спробуйте запустити редактор знову. (Примітка: якщо ви використовуєте допоміжні технології й цей файл вам потрібен, напишіть нам на info@defold.se, щоб обговорити інші способи розв’язання проблеми).

Обговорення є [в цій темі на форумі Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Запитання: Чому під час запуску редактора з’являється помилка `sun.security.validator.ValidatorException: PKIX path building failed`? {#q-why-am-i-getting-an-error-saying-sunsecurityvalidatorvalidatorexception-pkix-path-building-failed-when-launching-the-editor}
Відповідь: Цей виняток виникає, коли редактор намагається встановити з’єднання HTTPS, але не може перевірити ланцюжок сертифікатів, наданий сервером.

Докладніше про цю помилку див. [за цим посиланням](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md).


#### Запитання: Чому під час виконання певних операцій з’являється помилка `java.lang.OutOfMemoryError: Java heap space`? {#q-why-am-i-am-getting-a-javalangoutofmemoryerror-java-heap-space-when-performing-certain-operations}
Відповідь: Редактор Defold створено за допомогою Java, і в деяких випадках стандартних налаштувань пам’яті Java може бути недостатньо. Якщо це сталося, ви можете вручну налаштувати редактор на виділення більшого обсягу пам’яті, відредагувавши його файл конфігурації. У macOS файл конфігурації з назвою `config` розташований у папці `Defold.app/Contents/Resources/`. У Windows він розташований поруч із виконуваним файлом `Defold.exe`, а в Linux — поруч із виконуваним файлом `Defold`. Відкрийте файл `config` і додайте `-Xmx6gb` до рядка, що починається з `vmargs`. Додавання `-Xmx6gb` задає максимальний розмір купи пам’яті 6 гігабайтів (за замовчуванням зазвичай 4 ГБ). Результат має виглядати приблизно так:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
