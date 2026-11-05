---
title: Nagrywanie wideo w silniku Defold
brief: Ta instrukcja wyjaśnia, jak nagrywać okno gry do MP4 za pomocą Lua lub usługi HTTP silnika.
---

# Nagrywanie wideo {#video-recording}

Defold może nagrywać okno gry do pliku MP4 z wideo H.264 przez [moduł Lua `recorder`](/ref/recorder/) albo [usługę HTTP silnika](/manuals/engine-service/#recording-endpoints). Oba interfejsy współdzielą jeden rejestrator, więc tylko jedno nagranie może jednocześnie rozpoczynać się, trwać lub być finalizowane.

## Dostępność {#availability}

Nagrywanie jest dołączone do desktopowych silników **debug**. Jest pomijane w buildach release, headless, mobilnych i webowych. Włączenie **Exclude Record** w [manifeście aplikacji](/manuals/app-manifest/#exclude-record) również usuwa moduł Lua i trasy HTTP.

| Platforma | Wymagania wideo | Dźwięk aplikacji |
| --- | --- | --- |
| macOS | macOS 15 lub nowszy, z użyciem ScreenCaptureKit | Obsługiwany |
| Windows | Windows 10 w wersji 1903 lub nowszej, z użyciem Windows Graphics Capture i Media Foundation | Obsługiwany od buildu Windows 20348 |
| Linux | OpenGL, OpenGL ES lub Vulkan, z przechwytywaniem bufora klatki | Nieobsługiwany |

Obsługa wideo i dźwięku jest sprawdzana osobno. Klienci HTTP mogą odczytać `/recording/capabilities`; wywołujący z Lua otrzymują błąd, jeśli żądane przechwytywanie nie jest obsługiwane. Uprawnienia systemu operacyjnego i awarie urządzenia przechwytującego mogą też spowodować błąd asynchroniczny po przyjęciu żądania startu.

Rejestrator przechwytuje zawartość okna gry w jego natywnym rozmiarze w fizycznych pikselach. Może przyciąć jeden wiersz lub kolumnę, aby uzyskać parzyste wymiary wideo. Zmiana rozmiaru okna lub gęstości jego pikseli zatrzymuje i finalizuje nagranie. Częstotliwość przechwytywania wynosi 1–60 klatek na sekundę, domyślnie 30.

## Nagrywanie z Lua {#recording-from-lua}

Użyj [`recorder.start()`](/ref/recorder/#recorder.start) z zapisywalną ścieżką wyjściową i wywołaniem zwrotnym. Katalog nadrzędny musi istnieć; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) dostarcza odpowiednią ścieżkę zapisu aplikacji. Istniejący plik wyjściowy może zostać nadpisany. Nagrania Lua należą do wywołującego i pozostają na dysku po zakończeniu silnika.

Ścieżki używają strony kodowej Windows ANSI w systemie Windows i UTF-8 na innych platformach, tak jak operacje plikowe Lua. `result.path` w wywołaniu zwrotnym zachowuje ścieżkę przekazaną do `recorder.start()`.

Ten przykład `.script` nagrywa przez pięć sekund od rozpoczęcia przechwytywania:

```lua
local function on_recording_event(self, event, result)
    if event == recorder.EVENT_STARTED then
        self.recording = true
        timer.delay(5, false, function(self)
            if self.recording then
                local ok, err = recorder.stop()
                if not ok then
                    print("Could not stop recording:", err)
                end
            end
        end)
    elseif event == recorder.EVENT_STOPPED then
        self.recording = false
        print("MP4 ready:", result.path)
    elseif event == recorder.EVENT_ERROR then
        self.recording = false
        print("Recording failed:", result.error)
    end
end

function init(self)
    self.recording = false
    if not recorder then
        print("Recording is not included in this engine build")
        return
    end

    local ok, err = recorder.start({
        path = sys.get_save_file("recording_example", "capture.mp4"),
        fps = 30,
        audio = false,
    }, on_recording_event)
    if not ok then
        print("Could not start recording:", err)
    end
end
```

`recorder.start()` i [`recorder.stop()`](/ref/recorder/#recorder.stop) zwracają `true` po przyjęciu żądania albo `nil, error` po odrzuceniu. Przyjęcie nie oznacza zakończenia przechwytywania ani finalizacji pliku. Nieprawidłowe opcje powodują błędy Lua.

Wywołania zwrotne są wykonywane podczas aktualizacji silnika:

| Zdarzenie | Znaczenie |
| --- | --- |
| `recorder.EVENT_STARTED` | Przechwytywanie trwa; można je teraz zatrzymać. |
| `recorder.EVENT_STOPPED` | MP4 został sfinalizowany i jest gotowy do odczytu. Zdarzenie występuje również po automatycznym zatrzymaniu przy zmianie rozmiaru. |
| `recorder.EVENT_ERROR` | Przechwytywanie nie powiodło się; sprawdź `result.error`. Błąd startu może wywołać to zdarzenie bez `EVENT_STARTED`. |

Wynik zawiera również `path`, `width`, `height`, `fps` i `audio`. Odczytuj lub wysyłaj plik wyjściowy dopiero po `EVENT_STOPPED`. Zachowaj skrypt inicjujący, aby otrzymać wywołanie zwrotne: usunięcie go odrzuca wywołania zwrotne bez zatrzymania przechwytywania. Zamykanie silnika finalizuje przechwytywanie bez wywoływania callbacków Lua.

Dźwięk jest **domyślnie wyłączony w Lua**. Ustaw `audio = true`, aby zażądać dźwięku aplikacji na obsługiwanej platformie. Żądanie nieobsługiwanego dźwięku zwraca błąd.

### Współdzielenie rejestratora z klientami HTTP {#sharing-the-recorder-with-http-clients}

`recorder.stop()` odnosi się do bieżącego współdzielonego nagrania, także uruchomionego przez HTTP. Zwraca błąd, gdy operacja oczekuje albo żadne nagranie nie jest aktywne. Jeśli klient HTTP zatrzyma nagranie Lua, pierwotne wywołanie zwrotne Lua nadal otrzyma zdarzenie zakończenia. Uruchomienie przez HTTP nie tworzy wywołania zwrotnego Lua; obserwuj zakończenie przez stan HTTP.

Stan HTTP może opisywać nagranie Lua, ale jego pole `file` ma wartość `null`: usługa przygotowuje pobieranie tylko dla nagrań uruchomionych przez HTTP. Nagranie Lua odczytaj z `result.path` po `EVENT_STOPPED`.

## Nagrywanie przez HTTP {#recording-through-http}

Trasy nagrywania używają portu usługi silnika wypisanego w logu gry. Wykryj je przez `/openapi.json`, jak opisano w [podręczniku usługi silnika](/manuals/engine-service/#discovering-operations-through-openapi). Silnik headless lub release ich nie udostępnia.

Poniższe polecenia używają powłoki POSIX, `curl` i `jq`; etap weryfikacji pobrania korzysta też z Pythona 3. Uruchamiaj je w tej samej powłoce i zastąp `<port>` portem działającego silnika. Najpierw sprawdź możliwości i zachowaj tożsamość usługi:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Kontynuuj tylko wtedy, gdy `supported` wynosi `true`; w przeciwnym razie sprawdź `unsupported_reason` i `minimum_platform_version`. Pole `audio` zgłasza obsługę dźwięku. W odróżnieniu od Lua **nagrywanie HTTP domyślnie włącza dźwięk, gdy backend go obsługuje**. Poniższy przykład jawnie wyłącza dźwięk.

### Uruchamianie i sprawdzanie nagrania {#start-and-inspect-the-recording}

Uruchom nagrywanie z opcjonalnym obiektem JSON zawierającym `fps` i/lub `audio`. Usługa wybiera plik wyjściowy; nie przyjmuje ścieżki, szerokości, wysokości ani skali.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 oznacza przyjęcie żądania. Ponawiaj poniższe polecenie stanu, aż `pending` będzie `false`, a `active` będzie `true`. Sprawdzenie odrzuca odpowiedź dotyczącą innej operacji i zgłasza błędy przechwytywania lub przygotowania pliku. Jeśli automatyczne zatrzymanie już sfinalizowało nagranie, przed pobraniem przejdź do [finalizacji](#stop-and-wait-for-finalization).

```sh
STATUS=$(curl -fsS \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL/recording/status")
printf '%s\n' "$STATUS" | jq -e --argjson id "$OPERATION_ID" '
    if .operation_id != $id then error("Recording operation changed")
    elif .state == "failed" then error(.failure)
    elif .file.state == "failed" then error("Recording file preparation failed")
    else . end'
```

Pozwól grze działać przez czas, który chcesz nagrać, a następnie zażądaj zatrzymania. Jeśli rozmiar okna się zmienił i nagrywanie już się zakończyło, pomiń żądanie zatrzymania i przejdź do opisanej poniżej finalizacji.

### Zatrzymywanie i oczekiwanie na finalizację {#stop-and-wait-for-finalization}

Zatrzymaj operację, której identyfikator zachowano z odpowiedzi na żądanie startu:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 oznacza jedynie przyjęcie żądania zatrzymania. Powtarzaj polecenie stanu, aż `pending` będzie `false`, `finalized` będzie `true`, a `file.state` będzie `complete`. Usługa przygotowuje rozmiar pliku i SHA-256 po zakończeniu natywnego przechwytywania, więc same `state: "complete"` i `finalized: true` nie oznaczają gotowości do pobrania. Przerwij oczekiwanie, jeśli `state` lub `file.state` przyjmie `failed`; nie pobieraj pliku o stanie `pending` ani `failed`.

Klient automatyczny powinien odpytywać z opóźnieniem i limitem czasu, sprawdzając zachowany identyfikator operacji w każdej odpowiedzi. Podczas oczekiwania na przechwytywanie i finalizację silnik musi nadal wykonywać aktualizacje.

### Pobieranie i zwalnianie pliku {#download-and-release-the-file}

Użyj względnego adresu URL ukończonego pliku z odpowiedzi stanu. Poniższe sprawdzenie dodatkowo upewnia się, że odpowiedź nadal należy do twojej operacji:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Zachowaj potwierdzenie ukończonego stanu w `capture.json` razem z MP4. `/recording/status` opisuje bieżącą operację, więc kolejne nagranie zastępuje odpowiedź stanu, nawet jeśli wcześniejsze pliki HTTP nadal są dostępne.

Zweryfikuj rozmiar pobranego pliku w bajtach i SHA-256, zanim go użyjesz lub usuniesz kopię usługi:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path("capture.json").read_text(encoding="utf-8"))
capture = Path("capture.mp4")
if capture.stat().st_size != receipt["file"]["size"]:
    raise SystemExit("Recording download size mismatch")

digest = hashlib.sha256()
with capture.open("rb") as stream:
    for chunk in iter(lambda: stream.read(65536), b""):
        digest.update(chunk)
if digest.hexdigest() != receipt["file"]["sha256"]:
    raise SystemExit("Recording download SHA-256 mismatch")
print("Verified capture.mp4")
PY
```

GET bez nagłówka `Range` pobiera cały plik MP4. Usługa obsługuje również domknięte zakresy bajtów, takie jak `Range: bytes=0-1023`, jeśli klient potrzebuje częściowych pobrań. Zweryfikuj złożony plik względem tego samego potwierdzenia.

Po pobraniu i zweryfikowaniu pliku możesz zwolnić kopię przechowywaną przez usługę:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

Pliki nagrań HTTP pozostają dostępne do jawnego usunięcia albo zamknięcia lub restartu silnika. Pobierz je przed zamknięciem silnika. Usługa przechowuje najwyżej 128 plików; usuwaj ukończone pliki, które zapisałeś, aby zrobić miejsce na dalsze nagrania.

### Przechowywanie tożsamości operacji razem {#keeping-operation-identities-together}

Każde POST i DELETE wymaga `X-Recording-Instance`. Przykłady wysyłają go również w żądaniach stanu i pobierania, aby odrzucać odpowiedzi z zastępującego silnika. Przechowuj `instance_id`, `operation_id` i informacje o pliku razem: tożsamość usługi zmienia się przy ponownym uruchomieniu lub restarcie, a nowy proces może ponownie używać numerów operacji.

Brak tożsamości zwraca HTTP 400. Nieaktualna tożsamość, nieaktualna operacja zatrzymania lub usunięty plik zwracają HTTP 410. Nie pobieraj nowej tożsamości, aby użyć jej do ponowienia starej operacji. Zamiast tego wykryj nową usługę i rozpocznij nowe nagranie.

### Obsługa błędów HTTP {#handling-http-failures}

Odrzucone żądania zwracają JSON z `error.code` i `error.message`. Przy rozwiązywaniu problemów uruchom pojedyncze żądanie `curl` z `-i` i bez `-f`, aby zobaczyć status HTTP i treść błędu.

| Status HTTP | Co sprawdzić |
| --- | --- |
| 409 | Inne nagranie jest aktywne lub oczekuje, bieżące nagranie nie jest gotowe do zatrzymania albo plik jest nadal przygotowywany. Przed ponowieniem odczytaj stan. |
| 500 | Nie powiodło się uruchomienie nagrywania, inicjalizacja przechowywania albo przygotowanie/odczyt pliku. Sprawdź komunikat błędu; nieudane przechwytywanie zgłasza też `failure` w stanie. |
| 501 | Wideo lub żądany dźwięk nie jest obsługiwany. Sprawdź możliwości; użyj `audio: false`, jeśli niedostępny jest tylko dźwięk. |
| 507 | Osiągnięto limit plików przechowywanych przez usługę. Pobierz i usuń ukończone pliki przed rozpoczęciem kolejnego nagrania. |
