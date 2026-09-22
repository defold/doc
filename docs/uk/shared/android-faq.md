#### П: Чи можна приховати панелі навігації та стану в Android? {#q-is-it-possible-to-hide-the-navigation-and-status-bars-on-android}
В: Так, увімкніть налаштування *immersive_mode* у розділі *Android* файлу *game.project*. Це дасть вашому застосунку змогу зайняти весь екран і перехоплювати всі події дотику на екрані.


#### П: Чому під час установлення гри Defold на пристрій з’являється помилка "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]"? {#q-why-am-im-getting-failure-install_parse_failed_inconsistent_certificates-when-installing-a-defold-game-on-device}
В: Android виявляє спробу встановити застосунок із новим сертифікатом. Під час пакування налагоджувальних збірок кожну збірку підписують тимчасовим сертифікатом. Видаліть старий застосунок перед установленням нової версії:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### П: Чому під час збирання з певними розширеннями виникають помилки через конфлікт властивостей в AndroidManifest.xml? {#q-why-am-i-getting-errors-about-conflicting-properties-in-androidmanifestxml-when-building-with-certain-extensions}
В: Це може статися, коли два або більше розширень надають фрагменти маніфесту Android з однаковим тегом властивості, але різними значеннями. Наприклад, таке траплялося з Firebase та AdMob. Помилка збирання має приблизно такий вигляд:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Докладніше про проблему та спосіб її обходу можна прочитати в повідомленні про проблему Defold [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) і повідомленні про проблему Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).