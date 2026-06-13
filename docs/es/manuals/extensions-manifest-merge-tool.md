---
title: Extensiones nativas - Herramientas de fusión de manifiestos
brief: Este manual describe cómo funciona la fusión de manifiestos de la aplicación
---

# Manifiestos de la aplicación

Para algunas plataformas admitimos extensiones que proporcionan fragmentos (o stubs) de manifiestos de la aplicación.
Pueden ser parte de un `AndroidManifest.xml`, `Info.plist` o `engine_template.html`.

Cada stub de manifiesto de extensión se aplicará uno tras otro, empezando por el manifiesto base de la aplicación.
El manifiesto base es el predeterminado (en `builtins\manifests\<platforms>\...`) o uno personalizado proporcionado por el usuario.

## Nomenclatura y estructura

Los manifiestos de extensión deben colocarse en una estructura determinada para que la extensión funcione según lo previsto.

    /myextension
        ext.manifest
        /manifests
            /android
                AndroidManifest.xml
            /ios
                Info.plist
            /osx
                Info.plist
            /web
                engine_template.html


## Android

La plataforma Android ya tiene una herramienta de fusión de manifiestos (basada en `ManifestMerger2`), y la usamos dentro de `bob.jar` para fusionar manifiestos.
Para ver un conjunto completo de instrucciones sobre cómo modificar tus manifiestos de Android, consulta [su documentación](https://developer.android.com/studio/build/manifest-merge).

::: important
Si no defines `android:targetSdkVersion` de tu aplicación en el manifiesto de extensión, se agregarán automáticamente los siguientes permisos: `WRITE_EXTERNAL_STORAGE`, `READ_PHONE_STATE`, `READ_EXTERNAL_STORAGE`. Puedes leer más al respecto en la documentación oficial [aquí](https://developer.android.com/studio/build/manifest-merge#implicit_system_permissions).
Recomendamos usar: `<uses-sdk android:targetSdkVersion=“{{android.target_sdk_version}}” />`
:::
### Ejemplo

Manifiesto base

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
            package='com.defold.testmerge'
            android:versionCode='14'
            android:versionName='1.0'
            android:installLocation='auto'>
        <uses-feature android:required='true' android:glEsVersion='0x00020000' />
        <uses-sdk android:minSdkVersion='9' android:targetSdkVersion='26' />
        <application android:label='Test Project' android:hasCode='true'>
        </application>
        <uses-permission android:name='android.permission.VIBRATE' />
    </manifest>
```

Manifiesto de extensión:

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android' package='com.defold.testmerge'>
         <uses-sdk android:targetSdkVersion=“{{android.target_sdk_version}}” />
        <uses-feature android:required='true' android:glEsVersion='0x00030000' />
        <application>
            <meta-data android:name='com.facebook.sdk.ApplicationName'
                android:value='Test Project' />
            <activity android:name='com.facebook.FacebookActivity'
              android:theme='@android:style/Theme.Translucent.NoTitleBar'
              android:configChanges='keyboard|keyboardHidden|screenLayout|screenSize|orientation'
              android:label='Test Project' />
        </application>
    </manifest>
```

Resultado

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
        package='com.defold.testmerge'
        android:installLocation='auto'
        android:versionCode='14'
        android:versionName='1.0' >
        <uses-sdk
            android:minSdkVersion='9'
            android:targetSdkVersion='26' />
        <uses-permission android:name='android.permission.VIBRATE' />
        <uses-feature
            android:glEsVersion='0x00030000'
            android:required='true' />
        <application
            android:hasCode='true'
            android:label='Test Project' >
            <meta-data
                android:name='com.facebook.sdk.ApplicationName'
                android:value='Test Project' />
            <activity
                android:name='com.facebook.FacebookActivity'
                android:configChanges='keyboard|keyboardHidden|screenLayout|screenSize|orientation'
                android:label='Test Project'
                android:theme='@android:style/Theme.Translucent.NoTitleBar' />
        </application>
    </manifest>
```

## iOS / macOS

Para `Info.plist` usamos nuestra propia implementación para fusionar listas y diccionarios. Es posible especificar atributos marcadores de fusión `merge`, `keep` o `replace` en las claves, donde `merge` es el valor predeterminado.

### Ejemplo

Manifiesto base

```xml
    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'>
    <plist version='1.0'>
    <dict>
        <key>NSAppTransportSecurity</key>
        <dict>
            <key>NSExceptionDomains</key>
            <dict>
                <key>foobar.net</key>
                <dict>
                    <key>testproperty</key>
                    <true/>
                </dict>
            </dict>
        </dict>
        <key>INT</key>
        <integer>8</integer>

        <key>REAL</key>
        <real>8.0</real>

        <!-- Mantén este valor incluso si un manifiesto de extensión contiene la misma clave -->
        <key merge='keep'>BASE64</key>
        <data>SEVMTE8gV09STEQ=</data>

        <!-- Si un manifiesto de extensión también tiene un array con esta clave, cualquier valor de diccionario se fusionará con el primer valor de diccionario del array base -->
        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>

        <!-- No intentes fusionar los valores de este array; en su lugar, los valores de los manifiestos de extensión se deben agregar al final del array -->
        <key merge='keep'>Array2</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>
    </dict>
    </plist>
```

Manifiesto de extensión:

```xml
    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'>
    <plist version='1.0'>
    <dict>
        <key>NSAppTransportSecurity</key>
        <dict>
            <key>NSExceptionDomains</key>
            <dict>
                <key>facebook.com</key>
                <dict>
                    <key>NSIncludesSubdomains</key>
                    <true/>
                    <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                    <false/>
                </dict>
            </dict>
        </dict>
        <key>INT</key>
        <integer>42</integer>

        <!-- Reemplaza el valor existente en el manifiesto base -->
        <key merge='replace'>REAL</key>
        <integer>16.0</integer>

        <key>BASE64</key>
        <data>Rk9PQkFS</data>

        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>b</string>
                </array>
            </dict>
        </array>

        <key>Array2</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>b</string>
                </array>
            </dict>
        </array>
    </dict>
    </plist>
```

Resultado:

```xml
    <?xml version='1.0'?>
    <!DOCTYPE plist SYSTEM 'file://localhost/System/Library/DTDs/PropertyList.dtd'>
    <plist version='1.0'>
        <!-- Fusión anidada de diccionarios de los manifiestos base y de extensión -->
        <dict>
            <key>NSAppTransportSecurity</key>
            <dict>
                <key>NSExceptionDomains</key>
                <dict>
                    <key>foobar.net</key>
                    <dict>
                        <key>testproperty</key>
                        <true/>
                    </dict>
                    <key>facebook.com</key>
                    <dict>
                        <key>NSIncludesSubdomains</key>
                        <true/>
                        <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                        <false/>
                    </dict>
                </dict>
            </dict>

            <!-- Del manifiesto base -->
            <key>INT</key>
            <integer>8</integer>

            <!-- El valor del manifiesto base se reemplazó porque el marcador de fusión se configuró como "replace" en el manifiesto de extensión -->
            <key>REAL</key>
            <real>16.0</real>

            <!-- Se usó el valor del manifiesto base porque el marcador de fusión se configuró como "keep" en el manifiesto base -->
            <key>BASE64</key>
            <data>SEVMTE8gV09STEQ=</data>

            <!-- Se agregó el valor del manifiesto de extensión porque no se especificó ningún marcador de fusión -->
            <key>INT</key>
            <integer>42</integer>

            <!-- Los valores de diccionario del array se fusionaron porque el manifiesto base usa "merge" de forma predeterminada -->
            <key>Array1</key>
            <array>
                <dict>
                    <key>Foobar</key>
                    <array>
                        <string>a</string>
                        <string>b</string>
                    </array>
                </dict>
            </array>

            <!-- Los valores de diccionario se agregaron al array porque el manifiesto base usó "keep" -->
            <key>Array2</key>
            <array>
                <dict>
                    <key>Foobar</key>
                    <array>
                        <string>a</string>
                    </array>
                </dict>
                <dict>
                    <key>Foobar</key>
                    <array>
                        <string>b</string>
                    </array>
                </dict>
            </array>
        </dict>
    </plist>
```


## HTML5

Para la plantilla HTML, nombramos cada sección para poder hacerlas coincidir (por ejemplo, "engine-start").
Luego puedes especificar los atributos `merge` o `keep`. `merge` es el valor predeterminado.

### Ejemplo

Manifiesto base

```html
    <!DOCTYPE html>
    <html>
    <body>
     <script id='engine-loader' type='text/javascript' src='dmloader.js'></script>
     <script id='engine-setup' type='text/javascript'>
     function load_engine() {
         var engineJS = document.createElement('script');
         engineJS.type = 'text/javascript';
         engineJS.src = '{{exe-name}}_wasm.js';
         document.head.appendChild(engineJS);
     }
     </script>
     <script id='engine-start' type='text/javascript'>
         load_engine();
     </script>
    </body>
    </html>
```

Manifiesto de extensión

```html
    <html>
    <body>
     <script id='engine-loader' type='text/javascript' src='mydmloader.js'></script>
     <script id='engine-start' type='text/javascript' merge='keep'>
         my_load_engine();
     </script>
    </body>
    </html>
```

Resultado

```html
    <!doctype html>
    <html>
    <head></head>
    <body>
        <script id='engine-loader' type='text/javascript' src='mydmloader.js'></script>
        <script id='engine-setup' type='text/javascript'>
            function load_engine() {
                var engineJSdocument.createElement('script');
                engineJS.type = 'text/javascript';
                engineJS.src = '{{exe-name}}_wasm.js';
                document.head.appendChild(engineJS);
            }
        </script>
        <script id='engine-start' type='text/javascript' merge='keep'>
            my_load_engine(
        </script>
    </body>
    </html>
```
