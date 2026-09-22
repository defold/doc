---
title: Налагодження на Android
brief: У цьому посібнику описано, як налагоджувати збірку за допомогою Android Studio.
---

# Налагодження на Android {#debugging-on-android}

Тут описано, як налагоджувати збірку за допомогою [Android Studio](https://developer.android.com/studio/), офіційного середовища розробки для операційної системи Android від Google.


## Android Studio {#android-studio}

* Підготуйте пакет, увімкнувши параметр `android.debuggable` у *game.project*

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Створіть пакет застосунку в режимі налагодження у вибраній папці.

	![Пакування для Android](images/extensions/debugging/android/bundle_android.png)

* Запустіть [Android Studio](https://developer.android.com/studio/)

* Виберіть `Profile or debug APK`

	![Налагодження APK](images/extensions/debugging/android/android_profile_or_debug.png)

* Виберіть щойно створений пакет apk

	![Вибір apk](images/extensions/debugging/android/android_select_apk.png)

* Виберіть основний файл `.so` і переконайтеся, що він містить налагоджувальні символи

	![Вибір файлу .so](images/extensions/debugging/android/android_missing_symbols.png)

* Якщо ні, завантажте файл `.so` з невидаленими символами. (розмір становить приблизно 20 МБ)

* Зіставлення шляхів дає змогу зіставити окремі шляхи, за якими було зібрано виконуваний файл (у хмарі), з фактичною папкою на вашому локальному диску.

* Виберіть файл .so, а потім додайте зіставлення з папкою на локальному диску

	![Зіставлення шляхів 1](images/extensions/debugging/android/path_mappings_android.png)

	![Зіставлення шляхів 2](images/extensions/debugging/android/path_mappings_android2.png)

* Якщо у вас є доступ до вихідного коду рушія, додайте зіставлення шляхів і для нього.

* Обов’язково перемкніться на версію, яку ви зараз налагоджуєте

	defold$ git checkout 1.2.148

* Натисніть `Apply changes`

* Тепер у вашому проєкті має з’явитися зіставлений вихідний код

	![Зіставлений вихідний код](images/extensions/debugging/android/source_mappings_android.png)

* Додайте точку зупинки

	![Точка зупинки](images/extensions/debugging/android/breakpoint_android.png)

* Натисніть `Run` -> `Debug "Appname"` і викличте код, у якому хочете зупинити виконання

	![Точка зупинки](images/extensions/debugging/android/callstack_variables_android.png)

* Тепер ви можете покроково проходити стек викликів та інспектувати змінні


## Примітки {#notes}

### Папка завдання нативного розширення {#native-extension-job-folder}

Наразі цей робочий процес дещо незручний для розробки. Це пов’язано з тим, що назва папки завдання
є випадковою для кожної збірки, через що зіставлення шляхів стає недійсним після кожного збирання.

Проте для одного сеансу налагодження він цілком підходить.

Зіставлення шляхів зберігаються у файлі проєкту `.iml` у проєкті Android Studio.

Назву папки завдання можна отримати з виконуваного файлу

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

Назва папки завдання має вигляд `job1298751322870374150`, щоразу з випадковим числом.

