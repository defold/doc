---
title: Usando dependências CocoaPods em builds iOS e macOS
brief: Este manual explica como usar CocoaPods para resolver dependências em builds iOS e macOS.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) é um gerenciador de dependências para projetos Cocoa em Swift e Objective-C. CocoaPods normalmente é usado para gerenciar e integrar dependências em projetos Xcode. O Defold não usa Xcode ao compilar para iOS e macOS, mas ainda usa CocoaPods para resolver dependências no servidor de build.


## Resolvendo dependências

Extensões nativas podem incluir um arquivo `Podfile` nas pastas `manifests/ios` e `manifests/osx` para especificar as dependências da extensão. Exemplo:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

O servidor de build coletará os arquivos `Podfile` de todas as extensões e os usará para resolver todas as dependências e incluí-las ao compilar o código nativo.

Exemplos:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
