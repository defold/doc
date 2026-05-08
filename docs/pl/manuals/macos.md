---
title: Tworzenie aplikacji Defold na platformie macOS
brief: Ta instrukcja opisuje, jak budować i uruchamiać aplikacje Defold na macOS
---

# Tworzenie na macOS

Tworzenie aplikacji Defold na platformie macOS jest prostym procesem i wymaga bardzo niewielu dodatkowych czynności.

## Ustawienia projektu

Konfigurację aplikacji specyficzną dla macOS wykonuje się w sekcji [macOS](/manuals/project-settings/#macos) pliku ustawień *game.project*.

## Ikona aplikacji

Ikona aplikacji używana przez grę na macOS musi mieć format `.icns`. Możesz łatwo utworzyć plik `.icns` z zestawu plików `.png` zebranych w `.iconset`. Postępuj zgodnie z [oficjalnymi instrukcjami tworzenia pliku `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Krótkie podsumowanie kroków:

* Utwórz folder na ikony, np. `game.iconset`
* Skopiuj pliki ikon do utworzonego folderu:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Przekonwertuj folder `.iconset` do pliku `.icns` za pomocą narzędzia wiersza poleceń `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Publikowanie aplikacji

Możesz opublikować aplikację w Mac App Store, w zewnętrznym sklepie lub portalu, takim jak Steam albo itch.io, albo samodzielnie przez stronę internetową. Zanim opublikujesz aplikację, musisz przygotować ją do przesłania. Poniższe kroki są wymagane niezależnie od tego, w jaki sposób planujesz dystrybuować aplikację:

* 1) Upewnij się, że każdy może uruchomić grę, dodając uprawnienia do wykonania pliku (domyślnie tylko właściciel pliku ma takie uprawnienia):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* 2) Utwórz plik entitlements określający wymagane uprawnienia gry. W przypadku większości gier wystarczą następujące uprawnienia:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Określa, czy aplikacja może tworzyć pamięć zapisywalną i wykonywalną przy użyciu flagi MAP_JIT
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Określa, czy aplikacja może tworzyć pamięć zapisywalną i wykonywalną bez ograniczeń narzucanych przez flagę MAP_JIT
  * `com.apple.security.cs.allow-dyld-environment-variables` - Określa, czy na aplikację mogą wpływać zmienne środowiskowe dynamicznego linkera, których można użyć do wstrzyknięcia kodu do procesu aplikacji

Niektóre aplikacje mogą też wymagać dodatkowych uprawnień. Rozszerzenie Steamworks wymaga dodatkowego uprawnienia:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - Określa, czy aplikacja może wczytywać dowolne wtyczki lub frameworki bez wymogu podpisywania kodu

Wszystkie uprawnienia, które można przyznać aplikacji, są wymienione w oficjalnej [dokumentacji Apple dla deweloperów](https://developer.apple.com/documentation/bundleresources/entitlements).

* 3) Podpisz grę za pomocą `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Publikowanie poza Mac App Store

Apple wymaga, aby całe oprogramowanie dystrybuowane poza Mac App Store było notaryzowane przez Apple, żeby mogło domyślnie uruchamiać się w macOS Catalina. Zobacz [oficjalną dokumentację](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow), aby dowiedzieć się, jak dodać notaryzację do zautomatyzowanego środowiska budowania poza Xcode. Krótkie podsumowanie kroków:

* 1) Wykonaj powyższe kroki dodawania uprawnień i podpisywania aplikacji.

* 2) Spakuj grę do pliku zip i prześlij ją do notaryzacji za pomocą `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

* 3) Sprawdź status przesłania, używając zwróconego identyfikatora UUID żądania z wywołania `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

* 4) Poczekaj, aż status zmieni się na `success`, a następnie dołącz bilet notaryzacji do gry:

```
$ xcrun stapler staple "Game.app"
```

* 5) Twoja gra jest już gotowa do dystrybucji.

## Publikowanie w Mac App Store

Proces publikowania w Mac App Store jest dobrze opisany w [dokumentacji Apple Developer](https://developer.apple.com/macos/submit/). Przed przesłaniem upewnij się, że dodano uprawnienia i podpisano aplikację zgodnie z powyższym opisem.

Uwaga: Gra nie musi być notaryzowana, gdy publikujesz ją w Mac App Store.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
