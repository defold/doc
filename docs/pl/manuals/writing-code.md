---
title: Pisanie kodu
brief: Ta instrukcja krótko omawia pracę z kodem w Defold.
---

# Pisanie kodu

Choć Defold pozwala tworzyć sporą część zawartości gry za pomocą narzędzi wizualnych, takich jak edytory map kafelków i efektów cząsteczkowych, logikę gry nadal tworzysz w edytorze kodu. Logika gry jest pisana w [języku programowania Lua](https://www.lua.org/), a rozszerzenia samego silnika tworzy się w języku lub językach natywnych dla platformy docelowej.

## Pisanie kodu Lua

Defold używa Lua 5.1 i LuaJIT, zależnie od platformy docelowej, więc podczas pisania logiki gry trzeba stosować się do specyfikacji tych konkretnych wersji Lua. Więcej informacji o pracy z Lua w Defold znajdziesz w [instrukcji Lua w Defold](/manuals/lua).

## Używanie innych języków transpilujących do Lua

Defold obsługuje transpilatory generujące kod Lua. Po zainstalowaniu rozszerzenia transpilatora możesz używać alternatywnych języków, takich jak [Teal](https://github.com/defold/extension-teal), aby pisać statycznie sprawdzany kod Lua. To funkcja podglądowa i ma ograniczenia: obecna obsługa transpilatorów nie udostępnia informacji o modułach i funkcjach zdefiniowanych w środowisku uruchomieniowym Lua w Defold. Oznacza to, że korzystając z API Defold, takiego jak `go.animate`, musisz samodzielnie przygotować definicje zewnętrzne.

## Pisanie kodu natywnego

Defold pozwala rozszerzać silnik kodem natywnym, aby uzyskać dostęp do funkcji specyficznych dla platformy, których sam silnik nie udostępnia. Kod natywny przydaje się też wtedy, gdy wydajność Lua nie wystarcza, na przykład przy kosztownych obliczeniach lub przetwarzaniu obrazów. Więcej informacji znajdziesz w [instrukcjach o Native Extensions](/manuals/extensions/).

## Używanie wbudowanego edytora kodu

Defold ma wbudowany edytor kodu, który pozwala otwierać i edytować pliki Lua (.lua), pliki skryptów Defold (.script, .gui_script i .render_script), a także inne pliki z rozszerzeniami, których edytor nie obsługuje natywnie. Edytor zapewnia też podświetlanie składni dla plików Lua i plików skryptów.

![](/images/editor/code-editor.png)

### Uzupełnianie kodu

Wbudowany edytor kodu wyświetla podpowiedzi dotyczące funkcji podczas pisania:

![](/images/editor/codecompletion.png)

Naciśnięcie <kbd>CTRL</kbd> + <kbd>Space</kbd> pokazuje dodatkowe informacje o funkcjach, argumentach i wartościach zwracanych:

![](/images/editor/apireference.png)

### Konfiguracja lintingu

Wbudowany edytor kodu wykonuje linting przy użyciu [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) oraz [Lua language server](https://luals.github.io/wiki/diagnostics/). Aby skonfigurować Luacheck, utwórz plik `.luacheckrc` w katalogu głównym projektu. Listę dostępnych opcji znajdziesz na [stronie konfiguracji Luacheck](https://luacheck.readthedocs.io/en/stable/config.html). Defold używa domyślnie następującej konfiguracji Luacheck:

```lua
unused_args = false      -- nie ostrzegaj o nieużywanych argumentach (częste w plikach .script)
max_line_length = false  -- nie ostrzegaj o długich liniach
ignore = {
    "611",               -- linia zawiera tylko białe znaki
    "612",               -- linia zawiera białe znaki na końcu
    "614"                -- białe znaki na końcu komentarza
},
```

## Używanie zewnętrznego edytora kodu

Edytor kodu w Defold zapewnia podstawowe możliwości potrzebne do pisania kodu, ale w bardziej zaawansowanych zastosowaniach lub jeśli wolisz własny edytor, możesz skonfigurować Defold tak, aby otwierał pliki w zewnętrznym edytorze. W [oknie Preferences, na karcie Code](/manuals/editor-preferences/#code) można wskazać zewnętrzny edytor, którego Defold ma używać do pracy z kodem.

### Visual Studio Code - Defold Kit

Defold Kit to wtyczka do Visual Studio Code z następującymi funkcjami:

* instalowanie zalecanych rozszerzeń
* podświetlanie składni, autouzupełnianie i linting Lua
* stosowanie odpowiednich ustawień do obszaru roboczego
* adnotacje Lua dla API Defold
* adnotacje Lua dla zależności
* budowanie i uruchamianie
* debugowanie z punktami przerwania
* tworzenie paczek dla wszystkich platform
* wdrażanie na podłączone urządzenia mobilne

Więcej informacji i możliwość instalacji Defold Kit znajdziesz w [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).

## Oprogramowanie dokumentacyjne

Pakiety referencyjne API przygotowane przez społeczność są dostępne dla [Dash i Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
