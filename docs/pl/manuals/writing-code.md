---
title: Pisanie kodu
brief: Ta instrukcja krótko omawia pracę z kodem w silniku Defold.
---

# Pisanie kodu

Choć Defold pozwala tworzyć znaczną część zawartości gry za pomocą narzędzi wizualnych, takich jak edytory map kafelków i efektów cząsteczkowych, logikę gry nadal tworzysz w edytorze kodu. Logikę gry pisze się w [języku Lua](https://www.lua.org/), natomiast rozszerzenia samego silnika tworzy się w języku lub językach natywnych dla docelowej platformy.

## Pisanie kodu Lua

Defold używa Lua 5.1 oraz LuaJIT, zależnie od platformy docelowej, dlatego podczas pisania logiki gry trzeba trzymać się specyfikacji tych wersji języka. Więcej informacji znajdziesz w [instrukcji Lua w silniku Defold](/manuals/lua).

## Używanie innych języków kompilowanych do Lua

Defold obsługuje transpiler’y generujące kod Lua. Po zainstalowaniu rozszerzenia transpiler’a możesz używać alternatywnych języków, takich jak [Teal](https://github.com/defold/extension-teal), aby pisać statycznie sprawdzany kod Lua. To funkcja podglądowa i ma ograniczenia: obecna obsługa transpiler’ów nie udostępnia informacji o modułach i funkcjach zdefiniowanych w środowisku uruchomieniowym Lua w Defold. Oznacza to, że używając API Defold, takiego jak `go.animate`, musisz samodzielnie przygotować zewnętrzne definicje.

## Pisanie kodu natywnego

Defold pozwala rozszerzać silnik gry kodem natywnym, aby uzyskać dostęp do funkcji specyficznych dla platformy, których sam silnik nie udostępnia. Kod natywny przydaje się też wtedy, gdy wydajność Lua okazuje się niewystarczająca, na przykład przy kosztownych obliczeniach lub przetwarzaniu obrazów. Szczegóły znajdziesz w [instrukcjach o Native Extensions](/manuals/extensions/).

## Używanie wbudowanego edytora kodu

Defold ma wbudowany edytor kodu, który pozwala otwierać i edytować pliki Lua (`.lua`), pliki skryptów Defold (`.script`, `.gui_script` i `.render_script`), a także inne pliki z rozszerzeniami, których edytor nie obsługuje natywnie. Edytor zapewnia również podświetlanie składni dla plików Lua i skryptów.

![](/images/editor/code-editor.png)

### Uzupełnianie kodu

Wbudowany edytor kodu wyświetla podpowiedzi funkcji podczas pisania:

![](/images/editor/codecompletion.png)

Naciśnięcie <kbd>CTRL</kbd> + <kbd>Space</kbd> pokazuje dodatkowe informacje o funkcjach, argumentach i wartościach zwracanych:

![](/images/editor/apireference.png)

### Konfiguracja lintingu

Wbudowany edytor kodu wykonuje linting przy użyciu [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) oraz [Lua language server](https://luals.github.io/wiki/diagnostics/). Aby skonfigurować Luacheck, utwórz plik `.luacheckrc` w katalogu głównym projektu. Listę dostępnych opcji znajdziesz na [stronie konfiguracji Luacheck](https://luacheck.readthedocs.io/en/stable/config.html). Defold używa domyślnie następującej konfiguracji Luacheck:

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## Używanie zewnętrznego edytora kodu

Edytor kodu w Defold zapewnia podstawowe możliwości potrzebne do pisania kodu, ale w bardziej zaawansowanych zastosowaniach lub jeśli wolisz własne narzędzie, możesz skonfigurować Defold tak, aby otwierał pliki w zewnętrznym edytorze. W [oknie Preferences, w zakładce Code](/manuals/editor-preferences/#code), można wskazać zewnętrzny edytor używany podczas pracy z kodem.

### Visual Studio Code - Defold Kit

Defold Kit to wtyczka do Visual Studio Code z następującymi funkcjami:

* instalacja zalecanych rozszerzeń
* podświetlanie, autouzupełnianie i linting Lua
* stosowanie odpowiednich ustawień do obszaru roboczego
* adnotacje Lua dla API Defold
* adnotacje Lua dla zależności
* budowanie i uruchamianie
* debugowanie z punktami przerwania
* bundlowanie na wszystkie platformy
* wdrażanie na podłączone urządzenia mobilne

Więcej informacji i instalację Defold Kit znajdziesz w [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).

## Oprogramowanie dokumentacyjne

Społeczność przygotowała pakiety referencji API do programów [Dash i Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
