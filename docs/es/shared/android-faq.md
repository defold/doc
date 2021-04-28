#### Q: ¿Es posible esconder la barra de navegación y estado en Android?
A: Si, activa la opción *immersive_mode* en la sección de *Android* de tu archivo *game.project*. Esto deja a tu aplicación tomar la pantalla completa y capturar todos los eventos touch de la pantalla.


#### Q: ¿Por qué obtengo "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" cuando instalo un archivo de juego Defold en mi dispositivo?
A: Android detecta que hayas tratado de instalar la aplicación con un nuevo certificado. Cuando creas builds de depuración, cada build será firmada con un certificado temporal. Desinstala la aplicación anterior antes de instalar la nueva versión:

```
$ adb uninstall com.defold.examples
Success
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
      pkg: /data/local/tmp/Defold examples.apk
Success
```
