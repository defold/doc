---
title: Komunikacja sieciowa w Defold
brief: Ta instrukcja wyjaśnia, jak łączyć się ze zdalnymi serwerami i wykonywać inne rodzaje połączeń sieciowych.
---

# Komunikacja sieciowa

Nie jest niczym niezwykłym, że gry mają jakiś rodzaj połączenia z usługą backendową, na przykład do wysyłania wyników, obsługi dobierania graczy albo przechowywania zapisanych gier w chmurze. Wiele gier korzysta też z połączeń peer-to-peer, w których klienci gry komunikują się bezpośrednio ze sobą, bez udziału centralnego serwera. Połączenia sieciowe i wymianę danych można realizować przy użyciu kilku różnych protokołów i standardów. Więcej informacji o różnych sposobach korzystania z połączeń sieciowych w Defold znajdziesz tutaj:

* [Żądania HTTP](/manuals/http-requests)
* [Połączenia socketowe](/manuals/socket-connections)
* [Połączenia WebSocket](/manuals/websocket-connections)
* [Usługi online](/manuals/online-services)


## Szczegóły techniczne

### IPv4 i IPv6

Defold obsługuje połączenia IPv4 i IPv6 dla socketów oraz żądań HTTP.

### Bezpieczne połączenia

Defold obsługuje bezpieczne połączenia SSL dla socketów oraz żądań HTTP.

Defold może też opcjonalnie weryfikować certyfikat SSL dowolnego bezpiecznego połączenia. Weryfikacja SSL zostanie włączona, gdy w polu [SSL Certificates](/manuals/project-settings/#network) w sekcji Network w *game.project* zostanie podany plik PEM zawierający publiczne klucze certyfikatów głównych CA albo publiczny klucz samopodpisanego certyfikatu. Lista certyfikatów głównych CA jest dołączona w `builtins/ca-certificates`, ale zaleca się utworzenie nowego pliku PEM i wklejenie do niego potrzebnych certyfikatów głównych CA, zależnie od serwerów, z którymi łączy się gra.
