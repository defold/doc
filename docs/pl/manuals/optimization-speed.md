---
title: Optymalizacja wydajności w czasie działania gry w Defold
brief: Ta instrukcja opisuje, jak zoptymalizować grę w Defold, aby działała ze stabilną, wysoką liczbą klatek na sekundę.
---

# Optymalizacja szybkości działania w czasie gry
Zanim zaczniesz optymalizować grę z myślą o stabilnej, wysokiej liczbie klatek na sekundę, musisz wiedzieć, gdzie znajdują się wąskie gardła. Co właściwie zajmuje najwięcej czasu w jednej klatce gry? Czy jest to renderowanie? Logika gry? Graf sceny? Aby to ustalić, zaleca się korzystanie z wbudowanych narzędzi profilujących. Użyj [profilera ekranowego lub internetowego](/manuals/profiling/), aby zmierzyć wydajność gry, a następnie zdecyduj, co i czy w ogóle optymalizować. Gdy lepiej zrozumiesz, co pochłania czas, możesz zacząć usuwać problemy.

## Ogranicz czas wykonywania skryptów
Ograniczenie czasu wykonywania skryptów jest potrzebne wtedy, gdy profiler pokazuje wysokie wartości dla zakresu `Script`. Zasada ogólna jest prosta: w każdej klatce uruchamiaj możliwie jak najmniej kodu. Uruchamianie dużej ilości kodu w `update()` i `on_input()` w każdej klatce prawdopodobnie wpłynie na wydajność gry, zwłaszcza na słabszych urządzeniach. Kilka wskazówek:

### Stosuj reaktywne wzorce kodu
Nie sprawdzaj cyklicznie, czy coś się zmieniło, jeśli możesz dostać wywołanie zwrotne. Nie animuj ręcznie czegoś ani nie wykonuj zadania, które może przejąć silnik, np. `go.animate()` zamiast ręcznego animowania.

### Ogranicz zbieranie śmieci
Jeśli w każdej klatce tworzysz wiele obiektów krótkiego życia, takich jak tablice Lua, w końcu uruchomisz odśmiecanie pamięci przez Lua. Gdy do tego dojdzie, może się to objawiać krótkimi zacięciami lub skokami czasu klatki. W miarę możliwości ponownie używaj tablic i staraj się unikać tworzenia tablic Lua wewnątrz pętli oraz podobnych konstrukcji.

### Wstępnie haszuj identyfikatory wiadomości i akcji
Jeśli często obsługujesz wiadomości lub masz do przetworzenia wiele zdarzeń wejściowych, zaleca się wstępne haszowanie ciągów znaków. Rozważ ten fragment kodu:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

W powyższym scenariuszu haszowany ciąg znaków byłby tworzony ponownie za każdym razem, gdy odebrana zostanie wiadomość. Można to poprawić, tworząc hasze tylko raz i używając już zahaszowanych wartości podczas obsługi wiadomości:

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### Preferuj i buforuj URL-e
Przekazywanie wiadomości lub inne sposoby adresowania obiektu gry albo komponentu można realizować zarówno przez podanie identyfikatora jako stringa lub hasha, jak i jako URL. Jeśli użyjesz stringa lub hasha, zostanie on wewnętrznie przekształcony w URL. Dlatego zaleca się buforowanie URL-i, których używa się często, aby uzyskać z systemu możliwie najlepszą wydajność. Rozważ następujący przykład:

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- zrób coś z pos
```

We wszystkich trzech przypadkach pobrana zostałaby pozycja obiektu gry o identyfikatorze `enemy`. W pierwszym i drugim przypadku identyfikator (string lub hash) zostałby przekonwertowany do URL-a przed użyciem. Oznacza to, że lepiej jest buforować URL-e i używać wersji zbuforowanej, aby uzyskać możliwie najlepszą wydajność:

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- zrób coś z pos
    end
```

## Ogranicz czas renderowania klatki
Ograniczenie czasu potrzebnego na wyrenderowanie klatki jest potrzebne wtedy, gdy profiler pokazuje wysokie wartości w zakresach `Render` i `Render Script`. Przy próbie skrócenia czasu renderowania klatki warto wziąć pod uwagę kilka rzeczy:

* Ogranicz liczbę wywołań rysowania - więcej informacji o ograniczaniu draw calls znajdziesz w [tym poście na forum](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Ogranicz overdraw
* Ogranicz złożoność shaderów - więcej o optymalizacjach GLSL przeczytasz w [tym artykule Khronosa](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). Możesz też zmodyfikować domyślne shadery używane przez silnik Defold (znajdujące się w `builtins/materials`) i obniżyć precyzję shaderów, aby uzyskać pewien wzrost szybkości na słabszych urządzeniach. Wszystkie shadery używają precyzji `highp`, a zmiana na przykład na `mediump` w niektórych przypadkach może nieznacznie poprawić wydajność.

## Ogranicz złożoność grafu sceny
Ograniczenie złożoności grafu sceny jest potrzebne wtedy, gdy profiler pokazuje wysokie wartości w zakresie `GameObject`, a konkretnie dla próbki `UpdateTransform`. Kilka działań, które można podjąć:

* Culling - wyłączaj obiekty gry (i ich komponenty), jeśli nie są obecnie widoczne. To, jak to ustalić, zależy bardzo od rodzaju gry. W grze 2D może to być tak proste, jak zawsze wyłączanie obiektów gry znajdujących się poza prostokątnym obszarem. Możesz użyć wyzwalacza fizyki, aby to wykryć, albo podzielić obiekty na grupy. Gdy już wiesz, które obiekty wyłączyć lub włączyć, zrób to, wysyłając do każdego obiektu gry wiadomość `disable` lub `enable`.

## Wycinanie w bryle widoku
Skrypt renderowania może automatycznie pomijać renderowanie komponentów obiektów gry, które znajdują się poza zdefiniowaną ramką ograniczającą (frustum). Więcej o Frustum Culling przeczytasz w [instrukcji Render Pipeline](/manuals/render/#frustum-culling).

# Optymalizacje specyficzne dla platform

## Android Device Performance Framework
Android Dynamic Performance Framework to zestaw API, które pozwalają grom wchodzić w bezpośredniejszą interakcję z systemami zasilania i kontroli temperatury urządzeń Android. Można monitorować dynamiczne zachowanie na systemach Android i optymalizować wydajność gry na poziomie, który jest zrównoważony i nie powoduje przegrzewania urządzeń. Użyj [rozszerzenia Android Dynamic Performance Framework](https://defold.com/extension-adpf/), aby monitorować i optymalizować wydajność gry w silniku Defold na urządzeniach Android.
