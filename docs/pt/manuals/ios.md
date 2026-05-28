---
title: Desenvolvimento Defold para a plataforma iOS
brief: Este manual explica como compilar e executar jogos e apps em dispositivos iOS no Defold.
---

# Desenvolvimento para iOS

::: sidenote
Empacotar um jogo para iOS está disponível apenas na versão macOS do Defold Editor.
:::

O iOS exige que _qualquer_ app que você compile e queira executar no seu telefone ou tablet _seja_ assinado com um certificado emitido pela Apple e um perfil de provisionamento. Este manual explica as etapas envolvidas em empacotar seu jogo para iOS. Durante o desenvolvimento, executar seu jogo pelo [aplicativo de desenvolvimento](/manuals/dev-app) costuma ser preferível, pois permite fazer hot reload de conteúdo e código diretamente para o dispositivo.

## O processo de assinatura de código da Apple

A segurança associada a apps iOS consiste em vários componentes. Você pode obter acesso às ferramentas necessárias inscrevendo-se no [Apple's iOS Developer Program](https://developer.apple.com/programs/). Depois de se inscrever, acesse o [Apple's Developer Member Center](https://developer.apple.com/membercenter/index.action).

![Apple Member Center](images/ios/apple_member_center.png)

A seção *Certificates, Identifiers & Profiles* contém todas as ferramentas de que você precisa. A partir dela, você pode criar, excluir e editar:

Certificates
: Certificados criptográficos emitidos pela Apple que identificam você como desenvolvedor. Você pode criar certificados de desenvolvimento ou de produção. Certificados de desenvolvedor permitem testar determinados recursos, como o mecanismo de compras dentro do aplicativo, em um ambiente de teste sandbox. Certificados de produção são usados para assinar o app final para envio à App Store. Você precisa de um certificado para assinar apps antes de poder colocá-los no seu dispositivo para teste.

Identifiers
: Identificadores para vários usos. É possível registrar identificadores curinga (ou seja, `some.prefix.*`), que podem ser usados com vários apps. App IDs podem conter informações de Application Service, como se o app habilita integração com Passbook, Game Center etc. Esses App IDs não podem ser identificadores curinga. Para que Application Services funcionem, o *bundle identifier* da sua aplicação deve corresponder ao identificador do App ID.

Devices
: Cada dispositivo de desenvolvimento precisa ser registrado com seu UDID (Unique Device IDentifier, veja abaixo).

Provisioning Profiles
: Perfis de provisionamento associam certificados a App IDs e a uma lista de dispositivos. Eles indicam qual app, de qual desenvolvedor, tem permissão para estar em quais dispositivos.

Ao assinar seus jogos e apps no Defold, você precisa de um certificado válido e de um perfil de provisionamento válido.

::: sidenote
Algumas das coisas que você pode fazer na página inicial do Member Center também podem ser feitas dentro do ambiente de desenvolvimento Xcode, se você o tiver instalado.
:::

Identificador do dispositivo (UDID)
: O UDID de um dispositivo iOS pode ser encontrado conectando o dispositivo a um computador via wifi ou cabo. Abra o Xcode e selecione <kbd>Window ▸ Devices and Simulators</kbd>. O número de série e o identificador são exibidos quando você seleciona seu dispositivo.

  ![xcode devices](images/ios/xcode_devices.png)

  Se você não tiver o Xcode instalado, pode encontrar o identificador no iTunes. Clique no símbolo de dispositivos e selecione seu dispositivo.

  ![itunes devices](images/ios/itunes_devices.png)

  1. Na página *Summary*, localize *Serial Number*.
  2. Clique uma vez em *Serial Number* para que o campo mude para *UDID*. Se você clicar repetidamente, várias informações sobre o dispositivo serão exibidas. Continue clicando até *UDID* aparecer.
  3. Clique com o botão direito na string longa do UDID e selecione <kbd>Copy</kbd> para copiar o identificador para a área de transferência, para que você possa colá-lo facilmente no campo UDID ao registrar o dispositivo no Apple Developer Member Center.

## Desenvolvendo com uma conta gratuita de desenvolvedor Apple

Desde o Xcode 7, qualquer pessoa pode instalar o Xcode e desenvolver no dispositivo gratuitamente. Você não precisa se inscrever no iOS Developer Program. Em vez disso, o Xcode emitirá automaticamente um certificado para você como desenvolvedor (válido por 1 ano) e um perfil de provisionamento para seu app (válido por uma semana) no seu dispositivo específico.

1. Conecte seu dispositivo.
2. Instale o Xcode.
3. Adicione uma nova conta ao Xcode e entre com seu Apple ID.
4. Crie um novo projeto. O modelo mais simples "Single View App" funciona bem.
5. Selecione sua "Team" (criada automaticamente para você) e dê ao app um bundle identifier.

::: important
Anote o bundle identifier, pois você deve usar o mesmo bundle identifier no seu projeto Defold.
:::

6. Certifique-se de que o Xcode criou um *Provisioning Profile* e um *Signing Certificate* para o app.

   ![](images/ios/xcode_certificates.png)

7. Compile o app no seu dispositivo. Na primeira vez, o Xcode pedirá que você habilite o Developer mode e preparará o dispositivo com suporte a depurador. Isso pode levar algum tempo.
8. Depois de verificar que o app funciona, encontre-o no seu disco. Você pode ver o local da build no relatório de build no "Report Navigator".

   ![](images/ios/app_location.png)

9. Localize o app, clique com o botão direito nele e selecione <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. Copie o arquivo "embedded.mobileprovision" para algum lugar no seu disco onde você o encontrará.

   ![](images/ios/free_provisioning.png)

Esse arquivo de provisionamento pode ser usado junto com sua identidade de assinatura de código para assinar apps no Defold por uma semana.

Quando o provisionamento expirar, você precisará compilar o app novamente no Xcode e obter um novo arquivo de provisionamento temporário conforme descrito acima.

## Criando um pacote de aplicação iOS

Quando você tiver a identidade de assinatura de código e o perfil de provisionamento, estará pronto para criar um pacote de aplicação autônomo para seu jogo a partir do editor. Basta selecionar <kbd>Projeto ▸ Empacotar... ▸ Aplicação iOS...</kbd> no menu.

![Signing iOS bundle](images/ios/sign_bundle.png)

Selecione sua identidade de assinatura de código e procure seu arquivo de provisionamento mobile. Selecione para quais arquiteturas (32 bits, 64 bits e o simulador iOS) empacotar, bem como a variante (Debug ou Release). Opcionalmente, você pode desmarcar a caixa de seleção `Sign application` para pular o processo de assinatura e assinar manualmente em uma etapa posterior.

::: important
Você **deve** desmarcar a caixa de seleção `Sign application` ao testar seu jogo no simulador iOS. Você conseguirá instalar a aplicação, mas ela não iniciará.
:::

Pressione *Criar Pacote…* e então será solicitado que você especifique onde no seu computador o pacote será criado.

![ipa iOS application bundle](images/ios/ipa_file.png){.left}

Você especifica qual ícone usar para o app, o storyboard da tela de lançamento e assim por diante no arquivo de configurações do projeto *game.project*, na [seção iOS](/manuals/project-settings/#ios).

:[Build Variants](../shared/build-variants.md)

## Instalando e iniciando o pacote em um iPhone conectado

Você pode instalar e iniciar o pacote criado usando as caixas de seleção "Install on connected device" e "Launch installed app" do editor no diálogo Bundle:

![Install and launch iOS bundle](images/ios/install_and_launch.png)

Você precisa ter a ferramenta de linha de comando [ios-deploy](https://github.com/ios-control/ios-deploy) instalada para que esse recurso funcione. A forma mais simples de instalá-la é usando Homebrew:
```
$ brew install ios-deploy
```

Se o editor não conseguir detectar o local de instalação da ferramenta ios-deploy, você precisará especificá-lo em [Preferências](/manuals/editor-preferences/#tools). 

### Criando um storyboard

Você cria um arquivo de storyboard usando o Xcode. Inicie o Xcode e crie um novo projeto. Selecione iOS e Single View App:

![Create project](images/ios/xcode_create_project.png)

Clique em Next e prossiga para configurar seu projeto. Insira um Product Name:

![Project settings](images/ios/xcode_storyboard_create_project_settings.png)

Clique em Create para finalizar o processo. Seu projeto agora está criado e podemos prosseguir para criar o storyboard:

![The project view](images/ios/xcode_storyboard_project_view.png)

Arraste e solte uma imagem para importá-la para o projeto. Em seguida, selecione `Assets.xcassets` e solte a imagem em `Assets.xcassets`:

![Add image](images/ios/xcode_storyboard_add_image.png)

Abra `LaunchScreen.storyboard` e clique no botão de mais (<kbd>+</kbd>). Digite "imageview" no diálogo para encontrar o componente ImageView.

![Add image view](images/ios/xcode_storyboard_add_imageview.png)

Arraste o componente Image View para o storyboard:

![Add to storyboard](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Selecione a imagem que você adicionou anteriormente a `Assets.xcassets` no menu suspenso Image:

![](images/ios/xcode_storyboard_select_image.png)

Posicione a imagem e faça quaisquer outros ajustes necessários, talvez adicionando um Label ou outro elemento de UI. Quando terminar, defina o scheme ativo para "Build -> Any iOS Device (`arm64`, `armv7`)" (ou "Generic iOS Device") e selecione Product -> Build. Aguarde o processo de build terminar.

::: sidenote
Se você tiver apenas a opção `arm64` em "Any iOS Device (arm64)", altere `iOS Deployment target` para 10.3 nas configurações "Project -> Basic -> Deployment". Isso tornará seu storyboard compatível com dispositivos `armv7` (por exemplo, iPhone5c)  
:::

Se você usar imagens no storyboard, elas não serão incluídas automaticamente no seu `LaunchScreen.storyboardc`. Use o campo `Bundle Resources` em *game.project* para incluir recursos.
Por exemplo, crie a pasta `LaunchScreen` no projeto Defold e uma pasta `ios` dentro dela (a pasta `ios` é necessária para incluir esses arquivos apenas em pacotes iOS), então coloque seus arquivos em `LaunchScreen/ios/`. Adicione esse caminho em `Bundle Resources`.

![](images/ios/bundle_res.png)

A última etapa é copiar o arquivo compilado `LaunchScreen.storyboardc` para seu projeto Defold. Abra o Finder no seguinte local e copie o arquivo `LaunchScreen.storyboardc` para seu projeto Defold:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
O usuário do fórum Sergey Lerg preparou [um tutorial em vídeo mostrando o processo](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo).
:::

Depois de obter o arquivo storyboard, você pode referenciá-lo a partir de *game.project*.


### Criando um catálogo de assets de ícones

Usar um asset catalog é a forma preferida da Apple para gerenciar os ícones da sua aplicação. Na verdade, é a única forma de fornecer o ícone usado na listagem da App Store. Você cria um asset catalog da mesma forma que um storyboard, usando o Xcode. Inicie o Xcode e crie um novo projeto. Selecione iOS e Single View App:

![Create project](images/ios/xcode_create_project.png)

Clique em Next e prossiga para configurar seu projeto. Insira um Product Name:

![Project settings](images/ios/xcode_icons_create_project_settings.png)

Clique em Create para finalizar o processo. Seu projeto agora está criado e podemos prosseguir para criar o asset catalog:

![The project view](images/ios/xcode_icons_project_view.png)

Arraste e solte imagens nas caixas vazias que representam os diferentes tamanhos de ícone compatíveis:

![Add icons](images/ios/xcode_icons_add_icons.png)

::: sidenote
Não adicione ícones para Notifications, Settings ou Spotlight.
:::

Quando terminar, defina o scheme ativo para "Build -> Any iOS Device (arm64)" (ou "Generic iOS Device") e selecione <kbd>Product</kbd> -> <kbd>Build</kbd>. Aguarde o processo de build terminar.

::: sidenote
Certifique-se de compilar para "Any iOS Device (arm64)" ou "Generic iOS Device"; caso contrário, você receberá o erro `ERROR ITMS-90704` ao enviar sua build.
:::

![Build project](images/ios/xcode_icons_build.png)

A última etapa é copiar o arquivo compilado `Assets.car` para seu projeto Defold. Abra o Finder no seguinte local e copie o arquivo `Assets.car` para seu projeto Defold:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

Depois de obter o arquivo asset catalog, você pode referenciá-lo e aos ícones a partir de *game.project*:

![Add icon and asset catalog to game.project](images/ios/defold_icons_game_project.png)

::: sidenote
O ícone da App Store não precisa ser referenciado a partir de *game.project*. Ele é extraído automaticamente do arquivo `Assets.car` ao enviar para o iTunes Connect.
:::


## Instalando um pacote de aplicação iOS

O editor grava um arquivo *.ipa*, que é um pacote de aplicação iOS. Para instalar o arquivo no seu dispositivo, você pode usar uma das seguintes ferramentas:

* Xcode pela janela "Devices and Simulators"
* Ferramenta de linha de comando [`ios-deploy`](https://github.com/ios-control/ios-deploy)
* [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/) da macOS App Store
* iTunes

Você também pode usar a ferramenta de linha de comando `xcrun simctl` para trabalhar com os simuladores iOS disponíveis pelo Xcode:

```
# mostrar uma lista de dispositivos disponíveis
xcrun simctl list

# iniciar um simulador iPhone X
xcrun simctl boot "iPhone X"

# instalar your.app em um simulador iniciado
xcrun simctl install booted your.app

# iniciar o simulador
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## Informações de Export Compliance

Ao enviar seu jogo para a App Store, você será solicitado a fornecer informações de Export Compliance em relação ao uso de criptografia no seu jogo. [A Apple explica por que isso é necessário](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations):

"Quando você envia seu app para o TestFlight ou para a App Store, você envia seu app para um servidor nos Estados Unidos. Se você distribui seu app fora dos EUA ou do Canadá, seu app está sujeito às leis de exportação dos EUA, independentemente de onde sua entidade legal esteja sediada. Se seu app usa, acessa, contém, implementa ou incorpora criptografia, isso é considerado uma exportação de software de criptografia, o que significa que seu app está sujeito aos requisitos de conformidade de exportação dos EUA, bem como aos requisitos de conformidade de importação dos países onde você distribui seu app."

A engine de jogos Defold usa criptografia para os seguintes fins:

* Fazer chamadas por canais seguros (ou seja, HTTPS e SSL)
* Proteção de copyright do código Lua (para impedir duplicação)

Esses usos de criptografia na engine Defold são isentos de requisitos de documentação de conformidade de exportação segundo as leis dos Estados Unidos e da União Europeia. A maioria dos projetos Defold permanecerá isenta, mas a adição de outros métodos criptográficos pode alterar esse status. É sua responsabilidade garantir que seu projeto atenda aos requisitos dessas leis e às regras da App Store. Veja a [Visão geral de Export Compliance](https://help.apple.com/app-store-connect/#/dev88f5c7bf9) da Apple para mais informações.

Se você acredita que seu projeto está isento, defina a chave [`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) como `False` no `Info.plist` do projeto; veja [Manifestos de Aplicação](/manuals/extensions-manifest-merge-tool) para mais detalhes.

## FAQ
:[iOS FAQ](../shared/ios-faq.md)
