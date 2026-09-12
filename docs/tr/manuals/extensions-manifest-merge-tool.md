---
title: Yerel kod eklentileri - Bildirim birleştirme araçları
brief: Bu kılavuz, uygulama bildirimlerinin birleştirilmesinin nasıl çalıştığını açıklar
---

# Uygulama bildirimleri

Bazı platformlarda, eklentilerin (extension) uygulama bildirimi (application manifest) parçaları (snippet veya stub) sağlamasını destekliyoruz.
Bu, bir `AndroidManifest.xml`, `Info.plist` veya `engine_template.html` dosyasının bir bölümü olabilir

Her eklentinin bildirim parçası, uygulamanın temel bildiriminden başlanarak sırayla uygulanır.
Temel bildirim, varsayılan bildirim (`builtins\manifests\<platforms>\...` konumundaki) veya kullanıcının sağladığı özel bir bildirimdir.

## Adlandırma ve yapı

Eklentinin amaçlandığı gibi çalışabilmesi için eklenti bildirimlerinin belirli bir yapıya göre yerleştirilmesi gerekir.

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

Android platformunda zaten bir bildirim birleştirme aracı (`ManifestMerger2` tabanlı) vardır ve bildirimleri birleştirmek için bu aracı `bob.jar` içinde kullanıyoruz.
Android bildirimlerinizi nasıl değiştireceğinize ilişkin tüm yönergeler için [Android belgelerine](https://developer.android.com/studio/build/manifest-merge) bakın

::: important
Eklenti bildiriminizde uygulamanızın `android:targetSdkVersion` değerini ayarlamazsanız şu izinler otomatik olarak eklenir:  `WRITE_EXTERNAL_STORAGE`, `READ_PHONE_STATE`, `READ_EXTERNAL_STORAGE`. Bu konuda daha fazla bilgiyi [buradaki](https://developer.android.com/studio/build/manifest-merge#implicit_system_permissions) resmî belgelerde bulabilirsiniz.
Şunu kullanmanızı öneririz: `<uses-sdk android:targetSdkVersion="{{android.target_sdk_version}}" />`
:::
### Örnek

Temel bildirim

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
            package='com.defold.testmerge'
            android:versionCode='14'
            android:versionName='1.0'
            android:installLocation='auto'>
        <uses-feature android:required='true' android:glEsVersion='0x00020000' />
        <uses-sdk android:minSdkVersion='21' android:targetSdkVersion='26' />
        <application android:label='Test Project' android:hasCode='true'>
        </application>
        <uses-permission android:name='android.permission.VIBRATE' />
    </manifest>
```

Eklenti bildirimi:

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android' package='com.defold.testmerge'>
         <uses-sdk android:targetSdkVersion="{{android.target_sdk_version}}" />
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

Sonuç

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <manifest xmlns:android='http://schemas.android.com/apk/res/android'
        package='com.defold.testmerge'
        android:installLocation='auto'
        android:versionCode='14'
        android:versionName='1.0' >
        <uses-sdk
            android:minSdkVersion='21'
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

`Info.plist` dosyasında listeleri ve sözlükleri birleştirmek için kendi uygulamamızı kullanıyoruz. Anahtarlarda birleştirme işaretçisi öznitelikleri olarak `merge`, `keep` veya `replace` belirtilebilir; varsayılan değer `merge` olur.

### Örnek

Temel bildirim

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

        <!-- Keep this value even if an extension manifest contains the same key -->
        <key merge='keep'>BASE64</key>
        <data>SEVMTE8gV09STEQ=</data>

        <!-- If an extension manifest also has an array with this key then any dictionary values will be merged with the first dictionary value of the base array -->
        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>

        <!-- Do not attempt to merge the values of this array, instead values from extension manifests should be added to the end of the array -->
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

Eklenti bildirimi:

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

        <!-- Replace the existing value in the base manifest -->
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

Sonuç:

```xml
    <?xml version='1.0'?>
    <!DOCTYPE plist SYSTEM 'file://localhost/System/Library/DTDs/PropertyList.dtd'>
    <plist version='1.0'>
        <!-- Nested merge of dictionaries from base and extension manifests -->
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

            <!-- From the base manifest -->
            <key>INT</key>
            <integer>8</integer>

            <!-- The value from the base manifest was replaced since the merge marker was set to "replace" in the extension manifest -->
            <key>REAL</key>
            <real>16.0</real>

            <!-- The value from the base manifest was used since the merge marker was set to "keep" in the base manifest -->
            <key>BASE64</key>
            <data>SEVMTE8gV09STEQ=</data>

            <!-- The value from the extender manifest was added since no merge marker was specified -->
            <key>INT</key>
            <integer>42</integer>

            <!-- The dictionary values of the array were merged since the base manifest defaults to "merge" -->
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

            <!-- The dictionary values were added to the array since the base manifest used "keep" -->
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

HTML şablonunda, bölümleri eşleştirebilmek için her birine bir ad verdik (örneğin "engine-start").
Ardından `merge` veya `keep` özniteliklerini belirtebilirsiniz. Varsayılan değer `merge` olur.

### Örnek

Temel bildirim

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

Eklenti bildirimi

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

Sonuç

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
