#### Q : Est-il possible de masquer les barres de navigation et d'état sur Android ? {#q-is-it-possible-to-hide-the-navigation-and-status-bars-on-android}
R : Oui, activez le paramètre *immersive_mode* dans la section *Android* de votre fichier *game.project*. Cela permet à votre application d'occuper tout l'écran et de capturer tous les événements tactiles à l'écran.


#### Q : Pourquoi le message « Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES] » s'affiche-t-il lorsque j'installe un jeu Defold sur un appareil ? {#q-why-am-im-getting-failure-install_parse_failed_inconsistent_certificates-when-installing-a-defold-game-on-device}
R : Android détecte que vous essayez d'installer l'application avec un nouveau certificat. Lors de la création de bundles de builds de débogage, chaque build est signé avec un certificat temporaire. Désinstallez l'ancienne application avant d'installer la nouvelle version :

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q : Pourquoi est-ce que j'obtiens des erreurs concernant des propriétés en conflit dans AndroidManifest.xml lorsque je crée un build avec certaines extensions ? {#q-why-am-i-getting-errors-about-conflicting-properties-in-androidmanifestxml-when-building-with-certain-extensions}
R : Cela peut se produire lorsque deux extensions ou plus fournissent un fragment de manifeste Android contenant la même balise de propriété, mais avec des valeurs différentes. Cela s'est notamment produit avec Firebase et AdMob. L'erreur de build ressemble à ceci :

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override. 
```

Vous trouverez plus d'informations sur ce problème et sa solution de contournement dans le ticket Defold [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) et le ticket Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).