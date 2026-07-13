---
title: Depuração - logs do jogo e do sistema
brief: Este manual explica como ler logs do jogo e do sistema.
---

# Log do jogo e do sistema

O log do jogo mostra toda a saída da engine, das extensões nativas e da lógica do seu jogo. Os comandos [print()](/ref/stable/base/#print:...) e [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) podem ser usados nos seus scripts e módulos Lua para mostrar informações no log do jogo. Você pode usar as funções no [`namespace dmLog`](/ref/stable/dmLog/) para escrever no log do jogo a partir de extensões nativas. O log do jogo pode ser lido no editor, em uma janela de terminal, usando ferramentas específicas de plataforma ou a partir de um arquivo de log.

Logs do sistema são gerados pelo sistema operacional e podem fornecer informações adicionais que ajudam a identificar um problema. Os logs do sistema podem conter stack traces de travamentos e avisos de pouca memória.

::: important
Logging no console/na tela só mostra informações em builds Debug. Em builds Release, o log do console fica vazio, mas você pode habilitar logging em arquivo no Release definindo a configuração de projeto "Write Log File" como "Always". Veja detalhes abaixo.
:::

## Lendo o log do jogo pelo editor

Quando você executa seu jogo localmente pelo editor ou conectado ao [aplicativo de desenvolvimento mobile](/manuals/dev-app), toda a saída será mostrada no painel Console do editor:

![Editor 2](images/editor/editor2_overview.png)

## Lendo o log do jogo pelo terminal

Quando você executa um jogo Defold pelo terminal, o log aparecerá na própria janela do terminal. No Windows e no Linux, você digita o nome do executável no terminal para iniciar o jogo. No macOS, é preciso iniciar a engine de dentro do arquivo .app:

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Lendo logs do jogo e do sistema usando ferramentas específicas de plataforma

### HTML5

Logs podem ser lidos usando as ferramentas de desenvolvedor fornecidas pela maioria dos navegadores.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android

Você pode usar a ferramenta Android Debug Bridge (ADB) para visualizar o log do jogo e do sistema.

:[Android ADB](../shared/android-adb.md)

Depois de instalada e configurada, conecte seu dispositivo por USB, abra um terminal e execute:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

O dispositivo então despejará toda a saída no terminal atual, junto com quaisquer prints do jogo.

Se quiser ver apenas as saídas da aplicação Defold, use este comando:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

Você tem várias opções para ler logs do jogo e do sistema no iOS:

1. Você pode usar a [ferramenta Console](https://support.apple.com/guide/console/welcome/mac) para ler logs do jogo e do sistema.
2. Você pode usar o depurador LLDB para anexar a um jogo em execução no dispositivo. Para depurar um jogo, ele precisa estar assinado com um "Apple Developer Provisioning Profile" que inclua o dispositivo no qual você quer depurar. Empacote o jogo pelo editor e forneça o provisioning profile na caixa de diálogo de empacotamento (empacotamento para iOS só está disponível no macOS).

Para iniciar o jogo e anexar o depurador, você precisará de uma ferramenta chamada [ios-deploy](https://github.com/phonegap/ios-deploy). Instale e depure seu jogo executando o seguinte em um terminal:

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # OBSERVAÇÃO: não é o arquivo .ipa
```

Isso instalará o app no seu dispositivo, iniciará o app e anexará automaticamente um depurador LLDB a ele. Se você é novo no LLDB, leia [Getting Started with LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## Lendo o log do jogo pelo arquivo de log

Use a configuração de projeto "Write Log File" em *game.project* para controlar o logging em arquivo:

- "Never": não escreve um arquivo de log.
- "Debug": escreve um arquivo de log somente para builds Debug.
- "Always": escreve um arquivo de log para builds Debug e Release.

Quando habilitada, qualquer saída do jogo será gravada no disco em um arquivo chamado "`log.txt`". Veja como extrair o arquivo se você executar o jogo no dispositivo:

iOS
: Conecte seu dispositivo a um computador com macOS e Xcode instalado.

  Abra o Xcode e vá para <kbd>Window ▸ Devices and Simulators</kbd>.

  Selecione seu dispositivo na lista e então selecione o app relevante na lista *Installed Apps*.

  Clique no ícone de engrenagem abaixo da lista e selecione <kbd>Download Container...</kbd>.

  ![baixar container](images/debugging/download_container.png)

  Depois que o container for extraído, ele será mostrado no *Finder*. Use o botão direito no container e selecione <kbd>Show Package Content</kbd>. Localize o arquivo "`log.txt`", que deve estar em "`AppData/Documents/`".

Android
: A possibilidade de extrair o "`log.txt`" depende da versão do sistema operacional e do fabricante. Aqui está um [guia passo a passo](https://stackoverflow.com/a/48077004/129360) curto e simples.
