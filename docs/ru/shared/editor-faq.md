#### Q: Каковы системные требования редактора?
A: Редактор использует до 75% доступной памяти системы. На компьютере с 4 ГБ ОЗУ этого должно хватить для небольших проектов Defold. Для проектов среднего и большого размера рекомендуется 6 ГБ ОЗУ или больше.


#### Q: Обновляются ли бета-версии Defold автоматически?
A: Да. Бета-редактор Defold проверяет обновления при запуске, так же как и стабильная версия Defold.


#### Q: Почему при запуске редактора появляется ошибка `java.awt.AWTError: Assistive Technology not found`?
A: Эта ошибка связана с проблемами Java assistive technology, например [NVDA screen reader](https://www.nvaccess.org/download/). Скорее всего, у вас в домашней папке есть файл `.accessibility.properties`. Удалите этот файл и попробуйте снова запустить редактор. (Примечание: если вы действительно используете assistive technology и вам необходим этот файл, напишите нам на info@defold.se, чтобы обсудить альтернативные решения).

Обсуждение есть [здесь, на форуме Defold](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3).


#### Q: Почему при запуске редактора появляется ошибка `sun.security.validator.ValidatorException: PKIX path building failed`?
A: Это исключение возникает, когда редактор пытается установить https-соединение, но цепочка сертификатов, предоставленная сервером, не может быть проверена.

Подробности об этой ошибке смотрите [по этой ссылке](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md).


#### Q: Почему при выполнении некоторых операций я получаю `java.lang.OutOfMemoryError: Java heap space`?
A: Редактор Defold построен на Java, и в некоторых случаях стандартной конфигурации памяти Java может не хватать. Если это происходит, вы можете вручную настроить редактор на выделение большего объёма памяти, отредактировав файл конфигурации редактора. Файл конфигурации с именем `config` находится в папке `Defold.app/Contents/Resources/` на macOS. На Windows он находится рядом с исполняемым файлом `Defold.exe`, а на Linux — рядом с исполняемым файлом `Defold`. Откройте файл `config` и добавьте `-Xmx6gb` в строку, начинающуюся с `vmargs`. Параметр `-Xmx6gb` установит максимальный размер heap в 6 гигабайт (по умолчанию обычно 4Gb). Это должно выглядеть примерно так:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
