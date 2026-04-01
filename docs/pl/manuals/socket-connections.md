---
title: Połączenia socketów
brief: Ta instrukcja wyjaśnia, jak tworzyć połączenia socketów.
---

## Połączenia socketów

Defold zawiera bibliotekę [LuaSocket](https://lunarmodules.github.io/luasocket/) do tworzenia połączeń socketów TCP i UDP. Poniżej znajdziesz przykład tworzenia połączenia socketowego, wysyłania danych i odczytywania odpowiedzi:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

To utworzy socket TCP, połączy go z adresem IP 127.0.0.1 (localhost) i portem 8123. Ustawi czas oczekiwania na 0, aby socket był nieblokujący, a następnie wyśle ciąg "foobar" przez socket. Odczyta też jedną linię danych (bajty kończące się znakiem nowej linii) z socketu. Zwróć uwagę, że ten przykład nie zawiera żadnej obsługi błędów.

### Odwołanie do API i przykłady

W [odwołaniu do API](/ref/socket/) znajdziesz więcej informacji o funkcjach dostępnych przez LuaSocket. Oficjalna [dokumentacja LuaSocket](https://lunarmodules.github.io/luasocket/) zawiera także wiele przykładów korzystania z biblioteki. Przykłady i moduły pomocnicze znajdziesz również w [bibliotece DefNet](https://github.com/britzl/defnet/).
