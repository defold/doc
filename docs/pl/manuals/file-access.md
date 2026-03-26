---
title: Praca z plikami
brief: Ta instrukcja wyjaśnia, jak zapisywać i odczytywać pliki oraz wykonywać inne operacje na plikach.
---

# Praca z plikami
Istnieje wiele różnych sposobów tworzenia plików i uzyskiwania do nich dostępu. Ścieżki do plików oraz sposób korzystania z nich zależą od typu pliku i jego lokalizacji.

## Funkcje dostępu do plików i folderów
Defold udostępnia kilka różnych funkcji do pracy z plikami:

* Możesz użyć standardowych funkcji [`io.*`](https://defold.com/ref/stable/io/) do odczytu i zapisu plików. Funkcje te dają bardzo precyzyjną kontrolę nad całym procesem I/O.

```lua
-- otwórz myfile.txt do zapisu w trybie binarnym
-- w razie błędu zwraca nil oraz komunikat o błędzie
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- zapisz do pliku, wymuś zapis na dysk, a potem zamknij plik
f:write("Foobar")
f:flush()
f:close()

-- otwórz myfile.txt do odczytu w trybie binarnym
-- w razie błędu zwraca nil oraz komunikat o błędzie
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- odczytaj cały plik jako łańcuch znaków
-- w razie błędu zwraca nil
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* Możesz użyć [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) i [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) do zmieniania nazw plików i ich usuwania.

* Możesz użyć [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) i [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) do odczytu i zapisu tabel Lua. Dodatkowe funkcje [`sys.*`](https://defold.com/ref/stable/sys/) pomagają w rozwiązywaniu ścieżek do plików w sposób niezależny od platformy.

```lua
-- pobierz ścieżkę niezależną od platformy do pliku "highscore" dla aplikacji "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- zapisz tabelę Lua z danymi
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- wczytaj dane
local data = sys.load(path)
print(data.highscore) -- 100
```


## Lokalizacje plików i folderów
Lokalizacje plików i folderów można podzielić na trzy kategorie:

* Pliki specyficzne dla aplikacji, tworzone przez twoją aplikację
* Pliki i foldery dołączone do aplikacji
* Pliki systemowe, do których uzyskuje dostęp twoja aplikacja

### Jak zapisywać i odczytywać pliki specyficzne dla aplikacji
Podczas zapisywania i odczytywania plików specyficznych dla aplikacji, takich jak wyniki, ustawienia użytkownika i stan gry, zaleca się używanie lokalizacji dostarczonej przez system operacyjny i przeznaczonej właśnie do tego celu. Możesz użyć [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name), aby uzyskać bezwzględną ścieżkę do pliku zależną od systemu operacyjnego. Gdy masz już tę ścieżkę bezwzględną, możesz korzystać z funkcji `sys.*`, `io.*` i `os.*` (patrz wyżej).

[Sprawdź przykład pokazujący, jak używać `sys.save()` i `sys.load()`](/examples/file/sys_save_load/).

### Jak uzyskiwać dostęp do plików dołączonych do aplikacji
Pliki możesz dołączać do aplikacji za pomocą zasobów pakietu i zasobów niestandardowych.

#### Zasoby niestandardowe
:[Zasoby niestandardowe](../shared/custom-resources.md)

```lua
-- Wczytaj dane poziomu do łańcucha znaków
local data, error = sys.load_resource("/assets/level_data.json")
-- Zdekoduj łańcuch JSON do tabeli Lua
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Zasoby pakietu
:[Zasoby pakietu](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: sidenote
Ze względów bezpieczeństwa przeglądarki internetowe, a przez to także każdy kod JavaScript uruchamiany w przeglądarce, nie mają dostępu do plików systemowych. Operacje na plikach w kompilacjach HTML5 w silniku Defold nadal działają, ale tylko na „wirtualnym systemie plików” korzystającym z API IndexedDB w przeglądarce. Oznacza to, że nie ma sposobu na dostęp do zasobów pakietu przy użyciu funkcji `io.*` lub `os.*`. Możesz jednak uzyskać do nich dostęp za pomocą `http.request()`.
:::


#### Porównanie zasobów niestandardowych i zasobów pakietu

| Cecha                      | Zasoby niestandardowe                     | Zasoby pakietu                               |
|----------------------------|-------------------------------------------|----------------------------------------------|
| Szybkość wczytywania       | Szybsza - pliki wczytywane z archiwum binarnego | Wolniejsza - pliki wczytywane z systemu plików |
| Wczytywanie części plików   | Nie - tylko całe pliki                    | Tak - można odczytywać dowolne bajty z pliku   |
| Modyfikacja po zbudowaniu   | Nie - pliki przechowywane są w archiwum binarnym | Tak - pliki są przechowywane w lokalnym systemie plików |
| Obsługa HTML5              | Tak                                       | Tak - ale dostęp odbywa się przez HTTP, a nie przez I/O plików |


### Dostęp do plików systemowych
Dostęp do plików systemowych może być ograniczony przez system operacyjny ze względów bezpieczeństwa. Możesz użyć natywnego rozszerzenia [`extension-directories`](https://defold.com/assets/extensiondirectories/), aby uzyskać bezwzględną ścieżkę do niektórych często używanych katalogów systemowych (np. documents, resource, temp). Gdy masz już bezwzględną ścieżkę do tych plików, możesz używać funkcji `io.*` i `os.*` do uzyskiwania do nich dostępu (patrz wyżej).

::: sidenote
Ze względów bezpieczeństwa przeglądarki internetowe, a przez to także każdy kod JavaScript uruchamiany w przeglądarce, nie mają dostępu do plików systemowych. Operacje na plikach w kompilacjach HTML5 w silniku Defold nadal działają, ale tylko na „wirtualnym systemie plików” korzystającym z API IndexedDB w przeglądarce. Oznacza to, że nie ma sposobu na dostęp do plików systemowych w kompilacjach HTML5.
:::

## Rozszerzenia
W [Asset Portal](https://defold.com/assets/) znajduje się kilka zasobów, które upraszczają dostęp do plików i folderów. Na przykład:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - funkcje do pracy z katalogami, uprawnieniami do plików itp.
* [DefSave](https://defold.com/assets/defsave/) - moduł pomagający zapisywać i wczytywać konfigurację oraz dane gracza między sesjami.
