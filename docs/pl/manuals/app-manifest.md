---
title: Manifest aplikacji
brief: Ta instrukcja wyjaśnia, jak manifest aplikacji służy do wykluczania funkcji z silnika.
---

# Manifest aplikacji

Manifest aplikacji służy do wykluczania funkcji z silnika albo do określania, które z nich mają zostać do niego dołączone. Wykluczanie nieużywanych funkcji silnika to zalecana praktyka, ponieważ zmniejsza końcowy rozmiar pliku binarnego gry.
Manifest aplikacji zawiera też kilka opcji sterujących kompilacją kodu dla platformy HTML5, takich jak minimalna obsługiwana wersja przeglądarki i ustawienia pamięci. Te opcje również mogą wpływać na rozmiar wynikowego pliku binarnego.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Stosowanie manifestu

W pliku `game.project` przypisz manifest w <kbd>`Native Extensions`</kbd> -> <kbd>`App Manifest`</kbd>.

## Physics

Określa, którego silnika fizyki użyć, albo pozwala wybrać None, aby całkowicie wykluczyć fizykę.

## Physics 2d

Wybiera, której wersji Box2D użyć.

## Rig + Model

Steruje funkcjami rig i model albo pozwala wybrać None, aby całkowicie wykluczyć model i rig. Zobacz dokumentację [`Model`](https://defold.com/manuals/model/#model-component).


## Exclude Record

Wyklucza z silnika możliwość nagrywania wideo (zobacz dokumentację wiadomości [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Exclude Profiler

Wyklucza profiler z silnika. Profiler służy do zbierania danych o wydajności oraz liczników użycia. Więcej informacji o korzystaniu z profilera znajdziesz w [podręczniku profilowania](/manuals/profiling/).


## Exclude Sound

Wyklucza z silnika wszystkie możliwości odtwarzania dźwięku.


## Exclude Input

Wyklucza z silnika całą obsługę wejścia.


## Exclude Live Update

Wyklucza z silnika [funkcję Live Update](/manuals/live-update).


## Exclude Image

Wyklucza z silnika moduł skryptowy `image`. Więcej informacji znajdziesz w [dokumentacji](https://defold.com/ref/stable/image/).


## Exclude Types

Wyklucza z silnika moduł skryptowy `types`. Więcej informacji znajdziesz w [dokumentacji](https://defold.com/ref/stable/types/).


## Exclude Basis Universal

Wyklucza z silnika [bibliotekę kompresji tekstur Basis Universal](/manuals/texture-profiles).


## Use Android Support Lib

Korzysta z przestarzałej biblioteki Android Support Library zamiast AndroidX. [Więcej informacji](https://defold.com/manuals/android/#using-androidx).


## Graphics

Określa, którego backendu graficznego użyć.

* OpenGL - Dołącza tylko OpenGL.
* Vulkan - Dołącza tylko Vulkan.
* OpenGL and Vulkan - Dołącza zarówno OpenGL, jak i Vulkan. Vulkan będzie używany domyślnie, a jeśli nie będzie dostępny, silnik przełączy się na OpenGL.

## Use full text layout system

Jeśli ta opcja jest włączona (`true`), umożliwia generowanie w czasie działania fontów typu SDF przy użyciu fontów TrueType (`.ttf`) w projekcie. Więcej szczegółów znajdziesz w [podręczniku fontów](https://defold.com/manuals/font/#enabling-runtime-fonts).


## Minimum Safari version (js-web and wasm-web only)
Nazwa pola YAML: **`minSafariVersion`**
Wartość domyślna: **90000**

Minimalna obsługiwana wersja Safari. Nie może być mniejsza niż 90000. Więcej informacji znajdziesz w [opcjach kompilatora Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-safari-version).

## Minimum Firefox version (js-web and wasm-web only)
Nazwa pola YAML: **`minFirefoxVersion`**
Wartość domyślna: **34**

Minimalna obsługiwana wersja Firefoxa. Nie może być mniejsza niż 34. Więcej informacji znajdziesz w [opcjach kompilatora Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-firefox-version).

## Minimum Chrome version (js-web and wasm-web only)
Nazwa pola YAML: **`minChromeVersion`**
Wartość domyślna: **32**

Minimalna obsługiwana wersja Chrome. Nie może być mniejsza niż 32. Więcej informacji znajdziesz w [opcjach kompilatora Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-chrome-version).

## Initial memory (js-web and wasm-web only)
Nazwa pola YAML: **`initialMemory`**
Wartość domyślna: **33554432**

Rozmiar pamięci przydzielanej aplikacji webowej. Jeśli ALLOW_MEMORY_GROWTH=0 (js-web), jest to całkowita ilość pamięci dostępna dla aplikacji webowej. Więcej informacji znajdziesz w [opcjach kompilatora Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#initial-memory). Wartość podawana jest w bajtach. Zwróć uwagę, że musi ona być wielokrotnością rozmiaru strony WebAssembly (64KiB).
Ta opcja odnosi się do `html5.heap_size` w *game.project* ([więcej informacji](https://defold.com/manuals/html5/#heap-size)). Opcja skonfigurowana w manifeście aplikacji jest ustawiana podczas kompilacji i używana jako domyślna wartość `INITIAL_MEMORY`. Wartość z *game.project* nadpisuje wartość z manifestu aplikacji i jest używana w czasie działania.

## Stack size (js-web and wasm-web only)
Nazwa pola YAML: **`stackSize`**
Wartość domyślna: **5242880**

Rozmiar stosu aplikacji. Więcej informacji znajdziesz w [opcjach kompilatora Emscripten](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#stack-size). Wartość podawana jest w bajtach.
