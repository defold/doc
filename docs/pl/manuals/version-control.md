---
title: Kontrola wersji
brief: Ta instrukcja opisuje używanie Git w projektach Defold oraz sprawdzanie lokalnych zmian w edytorze.
---

# Kontrola wersji

Projekty Defold dobrze współpracują z [Git](https://git-scm.com), ale synchronizacja odbywa się poza edytorem. Używaj wybranego klienta Git albo wiersza poleceń, aby klonować repozytorium, pobierać i wysyłać zmiany, tworzyć commity i gałęzie oraz rozwiązywać konflikty.

## Zmodyfikowane pliki

Gdy katalog projektu jest katalogiem głównym drzewa roboczego Git z co najmniej jednym commitem, Defold wyświetla w panelu edytora *Changed Files* nieignorowane pliki wykryte jako dodane, zmodyfikowane, usunięte lub przemianowane. Wpisy te powstają przez bezpośrednie porównanie plików na dysku z bieżącym commitem (`HEAD`), więc dodanie zmiany do indeksu nie wpływa na listę. Konflikty scalania rozwiązuj w zewnętrznym kliencie Git.

![zmienione pliki](images/workflow/changed_files.png)

Zaznacz dokładnie jeden zmodyfikowany lub przemianowany plik i kliknij <kbd>Diff</kbd>, aby zobaczyć jego tekstowy diff. Kliknij <kbd>Revert</kbd>, aby odrzucić wybrane zmiany w drzewie roboczym i indeksie. Śledzone pliki zostaną przywrócone do stanu z `HEAD`; pliki nieobecne w `HEAD` zostaną usunięte bez względu na to, czy dodano je do indeksu; w przypadku przemianowania nowa ścieżka zostanie usunięta, a stara przywrócona. Tej operacji nie można cofnąć w edytorze, dlatego zacommituj albo utwórz kopię zapasową potrzebnej pracy.

## Git

Git wydajnie przechowuje tekstowe pliki projektów Defold. Często zmieniane duże zasoby binarne, takie jak pliki PSD czy pliki robocze produkcji audio, mogą jednak szybko powiększać historię repozytorium. Dla dużych plików roboczych rozważ Git LFS albo osobne rozwiązanie do przechowywania i tworzenia kopii zapasowych.

Panel *Changed Files* udostępnia tylko lokalny status, diff i operacje cofania. Nie wie, czy commity zostały wysłane do zdalnego repozytorium, i nie pobiera, nie scala, nie commituje ani nie wysyła zmian. Wykonuj te operacje w zewnętrznym kliencie Git albo z wiersza poleceń. Domyślnie po odzyskaniu fokusu Defold wczytuje zmiany zewnętrzne i odświeża panel. Jeśli opcja *Load External Changes on App Focus* jest wyłączona, wybierz *File ▸ Load External Changes*.
