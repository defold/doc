---
title: Запис відео в Defold
brief: Цей посібник пояснює, як записувати вікно гри у MP4 через Lua або HTTP-сервіс рушія.
---

# Запис відео {#video-recording}

Defold може записувати вміст вікна гри як відео H.264 у файл MP4 через [модуль Lua `recorder`](/ref/recorder/) або [HTTP-сервіс рушія](/manuals/engine-service/#recording-endpoints). Обидва інтерфейси спільно використовують один засіб запису, тому одночасно може запускатися, тривати або завершуватися лише один запис.

## Доступність {#availability}

Запис включено до **налагоджувальних** рушіїв для настільних платформ. Його виключено зі збірок випуску, збірок без графічного інтерфейсу, мобільних і вебзбірок. Увімкнення **Exclude Record** у [маніфесті застосунку](/manuals/app-manifest/#exclude-record) також вилучає модуль Lua й маршрути HTTP.

| Платформа | Вимоги до відео | Аудіо застосунку |
| --- | --- | --- |
| macOS | macOS 15 або новіша, використовується ScreenCaptureKit | Підтримується |
| Windows | Windows 10 версії 1903 або новіша, використовуються Windows Graphics Capture і Media Foundation | Підтримується у Windows build 20348 або новішій |
| Linux | OpenGL, OpenGL ES або Vulkan, використовується захоплення буфера кадру | Не підтримується |

Підтримка відео й аудіо перевіряється окремо. Клієнти HTTP можуть перевірити `/recording/capabilities`; виклики Lua отримують помилку, якщо запитане захоплення не підтримується. Дозволи операційної системи й збої пристрою захоплення також можуть спричинити асинхронну помилку після прийняття запиту на запуск.

Засіб запису захоплює вміст вікна гри в його початковому розмірі у фізичних пікселях. Він може обрізати один рядок або стовпець, щоб отримати парні розміри відео. Зміна розміру вікна або щільності пікселів зупиняє й завершує запис. Частота захоплення — 1–60 кадрів на секунду, за замовчуванням 30.

## Запис із Lua {#recording-from-lua}

Використовуйте [`recorder.start()`](/ref/recorder/#recorder.start) із доступним для запису вихідним шляхом і зворотним викликом. Батьківський каталог має існувати; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) надає відповідний шлях для збереження даних застосунку. Наявний вихідний файл може бути перезаписано. Записи Lua належать виклику, який їх створив, і залишаються на диску після завершення рушія.

Шляхи використовують кодову сторінку Windows ANSI у Windows і UTF-8 на інших платформах, як і файлове введення-виведення Lua. `result.path` у зворотному виклику зберігає шлях, переданий до `recorder.start()`.

Цей приклад `.script` записує п’ять секунд після початку захоплення:

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

`recorder.start()` і [`recorder.stop()`](/ref/recorder/#recorder.stop) повертають `true`, якщо запит прийнято, або `nil, error`, якщо відхилено. Прийняття не означає, що захоплення або завершення файлу вже закінчилося. Некоректні параметри спричиняють помилки Lua.

Зворотні виклики виконуються під час оновлень рушія:

| Подія | Значення |
| --- | --- |
| `recorder.EVENT_STARTED` | Захоплення активне; тепер його можна зупинити. |
| `recorder.EVENT_STOPPED` | MP4 завершено й він готовий до читання. Ця подія також виникає після автоматичного зупинення через зміну розміру. |
| `recorder.EVENT_ERROR` | Захоплення завершилося помилкою; перевірте `result.error`. Помилка запуску може спричинити цю подію без `EVENT_STARTED`. |

Результат також містить `path`, `width`, `height`, `fps` і `audio`. Читайте або надсилайте вихідний файл лише після `EVENT_STOPPED`. Зберігайте скрипт, що ініціював запис, щоб отримати зворотний виклик: його видалення відкидає зворотні виклики, але не зупиняє захоплення. Завершення рушія завершує захоплення без викликів Lua.

Аудіо **за замовчуванням вимкнено в Lua**. Задайте `audio = true`, щоб запитати аудіо застосунку на підтримуваній платформі. Запит непідтримуваного аудіо повертає помилку.

### Спільне використання засобу запису з клієнтами HTTP {#sharing-the-recorder-with-http-clients}

`recorder.stop()` діє на поточний спільний запис, зокрема запущений через HTTP. Функція повертає помилку, поки операція очікує завершення або коли активного запису немає. Якщо клієнт HTTP зупиняє запис Lua, початковий зворотний виклик Lua все одно отримує подію завершення. Запуск через HTTP не створює зворотного виклику Lua; відстежуйте завершення через стан HTTP.

Стан HTTP може описувати запис Lua, але його поле `file` дорівнює `null`: сервіс готує завантаження лише для записів, запущених через HTTP. Читайте запис Lua з `result.path` після `EVENT_STOPPED`.

## Запис через HTTP {#recording-through-http}

Маршрути запису використовують порт сервісу рушія, надрукований у журналі гри. Виявіть їх через `/openapi.json`, як описано в [посібнику із сервісу рушія](/manuals/engine-service/#discovering-operations-through-openapi). Рушій без графічного інтерфейсу або рушій випуску не надає цих маршрутів.

Наступні команди використовують оболонку POSIX, `curl` і `jq`; крок перевірки завантаження також використовує Python 3. Виконуйте їх в одній оболонці й замініть `<port>` на порт запущеного рушія. Спочатку запитайте можливості й збережіть ідентифікатор сервісу:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Продовжуйте лише тоді, коли `supported` дорівнює `true`; інакше перевірте `unsupported_reason` і `minimum_platform_version`. Поле `audio` повідомляє про підтримку аудіо. На відміну від Lua, **запис HTTP за замовчуванням вмикає аудіо, якщо бекенд його підтримує**. Приклад нижче явно вимикає аудіо.

### Запуск і перевірка запису {#start-and-inspect-the-recording}

Запустіть запис із необов’язковим об’єктом JSON, який містить `fps` та/або `audio`. Сервіс вибирає вихідний файл; він не приймає шлях, ширину, висоту або масштаб.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 означає, що запит прийнято. Повторюйте наведену нижче команду стану, доки `pending` не стане `false`, а `active` — `true`. Перевірка відхиляє відповідь для іншої операції й повідомляє про помилки захоплення або підготовки файлу. Якщо автоматичне зупинення вже завершило запис, перед завантаженням перейдіть до [завершення](#stop-and-wait-for-finalization).

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

Дайте грі працювати стільки часу, скільки потрібно записати, а потім запитайте зупинення. Якщо розмір вікна змінився й запис уже завершився, пропустіть запит зупинення та перейдіть до завершення нижче.

### Зупинення й очікування завершення {#stop-and-wait-for-finalization}

Зупиніть операцію, ідентифікатор якої ви зберегли з відповіді на запуск:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 лише приймає запит зупинення. Повторюйте команду стану, доки `pending` не стане `false`, `finalized` — `true`, а `file.state` — `complete`. Сервіс готує розмір і SHA-256 файлу після завершення нативного захоплення, тому самі `state: "complete"` і `finalized: true` ще не означають, що завантаження готове. Припиніть очікування, якщо `state` або `file.state` стає `failed`; не завантажуйте файл зі станом `pending` або `failed`.

Автоматизований клієнт має опитувати стан із затримкою й тайм-аутом, перевіряючи збережений ідентифікатор операції в кожній відповіді. Під час очікування захоплення й завершення рушій має продовжувати оновлюватися.

### Завантаження й вивільнення файлу {#download-and-release-the-file}

Використовуйте відносний URL завершеного файлу з відповіді стану. Перевірка нижче також гарантує, що відповідь досі належить вашій операції:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Зберігайте квитанцію завершеного стану в `capture.json` разом із MP4. `/recording/status` описує поточну операцію, тому пізніший запис замінює відповідь стану, навіть коли попередні файли HTTP залишаються доступними.

Перевірте розмір завантаженого файлу в байтах і його SHA-256, перш ніж використовувати файл або видаляти копію сервісу:

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

GET без заголовка `Range` завантажує весь MP4. Сервіс також підтримує закриті діапазони байтів, наприклад `Range: bytes=0-1023`, якщо клієнту потрібне часткове завантаження. Перевіряйте зібраний файл за тією самою квитанцією.

Після завантаження й перевірки файлу можна вивільнити копію, яку зберігає сервіс:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

Файли записів HTTP залишаються доступними до явного видалення, завершення або перезавантаження рушія. Завантажте їх перед закриттям рушія. Сервіс зберігає щонайбільше 128 файлів; видаляйте завершені файли, які вже зберегли, щоб звільнити місце для подальших записів.

### Спільне зберігання ідентифікаторів операції {#keeping-operation-identities-together}

Кожен POST і DELETE потребує `X-Recording-Instance`. Приклади також надсилають його в запитах стану й завантаження, щоб відхилити відповіді від заміненого рушія. Зберігайте `instance_id`, `operation_id` та інформацію про файл разом: ідентифікатор сервісу змінюється після перезапуску або перезавантаження, а новий процес може повторно використовувати номери операцій.

Відсутній ідентифікатор повертає HTTP 400. Застарілий ідентифікатор, застаріла операція зупинення або видалений файл повертають HTTP 410. Не отримуйте новий ідентифікатор, щоб із ним повторити стару операцію. Натомість виявіть новий сервіс і почніть новий запис.

### Обробка помилок HTTP {#handling-http-failures}

Відхилені запити повертають JSON з `error.code` і `error.message`. Для діагностики виконайте окремий запит `curl` із `-i` та без `-f`, щоб побачити статус HTTP і тіло помилки.

| Статус HTTP | Що перевірити |
| --- | --- |
| 409 | Інший запис активний або очікує завершення, поточний запис ще не готовий до зупинення або файл ще готується. Прочитайте стан перед повторною спробою. |
| 500 | Помилка запуску запису, ініціалізації сховища або підготовки/читання файлу. Перевірте повідомлення про помилку; невдале захоплення також повідомляє `failure` у стані. |
| 501 | Відео або запитане аудіо не підтримується. Перевірте можливості; використовуйте `audio: false`, якщо недоступне лише аудіо. |
| 507 | Досягнуто межі кількості файлів, які зберігає сервіс. Завантажте й видаліть завершені файли перед початком нового запису. |
