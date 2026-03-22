## Manifest prywatności Apple

Manifest prywatności to plik listy właściwości, w którym zapisuje się typy danych zbieranych przez aplikację lub zewnętrzne SDK oraz używane przez nie interfejsy API wymagające podania uzasadnienia. Dla każdego typu danych zbieranego przez aplikację lub zewnętrzne SDK oraz dla każdej kategorii używanego interfejsu API wymagającego uzasadnienia aplikacja lub zewnętrzne SDK musi zapisać powody w dołączonym pliku manifestu prywatności.

Defold udostępnia domyślny manifest prywatności przez pole <kbd>Privacy Manifest</kbd> w pliku `game.project`. Podczas tworzenia pakietu aplikacji manifest prywatności jest scalany z manifestami prywatności w zależnościach projektu i dołączany do pakietu aplikacji.

Więcej informacji o manifestach prywatności znajdziesz w [oficjalnej dokumentacji Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).
