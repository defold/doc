---
title: Kontrola wersji
brief: Ta instrukcja opisuje pracę z wbudowanym systemem kontroli wersji.
---

# Kontrola wersji

Defold został zaprojektowany z myślą o małych zespołach, które intensywnie współpracują przy tworzeniu gier. Członkowie zespołu mogą pracować równolegle nad tymi samymi zasobami z bardzo małymi utrudnieniami. Defold ma wbudowaną obsługę kontroli wersji z użyciem [Gita](https://git-scm.com). Git jest przeznaczony do rozproszonej pracy zespołowej i jest niezwykle potężnym narzędziem, które umożliwia szeroki zakres przepływów pracy.

## Zmienione pliki

Gdy zapisujesz zmiany w lokalnej kopii roboczej, Defold śledzi wszystkie zmiany w panelu edytora *Changed Files*, wymieniając każdy plik, który został dodany, usunięty lub zmodyfikowany.

![zmienione pliki](images/workflow/changed_files.png)

Zaznacz plik na liście i kliknij <kbd>Diff</kbd>, aby zobaczyć zmiany wprowadzone w pliku, albo <kbd>Revert</kbd>, aby cofnąć wszystkie zmiany i przywrócić plik do stanu sprzed ostatniej synchronizacji.

## Git

Git został zaprojektowany przede wszystkim do obsługi kodu źródłowego i plików tekstowych, dlatego przechowuje tego typu pliki bardzo oszczędnie. Zachowywane są tylko różnice między kolejnymi wersjami, dzięki czemu możesz utrzymywać rozbudowaną historię zmian wszystkich plików projektu przy stosunkowo niewielkim koszcie miejsca. Pliki binarne, takie jak obrazy lub pliki dźwiękowe, nie korzystają jednak z takiego sposobu przechowywania. Każda nowa wersja, którą zatwierdzasz i synchronizujesz, zajmuje mniej więcej tyle samo miejsca. Zwykle nie stanowi to dużego problemu w przypadku końcowych zasobów projektu, takich jak obrazy JPEG lub PNG czy pliki dźwiękowe OGG, ale może szybko stać się problemem przy roboczych plikach projektu, takich jak pliki PSD czy projekty Pro Tools. Tego typu pliki często bardzo rosną, ponieważ zwykle pracujesz w znacznie wyższej rozdzielczości niż docelowe zasoby. Ogólnie uważa się, że najlepiej unikać umieszczania dużych plików roboczych pod kontrolą Gita i zamiast tego korzystać z osobnego rozwiązania do przechowywania i tworzenia kopii zapasowych.

Istnieje wiele sposobów wykorzystania Gita w zespołowym przepływie pracy. Ten używany w Defold wygląda następująco. Gdy synchronizujesz projekt, dzieje się to w taki sposób:

1. Wszelkie lokalne zmiany są tymczasowo odkładane do stasha, aby można je było przywrócić, jeśli później coś się nie powiedzie w procesie synchronizacji.
2. Zmiany z serwera są pobierane.
3. Stash jest stosowany, a lokalne zmiany zostają przywrócone. Może to spowodować konflikty scalania, które trzeba rozwiązać.
4. Użytkownik dostaje możliwość zatwierdzenia lokalnych zmian plików.
5. Jeśli istnieją lokalne commity, użytkownik może wybrać, czy wypchnąć je na serwer. Również w tym przypadku może dojść do konfliktów, które trzeba rozwiązać.

Jeśli wolisz inny przepływ pracy, możesz używać Gita z wiersza poleceń albo przez aplikację firm trzecich do wykonywania `pull`, `push`, `commit` i `merge`, pracy na kilku gałęziach i tak dalej.
