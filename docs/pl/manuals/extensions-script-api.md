---
title: Dodawanie autouzupełniania edytora do rozszerzeń natywnych
brief: Ta instrukcja wyjaśnia, jak utworzyć definicję API skryptu, aby edytor Defold mógł oferować autouzupełnianie użytkownikom rozszerzenia.
---

# Autouzupełnianie dla rozszerzeń natywnych

Edytor Defold udostępnia podpowiedzi autouzupełniania dla wszystkich funkcji API Defold i generuje sugestie dla modułów Lua wymaganych przez twoje skrypty. Nie potrafi jednak automatycznie oferować podpowiedzi autouzupełniania dla funkcjonalności wystawianej przez rozszerzenia natywne. Rozszerzenie natywne może dostarczyć definicję API w osobnym pliku, aby włączyć podpowiedzi autouzupełniania także dla API rozszerzenia.

## Tworzenie definicji API skryptu

Plik definicji API skryptu ma rozszerzenie `.script_api`. Musi być zapisany w formacie [YAML](https://yaml.org/) i znajdować się razem z plikami rozszerzenia. Oczekiwany format definicji API skryptu wygląda tak:

```yml
- name: The name of the extension
  type: table
  desc: Extension description
  members:
  - name: Name of the first member
    type: Member type
    desc: Member description
    # if member type is "function"
    parameters:
    - name: Name of the first parameter
      type: Parameter type
      desc: Parameter description
    - name: Name of the second parameter
      type: Parameter type
      desc: Parameter description
    # if member type is "function"
    returns:
    - name: Name of first return value
      type: Return value type
      desc: Return value description
    examples:
    - desc: First example of member usage
    - desc: Second example of member usage

  - name: Name of the second member
    ...
```

Typami mogą być dowolne z `table, string , boolean, number, function`. Jeśli wartość może mieć wiele typów, zapisuje się ją jako `[type1, type2, type3]`.
::: sidenote
Typy nie są obecnie wyświetlane w edytorze. Warto mimo to je podawać, aby były dostępne, gdy edytor zyska obsługę wyświetlania informacji o typach.
:::

## Przykłady

Przykłady rzeczywistego użycia znajdziesz w następujących projektach:

* [Facebook extension](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [WebView extension](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
