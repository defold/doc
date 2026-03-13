---
title: Zawartość Live update w silniku Defold
brief: Funkcja Live update pozwala środowisku uruchomieniowemu pobierać i przechowywać zasoby, które zostały celowo pominięte w bundlu podczas budowania aplikacji. Ta instrukcja wyjaśnia, jak to działa.
---

# Live update

Podczas bundlowania gry Defold pakuje wszystkie zasoby do końcowej paczki specyficznej dla danej platformy. W większości przypadków jest to korzystne, ponieważ działający silnik ma natychmiastowy dostęp do wszystkich zasobów i może szybko ładować je z nośnika. Czasem jednak warto odłożyć ładowanie części zasobów na później. Na przykład wtedy, gdy:

- gra składa się z odcinków i chcesz dołączyć tylko pierwszy, aby gracz mógł go wypróbować przed odblokowaniem reszty
- gra jest przeznaczona na HTML5, gdzie przeglądarka musi pobrać całą paczkę aplikacji przed uruchomieniem, więc chcesz dostarczyć mały pakiet startowy i doładować resztę zawartości później
- gra zawiera bardzo duże zasoby, takie jak obrazy czy filmy, których pobieranie chcesz odłożyć do momentu, gdy faktycznie będą potrzebne

Funkcja Live update rozszerza koncepcję Collection proxy (pełnomocnika kolekcji) o mechanizm, który pozwala środowisku uruchomieniowemu pobierać i przechowywać w bundlu aplikacji zasoby celowo pominięte podczas budowania.

Pozwala to podzielić zawartość na wiele archiwów:

* _Archiwum bazowe_
* Wspólne pliki poziomów
* Pakiet poziomów 1
* Pakiet poziomów 2
* ...

## Przygotowanie zawartości do Live update

Załóżmy, że tworzymy grę z dużymi obrazami o wysokiej rozdzielczości. Gra przechowuje te obrazy w kolekcjach zawierających obiekt gry i sprite korzystający z obrazu:

![Mona Lisa collection](images/live-update/mona-lisa.png)

Aby silnik ładował taką kolekcję dynamicznie, wystarczy dodać komponent Collection proxy i wskazać w nim plik *`monalisa.collection`*. Gra może wtedy zdecydować, kiedy załadować zawartość tej kolekcji z nośnika do pamięci, wysyłając do Collection proxy wiadomość `load`. My jednak chcemy pójść krok dalej i samodzielnie sterować ładowaniem zasobów zawartych w kolekcji.

W tym celu zaznaczamy pole *Exclude* we właściwościach Collection proxy. Informuje to Defold, aby podczas tworzenia bundla aplikacji pominął całą zawartość z *`monalisa.collection`*.

::: important
Żadne zasoby, do których odwołuje się bazowa paczka gry, nie zostaną wykluczone.
:::

![Collection proxy excluded](images/live-update/proxy-excluded.png)

## Ustawienia Live update

Kiedy Defold tworzy bundle aplikacji, musi gdzieś zapisać wykluczone zasoby. Lokalizacją tych zasobów sterują ustawienia projektu dla Live update. Znajdziesz je pod <kbd>Project ▸ Live update Settings...</kbd>. Jeśli plik ustawień jeszcze nie istnieje, zostanie utworzony. W pliku *game.project* wybierasz, którego pliku ustawień Live update użyć podczas bundlowania. Dzięki temu możesz mieć różne ustawienia Live update dla różnych środowisk, na przykład produkcyjnego, QA albo deweloperskiego.

![Live update settings](images/live-update/05-liveupdate-settings-zip.png)

Obecnie Defold może przechowywać zasoby na dwa sposoby. Metodę wybierasz z listy *Mode* w oknie ustawień:

`Zip`
: Ta opcja każe Defold utworzyć archiwum Zip zawierające wszystkie wykluczone zasoby. Archiwum zostanie zapisane w lokalizacji wskazanej w ustawieniu *Export path*.

`Folder`
: Ta opcja każe Defold utworzyć katalog zawierający wszystkie wykluczone zasoby. Działa tak samo jak tryb Zip, ale zapisuje pliki w katalogu zamiast w archiwum. Przydaje się to wtedy, gdy chcesz dodatkowo przetwarzać pliki przed wysłaniem i samodzielnie spakować je później do archiwum.

`Amazon`
: Ta opcja każe Defold automatycznie wysłać wykluczone zasoby do bucketa S3 w Amazon Web Services (AWS). Podaj nazwę swojego profilu AWS w polu *Credential profile*, wybierz odpowiedni *Bucket* i wpisz *Prefix*. Więcej informacji o konfiguracji konta AWS znajdziesz w [instrukcji AWS](/manuals/live-update-aws).

## Bundlowanie z Live update

::: important
Budowanie i uruchamianie projektu z poziomu edytora (<kbd>Project ▸ Build</kbd>) nie obsługuje Live Update. Aby testować Live Update, musisz zbudować bundle.
:::

Aby zbudować bundle z Live update, wybierz <kbd>Project ▸ Bundle ▸ ...</kbd>, a następnie platformę, dla której chcesz utworzyć paczkę aplikacji. Otworzy się okno bundlowania:

![Bundle Live application](images/live-update/bundle-app.png)

Podczas bundlowania wszystkie wykluczone zasoby zostaną pominięte w bundlu aplikacji. Zaznaczając pole *Publish Live update content*, każesz Defold albo wysłać wykluczone zasoby do Amazon, albo utworzyć archiwum Zip, zależnie od konfiguracji ustawień Live update. Plik manifestu bundla również zostanie dołączony do wykluczonych zasobów.

Kliknij *Package* i wybierz lokalizację dla bundla aplikacji. Następnie możesz uruchomić aplikację i sprawdzić, czy wszystko działa zgodnie z oczekiwaniami.

## Archiwa `.zip`

Plik `.zip` dla Live update zawiera pliki wykluczone z bazowej paczki gry.

Obecny pipeline potrafi utworzyć tylko jeden plik `.zip`, ale w praktyce można go podzielić na kilka mniejszych archiwów `.zip`. Dzięki temu możesz przygotować mniejsze pobrania dla gry, na przykład pakiety poziomów albo sezonową zawartość. Każdy plik `.zip` zawiera również manifest opisujący metadane wszystkich zasobów znajdujących się w tym archiwum.

## Dzielenie archiwów `.zip`

Często warto podzielić wykluczoną zawartość na kilka mniejszych archiwów, aby precyzyjniej sterować użyciem zasobów. Typowym przykładem jest gra podzielona na kilka pakietów poziomów. Innym przykładem jest umieszczenie różnych sezonowych dekoracji interfejsu w osobnych archiwach i ładowanie tylko tego motywu, który jest aktualnie aktywny.

Graf zasobów jest zapisywany w pliku `build/default/game.graph.json`, generowanym automatycznie przy każdym bundlowaniu projektu. Plik ten zawiera listę wszystkich zasobów projektu oraz zależności każdego z nich. Przykładowy wpis:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Każdy wpis zawiera pole `path`, które reprezentuje unikalną ścieżkę zasobu w projekcie. Pole `hexDigest` to kryptograficzny odcisk zasobu i jednocześnie nazwa pliku używana w archiwum `.zip` dla Live update. Pole `children` zawiera listę zależności, od których dany zasób zależy. W powyższym przykładzie `/game/player.goc` zależy od komponentu sprite i komponentu script.

Możesz sparsować plik `game.graph.json` i użyć tych informacji do znalezienia grup wpisów w grafie zasobów, a następnie zapisać odpowiadające im zasoby w osobnych archiwach razem z oryginalnym plikiem manifestu. Manifest zostanie później przycięty w runtime tak, aby zawierał tylko pliki obecne w danym archiwum.

## Live Update na Androidzie

Możesz używać Play Asset Delivery do pobierania i montowania zawartości Live Update. Więcej informacji znajdziesz [w oficjalnej instrukcji](https://defold.com/extension-pad/).

## Weryfikacja zawartości

Jedną z ważniejszych cech systemu Live update jest możliwość używania wielu archiwów zawartości, potencjalnie pochodzących z wielu różnych wersji Defold.

Domyślne zachowanie `liveupdate.add_mount()` polega na dodaniu kontroli wersji silnika podczas dołączania mounta. Oznacza to, że zarówno bazowe archiwum gry, jak i archiwa Live update muszą zostać utworzone w tym samym czasie, tą samą wersją silnika i z użyciem opcji bundlowania. W przeciwnym razie klient unieważni wcześniej pobrane archiwa i wymusi ponowne pobranie zawartości.

To zachowanie można wyłączyć odpowiednią flagą opcji. Po wyłączeniu pełna odpowiedzialność za weryfikację zgodności zawartości spoczywa na programiście, który musi zagwarantować, że każde archiwum Live update będzie działało z uruchomionym silnikiem.

Zalecamy przechowywanie pewnych metadanych dla każdego mounta, aby _bezpośrednio po uruchomieniu_ zdecydować, czy dany mount lub archiwum należy usunąć. Jednym ze sposobów jest dodanie dodatkowego pliku do archiwum zip po zbudowaniu gry, na przykład `metadata.json` zawierającego potrzebne informacje. Następnie przy starcie gry można go odczytać przez `sys.load_resource("/metadata.json")`. _Pamiętaj, że dane niestandardowe każdego mounta muszą mieć unikalną nazwę. W przeciwnym razie silnik zwróci plik z mounta o najwyższym priorytecie._

Jeśli tego nie zrobisz, możesz doprowadzić do sytuacji, w której zawartość okaże się całkowicie niezgodna z silnikiem i wymusi zamknięcie aplikacji.

## Mounty

System Live update może używać jednocześnie wielu archiwów zawartości. Każde archiwum jest „montowane” do systemu zasobów silnika z własną nazwą i priorytetem.

Jeśli dwa archiwa zawierają ten sam plik `sprite.texturec`, silnik załaduje go z mounta o wyższym priorytecie.

Silnik nie utrzymuje referencji do zasobów znajdujących się w mouncie. Gdy zasób zostanie już załadowany do pamięci, archiwum może zostać odmontowane. Sam zasób pozostanie w pamięci do momentu jego zwolnienia.

Mounty są automatycznie dodawane ponownie po restarcie silnika.

::: sidenote
Zamontowanie archiwum nie kopiuje go ani nie przenosi. Silnik przechowuje jedynie ścieżkę do archiwum. Oznacza to, że programista może usunąć archiwum w dowolnym momencie, a mount zostanie usunięty przy następnym uruchomieniu.
:::

## Skryptowanie z Live Update

Aby faktycznie korzystać z zawartości Live update, musisz pobrać dane i zamontować je w swojej grze.
Więcej informacji znajdziesz w [instrukcji skryptowania Live update](/manuals/live-update-scripting).

## Uwagi deweloperskie

Debugowanie
: Gdy uruchamiasz zbundlowaną wersję gry, nie masz bezpośredniego dostępu do konsoli, co utrudnia debugowanie. Możesz jednak uruchomić aplikację z wiersza poleceń albo klikając bezpośrednio plik wykonywalny znajdujący się w bundlu:

  ![Running a bundle application](images/live-update/run-bundle.png)

  Gra uruchomi się wtedy z oknem powłoki, w którym będą widoczne wszystkie wywołania `print()`:

  ![Console output](images/live-update/run-bundle-console.png)

Wymuszenie ponownego pobrania zasobów
: Programista może pobrać zawartość do dowolnego pliku lub katalogu, ale często trafia ona do ścieżki aplikacji. Lokalizacja katalogu wsparcia aplikacji zależy od systemu operacyjnego. Możesz ją sprawdzić przez `print(sys.get_save_file("", ""))`.

  Plik `liveupdate.mounts` znajduje się w pamięci lokalnej, a jego ścieżka jest wypisywana do konsoli przy starcie jako `"INFO:LIVEUPDATE: Live update folder located at: ..."`

  ![Local storage](images/live-update/local-storage.png)
