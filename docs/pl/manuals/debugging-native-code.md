---
title: Debugowanie kodu natywnego w Defold
brief: Ta instrukcja wyjaśnia, jak debugować kod natywny w Defold.
---

# Debugowanie kodu natywnego

Defold jest dobrze przetestowany i w normalnych warunkach bardzo rzadko powinien się zawieszać. Nie da się jednak zagwarantować, że nigdy nie dojdzie do awarii, zwłaszcza jeśli Twoja gra korzysta z native extensions. Jeśli napotkasz problemy z awariami albo kod natywny nie zachowuje się tak, jak powinien, możesz pójść kilkoma różnymi drogami:

* użyć debuggera i prześledzić kod krok po kroku
* użyć debugowania przez wypisywanie
* przeanalizować log awarii
* zsymbolikować stos wywołań


## Użyj debuggera

Najczęściej uruchamia się kod w `debuggerze`. Pozwala on przechodzić przez kod krok po kroku, ustawiać punkty przerwania (`breakpoints`) i zatrzymać wykonanie, jeśli dojdzie do awarii.

Istnieje kilka debuggerów dla każdej platformy.

* Visual Studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Każde z tych narzędzi może debugować określone platformy:

* Visual Studio - Windows + platformy obsługujące gdbserver (np. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + platformy obsługujące gdbserver
* Xcode - macOS, iOS ([więcej informacji](/manuals/debugging-native-code-ios))
* Android Studio - Android ([więcej informacji](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (przez lldb)


## Użyj debugowania przez wypisywanie

Najprostszym sposobem debugowania kodu natywnego jest [debugowanie przez wypisywanie](http://en.wikipedia.org/wiki/Debugging#Techniques). Użyj funkcji z przestrzeni nazw [`dmLog`](/ref/stable/dmLog/), aby obserwować zmienne albo zaznaczać przebieg wykonania. Każda z funkcji logujących wypisze dane do widoku *Console* w edytorze oraz do [logu gry](/manuals/debugging-game-and-system-logs).


## Przeanalizuj log awarii

Silnik Defold zapisuje plik `_crash`, jeśli dojdzie do poważnej awarii. Plik awarii zawiera informacje o systemie oraz o samej awarii. [Wyjście logu gry](/manuals/debugging-game-and-system-logs) zapisze, gdzie znajduje się plik awarii (lokalizacja zależy od systemu operacyjnego, urządzenia i aplikacji).

Możesz użyć [modułu crash](https://www.defold.com/ref/crash/), aby odczytać ten plik w następnej sesji. Zaleca się odczytać plik, zebrać informacje, wypisać je do konsoli i wysłać do [usługi analitycznej](/tags/stars/analytics/), która obsługuje zbieranie logów awarii.

::: important
W systemie Windows generowany jest również plik `_crash.dmp`. Ten plik jest przydatny podczas debugowania awarii.
:::

### Pobieranie logu awarii z urządzenia

Jeśli awaria wystąpi na urządzeniu mobilnym, możesz pobrać plik awarii na własny komputer i przeanalizować go lokalnie.

#### Android

Jeśli aplikacja jest [debuggable](/manuals/project-settings/#android), możesz pobrać log awarii za pomocą narzędzia [Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) i polecenia `adb shell`:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

W iTunes możesz wyświetlić lub pobrać kontener aplikacji.

W oknie <kbd>Xcode ▸ Devices</kbd> możesz też wybrać logi awarii z menu `Xcode -> Devices`.


## Zsymbolikuj stos wywołań

Jeśli uzyskasz stos wywołań z pliku `_crash` albo z [pliku logu](/manuals/debugging-game-and-system-logs), możesz go zsymbolikować. Oznacza to przetłumaczenie każdego adresu w stosie wywołań na nazwę pliku i numer linii, co z kolei pomaga ustalić główną przyczynę problemu.

Bardzo ważne jest, aby dopasować właściwy silnik do stosu wywołań, w przeciwnym razie możesz zacząć debugować zupełnie niewłaściwe rzeczy. Użyj flagi [`--with-symbols`](https://www.defold.com/manuals/bob/) podczas bundlowania za pomocą [bob](https://www.defold.com/manuals/bob/) albo zaznacz <kbd>Generate debug symbols</kbd> w oknie bundlowania w edytorze:

* iOS - folder `dmengine.dSYM.zip` w `build/arm64-ios` zawiera symbole debugowe dla buildów iOS.
* macOS - folder `dmengine.dSYM.zip` w `build/x86_64-macos` zawiera symbole debugowe dla buildów macOS.
* Android - katalog wyjściowy bundla `projecttitle.apk.symbols/lib/` zawiera symbole debugowe dla docelowych architektur.
* Linux - plik wykonywalny zawiera symbole debugowe.
* Windows - plik `dmengine.pdb` w `build/x86_64-win32` zawiera symbole debugowe dla buildów Windows.
* HTML5 - plik `dmengine.js.symbols` w `build/js-web` lub `build/wasm-web` zawiera symbole debugowe dla buildów HTML5.

::: important
Bardzo ważne jest, aby zachować symbole debugowe dla każdego publicznego wydania gry i wiedzieć, do którego wydania należą. Bez symboli debugowych nie da się debugować natywnych awarii. Warto też zachować wersję silnika bez stripowania. Umożliwia to najlepszą możliwą symbolikację stosu wywołań.
:::


### Przesyłanie symboli do Google Play
Możesz [przesłać symbole debugowe do Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems), aby wszystkie awarie zarejestrowane w Google Play pokazywały zsymbolikowane stosy wywołań. Spakuj do ZIP-a zawartość katalogu wyjściowego bundla `projecttitle.apk.symbols/lib/`. Katalog zawiera jeden lub więcej podkatalogów o nazwach architektur, takich jak `arm64-v8a` i `armeabi-v7a`.


### Zsymbolikuj stos wywołań z Androida

1. Pobierz silnik z katalogu buildu

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Rozpakuj go do katalogu:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Znajdź adres ze stosu wywołań

	Na przykład w niezsymbolikowanym stosie wywołań może to wyglądać tak:

	`#00 pc 00257224 libmy_game_name.so`

	Gdzie *`00257224`* jest adresem

4. Rozwiąż adres

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Uwaga: jeśli zdobędziesz ślad stosu z [logów Androida](/manuals/debugging-game-and-system-logs), być może uda się go zsymbolikować za pomocą [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Zsymbolikuj stos wywołań z iOS

1. Jeśli używasz Native Extensions, serwer może dostarczyć symbole (.dSYM) (przekaż `--with-symbols` do `bob.jar`)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# spowoduje to utworzenie Contents/Resources/DWARF/dmengine
```

2. Jeśli nie używasz Native Extensions, pobierz standardowe symbole:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Zsymbolikuj, używając adresu załadowania

	Z jakiegoś powodu samo podanie adresu ze stosu wywołań nie działa (tj. adres załadowania 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Nie działa też podanie adresu załadowania bezpośrednio

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Dodanie adresu załadowania do adresu działa:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
