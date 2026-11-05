---
title: Enregistrement vidéo dans Defold
brief: Ce manuel explique comment enregistrer la fenêtre du jeu en MP4 avec Lua ou le service HTTP du moteur.
---

# Enregistrement vidéo {#video-recording}

Defold peut enregistrer la fenêtre du jeu en vidéo H.264 dans un fichier MP4 via le [module Lua `recorder`](/ref/recorder/) ou le [service HTTP du moteur](/manuals/engine-service/#recording-endpoints). Les deux interfaces partagent un seul enregistreur : un seul enregistrement peut donc être en phase de démarrage, de capture ou de finalisation à la fois.

## Disponibilité {#availability}

L'enregistrement est inclus dans les moteurs **debug** pour ordinateur. Il est omis des builds de publication, sans interface graphique, mobiles et web. L'activation de **Exclude Record** dans un [manifeste d'application](/manuals/app-manifest/#exclude-record) supprime également le module Lua et les routes HTTP.

| Plateforme | Conditions requises pour la vidéo | Audio de l'application |
| --- | --- | --- |
| macOS | macOS 15 ou version ultérieure, avec ScreenCaptureKit | Pris en charge |
| Windows | Windows 10 version 1903 ou ultérieure, avec Windows Graphics Capture et Media Foundation | Pris en charge à partir du build Windows 20348 |
| Linux | OpenGL, OpenGL ES ou Vulkan, avec capture du framebuffer | Non pris en charge |

La prise en charge de la vidéo et celle de l'audio sont vérifiées séparément. Les clients HTTP peuvent consulter `/recording/capabilities` ; les appels Lua reçoivent une erreur si la capture demandée n'est pas prise en charge. Les autorisations du système d'exploitation et les défaillances des périphériques de capture peuvent également provoquer une erreur asynchrone après l'acceptation d'une demande de démarrage.

L'enregistreur capture le contenu de la fenêtre du jeu à sa taille native en pixels physiques. Il peut rogner une ligne ou une colonne pour obtenir des dimensions vidéo paires. Le redimensionnement de la fenêtre ou la modification de sa densité de pixels arrête et finalise l'enregistrement. La fréquence de capture est comprise entre 1 et 60 images par seconde, avec une valeur par défaut de 30.

## Enregistrer depuis Lua {#recording-from-lua}

Utilisez [`recorder.start()`](/ref/recorder/#recorder.start) avec un chemin de sortie accessible en écriture et un callback. Le répertoire parent doit exister ; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) fournit un chemin de sauvegarde adapté à l'application. Un fichier de sortie existant peut être écrasé. Les enregistrements Lua appartiennent à l'appelant et restent sur le disque après l'arrêt du moteur.

Les chemins utilisent la page de codes ANSI de Windows sous Windows et UTF-8 ailleurs, comme les entrées-sorties de fichiers Lua. Le champ `result.path` du callback conserve le chemin transmis à `recorder.start()`.

Cet exemple `.script` enregistre pendant cinq secondes après le début de la capture :

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

`recorder.start()` et [`recorder.stop()`](/ref/recorder/#recorder.stop) renvoient `true` si la demande est acceptée, ou `nil, error` si elle est refusée. L'acceptation ne signifie pas que la capture ou la finalisation du fichier est terminée. Des options non valides déclenchent des erreurs Lua.

Les callbacks s'exécutent pendant les mises à jour du moteur :

| Événement | Signification |
| --- | --- |
| `recorder.EVENT_STARTED` | La capture est active ; elle peut maintenant être arrêtée. |
| `recorder.EVENT_STOPPED` | Le MP4 est finalisé et prêt à être lu. Cet événement se produit aussi après un arrêt automatique dû à un redimensionnement. |
| `recorder.EVENT_ERROR` | La capture a échoué ; consultez `result.error`. Un échec du démarrage peut produire cet événement sans `EVENT_STARTED`. |

Le résultat contient également `path`, `width`, `height`, `fps` et `audio`. Ne lisez ou ne téléversez la sortie qu'après `EVENT_STOPPED`. Maintenez le script à l'origine de la demande en vie pour recevoir le callback : sa suppression abandonne les callbacks sans arrêter la capture. L'arrêt du moteur finalise la capture sans appeler les callbacks Lua.

L'audio est **désactivé par défaut dans Lua**. Définissez `audio = true` pour demander l'audio de l'application sur une plateforme compatible. Une demande d'audio non pris en charge renvoie une erreur.

### Partager l'enregistreur avec les clients HTTP {#sharing-the-recorder-with-http-clients}

`recorder.stop()` cible l'enregistrement partagé courant, y compris s'il a été démarré via HTTP. Cette fonction renvoie une erreur lorsqu'une opération est en attente ou qu'aucun enregistrement n'est actif. Si un client HTTP arrête un enregistrement Lua, le callback Lua d'origine reçoit quand même son événement de fin. Un démarrage via HTTP ne crée pas de callback Lua ; utilisez l'état HTTP pour observer la fin de l'enregistrement.

L'état HTTP peut décrire un enregistrement Lua, mais son champ `file` vaut `null` : le service prépare uniquement les téléchargements des enregistrements démarrés via HTTP. Lisez un enregistrement Lua depuis `result.path` après `EVENT_STOPPED`.

## Enregistrer via HTTP {#recording-through-http}

Les routes d'enregistrement utilisent le port du service du moteur affiché dans le journal du jeu. Découvrez-les via `/openapi.json`, comme décrit dans le [manuel du service du moteur](/manuals/engine-service/#discovering-operations-through-openapi). Un moteur sans interface graphique ou de publication ne les expose pas.

Les commandes suivantes utilisent un shell POSIX, `curl` et `jq` ; l'étape de vérification du téléchargement utilise également Python 3. Exécutez-les dans le même shell et remplacez `<port>` par le port du moteur en cours d'exécution. Commencez par interroger les capacités et conserver l'identité du service :

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Ne continuez que si `supported` vaut `true` ; sinon, examinez `unsupported_reason` et `minimum_platform_version`. Le champ `audio` indique la prise en charge de l'audio. Contrairement à Lua, **l'enregistrement HTTP active l'audio par défaut lorsque le backend le prend en charge**. L'exemple ci-dessous désactive explicitement l'audio.

### Démarrer et inspecter l'enregistrement {#start-and-inspect-the-recording}

Démarrez avec un objet JSON facultatif contenant `fps` et/ou `audio`. Le service choisit le fichier de sortie ; il n'accepte ni chemin, ni largeur, ni hauteur, ni échelle.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 signifie que la demande a été acceptée. Réexécutez la commande d'état suivante jusqu'à ce que `pending` vaille `false` et `active` vaille `true`. La vérification refuse une réponse concernant une autre opération et signale les échecs de capture ou de préparation du fichier. Si un arrêt automatique a déjà finalisé l'enregistrement, passez à la [finalisation](#stop-and-wait-for-finalization) avant le téléchargement.

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

Laissez le jeu s'exécuter pendant la durée à capturer, puis demandez l'arrêt. Si la fenêtre a été redimensionnée et que l'enregistrement est déjà terminé, omettez la demande d'arrêt et poursuivez avec la finalisation ci-dessous.

### Arrêter et attendre la finalisation {#stop-and-wait-for-finalization}

Arrêtez l'opération dont vous avez conservé l'identifiant depuis la réponse au démarrage :

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 accepte uniquement la demande d'arrêt. Répétez la commande d'état jusqu'à ce que `pending` vaille `false`, `finalized` vaille `true` et `file.state` vaille `complete`. Le service prépare la taille et le SHA-256 du fichier après la fin de la capture native ; `state: "complete"` et `finalized: true` ne suffisent donc pas à indiquer que le téléchargement est prêt. Cessez d'attendre si `state` ou `file.state` devient `failed` ; ne téléchargez pas un fichier dont l'état est `pending` ou `failed`.

Un client automatisé devrait interroger périodiquement l'état avec un délai entre les requêtes et un délai d'expiration, en vérifiant l'identifiant d'opération conservé à chaque réponse. Laissez le moteur continuer ses mises à jour en attendant la capture et la finalisation.

### Télécharger et libérer le fichier {#download-and-release-the-file}

Utilisez l'URL relative du fichier terminé fournie dans la réponse d'état. La vérification ci-dessous garantit également que la réponse appartient toujours à votre opération :

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Conservez le reçu d'état final dans `capture.json` avec le MP4. `/recording/status` décrit l'opération courante ; un enregistrement ultérieur remplace donc la réponse d'état, même si les fichiers HTTP précédents restent disponibles.

Vérifiez la taille en octets et le SHA-256 du fichier téléchargé avant de l'utiliser ou de supprimer la copie du service :

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

Une requête GET sans en-tête `Range` télécharge le MP4 entier. Le service prend aussi en charge les plages d'octets fermées, comme `Range: bytes=0-1023`, si un client a besoin de téléchargements partiels. Vérifiez le fichier réassemblé à l'aide du même reçu.

Après avoir téléchargé et vérifié le fichier, vous pouvez libérer la copie conservée par le service :

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

Les fichiers d'enregistrement HTTP restent disponibles jusqu'à leur suppression explicite ou jusqu'à l'arrêt ou au redémarrage du moteur. Téléchargez-les avant de fermer le moteur. Le service conserve au maximum 128 fichiers ; supprimez les fichiers terminés que vous avez sauvegardés pour libérer de la place pour les enregistrements suivants.

### Conserver ensemble les identités des opérations {#keeping-operation-identities-together}

Chaque requête POST et DELETE exige `X-Recording-Instance`. Les exemples l'envoient également avec les requêtes d'état et de téléchargement pour refuser les réponses d'un moteur de remplacement. Conservez ensemble `instance_id`, `operation_id` et les informations du fichier : l'identité du service change après un redémarrage, et un nouveau processus peut réutiliser les numéros d'opération.

Une identité manquante renvoie HTTP 400. Une identité périmée, une opération d'arrêt périmée ou un fichier supprimé renvoie HTTP 410. Ne récupérez pas une nouvelle identité pour réessayer une ancienne opération avec celle-ci. Découvrez le nouveau service et démarrez plutôt un nouvel enregistrement.

### Gérer les erreurs HTTP {#handling-http-failures}

Les demandes refusées renvoient du JSON contenant `error.code` et `error.message`. Pour le dépannage, exécutez la requête `curl` concernée avec `-i` et sans `-f` pour afficher le code d'état HTTP et le corps de l'erreur.

| État HTTP | Vérifications |
| --- | --- |
| 409 | Un autre enregistrement est actif ou en attente, l'enregistrement courant n'est pas prêt à être arrêté, ou le fichier est encore en préparation. Consultez l'état avant de réessayer. |
| 500 | Le démarrage de l'enregistrement, l'initialisation du stockage ou la préparation/lecture du fichier a échoué. Consultez le message d'erreur ; une capture ayant échoué signale aussi `failure` dans l'état. |
| 501 | La vidéo ou l'audio demandé n'est pas pris en charge. Consultez les capacités ; utilisez `audio: false` si seul l'audio est indisponible. |
| 507 | La limite de fichiers conservés par le service a été atteinte. Téléchargez et supprimez les fichiers terminés avant de démarrer un nouvel enregistrement. |
