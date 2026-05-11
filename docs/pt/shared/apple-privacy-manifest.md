
## Apple Privacy Manifest

O manifesto de privacidade é uma lista de propriedades que registra os tipos de dados coletados pelo seu aplicativo ou SDK de terceiros, e as APIs de motivos exigidos que seu aplicativo ou SDK de terceiros usa. Para cada tipo de dado que seu aplicativo ou SDK de terceiros coleta e para cada categoria de API de motivos exigidos que ele usa, o aplicativo ou SDK de terceiros precisa registrar os motivos no arquivo de manifesto de privacidade incluído no bundle.

O Defold fornece um manifesto de privacidade padrão por meio do campo Privacy Manifest no arquivo *game.project*. Ao criar um bundle de aplicação, o manifesto de privacidade será mesclado com quaisquer manifestos de privacidade nas dependências do projeto e incluído no bundle da aplicação.

Leia mais sobre manifestos de privacidade na [documentação oficial da Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).
