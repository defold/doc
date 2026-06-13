## Manifiesto de privacidad de Apple

El manifiesto de privacidad es una lista de propiedades que registra los tipos de datos recopilados por tu app o por un SDK de terceros, y las API con razones requeridas que usa tu app o el SDK de terceros. Para cada tipo de dato que recopila tu app o el SDK de terceros, y para cada categoría de API con razones requeridas que utiliza, la app o el SDK de terceros debe registrar los motivos en su archivo de manifiesto de privacidad incluido en el bundle.

Defold proporciona un manifiesto de privacidad predeterminado mediante el campo Privacy Manifest del archivo *game.project*. Al crear un bundle de la aplicación, el manifiesto de privacidad se fusionará con cualquier manifiesto de privacidad de las dependencias del proyecto y se incluirá en el bundle de la aplicación.

Lee más sobre los manifiestos de privacidad en la [documentación oficial de Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).
