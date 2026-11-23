---
title: Usando Swift em extensões nativas para iOS e macOS
brief: Este manual explica como escrever em Swift o código de uma extensão nativa para builds de iOS e macOS.
---

# Swift em extensões nativas {#swift-in-native-extensions}

Muitas APIs da Apple, como StoreKit 2 e CryptoKit, só podem ser usadas em Swift. Uma extensão nativa (native extension) pode incluir seus próprios arquivos-fonte Swift junto aos arquivos Objective-C++. O servidor de build compila esses arquivos com o restante da extensão e vincula o resultado à engine. Esse recurso é independente dos [pacotes Swift](/manuals/extensions-spm) e do [CocoaPods](/manuals/extensions-cocoapods), que fornecem dependências prontas para uso.

O servidor compila o código Swift para macOS (`arm64` e `x86_64`) e iOS (dispositivos e simulador). Nos builds para outras plataformas, ele ignora os arquivos Swift.


## Adicionando arquivos-fonte Swift {#adding-swift-sources}

Coloque os arquivos `.swift` na pasta `src` da extensão, junto aos arquivos C++ e Objective-C++.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Mantenha todos os arquivos Swift em `src`. Se o servidor encontrar um arquivo Swift em `commonsrc` ou `pluginsrc`, o build para macOS ou iOS falhará.

O compilador reúne todos os arquivos Swift de uma extensão em um único módulo Swift. Para dar nome ao módulo, ele usa o valor de `name` em `ext.manifest` e substitui por `_` cada caractere que não seja uma letra, um dígito ou um sublinhado (`My-Extension` se torna `My_Extension`). O modo de linguagem usado é o Swift 5.

O nome do módulo deve ser diferente dos nomes dos módulos que o código importa. Uma extensão chamada `StoreKit` não pode usar `import StoreKit`, pois o compilador interpreta essa instrução como uma importação do próprio módulo.


## Chamando código Swift a partir de Objective-C++ {#calling-swift-from-objective-c}

O ponto de entrada de uma extensão continua sendo uma função C++ registrada com `DM_DECLARE_EXTENSION`. Por isso, a extensão precisa de pelo menos um arquivo `.cpp` ou `.mm`. Para chamar o código Swift a partir desse arquivo, use o cabeçalho gerado `<Module>-Swift.h`.

Apenas classes, protocolos e métodos marcados com `@objc` ficam visíveis em Objective-C. Declare as classes como `public` e faça com que herdem de `NSObject`.

`src/Greeter.swift`:

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* O cabeçalho gerado importa `Foundation`. Para tipos de outros frameworks, ele contém apenas declarações antecipadas. Importe o cabeçalho do framework (por exemplo, `UIKit`) no arquivo `.mm` antes de chamar métodos que usam esses tipos.
* As funções `throws` ficam disponíveis como métodos com um parâmetro `NSError **`. As funções `async` ficam disponíveis como métodos com uma função de retorno chamada ao término da operação.
* Recursos exclusivos do Swift, como tipos genéricos, enumerações com valores associados e estruturas, não ficam visíveis em Objective-C. Encapsule-os em uma classe `@objc`.
* Os arquivos `.mm` só são compilados para iOS e macOS. Em outras plataformas, o build de uma extensão que contém apenas arquivos `.mm` e `.swift` falha com o erro `Extension has no source!`. Para compilar a extensão também em outras plataformas, coloque `DM_DECLARE_EXTENSION` em um arquivo `.cpp`. Nesse arquivo, proteja a chamada ao código do arquivo `.mm` com uma condição de compilação que verifique `DM_PLATFORM_IOS` ou `DM_PLATFORM_OSX`.


## Chamando código Objective-C a partir de Swift {#calling-objective-c-from-swift}

Para usar declarações Objective-C ou C no código Swift, adicione à pasta `src` um cabeçalho de interoperabilidade (bridging header) com o nome `<Module>-Bridging-Header.h`, por exemplo `src/MyExtension-Bridging-Header.h`.

```cpp
#import "mynative.h"
```

Se esse cabeçalho existir, ele será importado automaticamente no módulo Swift. O compilador procura os cabeçalhos que ele inclui na pasta `include` da extensão e nas pastas listadas em `additionalSwiftIncludePaths` (veja abaixo).

Em Swift, use a instrução `import` habitual para importar frameworks da Apple, como `Foundation`, `UIKit` e `StoreKit`. Os frameworks listados em `frameworks` e `weakFrameworks` no arquivo `ext.manifest` são vinculados como de costume. A maioria dos frameworks do sistema é vinculada automaticamente quando o código Swift os importa.


## Usando pacotes Swift no código Swift {#using-swift-packages-from-swift}

Os produtos dos [pacotes Swift](/manuals/extensions-spm) que a extensão declara em `SwiftPackages.json` ficam disponíveis para o código Swift da extensão. Importe o módulo em um arquivo Swift.

```swift
import Foundation
import Sentry

@objc(MyExtensionCrashReporter)
public class CrashReporter: NSObject {
    @objc public func start(dsn: String) {
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

Você pode importar os cabeçalhos Objective-C de um pacote no cabeçalho de interoperabilidade da mesma forma que em um arquivo `.mm`.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Declare o pacote no arquivo `SwiftPackages.json` da extensão que o utiliza. O servidor de build compila primeiro os pacotes e depois o código Swift da extensão. Se um pacote exigir uma versão do sistema operacional posterior à mínima aceita pela engine, defina a versão exigida em `minVersion` no arquivo `SwiftPackages.json`. O código Swift da extensão também será compilado para essa versão. Não há suporte ao uso de dependências do CocoaPods diretamente em Swift. Use essas dependências no arquivo Objective-C++ e passe ao código Swift o que ele precisar.


## Opções do compilador {#compiler-options}

Defina as opções do compilador Swift no arquivo `ext.manifest`, no mesmo `context` usado para as opções do compilador C++.

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["include/vendor/headers"]
            additionalFrameworkSearchPaths: ["lib/ios/vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - As definições configuradas para C++ são passadas ao Swift como nomes para compilação condicional. Assim, `#if MY_DEFINE` também funciona em Swift. O Swift só aceita nomes, por isso o valor de uma definição como `MY_DEFINE=1` é descartado.
* `swiftFlags` - Flags adicionais para o compilador Swift. Coloque cada flag e cada valor em um item separado da lista. Se uma flag não estiver na lista de permissões, o build falhará com o erro `Invalid flag - 'swiftFlags'`. Se um valor contiver espaços em branco, uma barra invertida ou sintaxe de template, ou se indicar um arquivo de resposta, o build falhará com o erro `invalid 'swiftFlags' value`. Você pode usar as seguintes flags.
  * `-enable-upcoming-feature <Feature>` - Ativa um recurso de uma versão futura da linguagem, por exemplo `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` e `-Onone` - Definem o nível de otimização. O padrão é `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Pastas em que o compilador Swift procura cabeçalhos e módulos, além da pasta `include` da extensão.
* `additionalFrameworkSearchPaths` - Pastas em que o compilador procura frameworks, além da pasta `lib/<platform>` da extensão. Tanto o compilador Swift quanto o compilador de C++ e Objective-C++ consultam essas pastas ao compilar o código-fonte da extensão. O linker também as consulta.

Os caminhos são relativos à pasta da extensão, devem permanecer dentro dela e só podem conter letras, dígitos e os caracteres `._+-/`. Apenas as pastas `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` e `res/<platform>` da extensão são enviadas ao servidor de build. Os caminhos devem apontar para dentro de uma delas. Arquivos em outras pastas, como uma pasta `vendor` na raiz da extensão, não ficam disponíveis durante o build.

As chaves Swift da plataforma `ios` se aplicam tanto aos dispositivos quanto ao simulador. Um servidor de build anterior ao suporte a Swift rejeita essas chaves com o erro `Manifest context variable unsupported`. Nesse caso, o build do projeto falha até que você atualize a versão do Defold e o servidor de build.


## Versões mínimas do sistema operacional {#minimum-os-versions}

O ambiente de execução do Swift faz parte de todas as versões de iOS e macOS compatíveis com o Defold. O código Swift é compilado para a versão mínima de iOS ou macOS do build, e o aplicativo usa o ambiente de execução do Swift fornecido pelo sistema operacional. Use `#available` para verificar a disponibilidade de uma API antes de chamá-la se ela for posterior à versão mínima.

Algumas partes do ambiente de execução só foram incorporadas ao sistema operacional em versões mais recentes. Por exemplo, `MutableSpan` e os tipos relacionados fazem parte do iOS 26 e do macOS 26. Se a versão mínima for anterior e seu código Swift ou um framework dinâmico de um pacote usar um desses recursos, o aplicativo poderá precisar de uma biblioteca adicional para funcionar nesses dispositivos. O servidor de build cuida disso automaticamente. Assim como o Xcode, ele identifica as dependências da engine e das bibliotecas dinâmicas incorporadas com ela e adiciona as bibliotecas necessárias ao aplicativo. No iOS, o servidor coloca essas bibliotecas na pasta `Frameworks` do aplicativo e as assina junto com o restante do código.

A versão mínima de um build é a versão mínima aceita pela engine, determinada pela versão do Defold e pelo servidor de build. O campo `minVersion` de um arquivo `SwiftPackages.json` permite aumentar esse mínimo para os pacotes, o código Swift e a vinculação da engine, conforme descrito no [manual do Swift Package Manager](/manuals/extensions-spm). Não é possível reduzi-lo.


## Limitações {#limitations}

* A extensão ainda precisa de um arquivo C++ ou Objective-C++ com `DM_DECLARE_EXTENSION`. O código Swift não pode registrar a extensão e não tem acesso à API C++ do SDK do Defold (`dmsdk`). Use essa API no arquivo Objective-C++. Os cabeçalhos de `dmsdk` compatíveis com C, como `dmsdk/dlib/hash.h`, podem ser incluídos no cabeçalho de interoperabilidade. Um build que contém apenas arquivos `.swift` falha na etapa de vinculação com um erro de símbolo indefinido que contém o nome da extensão.
* Não há suporte ao uso de dependências do CocoaPods diretamente em Swift. Use essas dependências no arquivo Objective-C++ e passe ao código Swift o que ele precisar.
* Apenas o modo de linguagem Swift 5 é aceito. A interoperabilidade com C++ não está habilitada.
* O Defold aceita arquivos-fonte Swift a partir da versão 1.14.2. Em um servidor de build com um SDK anterior, o build falha com o erro `Swift sources are not supported by this Defold SDK version`.
* Ao gerar o artefato `library` (`--build-artifacts library` no [Bob](/manuals/bob)), o servidor não compila os arquivos-fonte Swift. Por isso, um arquivo Objective-C++ que importe `<Module>-Swift.h` não compila nesse tipo de build.


## Solução de problemas {#troubleshooting}

`no such module 'Name'`
: O módulo não é um produto de um pacote declarado em um arquivo `SwiftPackages.json`. Verifique se `products` lista um produto que fornece o módulo, conforme descrito no [manual do Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Mova os arquivos `.swift` para a pasta `src` da extensão.

`'MyExtension-Swift.h' file not found`
: O nome do módulo é gerado a partir de `name` em `ext.manifest`. Confira o nome na linha `#import`.

`unknown type name 'MyExtensionGreeter'`
: A classe não aparece no cabeçalho gerado. Confira se ela está marcada como `public` e `@objc`, se herda de `NSObject` e se o arquivo `.mm` usa o nome especificado em `@objc(...)`.

`cannot find 'AppStore' in scope` junto com `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: A extensão tem o mesmo nome de um módulo que ela importa. Altere o nome da extensão em `ext.manifest`.

`Undefined symbols ... _MyExtension`
: A extensão não contém `DM_DECLARE_EXTENSION`. Adicione um arquivo `.mm` que registre a extensão conforme descrito acima.

`Invalid flag - 'swiftFlags'`
: A flag não está na lista de permissões. Remova-a ou use uma das flags listadas.

`invalid 'swiftFlags' value`
: O valor contém espaços em branco, uma barra invertida ou sintaxe de template, ou indica um arquivo de resposta. Coloque cada flag e cada valor em um item separado da lista.
