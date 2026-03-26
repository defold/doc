---
title: Uruchamianie development app na urządzeniu
brief: Ta instrukcja wyjaśnia, jak zainstalować development app na urządzeniu, aby wygodnie rozwijać projekt iteracyjnie bezpośrednio na nim.
---

# Mobilna development app

Development app (aplikacja do tworzenia i testowania gry na urządzeniu) pozwala przesyłać do niej zawartość przez Wi-Fi. Dzięki temu znacznie skraca się czas iteracji, bo nie trzeba za każdym razem budować i instalować aplikacji, gdy chcesz sprawdzić zmiany. Instalujesz development app na urządzeniu lub urządzeniach, uruchamiasz ją, a potem wybierasz urządzenie jako cel budowania w edytorze.

## Instalowanie development app

Każda aplikacja na iOS lub Androidzie zbudowana w wariancie Debug może działać jako development app. To zalecane rozwiązanie, ponieważ taka development app ma poprawne ustawienia projektu i korzysta z tych samych [rozszerzeń natywnych](/manuals/extensions/) co projekt, nad którym pracujesz.

Od wersji Defold 1.4.0 można zbudować wariant Debug projektu bez żadnej zawartości. Użyj tej opcji, aby utworzyć wersję aplikacji z rozszerzeniami natywnymi, odpowiednią do iteracyjnego tworzenia i testowania opisanego w tej instrukcji.

![paczka bez zawartości](images/dev-app/contentless-bundle.png)

### Instalowanie na iOS

Postępuj zgodnie z [instrukcjami w podręczniku iOS](/manuals/ios/#creating-an-ios-application-bundle), aby utworzyć paczkę dla iOS. Upewnij się, że wybierasz wariant Debug!

### Instalowanie na Androidzie

Postępuj zgodnie z [instrukcjami w podręczniku Android](https://defold.com/manuals/android/#creating-an-android-application-bundle), aby utworzyć paczkę dla Androida.

## Uruchamianie gry

Aby uruchomić grę na urządzeniu, development app i edytor muszą móc połączyć się ze sobą przez tę samą sieć Wi-Fi albo przez USB (zobacz niżej).

1. Upewnij się, że edytor jest uruchomiony.
2. Uruchom development app na urządzeniu.
3. Wybierz urządzenie w menu <kbd>Project ▸ Targets</kbd> w edytorze.
4. Wybierz <kbd>Project ▸ Build</kbd>, aby uruchomić grę. Start może chwilę potrwać, ponieważ zawartość gry jest przesyłana strumieniowo na urządzenie przez sieć.
5. Gdy gra działa, możesz jak zwykle korzystać z [szybkiego przeładowania](/manuals/hot-reload/).

### Łączenie z urządzeniem iOS przez USB w systemie Windows

Jeśli łączysz się przez USB w systemie Windows z development app działającą na urządzeniu iOS, najpierw musisz [zainstalować iTunes](https://www.apple.com/lae/itunes/download/). Po zainstalowaniu iTunes musisz też [włączyć Personal Hotspot](https://support.apple.com/en-us/HT204023) na urządzeniu iOS w ustawieniach urządzenia. Jeśli zobaczysz alert z pytaniem <kbd>Trust This Computer?</kbd>, stuknij <kbd>Trust</kbd>. Gdy development app działa, urządzenie powinno teraz pojawić się w menu <kbd>Project ▸ Targets</kbd>.

### Łączenie z urządzeniem iOS przez USB w systemie Linux

W systemie Linux musisz włączyć Personal Hotspot na urządzeniu w ustawieniach urządzenia, gdy jest ono podłączone przez USB. Jeśli zobaczysz alert z pytaniem <kbd>Trust This Computer?</kbd>, stuknij <kbd>Trust</kbd>. Gdy development app działa, urządzenie powinno teraz pojawić się w menu <kbd>Project ▸ Targets</kbd>.

### Łączenie z urządzeniem iOS przez USB w systemie macOS

W nowszych wersjach iOS urządzenie po podłączeniu przez USB do macOS automatycznie otworzy nowy interfejs Ethernet między urządzeniem a komputerem. Gdy development app działa, urządzenie powinno pojawić się w menu <kbd>Project ▸ Targets</kbd>.

W starszych wersjach iOS musisz włączyć Personal Hotspot na urządzeniu w ustawieniach urządzenia, gdy jest ono podłączone przez USB do macOS. Jeśli zobaczysz alert z pytaniem <kbd>Trust This Computer?</kbd>, stuknij <kbd>Trust</kbd>. Gdy development app działa, urządzenie powinno teraz pojawić się w menu <kbd>Project ▸ Targets</kbd>.

### Łączenie z urządzeniem Android przez USB w systemie macOS

W macOS można połączyć się przez USB z działającą development app na urządzeniu Android, gdy na urządzeniu jest włączony tryb <kbd>USB Tethering</kbd>. W macOS trzeba zainstalować sterownik zewnętrzny, taki jak [HoRNDIS](https://joshuawise.com/horndis#available_versions). Po zainstalowaniu HoRNDIS trzeba też zezwolić mu na działanie w ustawieniach Security & Privacy. Gdy <kbd>USB Tethering</kbd> jest włączone, urządzenie pojawi się w menu <kbd>Project ▸ Targets</kbd>, jeśli development app działa.

### Łączenie z urządzeniem Android przez USB w systemie Windows lub Linux

W systemach Windows i Linux można połączyć się przez USB z działającą development app na urządzeniu Android, gdy na urządzeniu jest włączony tryb <kbd>USB Tethering</kbd>. Gdy <kbd>USB Tethering</kbd> jest włączone, urządzenie pojawi się w menu <kbd>Project ▸ Targets</kbd>, jeśli development app działa.

## Rozwiązywanie problemów

Nie można pobrać aplikacji (Unable to download application)
: Upewnij się, że UDID urządzenia znajduje się w profilu provisioning użytym do podpisania aplikacji.

Urządzenie nie pojawia się w menu <kbd>Project ▸ Targets</kbd>
: Upewnij się, że urządzenie jest połączone z tą samą siecią Wi-Fi co komputer. Upewnij się też, że development app została zbudowana w wariancie Debug.

Gra nie uruchamia się i pojawia się komunikat o niezgodnych wersjach
: Dzieje się tak, gdy zaktualizujesz edytor do najnowszej wersji. Musisz zbudować i zainstalować nową wersję.
