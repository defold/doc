#### P: Czy można ukryć paski nawigacji i stanu w Androidzie?
O: Tak, ustaw opcję *immersive_mode* w sekcji *Android* w pliku *game.project*. Dzięki temu aplikacja może przejąć cały ekran i przechwytywać wszystkie zdarzenia dotykowe na ekranie.


#### P: Dlaczego podczas instalowania gry Defold na urządzeniu pojawia się błąd "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]"?
O: Android wykrywa, że próbujesz zainstalować aplikację z nowym certyfikatem. Podczas tworzenia pakietów debugowych każda kompilacja jest podpisywana tymczasowym certyfikatem. Przed zainstalowaniem nowej wersji odinstaluj starą aplikację:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### P: Dlaczego podczas budowania z niektórymi rozszerzeniami pojawiają się błędy o sprzecznych właściwościach w AndroidManifest.xml?
O: Może się tak zdarzyć, gdy dwa lub więcej rozszerzeń dostarcza szablon manifestu Androida zawierający ten sam tag właściwości, ale z różnymi wartościami. Taka sytuacja miała na przykład miejsce z Firebase i AdMob. Błąd budowania wygląda podobnie do tego:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Więcej informacji o tym problemie i obejściu znajdziesz w zgłoszonym problemie Defold [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) oraz w problemie Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).
