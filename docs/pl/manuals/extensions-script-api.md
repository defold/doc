---
title: Dodawanie autouzupełniania edytora do rozszerzeń natywnych
brief: Ta instrukcja wyjaśnia, jak utworzyć definicję API skryptu, aby edytor Defold mógł podpowiadać autouzupełnianie użytkownikom rozszerzenia.
---

# Autouzupełnianie dla rozszerzeń natywnych

Edytor Defold udostępnia podpowiedzi autouzupełniania dla wszystkich funkcji API Defold i generuje sugestie dla modułów Lua wymaganych przez twoje skrypty. Nie potrafi jednak automatycznie udostępniać podpowiedzi autouzupełniania dla funkcjonalności wystawianej przez rozszerzenia natywne. Rozszerzenie natywne może dostarczyć definicję API w osobnym pliku, aby włączyć podpowiedzi autouzupełniania także dla API rozszerzenia.

## Tworzenie definicji API skryptu

Plik definicji API skryptu ma rozszerzenie `.script_api`. Musi być zapisany w formacie [YAML](https://yaml.org/) i znajdować się razem z plikami rozszerzenia. Oczekiwany format definicji API skryptu wygląda następująco:

```yml
- name: Nazwa rozszerzenia
  type: table
  desc: Opis rozszerzenia
  members:
  - name: Nazwa pierwszego elementu
    type: Typ elementu
    desc: Opis elementu
    # jeśli typ elementu to "function"
    parameters:
    - name: Nazwa pierwszego parametru
      type: Typ parametru
      desc: Opis parametru
    - name: Nazwa drugiego parametru
      type: Typ parametru
      desc: Opis parametru
    # jeśli typ elementu to "function"
    returns:
    - name: Nazwa pierwszej wartości zwracanej
      type: Typ wartości zwracanej
      desc: Opis wartości zwracanej
    examples:
    - desc: Pierwszy przykład użycia elementu
    - desc: Drugi przykład użycia elementu

  - name: Nazwa drugiego elementu
    ...
```

Typami mogą być dowolne z: `table`, `string`, `boolean`, `number`, `function`. Jeśli wartość może mieć wiele typów, zapisuje się ją jako `[type1, type2, type3]`.
::: sidenote
Typy nie są obecnie wyświetlane w edytorze. Warto mimo to je podawać, aby były dostępne, gdy edytor zyska obsługę wyświetlania informacji o typach.
:::

## Przykłady

Przykłady rzeczywistego użycia znajdziesz w następujących projektach:

* [Rozszerzenie Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Rozszerzenie WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
