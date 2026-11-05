---
title: Запись видео в Defold
brief: В этом руководстве описано, как записать окно игры в MP4 с помощью Lua или HTTP-сервиса движка.
---

# Запись видео {#video-recording}

Defold может записывать окно игры в видео H.264 в файле MP4 через [модуль Lua `recorder`](/ref/recorder/) или [HTTP-сервис движка](/manuals/engine-service/#recording-endpoints). Оба интерфейса используют один рекордер, поэтому одновременно может запускаться, выполняться или завершаться только одна запись.

## Доступность {#availability}

Запись включена в **отладочные** движки для настольных платформ. Она исключена из релизных сборок, сборок без графики, мобильных и веб-сборок. Включение **Exclude Record** в [манифесте приложения](/manuals/app-manifest/#exclude-record) также удаляет модуль Lua и маршруты HTTP.

| Платформа | Требования для видео | Аудио приложения |
| --- | --- | --- |
| macOS | macOS 15 или новее, используется ScreenCaptureKit | Поддерживается |
| Windows | Windows 10 версии 1903 или новее, используются Windows Graphics Capture и Media Foundation | Поддерживается в Windows сборки 20348 или новее |
| Linux | OpenGL, OpenGL ES или Vulkan, используется захват кадрового буфера | Не поддерживается |

Поддержка видео и аудио проверяется отдельно. HTTP-клиенты могут проверить `/recording/capabilities`; при вызове из Lua возвращается ошибка, если запрошенный захват не поддерживается. Разрешения операционной системы и сбои устройства захвата также могут вызвать асинхронную ошибку после принятия запроса на запуск.

Рекордер захватывает содержимое окна игры в исходном размере в физических пикселях. Для получения чётных размеров видео он может обрезать одну строку или столбец. Изменение размера окна или его плотности пикселей останавливает запись и завершает создание файла. Частота захвата — 1–60 кадров в секунду, по умолчанию 30.

## Запись из Lua {#recording-from-lua}

Вызовите [`recorder.start()`](/ref/recorder/#recorder.start), передав доступный для записи путь к файлу и callback. Родительский каталог должен существовать; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) предоставляет подходящий путь сохранения для приложения. Существующий файл может быть перезаписан. Записи Lua принадлежат вызывающему коду и остаются на диске после выхода из движка.

В Windows пути используют кодовую страницу Windows ANSI, на остальных платформах — UTF-8, как и файловый ввод-вывод Lua. Поле `result.path` в callback сохраняет путь, переданный в `recorder.start()`.

Этот пример `.script` записывает пять секунд после начала захвата:

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

`recorder.start()` и [`recorder.stop()`](/ref/recorder/#recorder.stop) возвращают `true`, если запрос принят, или `nil, error`, если отклонён. Принятие запроса не означает, что захват или завершение файла уже закончены. Некорректные параметры вызывают ошибки Lua.

Callback вызывается во время обновлений движка:

| Событие | Значение |
| --- | --- |
| `recorder.EVENT_STARTED` | Захват активен; теперь его можно остановить. |
| `recorder.EVENT_STOPPED` | Файл MP4 завершён и готов к чтению. Событие также возникает после автоматической остановки при изменении размера окна. |
| `recorder.EVENT_ERROR` | Ошибка захвата; проверьте `result.error`. Ошибка запуска может вызвать это событие без `EVENT_STARTED`. |

Результат также содержит `path`, `width`, `height`, `fps` и `audio`. Читайте или отправляйте файл только после `EVENT_STOPPED`. Скрипт, запустивший запись, должен оставаться активным для получения callback: его удаление отменяет callbacks, но не останавливает захват. При завершении работы движка захват завершается без вызова callbacks Lua.

В Lua аудио **по умолчанию отключено**. Задайте `audio = true`, чтобы запросить аудио приложения на поддерживаемой платформе. Запрос неподдерживаемого аудио возвращает ошибку.

### Совместное использование рекордера с HTTP-клиентами {#sharing-the-recorder-with-http-clients}

`recorder.stop()` останавливает текущую общую запись, включая запущенную через HTTP. Функция возвращает ошибку, пока операция ожидает завершения или если активной записи нет. Если HTTP-клиент останавливает запись Lua, исходный callback Lua всё равно получает событие завершения. Запуск через HTTP не создаёт callback Lua; отслеживайте завершение через статус HTTP.

Статус HTTP может описывать запись Lua, но его поле `file` равно `null`: сервис подготавливает загрузку только для записей, запущенных через HTTP. Читайте запись Lua по пути `result.path` после `EVENT_STOPPED`.

## Запись через HTTP {#recording-through-http}

Маршруты записи используют порт сервиса движка, выводимый в журнале игры. Найти их можно через `/openapi.json`, как описано в [руководстве по сервису движка](/manuals/engine-service/#discovering-operations-through-openapi). Движок без графики или релизный движок их не предоставляет.

Следующие команды используют оболочку POSIX, `curl` и `jq`; проверка загруженного файла также использует Python 3. Выполняйте их в одной оболочке, заменив `<port>` на порт работающего движка. Сначала запросите возможности и сохраните идентификатор сервиса:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Продолжайте только если `supported` равно `true`; иначе проверьте `unsupported_reason` и `minimum_platform_version`. Поле `audio` сообщает о поддержке аудио. В отличие от Lua, **запись через HTTP по умолчанию включает аудио, если бэкенд его поддерживает**. В примере ниже аудио явно отключено.

### Запуск и проверка записи {#start-and-inspect-the-recording}

Начните запись, при необходимости передав JSON-объект с `fps` и/или `audio`. Сервис сам выбирает выходной файл; он не принимает путь, ширину, высоту или масштаб.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 означает, что запрос принят. Повторяйте следующую команду проверки статуса, пока `pending` не станет `false`, а `active` — `true`. Проверка отклоняет ответ для другой операции и сообщает об ошибках захвата или подготовки файла. Если автоматическая остановка уже завершила запись, перед загрузкой перейдите к [завершению файла](#stop-and-wait-for-finalization).

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

Дайте игре поработать столько, сколько хотите записать, затем запросите остановку. Если размер окна изменился и запись уже завершена, пропустите запрос остановки и перейдите к завершению файла ниже.

### Остановка и ожидание завершения файла {#stop-and-wait-for-finalization}

Остановите операцию с идентификатором, сохранённым из ответа на запрос запуска:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 означает лишь принятие запроса остановки. Повторяйте команду проверки статуса, пока `pending` не станет `false`, `finalized` — `true`, а `file.state` — `complete`. После окончания нативного захвата сервис подготавливает размер файла и SHA-256, поэтому одни лишь `state: "complete"` и `finalized: true` не означают, что файл готов к загрузке. Прекратите ожидание, если `state` или `file.state` станет `failed`; не загружайте файл со статусом `pending` или `failed`.

Автоматический клиент должен опрашивать статус с задержкой и тайм-аутом, проверяя сохранённый идентификатор операции в каждом ответе. Во время ожидания захвата и завершения файла движок должен продолжать обновляться.

### Загрузка и освобождение файла {#download-and-release-the-file}

Используйте относительный URL завершённого файла из ответа со статусом. Следующая проверка также убеждается, что ответ по-прежнему относится к вашей операции:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Сохраните итоговый ответ со статусом в `capture.json` вместе с MP4. `/recording/status` описывает текущую операцию, поэтому следующая запись заменяет ответ со статусом, даже если более ранние HTTP-файлы остаются доступными.

Перед использованием загруженного файла или удалением копии на сервисе проверьте его размер в байтах и SHA-256:

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

GET без заголовка `Range` загружает весь MP4. Сервис также поддерживает замкнутые диапазоны байтов, например `Range: bytes=0-1023`, если клиенту нужна частичная загрузка. Проверьте собранный файл по тому же сохранённому ответу.

После загрузки и проверки файла можно освободить копию, хранящуюся на сервисе:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

Файлы HTTP-записи доступны до явного удаления либо завершения работы или перезапуска движка. Загружайте их до закрытия движка. Сервис хранит не более 128 файлов; удаляйте завершённые файлы, которые уже сохранили, чтобы освободить место для следующих записей.

### Совместное хранение идентификаторов операции {#keeping-operation-identities-together}

Каждый POST и DELETE требует `X-Recording-Instance`. Примеры также передают его в запросах статуса и загрузки, чтобы отклонять ответы от нового экземпляра движка. Храните `instance_id`, `operation_id` и сведения о файле вместе: идентификатор сервиса меняется при перезапуске, а новый процесс может повторно использовать номера операций.

Отсутствующий идентификатор возвращает HTTP 400. Устаревший идентификатор, устаревшая операция остановки или удалённый файл возвращают HTTP 410. Не получайте новый идентификатор, чтобы повторить с ним старую операцию. Вместо этого обнаружьте новый сервис и начните новую запись.

### Обработка ошибок HTTP {#handling-http-failures}

Отклонённые запросы возвращают JSON с `error.code` и `error.message`. Для диагностики выполните отдельный запрос `curl` с `-i` и без `-f`, чтобы увидеть статус HTTP и тело ошибки.

| Статус HTTP | Что проверить |
| --- | --- |
| 409 | Другая запись активна или ожидает завершения, текущая запись ещё не готова к остановке либо файл всё ещё подготавливается. Проверьте статус перед повтором. |
| 500 | Ошибка запуска записи, инициализации хранилища либо подготовки/чтения файла. Изучите сообщение об ошибке; ошибка захвата также сообщается в поле `failure` статуса. |
| 501 | Видео или запрошенное аудио не поддерживается. Проверьте возможности; используйте `audio: false`, если недоступно только аудио. |
| 507 | Достигнут лимит файлов, хранящихся на сервисе. Загрузите и удалите завершённые файлы перед запуском следующей записи. |
