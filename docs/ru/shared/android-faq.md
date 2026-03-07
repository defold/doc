#### Q: Можно ли скрыть панели навигации и статуса на Android?
A: Да, установите параметр *immersive_mode* в разделе *Android* вашего файла *game.project*. Это позволит приложению использовать весь экран и получать все касания по экрану.


#### Q: Почему при установке игры Defold на устройство я получаю ошибку "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]"?
A: Android обнаружил, что вы пытаетесь установить приложение с новым сертификатом. При сборке debug-версий каждая сборка подписывается временным сертификатом. Удалите старую версию приложения перед установкой новой:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: Почему при сборке с некоторыми расширениями появляются ошибки о конфликтующих свойствах в AndroidManifest.xml?
A: Это может произойти, когда два или более расширения предоставляют заглушку Android Manifest с одним и тем же тегом свойства, но с разными значениями. Например, такое случалось с Firebase и AdMob. Ошибка сборки выглядит примерно так:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Подробнее об этой проблеме и обходном решении можно прочитать в issue Defold [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) и issue Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).
