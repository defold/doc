---
title: Desenvolvimento Defold para a plataforma Android
brief: Este manual descreve como construir e executar aplicações Defold em dispositivos Android
---

# Desenvolvimento Android

Dispositivos Android permitem que você execute livremente seus próprios aplicativos neles. É muito fácil construir uma versão do seu jogo e copiá-la para um dispositivo Android. Este manual explica as etapas envolvidas na criação do pacote do seu jogo para Android. Durante o desenvolvimento, executar seu jogo através do [aplicativo de desenvolvimento](/manuals/dev-app) é frequentemente preferível, pois permite recarregar conteúdo e código diretamente no seu dispositivo.

## Processo de assinatura Android e Google Play

O Android exige que todos os APKs sejam assinados digitalmente com um certificado antes de serem instalados em um dispositivo ou atualizados. Se você usar Android App Bundles, precisa assinar apenas seu app bundle antes de enviá-lo para o Play Console, e o [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) cuida do resto. No entanto, você também pode assinar manualmente seu aplicativo para envio para o Google Play, outras lojas de aplicativos e para distribuição fora de qualquer loja.

Quando você cria um Android application bundle a partir do editor Defold ou da [ferramenta de linha de comando](/manuals/bob), você pode fornecer um keystore (contendo seu certificado e chave) e senha do keystore que serão usados ao assinar sua aplicação. Se você não fornecer, o Defold gera um keystore de depuração e o usa ao assinar o pacote de aplicativo.

::: important
Você **nunca** deve enviar sua aplicação para o Google Play se ela foi assinada usando um keystore de depuração. Sempre use um keystore dedicado que você mesmo criou.
:::

## Criando um keystore

::: sidenote
O processo de assinatura Android no Defold mudou na versão 1.2.173 de usar uma chave e certificado independentes para usar um keystore. [Mais informações neste post do fórum](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Você pode criar um keystore [usando o Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) ou a partir de um terminal/prompt de comando:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Isso irá criar um arquivo keystore chamado `mykeystore.keystore` contendo uma chave e certificado. O acesso à chave e certificado será protegido pela senha `5Up3r_53cR3t`. A chave e o certificado serão válidos por 25 anos (9125 dias). A chave e o certificado gerados serão identificados pelo alias `myAlias`.

::: important
Certifique-se de armazenar o keystore e a senha associada em um local seguro. Se você assinar e enviar suas aplicações para o Google Play e o keystore ou a senha do keystore for perdida, não há como atualizar a aplicação no Google Play. Você pode evitar isso usando o Google Play App Signing e deixar o Google assinar suas aplicações para você.
:::


## Criando um application bundle de Android

O editor permite que você crie facilmente um pacote de aplicativo independente para seu jogo. Antes de empacotar (criar um bundle), você pode especificar qual(is) ícone(s) usar para o aplicativo, definir o código de versão etc. no arquivo de [configurações do projeto](/manuals/project-settings/#android) *game.project*.

Para empacotar, selecione <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> no menu.

Se você quiser que o editor crie automaticamente certificados de depuração aleatórios, deixe os campos *Keystore* e *Keystore password* vazios:

<img width="605" height="486" alt="image" src="https://github.com/user-attachments/assets/bcdc3075-dd57-4a3a-b512-acd248a04511" />

Se você quiser assinar seu bundle com um keystore específico, especifique o *Keystore* e *Keystore password*. Espera-se que o *Keystore* tenha a extensão de arquivo `.keystore`, enquanto a senha deve ser armazenada em um arquivo de texto com a extensão `.txt`. Também é possível especificar uma *Key password* se a chave no keystore usar uma senha diferente do próprio keystore:

<img width="602" height="486" alt="image" src="https://github.com/user-attachments/assets/05cca12a-05a4-4cb2-b471-96f8ca776830" />

O Defold tem suporte à criação de arquivos APK e AAB. Selecione APK ou AAB no menu suspenso *Bundle Format*.

Pressione <kbd>Create Bundle</kbd> quando tiver configurado as definições do pacote de aplicativo. Em seguida, você será solicitado a especificar onde em seu computador o pacote será criado.

<img width="743" height="450" alt="image" src="https://github.com/user-attachments/assets/b1f2ae5f-281e-4659-882e-831c0307e5a3" />

:[Build Variants](../shared/build-variants.md)

### Instalando um application bundle de Android

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

<img width="1222" height="1172" alt="image" src="https://github.com/user-attachments/assets/0d42574c-d6ef-4432-b085-d07e4bc970ff" />

Para que este recurso funcione, você precisará ter o ADB instalado e a *Depuração USB* (*USB debugging*) habilitada no dispositivo conectado. Se o editor não conseguir detectar a localização de instalação da ferramenta de linha de comando ADB, você precisará especificá-la nas [Preferências](/manuals/editor-preferences/#tools).

#### Instalando um AAB

Um arquivo *.aab* pode ser enviado para o Google Play através do [console do desenvolvedor do Google Play](https://play.google.com/apps/publish/). Também é possível gerar um arquivo *`.apk`* a partir de um arquivo *.aab* para instalá-lo localmente usando o [Android bundletool](https://developer.android.com/studio/command-line/bundletool).

## Permissões

A engine Defold requer várias permissões diferentes para que todos os recursos do motor funcionem. As permissões são definidas no `AndroidManifest.xml`, especificado no arquivo de [configurações do projeto](/manuals/project-settings/#android) *game.project*. Você pode ler mais sobre permissões Android na [documentação oficial](https://developer.android.com/guide/topics/permissions/overview). As seguintes permissões são solicitadas no manifesto padrão:

### android.permission.INTERNET e android.permission.ACCESS_NETWORK_STATE (Nível de proteção: normal)
Permite que aplicativos abram soquetes de rede (*network sockets*) e acessem informações sobre redes. Essas permissões são necessárias para acesso à internet. ([Documentação oficial Android](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) e ([Documentação oficial Android](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Nível de proteção: normal)
Permite usar PowerManager WakeLocks para impedir que o processador entre em modo de suspensão ou que a tela escureça. Esta permissão é necessária para impedir temporariamente que o dispositivo entre em suspensão enquanto recebe uma notificação push. ([Documentação oficial Android](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))

## Usando AndroidX
O AndroidX é uma grande melhoria em relação à biblioteca de suporte Android original, que não é mais mantida. Os pacotes AndroidX substituem completamente a Biblioteca de Suporte, fornecendo paridade de recursos e novas bibliotecas. A maioria das extensões Android no [Portal de Assets](/assets) suporta AndroidX. Se você não deseja usar o AndroidX, pode explicitamente desativá-lo em favor da antiga Biblioteca de Suporte Android marcando a opção `Use Android Support Lib` no [manifesto da aplicação](https://defold.com/manuals/app-manifest/).

<img width="1333" height="1064" alt="image" src="https://github.com/user-attachments/assets/35e69cc4-9277-420b-9bc0-a73d29936761" />

## FAQ
:[Android FAQ](../shared/android-faq.md)
