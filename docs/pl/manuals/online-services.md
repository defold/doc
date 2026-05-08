---
title: Usługi online
brief: Ta instrukcja wyjaśnia, jak łączyć się z różnymi usługami gier i backendu.
---
# Usługi gier

Korzystanie z żądań HTTP i połączeń socketowych pozwala łączyć się z tysiącami różnych usług w internecie i współpracować z nimi, ale w większości przypadków to coś więcej niż samo wysłanie żądania HTTP. Zwykle trzeba użyć jakiejś formy uwierzytelniania, dane żądania mogą wymagać określonego formatu, a odpowiedź może wymagać sparsowania, zanim da się z niej skorzystać. Oczywiście możesz zrobić to ręcznie, ale istnieją też rozszerzenia i biblioteki, które przejmują ten rodzaj pracy za ciebie. Poniżej znajdziesz listę kilku rozszerzeń, których można użyć, aby łatwiej integrować się z konkretnymi usługami backendowymi:

## Ogólnego przeznaczenia
* [Colyseus](https://defold.com/assets/colyseus/) - klient do gry wieloosobowej
* [Nakama](https://defold.com/assets/nakama/) - dodaj do gry uwierzytelnianie, dobieranie graczy, analitykę, zapis w chmurze, tryb wieloosobowy, czat i inne funkcje
* [Photon Realtime](https://defold.com/assets/photon-realtime/) - Photon Realtime oferuje skalowalne rozwiązania dla podstawowych funkcji, takich jak uwierzytelnianie, dobieranie graczy oraz szybka i niezawodna komunikacja.
* [PlayFab](https://defold.com/assets/playfabsdk/) - dodaj do gry uwierzytelnianie, dobieranie graczy, analitykę, zapis w chmurze i inne funkcje
* [AWS SDK](https://github.com/britzl/aws-sdk-lua) - korzystaj z Amazon Web Services bezpośrednio z poziomu gry

## Uwierzytelnianie, rankingi, osiągnięcia
* [Google Play Game Services](https://defold.com/assets/googleplaygameservices/) - użyj Google Play Game Services do uwierzytelniania i korzystania z zapisu w chmurze w grze
* [Steamworks](https://defold.com/assets/steamworks/) - dodaj do gry obsługę Steam
* [Apple GameKit Game Center](https://defold.com/assets/gamekit/)

## Analityka
* [Firebase Analytics](https://defold.com/assets/googleanalyticsforfirebase/) - dodaj Firebase Analytics do gry
* [Game Analytics](https://gameanalytics.com/docs/item/defold-sdk) - dodaj GameAnalytics do gry
* [Google Analytics](https://defold.com/assets/gameanalytics/) - dodaj Google Analytics do gry

Sprawdź też [Asset Portal](https://www.defold.com/assets/), aby znaleźć jeszcze więcej rozszerzeń!
