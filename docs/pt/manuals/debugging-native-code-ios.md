---
title: Depuração no iOS/macOS
brief: Este manual descreve como depurar um build usando o Xcode.
---

# Depuração no iOS/macOS

Aqui descrevemos como depurar um build usando o [Xcode](https://developer.apple.com/xcode/), a IDE preferida da Apple para desenvolvimento em macOS e iOS.

## Xcode

* Empacote o app usando Bob, com a opção `--with-symbols` ([mais informações](/manuals/debugging-native-code/#symbolicate-a-callstack)):

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Instale o app, seja com `Xcode`, `iTunes` ou [ios-deploy](https://github.com/ios-control/ios-deploy)

```sh
$ ios-deploy -b <AppName>.ipa
```

* Obtenha a pasta `.dSYM` (isto é, os símbolos de debug)

	* Se não estiver usando extensões nativas, você pode baixar o arquivo `.dSYM` de [d.defold.com](http://d.defold.com)

	* Se você estiver usando uma extensão nativa, a pasta `.dSYM` é gerada quando você compila com [bob.jar](https://www.defold.com/manuals/bob/). Apenas o build é necessário (sem archive ou empacotamento):

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Criar projeto

Para depurar corretamente, precisamos ter um projeto e o código-fonte mapeado.
Não estamos usando este projeto para compilar coisas, apenas para depurar.

* Crie um novo projeto Xcode, escolha o template `Game`

	![project_template](images/extensions/debugging/ios/project_template.png)

* Escolha um nome (por exemplo, `debug`) e as configurações padrão

* Escolha uma pasta onde salvar o projeto

* Adicione seu código ao app

	![add_files](images/extensions/debugging/ios/add_files.png)

* Certifique-se de que "Copy items if needed" esteja desmarcado.

	![add_source](images/extensions/debugging/ios/add_source.png)

* Este é o resultado final

	![added_source](images/extensions/debugging/ios/added_source.png)


* Desative a etapa `Build`

	![edit_scheme](images/extensions/debugging/ios/edit_scheme.png)

	![disable_build](images/extensions/debugging/ios/disable_build.png)

* Defina a versão de `Deployment target` para que ela não seja maior que a versão do iOS do seu dispositivo

	![deployment_version](images/extensions/debugging/ios/deployment_version.png)

* Selecione o dispositivo de destino

	![select_device](images/extensions/debugging/ios/select_device.png)


### Iniciar o depurador

Você tem algumas opções para depurar um app

1. Escolha `Debug` -> `Attach to process...` e selecione o app ali

2. Ou escolha `Attach to process by PID or Process name`

	![select_device](images/extensions/debugging/ios/attach_to_process_name.png)

3. Inicie o app no dispositivo

4. Em `Edit Scheme`, adicione a pasta <AppName>.app como executável

### Símbolos de debug

**Para usar lldb, a execução precisa estar pausada**

* Adicione o caminho `.dSYM` ao lldb

```
(lldb) add-dsym <PathTo.dSYM>
```

	![add_dsym](images/extensions/debugging/ios/add_dsym.png)

* Verifique se o `lldb` leu os símbolos com sucesso

```
(lldb) image list <AppName>
```

### Mapeamentos de caminho

* Adicione o código-fonte da engine (altere conforme sua necessidade)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* É possível obter a pasta de job a partir do executável. A pasta de job se chama `job1298751322870374150`, a cada vez com um número aleatório.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Verifique os mapeamentos de código-fonte

```
(lldb) settings show target.source-map
```

Você pode verificar de qual arquivo-fonte um símbolo se originou usando

```
(lldb) image lookup -va <SymbolName>
```

### Breakpoints

* Abra um arquivo na visualização de projeto e defina um breakpoint

	![breakpoint](images/extensions/debugging/ios/breakpoint.png)

## Observações

### Verificar UUID do binário

Para que o depurador aceite a pasta `.dSYM`, o UUID precisa corresponder ao UUID do executável sendo depurado. Você pode verificar o UUID assim:

```sh
$ dwarfdump -u <PathToBinary>
```
