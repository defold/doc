---
title: Desenvolvimento Defold para a plataforma Android
brief: Este manual descreve como construir e executar aplicações Defold em dispositivos Android
---

# Desenvolvimento Android

Dispositivos Android permitem que você execute livremente seus próprios aplicativos neles. É muito fácil criar uma versão do seu jogo e copiá-la para um dispositivo Android. Este manual explica as etapas envolvidas em empacotar seu jogo para Android. Durante o desenvolvimento, executar seu jogo pelo [aplicativo de desenvolvimento](/manuals/dev-app) muitas vezes é preferível, pois permite usar hot reload de conteúdo e código diretamente no seu dispositivo.

## Processo de assinatura Android e Google Play

O Android exige que todos os APKs sejam assinados digitalmente com um certificado antes de serem instalados em um dispositivo ou atualizados. Se você usar Android App Bundles, precisa assinar apenas seu app bundle antes de enviá-lo para o Play Console, e o [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) cuida do resto. No entanto, você também pode assinar manualmente seu aplicativo para envio para o Google Play, outras lojas de aplicativos e para distribuição fora de qualquer loja.

Quando você cria um pacote de aplicativo Android a partir do editor Defold ou da [ferramenta de linha de comando](/manuals/bob), você pode fornecer um keystore (contendo seu certificado e chave) e a senha do keystore que serão usados ao assinar sua aplicação. Se você não fornecer, o Defold gera um keystore de depuração e o usa ao assinar o pacote de aplicativo.

::: important
Você **nunca** deve enviar sua aplicação para o Google Play se ela foi assinada usando um keystore de depuração. Sempre use um keystore dedicado que você mesmo criou.
:::

## Criando um keystore {#creating-a-keystore}

::: sidenote
O Defold usa um keystore no processo de assinatura Android. [Mais informações estão disponíveis neste post do fórum](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Você pode criar um keystore [usando o Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) ou a partir de um terminal/prompt de comando:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Isso irá criar um arquivo keystore chamado `mykeystore.keystore` contendo uma chave e certificado. O acesso à chave e certificado será protegido pela senha `5Up3r_53cR3t`. A chave e o certificado serão válidos por 25 anos (9125 dias). A chave e o certificado gerados serão identificados pelo alias `myAlias`.

::: important
Certifique-se de armazenar o keystore e a senha associada em um local seguro. Se você assinar e enviar suas aplicações para o Google Play e o keystore ou a senha do keystore for perdida, não há como atualizar a aplicação no Google Play. Você pode evitar isso usando o Google Play App Signing e deixar o Google assinar suas aplicações para você.
:::


## Criando um pacote de aplicativo Android {#creating-an-android-application-bundle}

O editor permite criar facilmente um pacote de aplicativo independente para seu jogo. Antes de empacotar, você pode especificar qual(is) ícone(s) usar para o aplicativo, definir o código de versão etc. no arquivo *game.project* de [configurações do projeto](/manuals/project-settings/#android).

Para empacotar, selecione <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> no menu.

Se você quiser que o editor crie automaticamente certificados de depuração aleatórios, deixe os campos *Keystore* e *Keystore password* vazios:

![Signing Android bundle](images/android/sign_bundle.png)

Se você quiser assinar seu bundle com um keystore específico, especifique o *Keystore* e *Keystore password*. Espera-se que o *Keystore* tenha a extensão de arquivo `.keystore`, enquanto a senha deve ser armazenada em um arquivo de texto com a extensão `.txt`. Também é possível especificar uma *Key password* se a chave no keystore usar uma senha diferente do próprio keystore:

![Signing Android bundle](images/android/sign_bundle2.png)

O Defold tem suporte à criação de arquivos APK e AAB. Selecione APK ou AAB no menu suspenso *Bundle Format*.

Pressione <kbd>Create Bundle</kbd> quando tiver configurado as definições do pacote de aplicativo. Em seguida, você será solicitado a especificar onde em seu computador o pacote será criado.

![Android Application Package file](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Instalando um pacote de aplicativo Android

#### Instalando um APK

Um arquivo *`.apk`* pode ser copiado para seu dispositivo com a ferramenta `adb` ou para o Google Play através do [console do desenvolvedor do Google Play](https://play.google.com/apps/publish/).

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Instalando um APK usando o editor

Você pode instalar e iniciar um arquivo *`.apk`* usando as caixas de seleção "Install on connected device" e "Launch installed app" no diálogo Bundle do editor:

![Install and Launch APK](images/android/install_and_launch.png)

Para que este recurso funcione, você precisará ter o ADB instalado e a *Depuração USB* (*USB debugging*) habilitada no dispositivo conectado. Se o editor não conseguir detectar a localização de instalação da ferramenta de linha de comando ADB, você precisará especificá-la nas [Preferências](/manuals/editor-preferences/#tools).

#### Instalando um AAB

Um arquivo *.aab* pode ser enviado para o Google Play através do [console do desenvolvedor do Google Play](https://play.google.com/apps/publish/). Também é possível gerar um arquivo *`.apk`* a partir de um arquivo *.aab* para instalá-lo localmente usando o [Android bundletool](https://developer.android.com/studio/command-line/bundletool).

## Redução de código Java com R8 {#shrinking-java-code-with-r8}

O R8 reduz o tamanho do código Java removendo código não utilizado, otimizando e ofuscando o código.

### Ativação do R8 {#enabling-r8}

Selecione `/builtins/manifests/android/dmengine.keep` em **Android ▸ R8 Keep Rules** no *game.project*. Isso usa diretamente as regras padrão do Defold:

```ini
[android]
r8_keep_rules = /builtins/manifests/android/dmengine.keep
```

Certifique-se de que cada extensão com código Java forneça um arquivo `.keep` para as classes necessárias em tempo de execução. As regras das extensões são combinadas com as regras selecionadas para o projeto durante o build. Teste um build de lançamento em um dispositivo depois de ativar o R8.

Deixar **R8 Keep Rules** vazio usa o D8 sem remover código não utilizado. Ativar o R8 usa o serviço de build de extensões nativas, mesmo em um projeto sem extensões nativas.

### Adição de regras a uma extensão {#adding-rules-to-an-extension}

As regras de preservação de uma extensão devem ficar no diretório `manifests/android`, ao lado de `build.gradle`. Consulte [regras de preservação do R8 para extensões Android](/manuals/extensions/#r8-keep-rules-for-android) para saber como adicionar um arquivo e preservar as classes Java da extensão.

### Preservação do mapeamento de ofuscação {#keeping-the-obfuscation-mapping}

Ative **Generate debug symbols** no diálogo de empacotamento Android ou passe `--with-symbols` ao Bob para preservar o `mapping.txt` do R8 quando o build gerar esse arquivo. Por exemplo, a partir do diretório do projeto:

```sh
java -jar bob.jar --platform arm64-android --variant release \
  --archive --with-symbols --bundle-output build/android \
  resolve build bundle
```

O mapeamento é salvo como `<binary-name>.apk.symbols/mapping.txt` ao lado do APK ou AAB gerado. Por exemplo, com o título de projeto `My Game`, o comando acima produz `build/android/MyGame/MyGame.apk.symbols/mapping.txt`.

Guarde o arquivo de mapeamento junto com a versão exata da qual ele foi gerado. Ele converte os nomes Java ofuscados de volta aos nomes originais para interpretar rastreamentos de pilha; um mapeamento de outro build pode produzir resultados incorretos.

## Permissões

A engine Defold requer várias permissões diferentes para que todos os recursos da engine funcionem. As permissões são definidas no `AndroidManifest.xml`, especificado no arquivo *game.project* de [configurações do projeto](/manuals/project-settings/#android). Você pode ler mais sobre permissões Android na [documentação oficial](https://developer.android.com/guide/topics/permissions/overview). As seguintes permissões são solicitadas no manifesto padrão:

### android.permission.INTERNET e android.permission.ACCESS_NETWORK_STATE (Nível de proteção: normal)
Permite que aplicativos abram soquetes de rede (*network sockets*) e acessem informações sobre redes. Essas permissões são necessárias para acesso à internet. ([Documentação oficial Android](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) e ([Documentação oficial Android](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Nível de proteção: normal)
Permite usar PowerManager WakeLocks para impedir que o processador entre em modo de suspensão ou que a tela escureça. Esta permissão é necessária para impedir temporariamente que o dispositivo entre em suspensão enquanto recebe uma notificação push. ([Documentação oficial Android](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))

## Usando AndroidX
O AndroidX é uma grande melhoria em relação à biblioteca de suporte Android original, que não é mais mantida. Os pacotes AndroidX substituem completamente a Biblioteca de Suporte, fornecendo paridade de recursos e novas bibliotecas. A maioria das extensões Android no [Portal de Assets](/assets) suporta AndroidX. Se você não deseja usar o AndroidX, pode explicitamente desativá-lo em favor da antiga Biblioteca de Suporte Android marcando a opção `Use Android Support Lib` no [manifesto da aplicação](https://defold.com/manuals/app-manifest/).

![](images/android/enable_supportlibrary.png)

## FAQ
:[Android FAQ](../shared/android-faq.md)
