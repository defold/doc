---
title: Podręcznik bezpieczeństwa aplikacji
brief: Ten podręcznik omawia kilka obszarów związanych z bezpiecznymi praktykami tworzenia oprogramowania.
---

# Bezpieczeństwo aplikacji

Bezpieczeństwo aplikacji to szeroki temat, obejmujący zarówno bezpieczne praktyki tworzenia oprogramowania, jak i zabezpieczanie zawartości gry po jej wydaniu. Ten podręcznik omawia kilka obszarów i umieszcza je w kontekście bezpieczeństwa aplikacji podczas korzystania z silnika Defold, narzędzi i usług:

* Ochrona własności intelektualnej
* Rozwiązania przeciwdziałające oszustwom
* Bezpieczna komunikacja sieciowa
* Korzystanie z oprogramowania firm trzecich
* Korzystanie z chmurowych serwerów budowania
* Zawartość do pobrania


## Ochrona własności intelektualnej przed kradzieżą
Jedną z głównych obaw wielu twórców jest to, jak chronić swoją twórczość przed kradzieżą. Z prawnego punktu widzenia prawa autorskie, patenty i znaki towarowe mogą służyć do ochrony różnych aspektów własności intelektualnej gier wideo. Prawa autorskie dają właścicielowi wyłączne prawo do rozpowszechniania utworu, patenty chronią wynalazki, a znaki towarowe chronią nazwy, symbole i logotypy.

Można też chcieć zastosować techniczne środki ostrożności, aby chronić twórczą zawartość gry. Trzeba jednak pamiętać, że gdy gra trafi już w ręce gracza, da się znaleźć sposoby na wyciągnięcie zasobów. Można to osiągnąć przez inżynierię wsteczną aplikacji i plików gry, ale też przy użyciu narzędzi do wyciągania tekstur i modeli w momencie, gdy są wysyłane do GPU albo gdy inne zasoby są ładowane do pamięci.

Z tego powodu przyjmujemy, że jeśli użytkownicy są zdeterminowani, by wyciągnąć zasoby gry, ostatecznie będą w stanie to zrobić.

Twórcy mogą dodać własne zabezpieczenia, aby utrudnić wyciągnięcie zasobów, __ale nie uczynić tego niemożliwym__. Zwykle obejmuje to różne metody szyfrowania i obfuskacji, które mają chronić i ukrywać zasoby gry.

### Obfuskacja kodu źródłowego
Obfuskacja kodu źródłowego to zautomatyzowany proces, w którym kod źródłowy jest celowo przekształcany tak, aby był trudny do zrozumienia dla człowieka, bez wpływu na wynik działania programu. Celem jest zwykle ochrona przed kradzieżą, ale też utrudnienie oszukiwania.

W Defold obfuskację kodu źródłowego można zastosować albo jako krok wykonywany przed budowaniem, albo jako zintegrowaną część procesu budowania. W przypadku obfuskacji wykonywanej przed budowaniem kod źródłowy jest przetwarzany przez narzędzie do obfuskacji, zanim rozpocznie się sam proces budowania.

Z kolei obfuskacja w czasie budowania jest zintegrowana z procesem budowania za pomocą wtyczki budowania Lua (Lua builder plugin). Taka wtyczka pobiera surowy kod źródłowy i zwraca jego obfuskowaną wersję. Przykład obfuskacji w czasie budowania pokazano w [rozszerzeniu Prometheus](https://github.com/defold/extension-prometheus), opartym na obfuskatorze Lua Prometheus dostępnym na GitHubie. Poniżej znajduje się przykład użycia Prometheus do agresywnej obfuskacji fragmentu kodu (zwróć uwagę, że tak silna obfuskacja wpłynie na wydajność kodu Lua w czasie działania):

Przykład:

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Wynik obfuskacji:

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Szyfrowanie zasobów
Podczas budowania w Defold zasoby gry są przetwarzane i zamieniane na formaty odpowiednie do użycia przez silnik w czasie działania. Tekstury są kompilowane do formatu Basis Universal, kolekcje, obiekty gry i komponenty są konwertowane z czytelnej dla człowieka postaci tekstowej do binarnych odpowiedników, a kod źródłowy Lua jest przetwarzany i kompilowany do bajtkodu. Inne zasoby, takie jak pliki dźwiękowe, są używane bez zmian.

Po zakończeniu tego procesu zasoby są dodawane do archiwum gry, jeden po drugim. Archiwum gry to duży plik binarny, a położenie każdego zasobu w archiwum jest zapisywane w pliku indeksu archiwum. Format opisano [tutaj](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md).

Zanim pliki źródłowe Lua zostaną dodane do archiwum, mogą też zostać opcjonalnie zaszyfrowane. Domyślne szyfrowanie dostępne w Defold to prosty szyfr blokowy używany po to, by ciągi znaków w kodzie nie były od razu widoczne, jeśli archiwum gry zostanie otwarte w narzędziu do podglądu plików binarnych. Nie należy go uznawać za kryptograficznie bezpieczne rozwiązanie, ponieważ kod źródłowy Defold jest dostępny na GitHubie, a klucz szyfru jest widoczny w kodzie źródłowym.

Można dodać własne szyfrowanie do plików źródłowych Lua, implementując wtyczkę szyfrowania zasobów (resource encryption plugin). Taka wtyczka składa się z części działającej w czasie budowania, która szyfruje zasoby w ramach procesu budowania, oraz części działającej w czasie działania, która odszyfrowuje zasoby podczas odczytu z archiwum gry. Podstawowa wtyczka szyfrowania zasobów, którą można wykorzystać jako punkt wyjścia do własnego szyfrowania, jest [dostępna na GitHubie](https://github.com/defold/extension-resource-encryption).


### Kodowanie wartości konfiguracji projektu
Plik *game.project* zostanie dołączony bez zmian do pakietu aplikacji. Czasami możesz chcieć przechowywać publiczne klucze API lub podobne wartości, które są wrażliwe, choć niekoniecznie poufne. Aby zwiększyć bezpieczeństwo takich wartości, można umieścić je w binarnym pliku aplikacji zamiast w *game.project*, a mimo to nadal mieć do nich dostęp za pomocą funkcji API Defold, takich jak `sys.get_config_string()` i podobnych. Można to zrobić, dodając natywne rozszerzenie w *game.project* i używając makra `DM_DECLARE_CONFIGFILE_EXTENSION`, aby dostarczyć własny sposób pobierania wartości konfiguracji przez funkcje API Defold. Przykładowy projekt, który może służyć jako punkt wyjścia, jest [dostępny na GitHubie](https://github.com/defold/example-configfile-extension/tree/master).


## Ochrona gry przed oszustami
Oszukiwanie w grach wideo istnieje tak długo, jak sama branża gier. Kody cheatowe były kiedyś drukowane w popularnych magazynach o grach wideo, a do wczesnych komputerów domowych sprzedawano specjalne kartridże z cheatami. Wraz z rozwojem branży i samych gier ewoluowali także oszuści i ich metody. Do najpopularniejszych mechanizmów oszukiwania w grach należą:

* przepakowywanie zawartości gry w celu wstrzyknięcia własnej logiki
* speed hacki, które przyspieszają lub spowalniają grę względem normalnego tempa
* automatyzacja i analiza obrazu do automatycznego celowania oraz botów
* wstrzykiwanie kodu i manipulowanie pamięcią w celu modyfikowania wyników, żyć, amunicji itd.

Ochrona przed oszustami jest trudna i niemal niemożliwa. Nawet granie w chmurze, w którym gry są uruchamiane na zdalnych serwerach i strumieniowane bezpośrednio na urządzenie użytkownika, nie jest całkowicie wolne od oszustów.

Defold nie oferuje w silniku ani w narzędziach żadnych rozwiązań anti-cheat i zamiast tego pozostawia taką pracę firmom specjalizującym się w dostarczaniu rozwiązań anti-cheat dla gier.


## Bezpieczna komunikacja sieciowa
Defold obsługuje bezpieczne połączenia dla komunikacji przez sockety i HTTP. Zaleca się używanie takich połączeń do każdej komunikacji z serwerem, aby uwierzytelnić serwer oraz chronić prywatność i integralność danych przesyłanych między klientem a serwerem w obu kierunkach. Defold korzysta z popularnej i szeroko stosowanej otwartoźródłowej implementacji protokołów TLS i SSL, [Mbed TLS](https://github.com/Mbed-TLS/mbedtls). Mbed TLS jest rozwijany przez ARM i ich partnerów technologicznych.

### Weryfikacja certyfikatu SSL
Aby zapobiec atakom man-in-the-middle na komunikację sieciową, można zweryfikować łańcuch certyfikatów podczas uzgadniania połączenia SSL z serwerem. Można to zrobić, przekazując klientowi sieciowemu w Defold listę kluczy publicznych. Więcej informacji o zabezpieczaniu komunikacji sieciowej znajdziesz w sekcji o weryfikacji SSL w [instrukcji sieciowej](https://defold.com/manuals/networking/#secure-connections).


## Bezpieczne korzystanie z oprogramowania firm trzecich
Choć do stworzenia gry nie trzeba używać bibliotek firm trzecich ani natywnych rozszerzeń, bardzo wielu twórców korzysta z zasobów z oficjalnego [Asset Portal](https://defold.com/assets/), aby przyspieszyć pracę. Asset Portal zawiera szeroki wybór zasobów: od integracji z zewnętrznymi SDK po menedżery ekranów, biblioteki UI, kamery i wiele więcej.

Żaden zasób z Asset Portal nie został zweryfikowany przez Defold Foundation. Fundacja nie ponosi odpowiedzialności za szkody w systemie komputerowym lub innym urządzeniu ani za utratę danych wynikające z użycia zasobów pozyskanych za pośrednictwem Asset Portal. Szczegóły znajdziesz w naszych [Warunkach i zasadach](https://defold.com/terms-and-conditions/#3-no-warranties).

Zalecamy, aby przed użyciem sprawdzić każdy zasób, a gdy uznasz go za odpowiedni do projektu, utworzyć jego fork lub kopię, aby mieć pewność, że nie zmieni się bez Twojej wiedzy.


## Bezpieczne korzystanie z chmurowych serwerów budowania
Chmurowe serwery budowania Defold (czyli serwery Extender) zostały stworzone po to, by pomóc twórcom dodawać nową funkcjonalność do silnika Defold bez konieczności przebudowy samego silnika. Gdy projekt Defold zawierający kod natywny jest budowany po raz pierwszy, kod natywny i wszelkie powiązane zasoby są wysyłane do chmurowych serwerów budowania, gdzie tworzona jest niestandardowa wersja silnika Defold, a następnie odsyłana do twórcy. Ten sam proces stosuje się, gdy projekt jest budowany z użyciem własnego manifestu aplikacji, aby usunąć niewykorzystywane komponenty z silnika.

Chmurowe serwery budowania są hostowane w AWS i tworzone zgodnie z najlepszymi praktykami bezpieczeństwa. Defold Foundation nie gwarantuje jednak, że spełnią Twoje wymagania, będą wolne od wad, wolne od wirusów, bezpieczne, bezbłędne ani że korzystanie z nich będzie nieprzerwane lub bezpieczne. Szczegóły znajdziesz w naszych [Warunkach i zasadach](https://defold.com/terms-and-conditions/#3-no-warranties).

Jeśli martwisz się o bezpieczeństwo i dostępność serwerów budowania, zalecamy skonfigurowanie własnych prywatnych serwerów budowania. Instrukcje dotyczące konfiguracji własnego serwera znajdziesz w [głównym pliku README](https://github.com/defold/extender) repozytorium extender na GitHubie.


## Zabezpieczanie zawartości do pobrania
System Defold Live Update pozwala twórcom wykluczyć zawartość z głównego pakietu gry, aby można ją było pobrać i użyć później. Typowym zastosowaniem jest pobieranie dodatkowych poziomów, map lub światów w miarę postępów gracza.

Gdy wykluczona zawartość zostanie pobrana i przygotowana do użycia w grze, silnik zweryfikuje ją kryptograficznie przed użyciem, aby upewnić się, że nie została zmodyfikowana. Weryfikacja składa się z kilku kontroli:

* Czy format binarny jest poprawny?
* Czy pobrana zawartość jest obsługiwana przez aktualnie uruchomioną wersję silnika?
* Czy pobrana zawartość jest podpisana właściwą parą kluczy publicznego i prywatnego?
* Czy pobrana zawartość jest kompletna i nie brakuje w niej żadnych plików?

Więcej informacji o tym procesie znajdziesz w [instrukcji Live Update](https://defold.com/manuals/live-update/#manifest-verification).
