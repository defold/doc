---
title: Executando o aplicativo de desenvolvimento no dispositivo
brief: Este manual explica como colocar o aplicativo de desenvolvimento no seu dispositivo para desenvolvimento iterativo no dispositivo.
---

# O aplicativo de desenvolvimento móvel

O aplicativo de desenvolvimento permite que você envie conteúdo para ele via wifi. Isso reduzirá bastante o tempo de iteração, pois você não precisa empacotar e instalar toda vez que desejar testar suas alterações. Você instala o aplicativo de desenvolvimento no(s) seu(s) dispositivo(s), inicia o aplicativo e então seleciona o dispositivo como um alvo de build a partir do editor.

## Instalando um aplicativo de desenvolvimento

Qualquer aplicativo iOS ou Android que seja empacotado no modo Debug será capaz de atuar como um aplicativo de desenvolvimento. Na verdade, esta é a solução recomendada, pois o aplicativo de desenvolvimento terá as configurações de projeto corretas e usa as mesmas [extensões nativas](/manuals/extensions/) do projeto em que você está trabalhando.

A partir do Defold 1.4.0, é possível empacotar uma variante Debug do seu projeto sem nenhum conteúdo. Use esta opção para criar uma versão do seu aplicativo com extensões nativas, adequada para desenvolvimento iterativo conforme descrito neste manual.

<img width="375" height="319" alt="image" src="https://github.com/user-attachments/assets/c911cd77-05fe-4996-bca7-9e8274667cdc" />

### Instalando no iOS

Siga as [instruções no manual do iOS](/manuals/ios/#creating-an-ios-application-bundle) para empacotar para iOS. Certifique-se de selecionar Debug como variante!

### Instalando no Android

Siga as [instruções no manual do Android](https://defold.com/manuals/android/#creating-an-android-application-bundle) para empacotar para Android.

## Iniciando seu jogo

Para iniciar seu jogo no seu dispositivo, o aplicativo de desenvolvimento e o editor devem ser capazes de se conectar, através da mesma rede wifi ou usando USB (veja abaixo).

1. Certifique-se de que o editor está em execução.
2. Inicie o aplicativo de desenvolvimento no dispositivo.
3. Selecione seu dispositivo em <kbd>Project ▸ Targets</kbd> no editor.
4. Selecione <kbd>Project ▸ Build</kbd> para executar o jogo. Pode levar um tempo para o jogo iniciar, pois o conteúdo do jogo é transmitido para o dispositivo pela rede.
5. Enquanto o jogo está em execução, você pode usar [hot reloading](/manuals/hot-reload/) como de costume.

### Conectando a um dispositivo iOS usando USB no Windows

Ao conectar via USB no Windows a um aplicativo de desenvolvimento em execução em um dispositivo iOS, você primeiro precisa [instalar o iTunes](https://www.apple.com/lae/itunes/download/). Quando o iTunes estiver instalado, você também precisa [habilitar o Hotspot Pessoal](https://support.apple.com/en-us/HT204023) no seu dispositivo iOS no menu Configurações. Se você vir um alerta que diz "Confiar neste Computador?", toque em Confiar. O dispositivo agora deve aparecer em <kbd>Project ▸ Targets</kbd> quando o aplicativo de desenvolvimento estiver em execução.

### Conectando a um dispositivo iOS usando USB no Linux

No Linux, você precisa habilitar o Hotspot Pessoal no seu dispositivo no menu Configurações quando conectado via USB. Se você vir um alerta que diz "Confiar neste Computador?", toque em Confiar. O dispositivo agora deve aparecer em <kbd>Project ▸ Targets</kbd> quando o aplicativo de desenvolvimento estiver em execução.

### Conectando a um dispositivo iOS usando USB no macOS

Em versões mais recentes do iOS, o dispositivo abrirá automaticamente uma nova interface ethernet entre o dispositivo e o computador quando conectado via USB no macOS. O dispositivo deve aparecer em <kbd>Project ▸ Targets</kbd> quando o aplicativo de desenvolvimento estiver em execução.

Em versões mais antigas do iOS, você precisa habilitar o Hotspot Pessoal no seu dispositivo no menu Configurações quando conectado via USB no macOS. Se você vir um alerta que diz "Confiar neste Computador?", toque em Confiar. O dispositivo agora deve aparecer em <kbd>Project ▸ Targets</kbd> quando o aplicativo de desenvolvimento estiver em execução.

### Conectando a um dispositivo Android usando USB no macOS

No macOS, é possível conectar via USB a um aplicativo de desenvolvimento em execução em um dispositivo Android quando o dispositivo está no Modo de Ancoragem USB. No macOS, você precisa instalar um driver de terceiros, como [HoRNDIS](https://joshuawise.com/horndis#available_versions). Quando o HoRNDIS estiver instalado, você também precisa permitir que ele seja executado através das configurações de Segurança e Privacidade. Uma vez que a Ancoragem USB esteja habilitada, o dispositivo aparecerá em <kbd>Project ▸ Targets</kbd> quando o aplicativo de desenvolvimento estiver em execução.

### Conectando a um dispositivo Android usando USB no Windows ou Linux

No Windows e Linux, é possível conectar via USB a um aplicativo de desenvolvimento em execução em um dispositivo Android quando o dispositivo está no Modo de Ancoragem USB. Uma vez que a Ancoragem USB esteja habilitada, o dispositivo aparecerá em <kbd>Project ▸ Targets</kbd> quando o aplicativo de desenvolvimento estiver em execução.

## Solução de problemas

Não é possível baixar o aplicativo
: Certifique-se de que o UDID do seu dispositivo está incluído no mobile provisioning que foi usado para assinar o aplicativo.

Seu dispositivo não aparece no menu Targets
: Certifique-se de que seu dispositivo está conectado à mesma rede wifi que seu computador. Certifique-se de que o aplicativo de desenvolvimento foi construído no modo Debug.

O jogo não inicia com uma mensagem sobre versões incompatíveis
: Isso acontece quando você atualizou o editor para a versão mais recente. Você precisa construir e instalar uma nova versão.
