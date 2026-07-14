---
title: Manifest aplikacji
brief: Ta instrukcja wyjaśnia, jak manifest aplikacji służy do wykluczania funkcji z silnika.
---

# Manifest aplikacji

Manifest aplikacji określa, które funkcje i backendy są dołączane do silnika. Zaleca się wykluczenie nieużywanych funkcji, ponieważ zmniejsza to końcowy rozmiar pliku binarnego gry. Manifest aplikacji zawiera również opcje używane podczas budowania, takie jak minimalne obsługiwane wersje przeglądarek HTML5 i ustawienia pamięci WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Stosowanie manifestu

W pliku `game.project` przypisz manifest w <kbd>`Native Extensions`</kbd> -> <kbd>`App Manifest`</kbd>.

## Physics 2D

Wybierz implementację Box2D, która ma zostać dołączona:

* **Box2D Version 3** - Dołącza Box2D 3. Jest to opcja wymagająca jawnego włączenia i może dawać inne wyniki symulacji niż starsza implementacja, dlatego istniejące projekty mogą wymagać ponownego dostrojenia ustawień fizyki.
* **Box2D (Legacy Defold version)** - Dołącza starszą implementację Box2D silnika Defold. Jest to ustawienie domyślne.
* **None** - Wyklucza fizykę 2D.

Ustawienia solvera Box2D zależą od wersji. Szczegóły znajdziesz w [ustawieniach projektu Box2D](/manuals/project-settings/#box2d).

## Physics 3D

Dołącza implementację fizyki 3D Bullet. Jest ona dołączona domyślnie; wyłącz to ustawienie, aby wykluczyć fizykę 3D.

## Rig + Model

Steruje funkcjami rig i model albo pozwala wybrać None, aby całkowicie wykluczyć model i rig. Zobacz dokumentację [`Model`](https://defold.com/manuals/model/#model-component).


## Exclude Record

Wyklucza z silnika możliwość nagrywania wideo (zobacz dokumentację wiadomości [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Profiler

Określa, kiedy funkcje profilera są dołączane do silnika:

* **Debug Only** - Dołącza profiler tylko do buildów debug. Jest to ustawienie domyślne.
* **None** - Wyklucza funkcje profilera ze wszystkich wariantów buildu.
* **Always** - Dołącza profiler zarówno do buildów debug, jak i release.

Ustawienie w manifeście aplikacji określa, czy kod profilera jest dołączany do buildu. Ustawienia w sekcji `profiler` pliku *game.project* sterują zachowaniem profilera w czasie działania. Więcej informacji o dostępnych funkcjach znajdziesz w [podręczniku profilowania](/manuals/profiling/).


## Sound

Ustawienia dźwięku określają, który system dźwięku i które dekodery są dołączane do silnika.

### Exclude Sound

Wyklucza z silnika wszystkie możliwości odtwarzania dźwięku.

### Exclude Sound Decoder: WAV

Wyklucza obsługę zasobów dźwiękowych WAV.

### Exclude Sound Decoder: OGG

Wyklucza obsługę zasobów dźwiękowych Ogg Vorbis.

### Include Sound Decoder: Opus

Dołącza obsługę zasobów dźwiękowych Ogg Opus. Dekoder Opus jest domyślnie wykluczony, dlatego przed odtwarzaniem zasobów `.opus` należy włączyć tę opcję. Obsługiwane formaty opisano w [podręczniku dźwięku](/manuals/sound/).


## Exclude Input

Wyklucza z silnika całą obsługę wejścia.


## Exclude Live Update

Wyklucza z silnika [funkcję Live Update](/manuals/live-update).


## Exclude Image

Wyklucza z silnika moduł skryptowy `image`. Więcej informacji znajdziesz w [dokumentacji](https://defold.com/ref/stable/image/).


## Exclude Types

Wyklucza z silnika moduł skryptowy `types`. Więcej informacji znajdziesz w [dokumentacji](https://defold.com/ref/stable/types/).


## Exclude Basis Transcoder

Wyklucza z silnika [bibliotekę kompresji tekstur Basis Universal](/manuals/texture-profiles).


## Use Android Support Lib

Korzysta z przestarzałej biblioteki Android Support Library zamiast AndroidX. [Więcej informacji](https://defold.com/manuals/android/#using-androidx).


## Graphics

Wybierz backendy graficzne, które mają zostać dołączone dla każdej platformy. Wybór łączony dołącza oba backendy, aby można było użyć rozwiązania zapasowego, gdy preferowany backend jest niedostępny.

| Pole | Platformy | Opcje | Domyślna |
|---|---|---|---|
| **Graphics** | Windows i Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

W systemie Linux ARM64 opcja **OpenGL** używa backendu OpenGL ES. Domyślna opcja łączona dla Androida preferuje Vulkan, gdy jest dostępny, i w przeciwnym razie przełącza się na OpenGL ES.

## Use full text layout system

Jeśli ta opcja jest włączona (`true`), umożliwia generowanie w czasie działania fontów typu SDF przy użyciu fontów TrueType (`.ttf`) w projekcie. Więcej szczegółów znajdziesz w [podręczniku fontów](https://defold.com/manuals/font/#enabling-runtime-fonts).


## Minimalne wersje przeglądarek

Pola YAML **`minSafariVersion`**, **`minFirefoxVersion`** i **`minChromeVersion`** określają minimalne wersje przeglądarek, na które ukierunkowany jest Emscripten. Bieżące wartości domyślne i minimalne obsługiwane wersje różnią się między celami bez wątków i z wątkami:

| Cel | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Wartości zastępujące należy określić w kontekście właściwego celu. Cel wielowątkowy ma również dodatkowe [wymagania dotyczące hostingu](/manuals/html5/#creating-html5-bundle). Więcej informacji znajdziesz w dokumentacji ustawień Emscripten: [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) i [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Initial memory (HTML5)
Nazwa pola YAML: **`initialMemory`**
Wartość domyślna: **33554432**

Początkowa ilość pamięci przydzielanej aplikacji webowej, w bajtach. Wartość musi być wielokrotnością rozmiaru strony WebAssembly (64 KiB). Zobacz ustawienie Emscripten [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory).

Ta opcja określa wartość domyślną podczas kompilacji. Wartość [`html5.heap_size`](/manuals/html5/#heap-size) w pliku *game.project* zastępuje ją w czasie działania.

## Stack size (HTML5)
Nazwa pola YAML: **`stackSize`**
Wartość domyślna: **5242880**

Rozmiar stosu aplikacji w bajtach. Zobacz ustawienie Emscripten [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size).
