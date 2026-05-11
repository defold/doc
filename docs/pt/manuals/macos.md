---
title: Desenvolvimento Defold para a plataforma macOS
brief: Este manual descreve como compilar e executar aplicações Defold no macOS
---

# Desenvolvimento para macOS

Desenvolver aplicações Defold para a plataforma macOS é um processo direto, com pouquíssimas considerações.

## Configurações do projeto

A configuração específica de uma aplicação macOS é feita na [seção macOS](/manuals/project-settings/#macos) do arquivo de configurações *game.project*.

## Ícone da aplicação

O ícone da aplicação usado para um jogo macOS deve estar no formato .`icns`. Você pode criar facilmente um arquivo `.icns` a partir de um conjunto de arquivos `.png` reunidos como um `.iconset`. Siga as [instruções oficiais para criar um arquivo `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Um resumo breve das etapas envolvidas:

* Crie uma pasta para os ícones, por exemplo `game.iconset`
* Copie os arquivos de ícone para a pasta criada:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Converta a pasta `.iconset` em um arquivo `.icns` usando a ferramenta de linha de comando `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Publicando sua aplicação
Você pode publicar sua aplicação na Mac App Store, usando uma loja ou portal de terceiros como Steam ou itch.io, ou por conta própria por meio de um site. Antes de publicar sua aplicação, você precisa prepará-la para envio. As etapas a seguir são necessárias independentemente de como você pretende distribuir a aplicação:

* 1) Certifique-se de que qualquer pessoa possa executar seu jogo adicionando as permissões de execução (o padrão é que apenas o proprietário do arquivo tenha permissões de execução):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* 2) Crie um arquivo de entitlements especificando as permissões exigidas pelo seu jogo. Para a maioria dos jogos, as seguintes permissões são suficientes:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Indica se o app pode criar memória gravável e executável usando a flag MAP_JIT
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Indica se o app pode criar memória gravável e executável sem as restrições impostas pelo uso da flag MAP_JIT
  * `com.apple.security.cs.allow-dyld-environment-variables` - Indica se o app pode ser afetado por variáveis de ambiente do linker dinâmico, que você pode usar para injetar código no processo do app

Algumas aplicações também podem precisar de entitlements adicionais. A extensão Steamworks precisa deste entitlement extra:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - Indica se o app pode carregar plug-ins ou frameworks arbitrários sem exigir assinatura de código.

Todos os entitlements que podem ser concedidos a uma aplicação estão listados na [documentação oficial para desenvolvedores Apple](https://developer.apple.com/documentation/bundleresources/entitlements).

* 3) Assine seu jogo usando `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Publicando fora da Mac App Store
A Apple exige que todo software distribuído fora da Mac App Store seja notarizado pela Apple para executar por padrão no macOS Catalina. Consulte a [documentação oficial](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) para aprender como adicionar notarização a um ambiente de build por script fora do Xcode. Um resumo breve das etapas envolvidas:

* 1) Siga as etapas acima de adicionar permissões e assinar a aplicação.

* 2) Compacte e envie seu jogo para notarização usando `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

* 3) Verifique o status do envio usando o UUID de requisição retornado pela chamada a `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

* 4) Aguarde até que o status se torne `success` e grampeie o ticket de notarização ao jogo:

```
$ xcrun stapler staple "Game.app"
```

* 5) Seu jogo agora está pronto para distribuição.

## Publicando na Mac App Store
O processo de publicação na Mac App Store é bem documentado na [documentação Apple Developer](https://developer.apple.com/macos/submit/). Certifique-se de adicionar permissões e assinar a aplicação com `codesign` conforme descrito acima antes de enviar.

Observação: o jogo não precisa ser notarizado ao publicar na Mac App Store.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
