---
title: Adresowanie w Defold
brief: Niniejsza instrukcja wyjaśnia, jak Defold rozwiązał problem adresowania.
---

# Adresowanie

Kod sterujący działającą grą musi mieć możliwość dotarcia do każdego obiektu gry i komponentu, aby przesuwać, skalować, animować, usuwać i manipulować tym, co gracz widzi i słyszy. Mechanizm adresowania w Defold sprawia, że jest to możliwe.

## Identyfikatory

Defold używa adresów (albo URL-i, ale na razie pomińmy ten szczegół), aby odwoływać się do obiektów gry i komponentów. Adresy te składają się z identyfikatorów. Poniżej znajdują się przykłady użycia adresów w Defold. W tej instrukcji przyjrzymy się dokładnie, jak działają:

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Zacznijmy od bardzo prostego przykładu. Załóżmy, że masz obiekt gry z jednym komponentem typu sprite. Masz też komponent skryptu, który steruje tym obiektem gry. Taki układ w edytorze wygląda mniej więcej tak:

![bean in editor](images/addressing/bean_editor.png)

Chcesz wyłączyć sprite na początku gry, aby móc pokazać go później. Wystarczy umieścić poniższy kod w pliku "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Nie przejmuj się na razie znakiem '#'. Wrócimy do niego za chwilę.

To działa zgodnie z oczekiwaniami. Gdy gra się uruchamia, komponent skryptowy *adresuje* komponent sprite po identyfikatorze "body" i używa tego adresu, aby wysłać do niego *wiadomość* "disable". Efektem tej specjalnej wiadomości silnika jest ukrycie grafiki sprite. Schematycznie wygląda to tak:

![bean](images/addressing/bean.png)

Identyfikatory w tym układzie są dowolne. Tutaj obiekt gry ma identyfikator "bean", jego komponent sprite ma identyfikator "body", a skrypt sterujący postacią nosi nazwę "controller".

::: sidenote
Jeśli nie wybierzesz własnego identyfikatora, zrobi to za Ciebie edytor. Gdy tworzysz nowy obiekt gry lub komponent, automatycznie ustawiane jest unikalne *Id*.

- Obiekty gry automatycznie dostają identyfikator "go" z kolejnym numerem ("go2", "go3" itd.).
- Komponenty dostają identyfikator odpowiadający typowi komponentu ("sprite", "sprite2" itd.).

Możesz pozostać przy tych automatycznie przypisanych nazwach, ale zachęcamy do nadawania identyfikatorom dobrych, opisowych nazw.
:::

Teraz dodajmy kolejny komponent sprite i wyposażmy fasolkę w tarczę:

![bean](images/addressing/bean_shield_editor.png)

Nowy komponent musi mieć unikalny identyfikator w obrębie obiektu gry. Gdybyś nadał mu nazwę "body", kod byłby niejednoznaczny, bo nie byłoby jasne, do którego sprite'a wysłać wiadomość "disable". Dlatego wybieramy unikalny i opisowy identyfikator "shield". Dzięki temu możemy włączać i wyłączać sprite'y "body" i "shield" według potrzeb.

![bean](images/addressing/bean_shield.png)

::: sidenote
Jeśli spróbujesz użyć tego samego identyfikatora dwa razy, edytor zgłosi błąd, więc w praktyce nie stanowi to problemu:

![bean](images/addressing/name_collision.png)
:::

Przyjrzyjmy się teraz temu, co się stanie, gdy dodasz więcej obiektów. Załóżmy, że chcesz połączyć dwie fasolki w mały zespół. Jeden obiekt nazwij "bean", a drugi "buddy". Gdy "bean" przez chwilę pozostaje bezczynny, ma powiedzieć "buddy", żeby zaczął tańczyć. Robi się to przez wysłanie niestandardowej wiadomości "dance" ze skryptu "controller" obiektu "bean" do skryptu "controller" obiektu "buddy":

![bean](images/addressing/bean_buddy.png)

::: sidenote
Widać tu dwa komponenty skryptowe o nazwie "controller", po jednym w każdym obiekcie gry, i to jest całkowicie poprawne, ponieważ każdy obiekt gry tworzy nowy kontekst nazewniczy.
:::

Ponieważ adresat wiadomości znajduje się poza obiektem wysyłającym ("bean"), kod musi określić, który komponent "controller" ma ją otrzymać. Trzeba więc podać zarówno identyfikator obiektu gry, jak i identyfikator komponentu. Pełny adres komponentu to `"buddy#controller"` i składa się z dwóch części.

- Najpierw podajemy identyfikator obiektu gry ("buddy"),
- następnie wpisujemy znak oddzielający obiekt od komponentu ("#"),
- a na końcu podajemy identyfikator komponentu ("controller").

Wracając do poprzedniego przykładu z jednym obiektem gry, widać, że jeśli pominiemy część identyfikującą obiekt docelowy, kod może adresować komponenty w *bieżącym obiekcie gry*.

Na przykład `"#body"` oznacza adres komponentu "body" w bieżącym obiekcie gry. To bardzo przydatne, ponieważ ten kod zadziała w *dowolnym* obiekcie gry, o ile tylko taki komponent "body" istnieje.

## Kolekcje

Kolekcje pozwalają tworzyć grupy lub hierarchie obiektów gry i używać ich wielokrotnie w kontrolowany sposób. W edytorze nowego *pliku kolekcji* używa się jako szablonu, czyli "prototypu" albo "prefabu", gdy dodajesz zawartość do gry.

Załóżmy, że chcesz utworzyć dużą liczbę duetów bean/buddy. Dobrym sposobem jest przygotowanie nowego pliku kolekcji (nazwij go "team.collection"), zbudowanie w nim obiektów i zapisanie pliku. Następnie umieść instancję zawartości tego pliku w głównej kolekcji bootstrapowej i nadaj tej instancji identyfikator, na przykład "team_1":

![bean](images/addressing/team_editor.png)

Dzięki takiej strukturze obiekt "bean" nadal może odwoływać się do komponentu "controller" obiektu "buddy" za pomocą adresu `"buddy#controller"`.

![bean](images/addressing/collection_team.png)

Jeśli dodasz drugą instancję "team.collection" (nazwij ją "team_2"), kod uruchomiony wewnątrz komponentów skryptowych tej instancji będzie działał tak samo. Obiekt "bean" z instancji "team_2" nadal może adresować komponent "controller" obiektu "buddy" przez adres `"buddy#controller"`.

![bean](images/addressing/teams_editor.png)

## Adresowanie względne

Adres `"buddy#controller"` działa dla obiektów z obu kolekcji, ponieważ jest *względny*. Każda instancja kolekcji "team_1" i "team_2" tworzy własny kontekst nazewniczy, czyli przestrzeń nazw. Defold unika kolizji nazw, uwzględniając ten kontekst podczas adresowania:

![relative id](images/addressing/relative_same.png)

- W ramach kontekstu nazewniczego kolekcji "team_1" obiekty "bean" i "buddy" mają unikalne identyfikatory.
- Analogicznie, w kontekście kolekcji "team_2" identyfikatory "bean" i "buddy" również są unikalne.

Adresowanie względne działa dzięki temu, że podczas rozwiązywania adresu Defold automatycznie dopisuje bieżący kontekst nazewniczy. To bardzo wygodne i pozwala tworzyć grupy obiektów z kodem, który można wielokrotnie wykorzystywać w całej grze.

### Skróty

Defold udostępnia dwa przydatne skróty, których możesz użyć do wysyłania wiadomości bez podawania pełnego URL:

:[Skróty](../shared/url-shorthands.md)

## Ścieżki obiektów gry

Aby poprawnie zrozumieć mechanizm nazewnictwa, zobaczmy, co dzieje się po zbudowaniu i uruchomieniu projektu:

1. Edytor odczytuje kolekcję bootstrapową ("main.collection") i całą jej zawartość, czyli obiekty gry oraz inne kolekcje.
2. Dla każdego statycznego obiektu gry kompilator tworzy identyfikator. Identyfikatory te są budowane jako "ścieżki" zaczynające się od korzenia kolekcji bootstrapowej i schodzące przez hierarchię kolekcji do obiektu. Na każdym poziomie dodawany jest znak '/'.

W naszym przykładzie gra uruchomi się z następującymi czterema obiektami gry:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Identyfikatory są przechowywane jako wartości haszowane. Runtime przechowuje też stan haszowania dla każdego identyfikatora kolekcji, co służy do dalszego haszowania względnego ciągu znaków do identyfikatora bezwzględnego.
:::

W czasie działania grupowanie kolekcji nie istnieje. Nie da się ustalić, do której kolekcji należał dany obiekt przed kompilacją. Nie można też manipulować wszystkimi obiektami w kolekcji naraz. Jeśli potrzebujesz takich operacji, możesz łatwo śledzić je samodzielnie w kodzie. Identyfikator każdego obiektu jest statyczny i pozostaje niezmienny przez cały czas jego życia. Oznacza to, że możesz go bezpiecznie przechowywać i używać później.

## Adresowanie bezwzględne

Można też używać pełnych identyfikatorów opisanych powyżej. W większości przypadków preferowane jest adresowanie względne, ponieważ ułatwia ponowne wykorzystanie zawartości, ale bywają sytuacje, w których potrzebne jest adresowanie bezwzględne.

Na przykład wyobraź sobie menedżera AI, który śledzi stan każdego obiektu bean. Chcesz, aby beany raportowały mu swój status, a menedżer na tej podstawie podejmował decyzje taktyczne i wydawał im polecenia. W takim przypadku sensowne jest utworzenie jednego obiektu gry z komponentem skryptowym i umieszczenie go w głównej kolekcji bootstrapowej obok instancji zespołów.

![manager object](images/addressing/manager_editor.png)

Każdy bean odpowiada za wysyłanie wiadomości statusowych do menedżera: "contact", gdy zauważy wroga, albo "ouch!", gdy otrzyma obrażenia. Aby to zadziałało, skrypt beana używa adresowania bezwzględnego, by wysłać wiadomość do komponentu "controller" obiektu "manager".

Każdy adres zaczynający się od '/' jest rozwiązywany względem korzenia świata gry. Odpowiada to korzeniowi *kolekcji bootstrapowej*, która jest ładowana przy starcie gry.

Bezwzględny adres skryptu menedżera to `"/manager#controller"` i niezależnie od miejsca użycia zawsze wskaże właściwy komponent.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Haszowane identyfikatory

Silnik przechowuje wszystkie identyfikatory jako wartości haszowane. Wszystkie funkcje przyjmujące jako argument komponent lub obiekt gry akceptują string, hash albo obiekt URL. Powyżej pokazywaliśmy adresowanie z użyciem stringów.

Gdy pobierasz identyfikator obiektu, silnik Defold zawsze zwraca haszowaną ścieżkę bezwzględną:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Możesz użyć takiego identyfikatora zamiast stringa albo samodzielnie go utworzyć. Pamiętaj jednak, że haszowany identyfikator odpowiada ścieżce obiektu, czyli adresowi bezwzględnemu:

::: sidenote
Powodem, dla którego adresy względne muszą być podawane jako stringi, jest to, że silnik oblicza nowy identyfikator haszowany na podstawie stanu haszowania bieżącego kontekstu nazewniczego, czyli kolekcji, do której dodaje podany ciąg znaków.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- To nie zadziała! Adresy względne muszą być podawane jako stringi.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL-e

Żeby dopełnić obraz, spójrzmy na pełny format adresu w Defold: URL.

URL to obiekt, zwykle zapisywany jako specjalnie sformatowany string. Ogólny format URL wygląda tak:

`[socket:][path][#fragment]`

socket
: Identyfikuje świat gry, do którego należy cel. Jest to ważne podczas pracy z [pełnomocnikami kolekcji](/manuals/collection-proxy) i służy do określenia _dynamicznie załadowanej kolekcji_.

path
: Ta część URL zawiera pełny identyfikator docelowego obiektu gry.

fragment
: Identyfikator komponentu w obrębie wskazanego obiektu gry.

Jak widzieliśmy wcześniej, w większości przypadków można pominąć część informacji. Zwykle nie trzeba podawać socketu, a często, ale nie zawsze, trzeba podać path. Gdy jednak musisz adresować coś w innym świecie gry, trzeba określić socket. Na przykład pełny string URL skryptu "controller" w obiekcie "manager" wygląda tak:

`"main:/manager#controller"`

a kontroler buddy'ego z "team_2" to:

`"main:/team_2/buddy#controller"`

Możemy wysyłać do nich wiadomości:

```lua
-- Wyślij "hello" do skryptu menedżera i beana z zespołu
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Konstruowanie obiektów URL

Obiekty URL można też konstruować programowo w kodzie Lua:

```lua
-- Utwórz obiekt URL z stringa:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (wewnętrzna wartość numeryczna)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Utwórz URL z parametrów:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Zbuduj z pustego obiektu URL:
local my_url = msg.url()
my_url.socket = "main" -- podaj poprawną nazwę
my_url.path = hash("/manager") -- podaj jako string lub hash
my_url.fragment = "controller" -- podaj jako string lub hash

-- Wyślij wiadomość do celu wskazanego przez URL
msg.post(my_url, "hello_manager!")
```
