---
title: Bufor
brief: Ta instrukcja wyjaśnia, jak działają zasoby Buffer w silniku Defold.
---

# Bufor

Zasób Buffer służy do opisywania jednego lub wielu strumieni wartości, na przykład pozycji albo kolorów. Każdy strumień ma nazwę, typ danych, liczbę wartości oraz same dane. Przykład:

```
[
  {
    "name": "position",
    "type": "float32",
    "count": 3,
    "data": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      1.0,
      ...
    ]
  }
]
```

Powyższy przykład opisuje strumień pozycji w trzech wymiarach, zapisanych jako 32-bitowe liczby zmiennoprzecinkowe. Format pliku zasobu Buffer to JSON, a jego rozszerzenie to `.buffer`.

Zasoby Buffer są zazwyczaj tworzone przy użyciu zewnętrznych narzędzi lub skryptów, na przykład podczas eksportu z programów do modelowania, takich jak Blender.

Zasób Buffer może być użyty jako dane wejściowe dla [komponentu Mesh](/manuals/mesh). Zasoby Buffer można też tworzyć w czasie działania przy użyciu `buffer.create()` oraz [powiązanych funkcji API](/ref/stable/buffer/#buffer.create:element_count-declaration).
