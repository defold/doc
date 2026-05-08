---
title: Zawartość Live update w Defold
brief: Funkcja Live update pozwala środowisku uruchomieniowemu pobierać i przechowywać zasoby, które zostały celowo pominięte w paczce aplikacji podczas budowania. Ta instrukcja wyjaśnia, jak to działa.
---

# Live update

Podczas pakowania gry Defold umieszcza wszystkie zasoby gry w końcowej paczce właściwej dla danej platformy. W większości przypadków jest to korzystne, ponieważ działający silnik ma natychmiastowy dostęp do wszystkich zasobów i może szybko wczytywać je z pamięci masowej. Czasem jednak warto odłożyć wczytywanie części zasobów na później. Na przykład gdy:

- gra składa się z serii odcinków i chcesz dołączyć tylko pierwszy z nich, aby gracz mógł go wypróbować, zanim zdecyduje, czy chce przejść dalej,
- gra jest przeznaczona na HTML5. W przeglądarce wczytanie aplikacji z pamięci masowej oznacza, że cała paczka aplikacji musi zostać pobrana przed uruchomieniem. W takim przypadku możesz chcieć wysłać minimalną paczkę startową i szybko uruchomić aplikację, a resztę zasobów gry pobrać później,
- gra zawiera bardzo duże zasoby, takie jak obrazy czy filmy, których pobieranie chcesz odłożyć do chwili, gdy mają się pojawić w grze. Dzięki temu zachowasz mały rozmiar instalacji.

Funkcja Live update rozszerza koncepcję Collection proxy (pełnomocnika kolekcji) o mechanizm, który pozwala środowisku uruchomieniowemu pobierać i przechowywać w paczce aplikacji zasoby celowo pominięte podczas budowania.

Pozwala to podzielić zawartość na wiele archiwów:

* _Archiwum bazowe_
* Wspólne pliki poziomów
* Pakiet poziomu 1
* Pakiet poziomu 2
* ...

## Przygotowanie zawartości do Live update

Załóżmy, że tworzymy grę zawierającą duże obrazy w wysokiej rozdzielczości. Gra przechowuje te obrazy w kolekcjach z obiektem gry i sprite'em korzystającym z obrazu:

![Kolekcja Mona Lisa](images/live-update/mona-lisa.png)

Aby silnik wczytywał taką kolekcję dynamicznie, wystarczy dodać komponent Collection proxy i wskazać w nim *`monalisa.collection`*. Gra może wtedy zdecydować, kiedy wczytać zawartość kolekcji z pamięci masowej do pamięci operacyjnej, wysyłając do Collection proxy wiadomość `load`. My jednak chcemy pójść dalej i samodzielnie kontrolować wczytywanie zasobów zawartych w kolekcji.

Robi się to po prostu przez zaznaczenie pola wyboru *Exclude* we właściwościach Collection proxy, co informuje Defold, aby podczas tworzenia paczki aplikacji pominął całą zawartość *`monalisa.collection`*.

::: important
Żadne zasoby, do których odwołuje się bazowa paczka gry, nie zostaną wykluczone.
:::

![Wykluczony Collection proxy](images/live-update/proxy-excluded.png)

## Ustawienia Live update

Gdy Defold tworzy paczkę aplikacji, musi gdzieś zapisać wykluczone zasoby. Lokalizację tych zasobów określają ustawienia projektu Live update. Znajdziesz je pod <kbd>Project ▸ Live update Settings...</kbd>. Jeśli plik ustawień jeszcze nie istnieje, zostanie utworzony. W pliku *game.project* wybierasz, którego pliku ustawień Live update użyć podczas pakowania. Umożliwia to stosowanie różnych ustawień Live update dla różnych środowisk, na przykład produkcyjnego, QA lub deweloperskiego.

![Ustawienia Live update](images/live-update/05-liveupdate-settings-zip.png)

Obecnie Defold może przechowywać zasoby na dwa sposoby. Metodę wybierasz w liście rozwijanej *Mode* w oknie ustawień:

`Zip`
: Ta opcja każe Defold utworzyć archiwum Zip zawierające wszystkie wykluczone zasoby. Archiwum zostanie zapisane w lokalizacji wskazanej w ustawieniu *Export path*.

`Folder`
: Ta opcja każe Defold utworzyć folder zawierający wszystkie wykluczone zasoby. Działa dokładnie tak samo jak Zip, ale zamiast archiwum używa katalogu. Może to być przydatne, gdy trzeba przetworzyć pliki przed wysłaniem i samodzielnie spakować je później do archiwum.

`Amazon`
: Ta opcja każe Defold automatycznie wysłać wykluczone zasoby do bucketa S3 w Amazon Web Services (AWS). Wpisz nazwę profilu AWS w polu *Credential profile*, wybierz odpowiedni *Bucket* i podaj *Prefix*. Więcej informacji o konfiguracji konta AWS znajdziesz w [instrukcji AWS](/manuals/live-update-aws).

## Pakowanie z Live update

::: important
Budowanie i uruchamianie projektu z poziomu edytora (<kbd>Project ▸ Build</kbd>) nie obsługuje Live Update. Aby przetestować Live Update, musisz spakować projekt.
:::

Aby spakować projekt z Live update, wybierz <kbd>Project ▸ Bundle ▸ ...</kbd>, a następnie platformę, dla której chcesz utworzyć paczkę aplikacji. Otworzy się okno pakowania:

![Pakowanie aplikacji Live](images/live-update/bundle-app.png)

Podczas pakowania wszystkie wykluczone zasoby zostaną pominięte w paczce aplikacji. Zaznaczając pole *Publish Live update content*, informujesz Defold, aby albo wysłał wykluczone zasoby do Amazon, albo utworzył archiwum Zip, zależnie od tego, jak skonfigurowano ustawienia Live update (zobacz wyżej). Plik manifestu dla paczki również zostanie dołączony do wykluczonych zasobów.

Kliknij *Package* i wybierz lokalizację dla paczki aplikacji. Teraz możesz uruchomić aplikację i sprawdzić, czy wszystko działa zgodnie z oczekiwaniami.

## Archiwa .zip

Plik .zip Live update zawiera pliki, które zostały wykluczone z bazowej paczki gry.

Obecny pipeline obsługuje tworzenie tylko jednego pliku .zip, ale w praktyce można podzielić ten plik na mniejsze pliki .zip. Umożliwia to mniejsze pobieranie dla gry: pakiety poziomów, zawartość sezonowa itp. Każdy plik .zip zawiera również manifest opisujący metadane każdego zasobu znajdującego się w tym pliku .zip.

## Dzielenie archiwów .zip

Często warto podzielić wykluczoną zawartość na kilka mniejszych archiwów, aby uzyskać dokładniejszą kontrolę nad użyciem zasobów. Jednym z przykładów jest podział gry opartej na poziomach na kilka pakietów poziomów. Innym jest umieszczenie różnych świątecznych dekoracji UI w osobnych archiwach i wczytywanie oraz montowanie tylko tego motywu, który jest aktualnie aktywny w kalendarzu.

Graf zasobów jest przechowywany w `build/default/game.graph.json` i jest generowany automatycznie przy każdym pakowaniu projektu. Wygenerowany plik zawiera listę wszystkich zasobów w projekcie oraz zależności każdego zasobu. Przykładowy wpis:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Każdy wpis ma pole `path`, które reprezentuje unikalną ścieżkę zasobu w projekcie. Pole `hexDigest` reprezentuje kryptograficzny odcisk zasobu i będzie jednocześnie nazwą pliku używaną w archiwum .zip Live update. Pole `children` zawiera listę innych zależności, od których zależy ten zasób. W powyższym przykładzie `/game/player.goc` zależy od komponentu sprite i komponentu script.

Możesz sparsować plik `game.graph.json` i użyć tych informacji do identyfikacji grup wpisów w grafie zasobów oraz zapisać odpowiadające im zasoby w osobnych archiwach razem z oryginalnym plikiem manifestu. Manifest zostanie później przycięty w runtime tak, aby zawierał tylko pliki znajdujące się w archiwum.

## Live Update na Androidzie

Możesz użyć Play Asset Delivery do pobierania i montowania zawartości Live Update. Więcej informacji znajdziesz [w oficjalnej instrukcji](https://defold.com/extension-pad/).

## Weryfikacja zawartości

Jedną z głównych cech systemu live update jest to, że możesz korzystać z wielu archiwów zawartości, potencjalnie pochodzących z wielu różnych wersji Defold.

Domyślne zachowanie `liveupdate.add_mount()` polega na dodaniu sprawdzenia wersji silnika podczas dołączania mounta. Oznacza to, że zarówno bazowe archiwum gry, jak i archiwa Live update muszą zostać utworzone jednocześnie, z tą samą wersją silnika i przy użyciu opcji bundle. W przeciwnym razie klient unieważni wcześniej pobrane archiwa i wymusi ponowne pobranie zawartości.

To zachowanie można wyłączyć odpowiednią flagą opcji. Po wyłączeniu pełna odpowiedzialność za weryfikację zawartości spoczywa na deweloperze, który musi zagwarantować, że każde archiwum Live update będzie działało z uruchomionym silnikiem.

Zalecamy przechowywanie metadanych dla każdego mounta, aby _bezpośrednio po uruchomieniu_ deweloper mógł zdecydować, czy dany mount lub archiwum należy usunąć. Jednym ze sposobów jest dodanie do archiwum zip dodatkowego pliku po spakowaniu gry, na przykład `metadata.json` z dowolnymi informacjami wymaganymi przez grę. Następnie przy starcie gry można je odczytać przez `sys.load_resource("/metadata.json")`. _Pamiętaj, że dla niestandardowych danych każdego mounta potrzebna jest unikalna nazwa, w przeciwnym razie mounty zwrócą plik o najwyższym priorytecie._

Jeśli tego nie zrobisz, możesz doprowadzić do sytuacji, w której zawartość w ogóle nie będzie zgodna z silnikiem, co zmusi go do zamknięcia się.

## Mounts

System Live update może jednocześnie używać wielu archiwów zawartości.
Każde archiwum jest „montowane” w systemie zasobów silnika z nazwą i priorytetem.

Jeśli dwa archiwa mają ten sam plik `sprite.texturec`, silnik wczyta plik z mounta o najwyższym priorytecie.

Silnik nie przechowuje referencji do żadnego zasobu znajdującego się w mouncie. Gdy zasób zostanie wczytany do pamięci, archiwum może zostać odmontowane. Zasób pozostanie w pamięci do momentu, gdy zostanie zwolniony.

Mounty są automatycznie dodawane ponownie po restarcie silnika.

::: sidenote
Montowanie archiwum nie kopiuje go ani nie przenosi. Silnik przechowuje tylko ścieżkę do archiwum. Dzięki temu deweloper może usunąć archiwum w dowolnej chwili, a mount zostanie usunięty przy następnym uruchomieniu.
:::

## Skryptowanie z Live Update

Aby faktycznie korzystać z zawartości Live update, musisz pobrać dane i zamontować je w swojej grze.
Więcej informacji znajdziesz [w instrukcji skryptowania z Live update](/manuals/live-update-scripting).

## Uwagi deweloperskie

Debugowanie
: Gdy uruchamiasz zbundlowaną wersję gry, nie masz bezpośredniego dostępu do konsoli. To utrudnia debugowanie. Możesz jednak uruchomić aplikację z wiersza poleceń albo przez bezpośrednie dwukrotne kliknięcie pliku wykonywalnego w bundle:

  ![Uruchamianie aplikacji z bundle](images/live-update/run-bundle.png)

  Gra uruchomi się wtedy z oknem powłoki, w którym będą wyświetlane wszystkie wywołania `print()`:

  ![Wyjście konsoli](images/live-update/run-bundle-console.png)

Wymuszenie ponownego pobrania zasobów
: Deweloper może pobrać zawartość do dowolnego pliku lub folderu, ale często znajdują się one w ścieżce aplikacji. Lokalizacja folderu wsparcia aplikacji zależy od systemu operacyjnego. Możesz ją sprawdzić przez `print(sys.get_save_file("", ""))`.

  Plik liveupdate.mounts znajduje się w "local storage", a jego ścieżka jest wypisywana na konsolę przy uruchomieniu jako "INFO:LIVEUPDATE: Live update folder located at: ..."

  ![Local storage](images/live-update/local-storage.png)
