#### Q: ¿Es posible ocultar las barras de navegación y de estado en Android?
A: Sí, define la opción *immersive_mode* en la sección *Android* de tu archivo *game.project*. Esto permite que tu app ocupe toda la pantalla y capture todos los eventos touch de la pantalla.


#### Q: ¿Por qué obtengo "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" al instalar un juego Defold en un dispositivo?
A: Android detecta que intentas instalar la app con un certificado nuevo. Al crear builds de depuración, cada build se firma con un certificado temporal. Desinstala la app anterior antes de instalar la nueva versión:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```


#### Q: ¿Por qué obtengo errores sobre propiedades en conflicto en AndroidManifest.xml al crear una build con ciertas extensiones?
A: Esto puede ocurrir cuando dos o más extensiones proporcionan un stub de Android Manifest que contiene la misma etiqueta de propiedad, pero con valores distintos. Esto ha ocurrido, por ejemplo, con Firebase y AdMob. El error de build tiene un aspecto similar a este:

```
SEVERE: /tmp/job4531953598647135356/upload/AndroidManifest.xml:32:13-58
Error: Attribute property#android.adservices.AD_SERVICES_CONFIG@resource
value=(@xml/ga_ad_services_config) from AndroidManifest.xml:32:13-58 is also
present at AndroidManifest.xml:92:13-59 value=(@xml/gma_ad_services_config).
Suggestion: add 'tools:replace="android:resource"' to <property> element at
AndroidManifest.xml to override.
```

Puedes leer más sobre el problema y la solución temporal en el issue de Defold reportado [#9453](https://github.com/defold/defold/issues/9453#issuecomment-2367367269) y el issue de Google [#327696048](https://issuetracker.google.com/issues/327696048?pli=1).
