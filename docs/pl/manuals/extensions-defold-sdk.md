---
title: Natywne rozszerzenia - Defold SDK
brief: Ta instrukcja opisuje, jak pracować z Defold SDK podczas tworzenia natywnych rozszerzeń.
---

# Defold SDK

Defold SDK zawiera funkcje potrzebne do zadeklarowania natywnego rozszerzenia oraz do komunikacji z niskopoziomową natywną warstwą platformy, na której działa aplikacja, i wysokopoziomową warstwą Lua, w której tworzona jest logika gry.

## Użycie

Z Defold SDK korzystasz, dołączając plik nagłówkowy `dmsdk/sdk.h`:

    #include <dmsdk/sdk.h>

Dostępne funkcje i przestrzenie nazw Defold SDK są opisane w naszej [dokumentacji API](/ref/overview_cpp). Pliki nagłówkowe Defold SDK są udostępniane jako osobne archiwum `defoldsdk_headers.zip` dla każdego wydania Defold opublikowanego na [GitHub](https://github.com/defold/defold/releases). Możesz używać tych plików nagłówkowych do podpowiadania kodu w wybranym edytorze.
