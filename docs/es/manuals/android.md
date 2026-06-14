---
title: Desarrollo de Defold para la plataforma Android
brief: Este manual describe cómo crear y ejecutar aplicaciones Defold en dispositivos Android
---

# Desarrollo en Android

Los dispositivos Android te permiten ejecutar libremente tus propias apps en ellos. Es muy fácil crear una versión de tu juego y copiarla a un dispositivo Android. Este manual explica los pasos necesarios para crear un bundle de tu juego para Android. Durante el desarrollo, suele ser preferible ejecutar tu juego mediante la [app de desarrollo](/manuals/dev-app), ya que te permite recargar contenido y código en caliente directamente en tu dispositivo.

## Proceso de firmado de Android y Google Play

Android requiere que todos los APK estén firmados digitalmente con un certificado antes de que se instalen en un dispositivo o se actualicen. Si usas Android App Bundles, solo necesitas firmar tu app bundle antes de subirlo a Play Console, y [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) se encarga del resto. Sin embargo, también puedes firmar manualmente tu app para subirla a Google Play, a otras tiendas de apps y para distribuirla fuera de cualquier tienda.

Cuando creas un bundle de aplicación Android desde el editor Defold o desde la [herramienta de línea de comando](/manuals/bob), puedes proporcionar un keystore (que contiene tu certificado y clave) y la contraseña del keystore, que se usarán al firmar tu aplicación. Si no lo haces, Defold genera un keystore de depuración y lo usa al firmar el bundle de la aplicación.

::: important
**Nunca** debes subir tu aplicación a Google Play si se firmó con un keystore de depuración. Usa siempre un keystore dedicado que hayas creado tú mismo.
:::

## Crear un keystore {#creating-a-keystore}

::: sidenote
Defold usa un keystore para el proceso de firmado de Android. [Hay más información disponible en esta publicación del foro](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Puedes crear un keystore [usando Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) o desde una terminal/símbolo del sistema:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Esto creará un archivo keystore llamado `mykeystore.keystore` que contiene una clave y un certificado. El acceso a la clave y al certificado estará protegido por la contraseña `5Up3r_53cR3t`. La clave y el certificado serán válidos durante 25 años (9125 días). La clave y el certificado generados se identificarán con el alias `myAlias`.

::: important
Asegúrate de guardar el keystore y la contraseña asociada en un lugar seguro. Si firmas y subes tus aplicaciones a Google Play por tu cuenta y se pierde el keystore o la contraseña del keystore, no tendrás forma de actualizar la aplicación en Google Play. Puedes evitar esto usando Google Play App Signing y dejando que Google firme tus aplicaciones por ti.
:::


## Crear un bundle de aplicación Android {#creating-an-android-application-bundle}

El editor te permite crear fácilmente un bundle de aplicación independiente para tu juego. Antes de crear el bundle, puedes especificar qué iconos usar para la app, definir el código de versión, etc. en el [archivo de configuración del proyecto](/manuals/project-settings/#android) *game.project*.

Para crear el bundle, selecciona <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> en el menú.

Si quieres que el editor cree automáticamente certificados de depuración aleatorios, deja vacíos los campos *Keystore* y *Keystore password*:

![Firmado de bundle Android](images/android/sign_bundle.png)

Si quieres firmar tu bundle con un keystore concreto, especifica *Keystore* y *Keystore password*. Se espera que *Keystore* tenga la extensión de archivo `.keystore`, mientras que se espera que la contraseña esté almacenada en un archivo de texto con la extensión `.txt`. También es posible especificar una *Key password* si la clave del keystore usa una contraseña distinta de la del propio keystore:

![Firmado de bundle Android](images/android/sign_bundle2.png)

Defold permite crear archivos APK y AAB. Selecciona APK o AAB en el menú desplegable Bundle Format.

Pulsa <kbd>Create Bundle</kbd> cuando hayas configurado las opciones del bundle de la aplicación. Luego se te pedirá que especifiques en qué lugar de tu computadora se creará el bundle.

![Archivo de paquete de aplicación Android](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Instalar un bundle de aplicación Android

#### Instalar un APK

Un archivo *`.apk`* se puede copiar a tu dispositivo con la herramienta `adb`, o a Google Play mediante la [consola para desarrolladores de Google Play](https://play.google.com/apps/publish/).

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Instalar un APK usando el editor

Puedes instalar y ejecutar un archivo *`.apk`* usando las casillas "Install on connected device" y "Launch installed app" del editor en el diálogo Bundle:

![Instalar y ejecutar APK](images/android/install_and_launch.png)

Para que esta funcionalidad funcione, necesitarás tener ADB instalado y *USB debugging* activado en el dispositivo conectado. Si el editor no puede detectar la ubicación de instalación de la herramienta de línea de comando ADB, tendrás que especificarla en [Preferences](/manuals/editor-preferences/#tools).

#### Instalar un AAB

Un archivo *.aab* se puede subir a Google Play mediante la [consola para desarrolladores de Google Play](https://play.google.com/apps/publish/). También es posible generar un archivo *`.apk`* a partir de un archivo *.aab* para instalarlo localmente usando [Android bundletool](https://developer.android.com/studio/command-line/bundletool).

## Permisos

El motor Defold requiere varios permisos para que funcionen todas sus funcionalidades. Los permisos se definen en `AndroidManifest.xml`, especificado en el [archivo de configuración del proyecto](/manuals/project-settings/#android) *game.project*. Puedes leer más sobre los permisos de Android en [la documentación oficial](https://developer.android.com/guide/topics/permissions/overview). En el manifiesto predeterminado se solicitan los siguientes permisos:

### android.permission.INTERNET y android.permission.ACCESS_NETWORK_STATE (Nivel de protección: normal)
Permite que las aplicaciones abran sockets de red y accedan a información sobre redes. Estos permisos son necesarios para el acceso a internet. ([Documentación oficial de Android](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) y ([documentación oficial de Android](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Nivel de protección: normal)
Permite usar PowerManager WakeLocks para evitar que el procesador entre en suspensión o que la pantalla se atenúe. Este permiso es necesario para evitar temporalmente que el dispositivo entre en suspensión mientras recibe una notificación push. ([Documentación oficial de Android](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## Usar AndroidX
AndroidX es una mejora importante respecto a la Android Support Library original, que ya no se mantiene. Los paquetes AndroidX sustituyen por completo a la Support Library al ofrecer paridad de funcionalidades y nuevas bibliotecas. La mayoría de las extensiones Android en el [Asset Portal](/assets) son compatibles con AndroidX. Si no quieres usar AndroidX, puedes desactivarlo explícitamente en favor de la antigua Android Support Library marcando `Use Android Support Lib` en el [manifiesto de la aplicación](https://defold.com/manuals/app-manifest/).

![](images/android/enable_supportlibrary.png)

## FAQ
:[Android FAQ](../shared/android-faq.md)
