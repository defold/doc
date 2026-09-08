#### D: È possibile nascondere la barra di navigazione e la barra di stato su Android? {#q-is-it-possible-to-hide-the-navigation-and-status-bars-on-android}
R: Sì, attiva l'impostazione *immersive_mode* nella sezione *Android* del file *game.project*. In questo modo l'app può occupare l'intero schermo e acquisire tutti gli eventi di tocco sullo schermo.


#### D: Perché compare "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" quando installo un gioco Defold su un dispositivo? {#q-why-am-im-getting-failure-install_parse_failed_inconsistent_certificates-when-installing-a-defold-game-on-device}
R: Android rileva che stai tentando di installare l'app con un nuovo certificato. Quando crei bundle di build di debug, ogni build viene firmata con un certificato temporaneo. Disinstalla la vecchia app prima di installare la nuova versione:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### D: Perché si verificano errori relativi a proprietà in conflitto in AndroidManifest.xml quando creo una build con alcune estensioni? {#q-why-am-i-getting-errors-about-conflicting-properties-in-androidmanifestxml-when-building-with-certain-extensions}
R: Questo può accadere quando due o più estensioni forniscono un frammento di Android Manifest che contiene lo stesso tag di proprietà ma con valori diversi. È successo, ad esempio, con Firebase e AdMob. L'errore di build è simile al seguente:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Puoi trovare maggiori dettagli sul problema e sulla soluzione temporanea nella segnalazione Defold [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) e nella segnalazione Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).