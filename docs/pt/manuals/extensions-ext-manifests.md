---
title: Extensões nativas - manifestos de extensão
brief: Este manual descreve o manifesto de extensão e sua relação com o manifesto da aplicação e o manifesto da engine.
---

# Arquivos de manifesto de extensão, aplicação e engine

O manifesto de extensão é um arquivo de configuração com flags e definições usados ao compilar uma única extensão. Essa configuração é combinada com uma configuração no nível da aplicação e com uma configuração base da própria engine Defold.

## App Manifest

O manifesto da aplicação (extensão de arquivo `.appmanifest`) é uma configuração no nível da aplicação que define como compilar seu jogo nos servidores de build. O manifesto da aplicação permite remover partes da engine que você não usa. Se você não precisa de uma engine de física, pode removê-la do executável para reduzir seu tamanho. Saiba como excluir recursos não usados [no manual de manifesto da aplicação](/manuals/app-manifest).

## Engine manifest

A engine Defold tem um manifesto de build (`build.yml`) que é incluído com cada release da engine e do SDK do Defold. O manifesto controla quais versões de SDK usar, quais compiladores, linkers e outras ferramentas executar, e quais flags padrão de compilação e link passar para essas ferramentas. O manifesto pode ser encontrado em share/extender/build_input.yml [no GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Extension Manifest

O manifesto de extensão (`ext.manifest`), por outro lado, é um arquivo de configuração específico de uma extensão. O manifesto de extensão controla como o código-fonte da extensão é compilado e vinculado, e quais bibliotecas adicionais devem ser incluídas.

Os três arquivos de manifesto compartilham a mesma sintaxe para que possam ser mesclados e controlar por completo como as extensões e o jogo são compilados.

Para cada extensão compilada, os manifestos são combinados assim:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Isso permite que o usuário sobrescreva o comportamento padrão da engine e também de cada extensão. E, para a etapa final de link, mesclamos o manifesto da aplicação com o manifesto do Defold:

	manifest = merge(game.appmanifest, build.yml)


### O arquivo ext.manifest

Além do nome da extensão, o arquivo de manifesto pode conter flags de compilação específicas de plataforma, flags de link, bibliotecas e frameworks. Se o arquivo *ext.manifest* não contiver uma seção "platforms", ou se uma plataforma estiver ausente da lista, a plataforma para a qual você empacotar ainda será compilada, mas sem flags extras definidas.

Veja um exemplo:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Chaves permitidas

As chaves permitidas para flags de compilação específicas de plataforma são:

* `frameworks` - Frameworks da Apple a incluir ao compilar (iOS e macOS)
* `weakFrameworks` - Frameworks da Apple a incluir opcionalmente ao compilar (iOS e macOS)
* `flags` - Flags que devem ser passadas ao compilador
* `linkFlags` - Flags que devem ser passadas ao linker
* `libs` - Bibliotecas adicionais a incluir ao fazer o link
* `defines` - Definições a configurar ao compilar
* `aaptExtraPackages` - Nome de pacote extra que deve ser gerado (Android)
* `aaptExcludePackages` - Expressão regular (ou nomes exatos) de pacotes a excluir (Android)
* `aaptExcludeResourceDirs` - Expressão regular (ou nomes exatos) de diretórios de recursos a excluir (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - Essas flags são usadas para remover itens definidos anteriormente no contexto da plataforma.

Para todas as palavras-chave, aplicamos um filtro de lista de permissões. Isso evita manipulação ilegal de caminhos e acesso a arquivos fora da pasta enviada para o build.
