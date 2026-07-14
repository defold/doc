---
title: Natywne rozszerzenia - Defold SDK
brief: Ta instrukcja opisuje, jak pracować z Defold SDK podczas tworzenia natywnych rozszerzeń.
---

# Defold SDK

Defold SDK zawiera funkcje potrzebne do zadeklarowania natywnego rozszerzenia oraz do komunikacji z niskopoziomową natywną warstwą platformy, na której działa aplikacja, i wysokopoziomową warstwą Lua, w której tworzona jest logika gry.

## Użycie

C++ rozszerzenia mogą dołączać zbiorczy plik nagłówkowy `dmsdk/sdk.h`:

```cpp
#include <dmsdk/sdk.h>
```

Zbiorczy nagłówek zawiera deklaracje C++ i nie można go dołączać z pliku źródłowego C. Pliki źródłowe C powinny dołączać potrzebne im pojedyncze nagłówki `.h` zgodne z C, na przykład:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Tylko część dmSDK ma obecnie interfejs w czystym C; nie każdy podsystem C++ ma odpowiednik w C. Dostępne funkcje i typy są opisane w [przeglądzie API C](/ref/overview_defoldc/) oraz [przeglądzie API C++](/ref/overview_defoldcpp/). Pliki nagłówkowe Defold SDK są udostępniane jako osobne archiwum `defoldsdk_headers.zip` dla każdego wydania Defold opublikowanego na [GitHub](https://github.com/defold/defold/releases). Możesz używać tych plików nagłówkowych do podpowiadania kodu w wybranym edytorze.
