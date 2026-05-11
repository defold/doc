#### P: É possível ocultar as barras de navegação e status no Android?
R: Sim, defina a configuração *immersive_mode* na seção *Android* do seu arquivo *game.project*. Isso permite que seu aplicativo ocupe a tela inteira e capture todos os eventos de toque na tela.


#### P: Por que recebo "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" ao instalar um jogo Defold no dispositivo?
R: O Android detecta que você está tentando instalar o aplicativo com um novo certificado. Ao empacotar builds de debug, cada build será assinada com um certificado temporário. Desinstale o aplicativo antigo antes de instalar a nova versão:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### P: Por que recebo erros sobre propriedades conflitantes em AndroidManifest.xml ao compilar com certas extensões?
R: Isso pode acontecer quando duas ou mais extensões fornecem um stub de Android Manifest que contém a mesma tag de propriedade, mas com valores diferentes. Isso já aconteceu, por exemplo, com Firebase e AdMob. O erro de build se parece com isto:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override.
```

Você pode ler mais sobre o problema e a solução alternativa na issue do Defold relatada [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) e na issue do Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).
