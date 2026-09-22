#### Q: Kann ich die Navigations- und Statusleiste unter Android ausblenden? {#q-is-it-possible-to-hide-the-navigation-and-status-bars-on-android}
A: Ja, aktiviere die Einstellung *immersive_mode* im Abschnitt *Android* deiner Datei *game.project*. Dadurch kann deine App den gesamten Bildschirm nutzen und alle Ereignisse für Berührungseingaben auf dem Bildschirm erfassen.


#### Q: Warum erhalte ich „Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]“, wenn ich ein Defold-Spiel auf einem Gerät installiere? {#q-why-am-im-getting-failure-install_parse_failed_inconsistent_certificates-when-installing-a-defold-game-on-device}
A: Android erkennt, dass du versuchst, die App mit einem neuen Zertifikat zu installieren. Wenn du Bundles für Debug-Builds erstellst, wird jeder Build mit einem temporären Zertifikat signiert. Deinstalliere die alte App, bevor du die neue Version installierst:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: Warum erhalte ich beim Erstellen eines Builds mit bestimmten Erweiterungen Fehlermeldungen zu widersprüchlichen Eigenschaften in AndroidManifest.xml? {#q-why-am-i-getting-errors-about-conflicting-properties-in-androidmanifestxml-when-building-with-certain-extensions}
A: Das kann passieren, wenn zwei oder mehr Erweiterungen jeweils einen Stub eines Android-Manifests bereitstellen, der dasselbe property-Tag mit unterschiedlichen Werten enthält. Das ist beispielsweise bei Firebase und AdMob aufgetreten. Der Build-Fehler sieht etwa so aus:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Mehr über das Problem und die Übergangslösung erfährst du im gemeldeten Defold-Issue [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) und im Google-Issue [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).