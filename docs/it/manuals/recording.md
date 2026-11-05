---
title: Registrazione video in Defold
brief: Questo manuale spiega come registrare la finestra del gioco in MP4 usando Lua o il servizio HTTP del motore.
---

# Registrazione video {#video-recording}

Defold può registrare la finestra del gioco in un video H.264 contenuto in un file MP4 tramite il [modulo Lua `recorder`](/ref/recorder/) o il [servizio HTTP del motore](/manuals/engine-service/#recording-endpoints). Entrambe le interfacce condividono un solo registratore, quindi una sola registrazione alla volta può avviarsi, essere attiva o essere finalizzata.

## Disponibilità {#availability}

La registrazione è inclusa nei motori **debug** desktop. È esclusa dalle build di release, headless, mobili e web. Abilitare **Exclude Record** in un [App Manifest](/manuals/app-manifest/#exclude-record) rimuove anche il modulo Lua e le route HTTP.

| Piattaforma | Requisiti video | Audio dell'applicazione |
| --- | --- | --- |
| macOS | macOS 15 o versioni successive, tramite ScreenCaptureKit | Supportato |
| Windows | Windows 10 versione 1903 o successiva, tramite Windows Graphics Capture e Media Foundation | Supportato su Windows build 20348 o successive |
| Linux | OpenGL, OpenGL ES o Vulkan, tramite acquisizione del framebuffer | Non supportato |

Il supporto video e audio viene verificato separatamente. I client HTTP possono ispezionare `/recording/capabilities`; i chiamanti Lua ricevono un errore se l'acquisizione richiesta non è supportata. Anche i permessi del sistema operativo e i guasti del dispositivo di acquisizione possono causare un errore asincrono dopo l'accettazione di una richiesta di avvio.

Il registratore acquisisce il contenuto della finestra del gioco alle dimensioni native in pixel fisici. Può ritagliare una riga o una colonna per ottenere dimensioni video pari. Ridimensionare la finestra o cambiarne la densità di pixel arresta e finalizza la registrazione. La frequenza di acquisizione va da 1 a 60 frame al secondo, con un valore predefinito di 30.

## Registrazione da Lua {#recording-from-lua}

Usa [`recorder.start()`](/ref/recorder/#recorder.start) con un percorso di uscita scrivibile e un callback. La directory genitore deve esistere; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) fornisce un percorso di salvataggio adatto all'applicazione. Un file di uscita esistente può essere sovrascritto. Le registrazioni Lua appartengono al chiamante e rimangono su disco dopo la chiusura del motore.

I percorsi usano la pagina di codici ANSI di Windows su Windows e UTF-8 sulle altre piattaforme, come per l'I/O dei file Lua. `result.path` del callback conserva il percorso passato a `recorder.start()`.

Questo esempio `.script` registra per cinque secondi dopo l'inizio dell'acquisizione:

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

`recorder.start()` e [`recorder.stop()`](/ref/recorder/#recorder.stop) restituiscono `true` quando la richiesta viene accettata oppure `nil, error` quando viene rifiutata. L'accettazione non significa che l'acquisizione o la finalizzazione del file siano terminate. Le opzioni non valide generano errori Lua.

I callback vengono eseguiti durante gli aggiornamenti del motore:

| Evento | Significato |
| --- | --- |
| `recorder.EVENT_STARTED` | L'acquisizione è attiva; ora può essere arrestata. |
| `recorder.EVENT_STOPPED` | L'MP4 è stato finalizzato ed è pronto per la lettura. Si verifica anche dopo un arresto automatico dovuto al ridimensionamento. |
| `recorder.EVENT_ERROR` | L'acquisizione è fallita; esamina `result.error`. Un errore di avvio può produrre questo evento senza `EVENT_STARTED`. |

Il risultato contiene anche `path`, `width`, `height`, `fps` e `audio`. Leggi o carica l'output solo dopo `EVENT_STOPPED`. Mantieni attivo lo script che ha avviato la registrazione per ricevere il callback: eliminarlo scarta i callback senza arrestare l'acquisizione. La chiusura del motore finalizza l'acquisizione senza invocare i callback Lua.

L'audio è **disabilitato per impostazione predefinita in Lua**. Imposta `audio = true` per richiedere l'audio dell'applicazione su una piattaforma supportata. Richiedere audio non supportato restituisce un errore.

### Condivisione del registratore con i client HTTP {#sharing-the-recorder-with-http-clients}

`recorder.stop()` agisce sulla registrazione condivisa corrente, compresa una avviata tramite HTTP. Restituisce un errore mentre un'operazione è in attesa o quando nessuna registrazione è attiva. Se un client HTTP arresta una registrazione Lua, il callback Lua originale riceve comunque l'evento di completamento. L'avvio tramite HTTP non crea un callback Lua; usa lo stato HTTP per osservarne il completamento.

Lo stato HTTP può descrivere una registrazione Lua, ma il suo campo `file` è `null`: il servizio prepara i download soltanto per le registrazioni avviate tramite HTTP. Leggi una registrazione Lua da `result.path` dopo `EVENT_STOPPED`.

## Registrazione tramite HTTP {#recording-through-http}

Le route di registrazione usano la porta del servizio del motore stampata nel log del gioco. Rilevale tramite `/openapi.json`, come descritto nel [manuale del servizio del motore](/manuals/engine-service/#discovering-operations-through-openapi). Un motore headless o di release non le espone.

I comandi seguenti usano una shell POSIX, `curl` e `jq`; il passaggio di verifica del download usa anche Python 3. Eseguili nella stessa shell e sostituisci `<port>` con la porta del motore in esecuzione. Per prima cosa interroga le funzionalità e conserva l'identità del servizio:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Procedi soltanto se `supported` è `true`; altrimenti esamina `unsupported_reason` e `minimum_platform_version`. Il campo `audio` riporta il supporto audio. A differenza di Lua, **la registrazione HTTP abilita l'audio per impostazione predefinita quando il backend lo supporta**. L'esempio seguente disabilita esplicitamente l'audio.

### Avvio e ispezione della registrazione {#start-and-inspect-the-recording}

Avvia con un oggetto JSON facoltativo contenente `fps` e/o `audio`. Il servizio sceglie il file di uscita; non accetta percorso, larghezza, altezza o scala.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 indica che la richiesta è stata accettata. Riesegui il comando di stato seguente finché `pending` non è `false` e `active` non è `true`. Il controllo rifiuta una risposta relativa a un'altra operazione e segnala errori di acquisizione o preparazione del file. Se un arresto automatico ha già finalizzato la registrazione, prosegui con la [finalizzazione](#stop-and-wait-for-finalization) prima di scaricare.

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

Lascia il gioco in esecuzione per la durata che vuoi acquisire, quindi richiedi l'arresto. Se la finestra è stata ridimensionata e la registrazione è già completata, salta la richiesta di arresto e prosegui con la finalizzazione seguente.

### Arresto e attesa della finalizzazione {#stop-and-wait-for-finalization}

Arresta l'operazione il cui ID hai conservato dalla risposta di avvio:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 accetta soltanto la richiesta di arresto. Ripeti il comando di stato finché `pending` non è `false`, `finalized` non è `true` e `file.state` non è `complete`. Il servizio prepara le dimensioni e lo SHA-256 del file dopo il termine dell'acquisizione nativa, quindi `state: "complete"` e `finalized: true` da soli non significano che il download sia pronto. Smetti di attendere se `state` o `file.state` diventa `failed`; non scaricare un file il cui stato è `pending` o `failed`.

Un client automatico dovrebbe interrogare il servizio con un intervallo e un timeout, controllando l'ID dell'operazione conservato in ogni risposta. Lascia che il motore continui ad aggiornarsi durante l'attesa dell'acquisizione e della finalizzazione.

### Download e rilascio del file {#download-and-release-the-file}

Usa l'URL relativo del file completato presente nella risposta di stato. Il controllo seguente assicura anche che la risposta appartenga ancora alla tua operazione:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Conserva la ricevuta di stato completato in `capture.json` insieme all'MP4. `/recording/status` descrive l'operazione corrente, quindi una registrazione successiva sostituisce la risposta di stato anche mentre i file HTTP precedenti restano disponibili.

Verifica le dimensioni in byte e lo SHA-256 del file scaricato prima di usarlo o eliminare la copia del servizio:

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

Una richiesta GET senza intestazione `Range` scarica l'intero MP4. Il servizio supporta anche intervalli di byte chiusi, come `Range: bytes=0-1023`, se un client richiede download parziali. Verifica il file ricomposto rispetto alla stessa ricevuta.

Dopo aver scaricato e verificato il file, puoi rilasciare la copia conservata dal servizio:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

I file delle registrazioni HTTP rimangono disponibili finché non vengono eliminati esplicitamente o il motore non viene chiuso o riavviato. Scaricali prima di chiudere il motore. Il servizio conserva al massimo 128 file; elimina i file completati che hai salvato per fare spazio a ulteriori registrazioni.

### Conservazione congiunta delle identità delle operazioni {#keeping-operation-identities-together}

Ogni POST e DELETE richiede `X-Recording-Instance`. Gli esempi lo inviano anche nelle richieste di stato e download per rifiutare risposte provenienti da un motore sostitutivo. Conserva insieme `instance_id`, `operation_id` e le informazioni sul file: l'identità del servizio cambia alla riapertura o al riavvio e un nuovo processo può riutilizzare i numeri delle operazioni.

Un'identità mancante restituisce HTTP 400. Un'identità obsoleta, un'operazione di arresto obsoleta o un file eliminato restituisce HTTP 410. Non recuperare una nuova identità per riutilizzarla nel tentativo di ripetere una vecchia operazione. Rileva invece il nuovo servizio e avvia una nuova registrazione.

### Gestione degli errori HTTP {#handling-http-failures}

Le richieste rifiutate restituiscono JSON con `error.code` ed `error.message`. Per la risoluzione dei problemi, esegui la singola richiesta `curl` con `-i` e senza `-f` per vedere lo stato HTTP e il corpo dell'errore.

| Stato HTTP | Cosa controllare |
| --- | --- |
| 409 | Un'altra registrazione è attiva o in attesa, quella corrente non è pronta per essere arrestata oppure il file è ancora in preparazione. Leggi lo stato prima di riprovare. |
| 500 | L'avvio della registrazione, l'inizializzazione dello spazio di archiviazione oppure la preparazione/lettura del file sono falliti. Esamina il messaggio di errore; un'acquisizione fallita riporta anche `failure` nello stato. |
| 501 | Il video o l'audio richiesto non sono supportati. Esamina le funzionalità; usa `audio: false` se non è disponibile soltanto l'audio. |
| 507 | È stato raggiunto il limite dei file conservati dal servizio. Scarica ed elimina i file completati prima di avviare un'altra registrazione. |
