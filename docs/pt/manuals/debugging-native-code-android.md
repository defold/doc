---
title: Depuração no Android
brief: Este manual descreve como depurar um build usando o Android Studio.
---

# Depuração no Android

Aqui descrevemos como depurar um build usando o [Android Studio](https://developer.android.com/studio/), a IDE oficial para o sistema operacional Android do Google.


## Android Studio

* Prepare o pacote definindo a opção `android.debuggable` em *game.project*

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Empacote o app em modo debug em uma pasta de sua escolha.

	![bundle_android](images/extensions/debugging/android/bundle_android.png)

* Inicie o [Android Studio](https://developer.android.com/studio/)

* Escolha `Profile or debug APK`

	![debug_apk](images/extensions/debugging/android/android_profile_or_debug.png)

* Escolha o pacote apk que você acabou de criar

	![select_apk](images/extensions/debugging/android/android_select_apk.png)

* Selecione o arquivo `.so` principal e certifique-se de que ele tenha símbolos de debug

	![select_so](images/extensions/debugging/android/android_missing_symbols.png)

* Se ele não tiver, faça upload de um arquivo `.so` não stripped. (o tamanho é cerca de 20 MB)

* Mapeamentos de caminho ajudam a remapear os caminhos individuais de onde o executável foi compilado (na nuvem) para uma pasta real no seu disco local.

* Selecione o arquivo .so e adicione um mapeamento para seu disco local

	![path_mapping1](images/extensions/debugging/android/path_mappings_android.png)

	![path_mapping2](images/extensions/debugging/android/path_mappings_android2.png)

* Se você tiver acesso ao código-fonte da engine, adicione também um mapeamento de caminho para ele.

* Certifique-se de fazer checkout da versão que você está depurando no momento

	defold$ git checkout 1.2.148

* Pressione `Apply changes`

* Agora você deve ver o código-fonte mapeado no seu projeto

	![source](images/extensions/debugging/android/source_mappings_android.png)

* Adicione um breakpoint

	![breakpoint](images/extensions/debugging/android/breakpoint_android.png)

* Pressione `Run` -> `Debug "Appname"` e invoque o código no qual você pretendia parar

	![breakpoint](images/extensions/debugging/android/callstack_variables_android.png)

* Agora você pode percorrer a callstack e também inspecionar as variáveis


## Observações

### Pasta de job da extensão nativa

Atualmente, o fluxo de trabalho é um pouco incômodo para desenvolvimento. Isso acontece porque o nome da pasta de job
é aleatório para cada build, tornando o mapeamento de caminho inválido a cada build.

No entanto, funciona bem para uma sessão de depuração.

Os mapeamentos de caminho são armazenados no arquivo `.iml` do projeto no projeto do Android Studio.

É possível obter a pasta de job a partir do executável

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

A pasta de job é nomeada assim: `job1298751322870374150`, a cada vez com um número aleatório.

