---
title: Budowanie prostego samochodu w Defold.
brief: Jeśli dopiero zaczynasz pracę z Defold, ten przewodnik pomoże Ci oswoić się z edytorem. Wyjaśnia też podstawowe idee i najczęściej używane elementy składowe w Defold: obiekty gry, kolekcje, skrypty i sprite'y.
---

# Budowanie samochodu

Jeśli dopiero zaczynasz pracę z Defold, ten przewodnik pomoże Ci oswoić się z edytorem. Wyjaśnia też podstawowe idee i najczęściej używane elementy składowe w Defold: obiekty gry (ang. game objects), kolekcje (ang. collections), skrypty (ang. scripts) i sprite'y (ang. sprites).

Zaczniemy od pustego projektu i krok po kroku zbudujemy bardzo małą, grywalną aplikację. Na końcu powinieneś już mniej więcej czuć, jak działa Defold, i będziesz gotowy, by przejść do bardziej rozbudowanego samouczka albo od razu zanurzyć się w instrukcjach.

::: sidenote
W całym samouczku szczegółowe opisy pojęć i sposobu wykonywania niektórych czynności są oznaczone tak jak ten akapit. Jeśli uznasz, że te sekcje wchodzą w zbyt duży detal, po prostu je pomiń.
:::

## Tworzenie nowego projektu

![New Project](images/new_empty.png)

1. Uruchom Defold.
2. Po lewej wybierz *New Project*.
3. Wybierz kartę *From Template*.
4. Wybierz *Empty Project*.
5. Wskaż lokalizację projektu na dysku lokalnym.
6. Kliknij *Create New Project*.

## Edytor

Zacznij od utworzenia [nowego projektu](/manuals/project-setup/) i otwarcia go w edytorze. Jeśli dwukrotnie klikniesz plik *main/main.collection*, plik otworzy się w edytorze:

![Editor overview](../manuals/images/editor/editor2_overview.png)

Edytor składa się z następujących głównych obszarów:

Assets pane
: To widok wszystkich plików w projekcie. Różne typy plików mają różne ikony. Kliknij plik dwukrotnie, aby otworzyć go w przypisanym edytorze dla tego typu pliku. Specjalny folder tylko do odczytu *builtins* jest wspólny dla wszystkich projektów i zawiera przydatne elementy, takie jak domyślny skrypt do renderowania, font, materiały do renderowania różnych komponentów i inne zasoby.

Main Editor View
: W zależności od typu aktualnie edytowanego pliku ten obszar pokaże odpowiedni edytor. Najczęściej używany jest widoczny tutaj edytor sceny. Każdy otwarty plik jest pokazany na osobnej karcie.

Changed Files
: Zawiera listę wszystkich zmian wprowadzonych w Twojej gałęzi od ostatniej synchronizacji. Jeśli więc widzisz coś w tym panelu, masz zmiany, których nie ma jeszcze na serwerze. Z tego widoku możesz otworzyć tekstowy diff i cofnąć zmiany.

Outline
: Zawartość aktualnie edytowanego pliku w widoku hierarchicznym. Z tego miejsca możesz dodawać, usuwać, modyfikować i zaznaczać obiekty oraz komponenty.

Properties
: Właściwości ustawione dla aktualnie zaznaczonego obiektu lub komponentu.

Console
: Podczas uruchamiania gry ten widok przechwytuje dane wyjściowe (logi, błędy, informacje debugowe itd.) pochodzące z silnika gry, a także wszelkie niestandardowe komunikaty debugowe `print()` i `pprint()` ze skryptów. Jeśli aplikacja albo gra nie chce się uruchomić, `Console` to pierwsze miejsce, które warto sprawdzić. Za `Console` znajduje się zestaw kart pokazujących informacje o błędach, a także edytor krzywych używany przy tworzeniu efektów cząsteczkowych.

## Uruchamianie gry

Szablon projektu "Empty" jest w rzeczywistości całkowicie pusty. Mimo to wybierz <kbd>Project ▸ Build</kbd>, aby zbudować projekt i uruchomić grę.

![Build](images/car/start_build_and_launch.png)

Czarny ekran może nie jest szczególnie ekscytujący, ale to działająca aplikacja gry w Defold i łatwo możemy ją przerobić na coś ciekawszego. Zróbmy to.

::: sidenote
Edytor Defold pracuje na plikach. Klikając dwukrotnie plik w *Assets pane*, otwierasz go w odpowiednim edytorze. Następnie możesz pracować z zawartością pliku.

Kiedy skończysz edytować plik, musisz go zapisać. Wybierz <kbd>File ▸ Save</kbd> w głównym menu. Edytor podpowiada to, dodając gwiazdkę `*` do nazwy pliku na karcie każdego pliku zawierającego niezapisane zmiany.

![File with unsaved changes](images/car/file_changed.png)
:::

## Składanie samochodu

Pierwszą rzeczą, którą zrobimy, będzie utworzenie nowej kolekcji. Kolekcja to kontener na obiekty gry, które zostały rozmieszczone i ustawione w odpowiednich pozycjach. Kolekcje najczęściej służą do budowania poziomów gry, ale są bardzo przydatne wszędzie tam, gdzie trzeba wielokrotnie używać grup i/lub hierarchii obiektów gry, które należą do siebie. Pomocne może być myślenie o kolekcjach jak o pewnym rodzaju prefabu.

Kliknij folder *main* w *Assets pane*, potem kliknij prawym przyciskiem myszy i wybierz <kbd>New ▸ Collection File</kbd>. Możesz też wybrać <kbd>File ▸ New ▸ Collection File</kbd> z głównego menu.

![New Collection file](images/car/start_new_collection.png)

Nazwij nowy plik kolekcji *car.collection* i otwórz go. Użyjemy tej nowej, pustej kolekcji, by zbudować mały samochód z kilku obiektów gry. Obiekt gry to kontener na komponenty (takie jak sprite'y, dźwięki, skrypty logiki itd.), których używasz do budowania gry. Każdy obiekt gry jest jednoznacznie identyfikowany w grze przez swoje id. Obiekty gry mogą komunikować się ze sobą przez przekazywanie wiadomości, ale o tym za chwilę.

Możliwe jest też tworzenie obiektu gry bezpośrednio w kolekcji, tak jak zrobiliśmy tutaj. W rezultacie powstaje obiekt jedyny w swoim rodzaju. Możesz go kopiować, ale każda kopia jest oddzielna, więc zmiana jednej nie wpływa na pozostałe. To oznacza, że jeśli utworzysz 10 kopii obiektu gry i później uznasz, że chcesz zmienić je wszystkie, będziesz musiał edytować wszystkie 10 instancji. Dlatego obiektów gry tworzonych bezpośrednio w miejscu należy używać dla obiektów, których nie planujesz powielać wiele razy.

Natomiast obiekt gry zapisany w _pliku_ działa jak prototyp (w innych silnikach znany też jako "prefab" albo "blueprint"). Gdy umieszczasz w kolekcji instancje obiektu gry zapisanego w pliku, każdy obiekt jest umieszczany _przez referencję_ i stanowi klon oparty na prototypie. Jeśli uznasz, że prototyp wymaga zmiany, każda umieszczona instancja obiektu gry oparta na tym prototypie zostanie natychmiast zaktualizowana.

![Add car gameobject](images/car/start_add_car_gameobject.png)

Zaznacz główny węzeł "Collection" w widoku *Outline*, kliknij prawym przyciskiem myszy i wybierz <kbd>Add Game Object</kbd>. W kolekcji pojawi się nowy obiekt gry o id "go". Zaznacz go i ustaw jego id na "car" w widoku *Properties*. Na razie "car" jest bardzo nieciekawy. Jest pusty, nie ma ani reprezentacji wizualnej, ani logiki. Aby dodać reprezentację wizualną, musimy dodać _komponent_ sprite'a.

Komponenty służą do rozszerzania obiektów gry o obecność (grafika, dźwięk) i funkcjonalność (fabryki tworzenia, kolizje, zachowania skryptowe). Komponent nie może istnieć samodzielnie, tylko musi znajdować się wewnątrz obiektu gry. Komponenty są zwykle definiowane bezpośrednio w tym samym pliku co obiekt gry. Jeśli jednak chcesz używać komponentu wielokrotnie, możesz zapisać go w osobnym pliku (tak samo jak obiekty gry) i dołączać go jako referencję w dowolnym pliku obiektu gry. Niektóre typy komponentów (na przykład skrypty Lua) muszą być umieszczone w oddzielnym pliku komponentu, a następnie dołączone przez referencję do obiektów.

Pamiętaj, że komponentami nie manipuluje się bezpośrednio. Możesz przesuwać, obracać, skalować i animować właściwości obiektów gry, które z kolei zawierają komponenty.

![Add car component](images/car/start_add_car_component.png)

Zaznacz obiekt gry "car", kliknij prawym przyciskiem myszy i wybierz <kbd>Add Component</kbd>, następnie wybierz *Sprite* i kliknij *Ok*. Jeśli zaznaczysz sprite w widoku *Outline*, zobaczysz, że trzeba ustawić mu kilka właściwości:

Image
: Tutaj potrzebne jest źródło obrazu dla sprite'a. Utwórz plik atlasu obrazów, zaznaczając "main" w widoku *Assets pane*, klikając prawym przyciskiem myszy i wybierając <kbd>New ▸ Atlas File</kbd>. Nazwij nowy plik atlasu *sprites.atlas* i kliknij go dwukrotnie, aby otworzyć go w edytorze atlasu. Zapisz poniższe dwa pliki obrazów na swoim komputerze i przeciągnij je do *main* w widoku *Assets pane*. Teraz możesz zaznaczyć główny węzeł Atlas w edytorze atlasu, kliknąć prawym przyciskiem myszy i wybrać <kbd>Add Images</kbd>. Dodaj obraz samochodu i opony do atlasu, a następnie zapisz plik. Teraz możesz wybrać *sprites.atlas* jako źródło obrazu dla komponentu sprite w obiekcie gry "car" w kolekcji "car".

Obrazy do naszej gry:

![Car image](images/car/start_car.png)
![Tire image](images/car/start_tire.png)

Dodaj te obrazy do atlasu:

![Sprites atlas](images/car/start_sprites_atlas.png)

![Sprite properties](images/car/start_sprite_properties.png)

Default Animation
: Ustaw tę właściwość na "car" (albo jakkolwiek nazwałeś obraz samochodu). Każdy sprite potrzebuje domyślnej animacji odtwarzanej wtedy, gdy jest wyświetlany w grze. Gdy dodajesz obrazy do atlasu, Defold wygodnie tworzy dla każdego pliku obrazu jednoklatkowe (statyczne) animacje.

## Dokończenie samochodu

Następnie dodaj w kolekcji jeszcze dwa obiekty gry. Nazwij je "left_wheel" i "right_wheel" i dodaj do każdego komponent sprite pokazujący obraz opony, który dodaliśmy do *sprites.atlas*. Następnie chwyć obiekty gry kół i przeciągnij je na "car", aby stały się dziećmi pod "car". Obiekty gry będące dziećmi innych obiektów gry są przyczepione do rodzica, kiedy rodzic się porusza. Można je też przesuwać indywidualnie, ale cały ruch odbywa się względem obiektu rodzica. Dla opon to idealne rozwiązanie, ponieważ chcemy, żeby trzymały się samochodu, a przy skręcaniu możemy po prostu lekko obracać je w lewo i w prawo. Kolekcja może zawierać dowolną liczbę obiektów gry, ustawionych obok siebie, zorganizowanych w złożone drzewa rodzic-dziecko albo w dowolnej mieszance tych układów.

Przesuń obiekty gry opon na miejsce, zaznaczając je, a następnie wybierając <kbd>Scene ▸ Move Tool</kbd>. Chwyć uchwyty strzałek albo zielony kwadrat pośrodku, aby przesunąć obiekt w odpowiednie miejsce. Ostatnią rzeczą, którą musimy zrobić, jest upewnienie się, że opony są rysowane pod samochodem. Osiągniemy to przez ustawienie składowej Z pozycji na -0.5. Każdy element wizualny w grze jest rysowany od tyłu do przodu, posortowany według wartości Z. Obiekt z wartością Z równą 0 zostanie narysowany nad obiektem z wartością Z równą -0.5. Ponieważ domyślna wartość Z obiektu gry samochodu wynosi 0, nowa wartość ustawiona dla obiektów opon umieści je pod obrazem samochodu.

![Car collection complete](images/car/start_car_collection_complete.png)

## Skrypt samochodu

Ostatni element układanki to _skrypt_ sterujący samochodem. Skrypt jest komponentem zawierającym program definiujący zachowanie obiektów gry. Dzięki skryptom możesz określić zasady działania gry oraz to, jak obiekty powinny reagować na różne interakcje (zarówno z graczem, jak i z innymi obiektami). Wszystkie skrypty są pisane w języku Lua. Aby pracować z Defold, Ty albo ktoś z Twojego zespołu musi nauczyć się programować w Lua.

Zaznacz "main" w *Assets pane*, kliknij prawym przyciskiem myszy i wybierz <kbd>New ▸ Script File</kbd>. Nazwij nowy plik *car.script*, a następnie dodaj go do obiektu gry "car", zaznaczając "car" w widoku *Outline*, klikając prawym przyciskiem myszy i wybierając <kbd>Add Component File</kbd>. Wybierz *car.script* i kliknij *OK*. Zapisz plik kolekcji.

Kliknij dwukrotnie *car.script*, aby go otworzyć.

::: sidenote
Defold udostępnia kilka funkcji cyklu życia do kodowania logiki gry. Przeczytaj o nich więcej w [instrukcji skryptów](/manuals/script).
:::

Na początek usuń funkcje `final`, `on_message` i `on_reload`, ponieważ w tym samouczku nie będą nam potrzebne.

Następnie dodaj poniższe linie kodu przed początkiem funkcji `init`.

```lua
-- Constants
local turn_speed = 0.1                           									  -- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector from center of back and front wheel pairs

local acceleration = 100 																						-- The acceleration of the car

-- prehash the inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Wprowadzone tutaj zmiany są dość proste. Dodaliśmy po prostu kilka `constants` do skryptu, których później użyjemy do zaprogramowania naszego samochodu.

::: sidenote
Zwróć uwagę, że wcześniej zapisujemy hasze w zmiennych. To naprawdę dobra praktyka, bo poprawia czytelność kodu i wydajność.
:::

Następnie zmień funkcję `init`, tak aby zawierała poniższy kod:

```lua
function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Some variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end
```

Zastanawiasz się, co właśnie zmieniliśmy? Oto wyjaśnienie.

1. Wysyłamy wiadomość do skryptu renderowania z prośbą o ustawienie koloru tła na szary. Skrypty renderowania to specjalne skrypty w Defold, które sterują tym, jak obiekty są wyświetlane na ekranie.
2. Aby skrypt komponentu lub skrypt GUI mógł nasłuchiwać akcji wejściowych, trzeba wysłać wiadomość `acquire_input_focus` do obiektu gry, który zawiera ten komponent. W naszym przypadku wysyłamy tę wiadomość do obiektu gry przechowującego skrypt samochodu.
3. Następnie deklarujemy kilka zmiennych, których użyjemy do śledzenia bieżącego stanu naszego samochodu.

To było łatwe, prawda? Teraz przejdźmy dalej i zmieńmy funkcję `update`, tak aby wyglądała następująco:

```lua
function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

To była spora funkcja! Ale bez obaw, działa to tak:

1. Najpierw ustawiamy wektor przyspieszenia na podstawie naszego wektora wejścia. Dzięki temu przyspieszenie samochodu jest skierowane zgodnie z wejściem.
2. Następnie obliczane jest przemieszczenie obu kół na podstawie prostej logiki: tylne koła samochodu zawsze poruszają się do przodu, a przednie poruszają się w kierunku, w którym są skręcone.
3. Na podstawie przemieszczenia obu kół obliczany jest nowy kierunek ruchu samochodu.
4. Tutaj dodajemy obliczone przyspieszenie do prędkości.
5. Na końcu aktualizujemy pozycję samochodu na podstawie bieżącej prędkości.
6. Wykonujemy slerp kąta skrętu na podstawie wejścia lewo/prawo. Dzięki temu koła nie przeskakują natychmiast za każdym razem, gdy zmienia się wejście.
7. Następnie obrót kół jest ustawiany na podstawie bieżącego kąta skrętu samochodu. Podobnie obrót samochodu jest ustawiany na podstawie kierunku, w którym aktualnie się porusza.
8. Na końcu zerujemy wektory przyspieszenia i wejścia.

Na koniec pora sprawić, by samochód reagował na wejście. Zmień funkcję `on_input`, aby wyglądała tak:

```lua
function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Ta funkcja jest w gruncie rzeczy dość prosta. Po prostu odbieramy wejście i ustawiamy nasz wektor wejścia.

Nie zapomnij zapisać zmian.

## Wejście

Nie ma jeszcze skonfigurowanych akcji wejściowych, więc to naprawmy. Otwórz plik */input/game.input_bindings* i dodaj wiązania *key_trigger* dla "accelerate", "brake", "left" i "right". Ustawiamy je na klawisze strzałek (`KEY_LEFT`, `KEY_RIGHT`, `KEY_UP` i `KEY_DOWN`):

![Input bindings](images/car/start_input_bindings.png)

## Dodawanie samochodu do gry

Teraz samochód jest gotowy do jazdy. Utworzyliśmy go wewnątrz "car.collection", ale nie istnieje jeszcze w grze. Dzieje się tak dlatego, że silnik obecnie ładuje przy starcie "main.collection". Aby to naprawić, wystarczy dodać *car.collection* do *main.collection*. Otwórz *main.collection*, zaznacz główny węzeł "Collection" w widoku *Outline*, kliknij prawym przyciskiem myszy i wybierz <kbd>Add Collection From File</kbd>, wybierz *car.collection* i kliknij *OK*. Teraz zawartość *car.collection* zostanie umieszczona w *main.collection* jako nowe instancje. Jeśli zmienisz zawartość *car.collection*, każda instancja kolekcji będzie aktualizowana automatycznie przy budowaniu gry.

![Adding the car collection](images/car/start_adding_car_collection.png)

Teraz wybierz <kbd>Project ▸ Build</kbd> i przejedź się swoim nowym samochodem!
Zauważysz, że możesz już sterować samochodem i poruszać nim zgodnie ze swoją wolą. Ale coś nadal nie działa poprawnie. Kiedy puszczasz sterowanie, samochód się nie zatrzymuje, a przecież powinien. Czas to dodać!

## Opór na ratunek

Kiedy obiekt porusza się w świecie rzeczywistym, działa na niego siła oporu, która przeciwdziała ruchowi i powoduje wyhamowanie. Siła ta jest w przybliżeniu proporcjonalna do kwadratu prędkości poruszającego się obiektu i dlatego można ją opisać wzorem `D = k * |V| * V`, gdzie `k` jest stałą, `V` to prędkość, a `|V|` oznacza jej wartość bezwzględną (szybkość). Dodajmy to.

W sekcji stałych na początku skryptu dodaj następującą stałą:

```lua
local drag = 1.1	        --the drag constant <1>
```

Następnie w funkcji `update`, tuż nad tym wierszem, dodaj poniższe linie i zapisz plik.

```lua
function update(self, dt)
	...
  -- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Speed is the magnitude of the velocity
	local speed = vmath.length_sqr(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Zadeklaruj wartość oporu jako stałą.
2. Oblicz prędkość, z jaką się poruszamy.
3. Zastosuj opór do bieżącego przyspieszenia zgodnie ze wzorem.
4. Zatrzymaj samochód, jeśli porusza się już wystarczająco wolno.

## Pełny skrypt samochodu

Po wykonaniu powyższych kroków Twój *car.script* powinien wyglądać tak:

```lua
local turn_speed = 0.1                           				          	-- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector from center of back and front wheel pairs

local acceleration = 100 		                      									-- The acceleration of the car
local drag = 1.1                                                  	-- the drag constant

function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")

	-- Some variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Speed is the magnitude of the velocity
	local speed = vmath.length(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Testowanie gotowej gry

Teraz wybierz <kbd>Project ▸ Build</kbd> z głównego menu i przejedź się swoim nowym samochodem!

To kończy ten wprowadzający samouczek. Oto kilka wyzwań, z którymi możesz spróbować zmierzyć się samodzielnie:

1. Obecnie samochód porusza się z takim samym przyspieszeniem do przodu i do tyłu. Możesz spróbować to zmienić tak, aby przy jeździe wstecz poruszał się wolniej.
2. Zamień część stałych (na przykład przyspieszenie) na `properties`, aby można je było zmieniać dla różnych instancji samochodu.
3. Dodaj do samochodu dźwięki i spraw, żeby robił vroom! ([Wskazówka](manuals/sound/))

Teraz śmiało zanurz się w Defold. Przygotowaliśmy wiele [instrukcji i samouczków](/learn), które Cię poprowadzą, a jeśli utkniesz, serdecznie zapraszamy na [forum](//forum.defold.com).

Przyjemnego Defoldowania!
