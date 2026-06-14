---
title: Depurando código nativo no Defold
brief: Este manual explica como depurar código nativo no Defold.
---

# Depurando código nativo

O Defold é bem testado e deve travar muito raramente em circunstâncias normais. No entanto, é impossível garantir que ele nunca travará, especialmente se seu jogo usa extensões nativas. Se você encontrar problemas com travamentos ou código nativo que não se comporta como esperado, há várias formas de avançar:

* Use um depurador para percorrer o código passo a passo
* Use depuração com print
* Analise um log de travamento
* Simbolique uma callstack


## Usar um depurador

A forma mais comum é executar o código por meio de um `debugger`. Ele permite percorrer o código passo a passo, definir `breakpoints` e interromperá a execução se ocorrer um travamento.

Há vários depuradores para cada plataforma.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Cada ferramenta pode depurar certas plataformas:

* Visual studio - Windows + plataformas com suporte a gdbserver (por exemplo, Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + plataformas com suporte a gdbserver
* Xcode - macOS, iOS ([saiba mais](/manuals/debugging-native-code-ios))
* Android Studio - Android ([saiba mais](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (via lldb)


## Usar depuração com print

A forma mais simples de depurar seu código nativo é usar [print debugging](http://en.wikipedia.org/wiki/Debugging#Techniques). Use as funções no [`namespace dmLog`](/ref/stable/dmLog/) para observar variáveis ou indicar o fluxo de execução. Usar qualquer uma das funções de log imprimirá na visualização *Console* do editor e no [log do jogo](/manuals/debugging-game-and-system-logs).


## Analisar um log de travamento

A engine Defold salva um arquivo `_crash` se ocorrer um hard crash. O arquivo de crash conterá informações sobre o sistema e sobre o travamento. A [saída do log do jogo](/manuals/debugging-game-and-system-logs) escreverá onde o arquivo de crash está localizado (isso varia conforme sistema operacional, dispositivo e aplicação).

Você pode usar o [módulo crash](https://www.defold.com/ref/crash/) para ler esse arquivo na sessão seguinte. Recomenda-se ler o arquivo, coletar as informações, imprimi-las no console e enviá-las para um [serviço de analytics](/tags/stars/analytics/) que ofereça suporte à coleta de logs de travamento.

::: important
No Windows, um arquivo `_crash.dmp` também é gerado. Esse arquivo é útil ao depurar um travamento.
:::

### Obtendo o log de travamento de um dispositivo

Se um travamento acontecer em um dispositivo móvel, você pode optar por baixar o arquivo de crash para seu próprio computador e analisá-lo localmente.

#### Android

Se o app for [debuggable](/manuals/project-settings/#android), você pode obter o log de travamento usando a [ferramenta Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) e o comando `adb shell`:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

No iTunes, você pode visualizar/baixar o container de um app.

Na janela `Xcode -> Devices`, você também pode selecionar os logs de travamento.


## Simbolicar uma callstack {#symbolicate-a-callstack}

Se você obtiver uma callstack de um arquivo `_crash` ou de um [arquivo de log](/manuals/debugging-game-and-system-logs), poderá simbolicá-la. Isso significa traduzir cada endereço na callstack para um nome de arquivo e número de linha, o que por sua vez ajuda a encontrar a causa raiz.

É importante que você combine a engine correta com a callstack; caso contrário, é muito provável que você acabe depurando coisas incorretas. Use a flag [`--with-symbols`](https://www.defold.com/manuals/bob/) ao empacotar com [Bob](https://www.defold.com/manuals/bob/) ou marque a checkbox "Generate debug symbols" na caixa de diálogo de empacotamento do editor:

* iOS - a pasta `dmengine.dSYM.zip` em `build/arm64-ios` contém os símbolos de debug para builds iOS.
* macOS - a pasta `dmengine.dSYM.zip` em `build/x86_64-macos` contém os símbolos de debug para builds macOS.
* Android - a pasta de saída de pacote `projecttitle.apk.symbols/lib/` contém os símbolos de debug para as arquiteturas-alvo.
* Linux - o executável contém os símbolos de debug.
* Windows - o arquivo `dmengine.pdb` em `build/x86_64-win32` contém os símbolos de debug para builds Windows.
* HTML5 - o arquivo `dmengine.js.symbols` em `build/wasm-web` contém os símbolos de debug para builds HTML5.

::: important
É muito importante que você salve os símbolos de debug em algum lugar para cada release pública do seu jogo e que saiba a qual release os símbolos de debug pertencem. Você não conseguirá depurar nenhum travamento nativo se não tiver os símbolos de debug. Além disso, mantenha uma versão `não stripped` da engine. Isso permite a melhor simbolicação da callstack.
:::


### Enviando símbolos para o Google Play
Você pode [enviar os símbolos de debug para o Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems) para que quaisquer travamentos registrados no Google Play mostrem call stacks simbolicadas. Compacte o conteúdo da pasta de saída de pacote `projecttitle.apk.symbols/lib/`. A pasta inclui uma ou mais subpastas com nomes de arquitetura, como `arm64-v8a` e `armeabi-v7a`.


### Simbolicar uma callstack do Android

1. Obtenha a engine da sua pasta de build

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Descompacte em uma pasta:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Encontre o endereço da callstack

	Por exemplo, na callstack não simbolicada, poderia aparecer assim:

	`#00 pc 00257224 libmy_game_name.so`

	Onde *`00257224`* é o endereço

4. Resolva o endereço

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Observação: se você obtiver um stack trace dos [logs do Android](/manuals/debugging-game-and-system-logs), talvez consiga simbolicá-lo usando [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Simbolicar uma callstack do iOS

1. Se você estiver usando extensões nativas, o servidor pode fornecer os símbolos (.dSYM) para você (passe `--with-symbols` para bob.jar)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. Se você não estiver usando extensões nativas, baixe os símbolos vanilla:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Simbolique usando o endereço de carregamento

	Por algum motivo, simplesmente colocar o endereço da callstack não funciona (isto é, endereço de carregamento 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Nem especificar diretamente o endereço de carregamento

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Adicionar o endereço de carregamento ao endereço funciona:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
