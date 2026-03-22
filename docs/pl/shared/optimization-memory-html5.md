## Rozmiar sterty (HTML5)
Rozmiar sterty gry HTML5 w Defold można skonfigurować w polu [`heap_size`](/manuals/project-settings/#heap-size) w *game.project*. Pamiętaj, aby zoptymalizować zużycie pamięci w grze i ustawić możliwie najmniejszy rozmiar sterty.

W przypadku małych gier osiągalny jest rozmiar sterty na poziomie 32 MB. W przypadku większych gier celuj w 64-128 MB. Jeśli na przykład jesteś na poziomie 58 MB i dalsza optymalizacja nie jest już możliwa, możesz bez zbędnego roztrząsania zatrzymać się na 64 MB. Nie ma sztywno ustalonego docelowego rozmiaru - zależy to od gry. Staraj się po prostu, aby wartości były mniejsze, najlepiej skokami odpowiadającymi potęgom dwójki.

Aby sprawdzić bieżące zużycie sterty, możesz uruchomić grę i zagrać w najbardziej zasobożernym poziomie lub sekcji, a następnie obserwować zużycie pamięci:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

Możesz też otworzyć narzędzia deweloperskie przeglądarki i wpisać w konsoli następującą komendę:

```js
HEAP8.length / 1024 / 1024
```

Jeśli zużycie pamięci pozostaje na poziomie 32 MB, to świetnie. Jeśli nie, wykonaj kroki, aby [zoptymalizować rozmiar samego silnika oraz dużych zasobów, takich jak dźwięki i tekstury](/manuals/optimization-size).
