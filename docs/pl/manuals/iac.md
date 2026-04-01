---
title: Komunikacja między aplikacjami w Defold
brief: Komunikacja między aplikacjami pozwala odczytywać argumenty uruchomieniowe użyte przy starcie aplikacji. Ta instrukcja opisuje API Defold dostępne dla tej funkcji.
---

# Komunikacja między aplikacjami

Aplikacje na większości systemów operacyjnych można uruchamiać na kilka sposobów:

* Z listy zainstalowanych aplikacji
* Z linku przeznaczonego dla konkretnej aplikacji
* Z powiadomienia push
* Jako końcowy etap procesu instalacji.

W przypadku uruchomienia aplikacji z linku, powiadomienia albo po instalacji można przekazać dodatkowe argumenty, takie jak install referrer podczas instalacji lub deep-link przy uruchamianiu z linku aplikacji albo z powiadomienia. Defold udostępnia ujednolicony sposób pobierania informacji o tym, jak aplikacja została wywołana, za pomocą rozszerzenia natywnego.

## Instalowanie rozszerzenia

Aby zacząć korzystać z rozszerzenia komunikacji między aplikacjami (Inter-app communication), trzeba dodać je jako zależność do pliku *game.project*. Najnowsza stabilna wersja jest dostępna pod adresem URL zależności:
```
https://github.com/defold/extension-iac/archive/master.zip
```

Zalecamy użycie linku do archiwum zip z [konkretną wersją](https://github.com/defold/extension-iac/releases).

## Korzystanie z rozszerzenia

API jest bardzo proste w użyciu. Przekazujesz rozszerzeniu funkcję nasłuchującą i reagujesz na wywołania zwrotne, które od niej otrzymujesz.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- To było wywołanie.
         print(payload.origin) -- origin może być pustym ciągiem, jeśli nie dało się go ustalić
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

Pełna dokumentacja API jest dostępna na [stronie GitHub rozszerzenia](https://defold.github.io/extension-iac/).
