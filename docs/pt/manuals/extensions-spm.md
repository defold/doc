---
title: Usando dependências do Swift Package Manager em builds para iOS e macOS
brief: Este manual explica como usar o Swift Package Manager para resolver dependências em builds para iOS e macOS.
---

# Swift Package Manager {#swift-package-manager}

O [Swift Package Manager](https://www.swift.org/documentation/package-manager/) é o gerenciador de dependências integrado ao Swift e ao Xcode. Muitos SDKs para iOS e macOS são distribuídos como pacotes Swift, e alguns não são mais publicados como CocoaPods. O Defold não usa o Xcode ao compilar a engine, mas o servidor de build usa o Xcode para baixar e compilar os pacotes Swift dos quais uma extensão depende. O resultado é então vinculado à engine da mesma forma que as [dependências CocoaPods](/manuals/extensions-cocoapods).

CocoaPods e pacotes Swift podem ser usados no mesmo projeto e até na mesma extensão.


## Declarando dependências {#declaring-dependencies}

Extensões nativas podem incluir um arquivo `SwiftPackages.json` nas pastas `manifests/ios` e `manifests/osx` para especificar os pacotes Swift dos quais dependem. Exemplo:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/firebase/firebase-ios-sdk.git",
      "version": "12.16.0",
      "products": ["FirebaseCore", "FirebaseInstallations"]
    }
  ]
}
```

O arquivo é JSON simples. Você não escreve um arquivo `Package.swift` por conta própria; o servidor de build gera um a partir dos arquivos `SwiftPackages.json` de todas as extensões.

O arquivo contém os seguintes campos:

* `platform` - Obrigatório. `"ios"` em `manifests/ios/SwiftPackages.json` e `"osx"` em `manifests/osx/SwiftPackages.json`.
* `minVersion` - Opcional. A versão mínima de iOS ou macOS para a qual os pacotes são compilados, por exemplo `"15.0"`. É usado o maior valor entre os de todas as extensões e a versão mínima aceita pela engine, tanto ao compilar os pacotes quanto ao vincular a engine.
* `wrapperType` - Opcional. `"static"` (padrão) ou `"dynamic"`. Consulte [Vinculação estática e dinâmica](#static-and-dynamic-linking) abaixo.
* `packages` - Obrigatório. Uma lista de pacotes. Cada pacote tem os seguintes campos:
  * `url` - A URL `https://` do repositório git do pacote. URLs com credenciais, porta personalizada ou parâmetros de consulta, assim como URLs `ssh`, não são aceitas; portanto, o repositório deve ser acessível publicamente.
  * `products` - Os produtos do pacote a vincular à engine. São os produtos de biblioteca listados na seção `products` do arquivo `Package.swift` do pacote. O nome de um produto não é necessariamente igual ao nome do pacote ou do módulo que você importa.
  * Exatamente um requisito de versão:
    * `version` - Esta versão exata, por exemplo `"12.16.0"`.
    * `from` - Esta versão ou qualquer versão posterior com a mesma versão principal. Por exemplo, `"9.0.0"` resolve para a versão `9.x.x` mais recente.
    * `branch` - O commit mais recente de uma branch, por exemplo `"main"`.
    * `revision` - Um commit específico, informado como o hash completo de 40 caracteres.

O servidor de build coleta os arquivos `SwiftPackages.json` de todas as extensões e os usa para resolver todas as dependências, incluindo as dos próprios pacotes, e as inclui ao compilar o código nativo.


## Usando pacotes no código da extensão {#using-packages-from-extension-code}

Os cabeçalhos dos produtos ficam disponíveis para o código-fonte da extensão. Use-os em arquivos-fonte Objective-C++ (`.mm`). Este exemplo inicia o SDK do [Sentry](https://github.com/getsentry/sentry-cocoa) quando a aplicação inicia:

`manifests/ios/SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/getsentry/sentry-cocoa.git",
      "from": "9.0.0",
      "products": ["Sentry"]
    }
  ]
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>

#if defined(DM_PLATFORM_IOS)
#import <UIKit/UIKit.h>
#import <Sentry/Sentry.h>
#import <Sentry/Sentry-Swift.h>
#endif

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
#if defined(DM_PLATFORM_IOS)
    [SentrySDK startWithConfigureOptions:^(SentryOptions* options) {
        options.dsn = @"https://examplePublicKey@o0.ingest.sentry.io/0";
    }];
#endif
    return dmExtension::RESULT_OK;
}
```

* Cabeçalhos Objective-C são importados como `#import <Module/Header.h>`, em que `Module` é o nome do módulo que os fornece.
* Classes implementadas em Swift são declaradas no cabeçalho gerado `<Module/Module-Swift.h>`. Ele contém apenas as classes e os métodos que o módulo expõe ao Objective-C (marcados com `@objc` no Swift). Importe `UIKit` (ou `AppKit` no macOS) antes dele, pois o cabeçalho gerado usa seus tipos.


## Dependências de várias extensões {#dependencies-of-several-extensions}

Quando várias extensões de um projeto usam pacotes Swift, todos os seus arquivos `SwiftPackages.json` para a plataforma são combinados em um único grafo de pacotes:

* Pacotes com a mesma URL são mesclados, e os produtos solicitados são combinados.
* Um pacote compartilhado por várias extensões deve ter o mesmo requisito de versão em todas elas. Requisitos diferentes, por exemplo `"version": "12.16.0"` em uma extensão e `"from": "12.0.0"` em outra, fazem o build falhar com o erro `Conflicting requirements for Swift package`.
* É usado o maior valor de `minVersion`.
* Todas as extensões que definem `wrapperType` devem definir o mesmo valor.

Um projeto também pode combinar extensões que usam CocoaPods e extensões que usam pacotes Swift. Ambos são resolvidos e vinculados à engine. Contudo, o mesmo SDK não deve vir dos dois: se uma extensão obtiver Firebase de um `Podfile` e outra de um `SwiftPackages.json`, a vinculação da engine falhará com erros de símbolos duplicados. Extensões que compartilham um SDK devem usar o mesmo gerenciador de dependências.


## Fixando versões de pacotes {#locking-package-versions}

Quando o build é concluído com sucesso, o servidor retorna um arquivo `Package.resolved` que lista a versão e o commit exatos de cada pacote no grafo, incluindo as dependências dos pacotes. Ele é colocado na pasta de build do projeto, por exemplo `build/arm64-ios/Package.resolved`.

Copie esse arquivo para a extensão, ao lado de `SwiftPackages.json` (por exemplo, `manifests/ios/Package.resolved`), para fixar as versões dos pacotes. O servidor de build passa a usar as versões fixadas enquanto elas atenderem aos requisitos em `SwiftPackages.json`. Isso também acelera o build: sem um arquivo `Package.resolved`, o servidor descobre as dependências dos pacotes passo a passo, o que pode demorar muito para pacotes com muitas dependências.

Se várias extensões incluírem um arquivo `Package.resolved` para a mesma plataforma, apenas um deles será usado.


## Vinculação estática e dinâmica {#static-and-dynamic-linking}

Por padrão, todos os pacotes Swift são combinados em uma biblioteca estática, que é vinculada ao executável da engine.

Alguns SDKs não podem ser combinados em uma biblioteca estática, fazendo a vinculação da engine falhar com erros de símbolos duplicados. Nesse caso, defina `"wrapperType": "dynamic"` em `SwiftPackages.json`. Os pacotes serão então compilados em um framework dinâmico, que é incorporado ao bundle da aplicação.


## Recursos e manifestos de privacidade {#resources-and-privacy-manifests}

Os bundles de recursos e os manifestos de privacidade (`PrivacyInfo.xcprivacy`) dos pacotes são incluídos no bundle da aplicação da mesma forma que nas dependências CocoaPods.


## Migrando de CocoaPods {#migrating-from-cocoapods}

Muitos SDKs são publicados tanto como pod quanto como pacote Swift. Para migrar uma extensão de um `Podfile` para um arquivo `SwiftPackages.json`:

1. Encontre o repositório git do pacote Swift na documentação do SDK. Frequentemente, é o mesmo repositório do pod.
2. Encontre os nomes dos produtos no arquivo `Package.swift` do pacote. Nomes de pods e de produtos costumam ser diferentes.
3. Substitua o `Podfile` por um arquivo `SwiftPackages.json`. A versão de `platform :ios` do `Podfile` passa a ser `minVersion`.
4. Verifique se as linhas `#import` da extensão ainda correspondem aos nomes dos módulos dos produtos.

Por exemplo, este `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

se torna este `SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "12.0",
  "packages": [
    {
      "url": "https://github.com/facebook/facebook-ios-sdk.git",
      "version": "17.0.0",
      "products": ["FacebookCore", "FacebookLogin", "FacebookShare", "FacebookGamingServices"]
    }
  ]
}
```

Nesse caso, os módulos mantêm seus nomes, portanto `#import <FBSDKCoreKit/FBSDKCoreKit.h>` funciona com ambos.


## Limitações {#limitations}

* Apenas repositórios de pacotes acessíveis publicamente por `https://` são aceitos. Registros de pacotes Swift não são aceitos.
* Os arquivos `Package.swift` e os plugins dos pacotes são executados sem acesso à rede no servidor de build. O próprio servidor baixa os pacotes e seus frameworks binários antes de compilar os pacotes.
* Compilar pacotes que contêm catálogos de assets (`.xcassets`) para iOS exige um servidor de build que use Xcode 27 ou posterior. Com uma versão anterior do Xcode, o build falha com um erro que identifica esses pacotes.
* Os arquivos `SwiftPackages.json` de um projeto podem declarar no máximo 32 pacotes e 64 produtos por plataforma.


## Solução de problemas {#troubleshooting}

`'Module/Header.h' file not found` ou símbolos indefinidos
: Verifique se os `products` em `SwiftPackages.json` são nomes de produtos de `Package.swift` e se o cabeçalho pertence a um deles. Um servidor de build sem suporte ao Swift Package Manager ignora `SwiftPackages.json`, e a extensão falha ao compilar ou vincular da mesma forma.

`The Swift package graph did not resolve within the ... time budget`
: Os pacotes têm dependências demais para serem descobertas sem um arquivo de bloqueio. Adicione um arquivo `Package.resolved` ao lado de `SwiftPackages.json`, conforme descrito em [Fixando versões de pacotes](#locking-package-versions). Como o build não foi concluído, crie o arquivo localmente, por exemplo adicionando os mesmos pacotes a um projeto Xcode. O Xcode armazena o arquivo em `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Servidor de build local {#local-build-server}

Os pacotes Swift são compilados pelo servidor de build macOS. Para usar pacotes Swift com um [servidor de build local](/manuals/extender-local-setup), ele precisa de uma instalação completa do Xcode (apenas as Command Line Tools não bastam), [XcodeGen](https://github.com/yonaskolb/XcodeGen) e suporte ao Swift Package Manager habilitado pela configuração `extender.spm.enabled`. Consulte a [documentação do servidor de build no GitHub](https://github.com/defold/extender) para mais informações.
