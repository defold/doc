---
title: Pisanie kodu
brief: Ta instrukcja krótko omawia, jak pracować z kodem w Defold.
---

# Pisanie kodu

Podczas gdy Defold pozwala tworzyć wiele zawartości gry za pomocą narzędzi wizualnych, takich jak Edytory map kafelków (tilemap) i efektów cząsteczkowych (particle FX), logikę gry tworzysz za pomocą Edytora kodu. Logikę gry pisze się za pomocą języka programowania [Lua](https://www.lua.org/), podczas gdy rozszerzenia samego silnika pisze się przy użyciu języków niskopoziomowych dedykowanych dla docelowej platformy.

## Pisanie kodu Lua

Defold używa Lua 5.1 i LuaJIT (w zależności od docelowej platformy) i należy stosować specyfikację tego języka dla konkretnych wersji Lua podczas pisania logiki gry. Aby uzyskać więcej szczegółów na temat pracy z Lua w Defoldzie, zobacz nasz [podręcznik Lua w Defold](/manuals/lua).

## Pisanie kodu natywnego

Defold pozwala na rozszerzenie silnika gry kodem natywnym (native extensions), aby uzyskać dostęp do funkcji specyficznych dla danej platformy, których nie dostarcza sam silnik. Możesz również użyć kodu natywnego, gdy wydajność Lua nie jest wystarczająca (obliczenia wymagające dużych zasobów, przetwarzanie obrazów itp.). Aby dowiedzieć się więcej, zajrzyj do naszych [podręczników dotyczących Rozszerzeń Natywnych](/manuals/extensions/).

## Używanie wbudowanego Edytora kodu

Defold posiada wbudowany Edytor kodu, który pozwala na otwieranie i edytowanie plików Lua (.lua), plików skryptów Defold (.script, .gui_script i .render_script) oraz innych plików z rozszerzeniem, które nie są obsługiwane natywnie przez Edytor. Dodatkowo Edytor ten oferuje podświetlanie składni dla plików Lua i skryptów oraz podręczny dostęp do dokumentacji dla funkcji API.

![](/images/editor/code-editor.png)


### Dodawanie sprawdzania poprawności kodu Lua za pomocą LSP

Defold obsługuje część protokołu Language Server Protocol (LSP), który można użyć do analizy kodu i wskazywania błędów programistycznych i stylowych. Proces ten jest również znany jako sprawdzanie poprawności kodu (linting).

Serwer języka Lua i linter kodu są dostępne jako wtyczka (plugin). Zainstaluj wtyczkę, [dodając ją jako zależność](/manuals/libraries/#setting-up-library-dependencies):

```
https://github.com/defold/lua-language-server/releases/download/v0.0.5/release.zip
```
Dostępne wersje można znaleźć na [stronie wydań](https://github.com/defold/lua-language-server/releases) wtyczki. Dowiedz się więcej na temat tej wtyczki na [stronie wsparcia na forum Defold](https://forum.defold.com/t/linting-in-the-code-editor/72465).


## Użycie zewnętrznego Edytora kodu

Edytor kodu w Defoldzie zapewnia podstawową funkcjonalność do pisania kodu, ale dla bardziej zaawansowanych przypadków użycia lub dla użytkowników z ulubionym Edytorem kodu, można pozwolić Defoldowi otwierać pliki za pomocą zewnętrznego Edytora, ponieważ skrypty i pliki tworzone przez Defolda w projekcie są edytowalnymi plikami tekstowymi. W [oknie preferencji w zakładce "Code"](/manuals/editor-preferences/#code) można zdefiniować zewnętrzny Edytor, który ma być używany podczas edycji kodu.

### Visual Studio Code - Defold Kit

Defold Kit to wtyczka dla Visual Studio Code z następującymi funkcjami:

* Instalowanie zalecanych rozszerzeń
* Podświetlanie, autouzupełnianie i sprawdzanie poprawności (linting) Lua
* Zastosowanie odpowiednich ustawień do przestrzeni roboczej
* Adnotacje Lua dla interfejsu API Defold
* Adnotacje Lua dla zależności
* Budowanie i uruchamianie
* Debugowanie z punktami przerwania (breakpoints)
* Budowanie i pakowanie dla wszystkich platform
* Wdrażanie na podłączone urządzenia mobilne

Dowiedz się więcej i zainstaluj Defold Kit z [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).

## Oprogramowanie dokumentacyjne

Dostępne są paczki przygotowane przez społeczność Defolda do generowania dokumentacji API dla [Dash i Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
