---
title: Połączenia socketowe
brief: Ta instrukcja wyjaśnia, jak tworzyć połączenia socketowe.
---

## Połączenia socketowe

Defold zawiera bibliotekę [LuaSocket](https://lunarmodules.github.io/luasocket/) do tworzenia połączeń socketowych TCP i UDP. Poniżej znajduje się przykład tworzenia połączenia socketowego, wysyłania danych i odczytywania odpowiedzi:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

To utworzy socket TCP, połączy go z adresem IP 127.0.0.1 (localhost) i portem 8123. Ustawi timeout na 0, aby socket był nieblokujący, i wyśle ciąg `"foobar"` przez socket. Odczyta też jedną linię danych (bajty kończące się znakiem nowej linii) z socketu. Zwróć uwagę, że powyższy przykład nie zawiera żadnej obsługi błędów.

### Dokumentacja API i przykłady

Więcej informacji o funkcjonalności dostępnej przez LuaSocket znajdziesz w [odwołaniu do API](/ref/socket/). Oficjalna [dokumentacja LuaSocket](https://lunarmodules.github.io/luasocket/) zawiera też wiele przykładów korzystania z biblioteki. Kilka przykładów i modułów pomocniczych znajdziesz również w [bibliotece DefNet](https://github.com/britzl/defnet/).
