---
title: Buforowanie zasobów
brief: Ta instrukcja wyjaśnia jak korzystać z buforowania zasobów w celu przyspieszenia budowania.
---

# Buforowanie zasobów

Gry tworzone w Defold zazwyczaj budują się w kilka sekund, ale w miarę rozwoju projektu rośnie też liczba zasobów. Kompilacja czcionek i kompresja tekstur może zajmować znaczną ilość czasu w dużym projekcie, a bufor zasobów (asset cache) służy do przyspieszenia kompilacji poprzez rekompilowanie tylko tych zasobów, które uległy zmianie, jednocześnie korzystając z już skompilowanych zasobów z bufora dla tych, które nie uległy zmianie.

Defold wykorzystuje trzy poziomy bufora:

1. Project cache (Bufor projektu)
2. Local cache (Bufor lokalny)
3. Remote cache (Bufor zdalny)

## Project cache (Bufor projektu)

Defold domyślnie buforuje skompilowane zasoby w katalogu `build/default` projektu w Defoldzie. Bufor projektu przyspieszy kolejne kompilacje, ponieważ będą ponownie kompilowane tylko zmienione zasoby, podczas gdy zasoby bez zmian będą wykorzystywane z bufora projektu. Ten bufor jest zawsze włączony i używany zarówno przez edytor, jak i narzędzia wiersza poleceń.

Bufor projektu można usunąć ręcznie, usuwając pliki w katalogu `build/default`, lub wydając polecenie `clean` za pomocą [narzędzia do kompilacji wiersza poleceń Bob](/manuals/bob).

## Local cache (Bufor lokalny)

Dodano w wersji Defold 1.2.187.

Bufor lokalny to opcjonalny, drugi bufor, w którym skompilowane zasoby są przechowywane w zewnętrznym miejscu na tym samym komputerze lub na dysku sieciowym. Dzięki swojemu zewnętrznemu położeniu zawartość bufora przetrwa oczyszczenie bufora projektu. Może być również współdzielony przez kilku programistów pracujących nad tym samym projektem. Bufor jest obecnie dostępny tylko podczas kompilacji za pomocą narzędzi wiersza poleceń. Jest aktywowany za pomocą opcji `resource-cache-local`:


```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```
Skompilowane zasoby są pobierane z bufora lokalnego na podstawie obliczonej sumy kontrolnej, która uwzględnia wersję silnika Defold, nazwy i treść źródłowych zasobów oraz opcje kompilacji projektu. Zapewnia to unikalność buforowanych zasobów i umożliwia współdzielenie bufora między różnymi wersjami Defold.

::: sidenote
Pliki przechowywane w buforze lokalnym są przechowywane na stałe. To programista jest odpowiedzialny za ręczne usuwanie starych/niewykorzystywanych plików.
:::


## Remote cache (Bufor zdalny)

Dodano w wersji Defold 1.2.187.

Bufor zdalny to opcjonalny, trzeci bufor, w którym skompilowane zasoby są przechowywane na serwerze i dostępne za pomocą żądania HTTP. Bufor jest obecnie dostępny tylko podczas kompilacji za pomocą narzędzi wiersza poleceń. Jest aktywowany za pomocą opcji `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Podobnie jak w przypadku bufora lokalnego, wszystkie zasoby są pobierane z bufora zdalnego na podstawie obliczonej sumy kontrolnej. Buforowane zasoby są dostępne za pomocą metod żądania HTTP GET, PUT i HEAD. Defold nie dostarcza serwera bufora zdalnego. Każdy programista, który chce korzystać z tego rozwiązania, jest odpowiedzialny za jego konfigurację. Przykładowo implementację podstawowego serwera Pythona można znaleźć [tutaj](https://github.com/britzl/httpserver-python).
