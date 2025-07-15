---
title: Отладка на Android
brief: В этом руководстве описывается, как отлаживать сборку, работающую на устройстве Android.
---

# Отладка на Android

Здесь мы перечислим ряд способов отладки вашего исполняемого файла, работающего на устройстве Android


## Android Studio

* Подготовьте бандл, установив параметр `android.debuggable` в *game.project*

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Поместите бандл приложения в режиме отладки в папку по выбору.

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* Запустите [Android Studio](https://developer.android.com/studio/)

* Выберите `Profile or debug APK`

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* Выберите только что созданный apk бандл

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* Выберите основной файл `.so` и убедитесь, что в нем есть отладочные символы 

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* Если их нет в файле, загрузите не урезанный файл с отладочными символами с расширением `.so`. (размер около 20 МБ)

* Сопоставления путей помогают переназначить отдельные пути, из которых был создан исполняемый файл (в облаке), в реальную папку на вашем локальном диске.

* Выберите .so файл, затем добавьте сопоставление на вашем локальном диске

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* Если у вас есть доступ к исходным кодам движка, добавьте сопоставление пути и для него

		* Убедитесь, что вы используете ту же версию исходного кода, которую собираетесь отлаживать

			defold $ git checkout 1.2.148 

* Нажмите `Apply changes`

* Теперь вы должны увидеть исходный код, имеющий привязки в вашем пректе. 

	![source](images/extensions/debugging/android/source_mappings_android.png)

* Добавить точку останова 

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* Нажмите `Run` -> `Debug "Appname"` и затем вызовите код, в который вы хотели бы вклиниться

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* Теперь вы можете пошагово войти в стек вызовов, а также отслеживать переменные 


## Примечания

### Директория задач нативного расширения 

В настоящее время рабочий процесс немного сложен для разработки. Это потому, что имя директории с задачами
является случайным для каждой сборки, что делает сопоставление пути недействительным для каждой новой сборки.

Однако он отлично работает для единичного сеанса отладки.

Сопоставления путей хранятся в файле <project>.iml в проекте Android Studio.

Можно получить директорию с задачами из исполняемого файла

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

Папка задачи называется так `job1298751322870374150`, каждый раз это название с уникальным случайным номером. 

