---
title: Natywne rozszerzenia - narzędzia scalania manifestów
brief: Ta instrukcja opisuje, jak działa scalanie manifestów aplikacji
---

# Manifesty aplikacji

Dla niektórych platform obsługujemy rozszerzenia, które dostarczają fragmenty manifestów aplikacji.
Może to być fragment `AndroidManifest.xml`, `Info.plist` albo `engine_template.html`.

Każdy fragment manifestu rozszerzenia jest stosowany kolejno, począwszy od bazowego manifestu aplikacji.
Manifest bazowy jest albo domyślnym manifestem (w `builtins\manifests\<platforms>\...`), albo niestandardowym manifestem dostarczonym przez użytkownika.

## Nazewnictwo i struktura

Manifesty rozszerzeń muszą być umieszczone w określonej strukturze, aby rozszerzenie działało zgodnie z przeznaczeniem.

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

Platforma Android ma już narzędzie do scalania manifestów oparte na `ManifestMerger2`, a my używamy go w `bob.jar` do tego samego zadania.
Pełny zestaw instrukcji dotyczących modyfikowania manifestów Androida znajdziesz w [ich dokumentacji](https://developer.android.com/studio/build/manifest-merge).

::: important
Jeśli w manifeście rozszerzenia nie ustawisz `android:targetSdkVersion` dla swojej aplikacji, automatycznie zostaną dodane następujące uprawnienia: `WRITE_EXTERNAL_STORAGE`, `READ_PHONE_STATE`, `READ_EXTERNAL_STORAGE`. Więcej na ten temat znajdziesz w oficjalnej dokumentacji [tutaj](https://developer.android.com/studio/build/manifest-merge#implicit_system_permissions).
Zalecamy użycie: `<uses-sdk android:targetSdkVersion=“{{android.target_sdk_version}}” />`
:::
### Przykład

Manifest bazowy

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

Manifest rozszerzenia

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

Wynik

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

W przypadku `Info.plist` używamy własnej implementacji do scalania list i słowników. Na kluczach można określić atrybuty scalania `merge`, `keep` lub `replace`, przy czym `merge` jest domyślny.

### Przykład

Manifest bazowy

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

        <!-- Zachowaj tę wartość, nawet jeśli manifest rozszerzenia zawiera ten sam klucz -->
        <key merge='keep'>BASE64</key>
        <data>SEVMTE8gV09STEQ=</data>

        <!-- Jeśli manifest rozszerzenia również ma tablicę z tym kluczem, wartości słowników zostaną scalone z pierwszą wartością słownika w tablicy bazowej -->
        <key>Array1</key>
        <array>
            <dict>
                <key>Foobar</key>
                <array>
                    <string>a</string>
                </array>
            </dict>
        </array>

        <!-- Nie próbuj scalać wartości tej tablicy; zamiast tego dodaj wartości z manifestów rozszerzeń na końcu tablicy -->
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

Manifest rozszerzenia

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

        <!-- Zastąp istniejącą wartość w manifeście bazowym -->
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

Wynik:

```xml
    <?xml version='1.0'?>
    <!DOCTYPE plist SYSTEM 'file://localhost/System/Library/DTDs/PropertyList.dtd'>
    <plist version='1.0'>
        <!-- Zagnieżdżone scalanie słowników z manifestu bazowego i manifestu rozszerzenia -->
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

            <!-- Z manifestu bazowego -->
            <key>INT</key>
            <integer>8</integer>

            <!-- Wartość z manifestu bazowego została zastąpiona, ponieważ w manifeście rozszerzenia ustawiono znacznik scalania na "replace" -->
            <key>REAL</key>
            <real>16.0</real>

            <!-- Użyto wartości z manifestu bazowego, ponieważ w manifeście bazowym ustawiono znacznik scalania na "keep" -->
            <key>BASE64</key>
            <data>SEVMTE8gV09STEQ=</data>

            <!-- Dodano wartość z manifestu rozszerzenia, ponieważ nie określono znacznika scalania -->
            <key>INT</key>
            <integer>42</integer>

            <!-- Wartości słowników w tablicy zostały scalone, ponieważ domyślną wartością manifestu bazowego jest "merge" -->
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

            <!-- Wartości słowników zostały dodane do tablicy, ponieważ manifest bazowy używał opcji "keep" -->
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

Dla szablonu HTML oznaczyliśmy każdą sekcję, aby można było je dopasowywać, na przykład "engine-start".
Następnie można określić atrybuty `merge` albo `keep`. `merge` jest domyślny.

### Przykład

Manifest bazowy

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

Manifest rozszerzenia

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

Wynik

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
