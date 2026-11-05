---
title: Gravação de vídeo no Defold
brief: Este manual explica como gravar a janela do jogo em MP4 usando Lua ou o serviço HTTP da engine.
---

# Gravação de vídeo {#video-recording}

O Defold pode gravar a janela do jogo como vídeo H.264 em um arquivo MP4 por meio do [módulo Lua `recorder`](/ref/recorder/) ou do [serviço HTTP da engine](/manuals/engine-service/#recording-endpoints). Ambas as interfaces compartilham um único gravador, portanto apenas uma gravação pode iniciar, executar ou finalizar por vez.

## Disponibilidade {#availability}

A gravação está incluída em engines de **depuração** para desktop. Ela é omitida de builds de release, headless, móveis e web. Habilitar **Exclude Record** em um [App Manifest](/manuals/app-manifest/#exclude-record) também remove o módulo Lua e as rotas HTTP.

| Plataforma | Requisitos de vídeo | Áudio da aplicação |
| --- | --- | --- |
| macOS | macOS 15 ou posterior, usando ScreenCaptureKit | Compatível |
| Windows | Windows 10 versão 1903 ou posterior, usando Windows Graphics Capture e Media Foundation | Compatível a partir do build 20348 do Windows |
| Linux | OpenGL, OpenGL ES ou Vulkan, usando captura de framebuffer | Não compatível |

O suporte a vídeo e áudio é verificado separadamente. Clientes HTTP podem inspecionar `/recording/capabilities`; chamadas Lua recebem um erro se a captura solicitada não for compatível. Permissões do sistema operacional e falhas do dispositivo de captura também podem causar um erro assíncrono após a aceitação de uma solicitação de início.

O gravador captura o conteúdo da janela do jogo em seu tamanho nativo em pixels físicos. Pode recortar uma linha ou coluna para produzir dimensões de vídeo pares. Redimensionar a janela ou alterar sua densidade de pixels para e finaliza a gravação. A taxa de captura é de 1 a 60 frames por segundo, com padrão de 30.

## Gravando a partir do Lua {#recording-from-lua}

Use [`recorder.start()`](/ref/recorder/#recorder.start) com um caminho de saída gravável e um callback. O diretório pai deve existir; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) fornece um caminho adequado de salvamento da aplicação. Um arquivo de saída existente pode ser sobrescrito. Gravações Lua pertencem ao chamador e permanecem em disco após o encerramento da engine.

Caminhos usam a página de códigos ANSI do Windows nessa plataforma e UTF-8 nas demais, como na entrada e saída de arquivos do Lua. O `result.path` do callback preserva o caminho passado para `recorder.start()`.

Este exemplo `.script` grava por cinco segundos após o início da captura:

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

`recorder.start()` e [`recorder.stop()`](/ref/recorder/#recorder.stop) retornam `true` quando aceitos ou `nil, error` quando rejeitados. A aceitação não significa que a captura ou a finalização do arquivo terminou. Opções inválidas geram erros Lua.

Os callbacks são executados durante as atualizações da engine:

| Evento | Significado |
| --- | --- |
| `recorder.EVENT_STARTED` | A captura está ativa e já pode ser parada. |
| `recorder.EVENT_STOPPED` | O MP4 foi finalizado e está pronto para leitura. Isso também ocorre após uma parada automática por redimensionamento. |
| `recorder.EVENT_ERROR` | A captura falhou; inspecione `result.error`. Uma falha na inicialização pode produzir esse evento sem `EVENT_STARTED`. |

O resultado também contém `path`, `width`, `height`, `fps` e `audio`. Leia ou envie a saída somente após `EVENT_STOPPED`. Mantenha o script que iniciou a gravação ativo para receber o callback: excluí-lo descarta os callbacks sem parar a captura. O encerramento da engine finaliza a captura sem invocar callbacks Lua.

O áudio é **desabilitado por padrão no Lua**. Defina `audio = true` para solicitar áudio da aplicação em uma plataforma compatível. Solicitar áudio sem suporte retorna um erro.

### Compartilhando o gravador com clientes HTTP {#sharing-the-recorder-with-http-clients}

`recorder.stop()` atua sobre a gravação compartilhada atual, incluindo uma iniciada por HTTP. Retorna um erro enquanto uma operação está pendente ou quando nenhuma gravação está ativa. Se um cliente HTTP parar uma gravação Lua, o callback Lua original ainda recebe seu evento de conclusão. Iniciar por HTTP não cria um callback Lua; use o status HTTP para observar sua conclusão.

O status HTTP pode descrever uma gravação Lua, mas seu campo `file` é `null`: o serviço só prepara downloads de gravações iniciadas por HTTP. Leia uma gravação Lua de `result.path` após `EVENT_STOPPED`.

## Gravando por HTTP {#recording-through-http}

As rotas de gravação usam a porta do serviço da engine impressa no log do jogo. Descubra-as por meio de `/openapi.json`, conforme descrito no [manual do serviço da engine](/manuals/engine-service/#discovering-operations-through-openapi). Engines headless ou de release não as expõem.

Os comandos abaixo usam um shell POSIX, `curl` e `jq`; a etapa de verificação do download também usa Python 3. Execute-os no mesmo shell e substitua `<port>` pela porta da engine em execução. Primeiro, consulte as capacidades e guarde a identidade do serviço:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Prossiga apenas se `supported` for `true`; caso contrário, inspecione `unsupported_reason` e `minimum_platform_version`. O campo `audio` informa o suporte a áudio. Diferentemente do Lua, **a gravação HTTP habilita áudio por padrão quando o backend oferece suporte**. O exemplo abaixo desabilita o áudio explicitamente.

### Iniciando e inspecionando a gravação {#start-and-inspect-the-recording}

Inicie com um objeto JSON opcional contendo `fps` e/ou `audio`. O serviço escolhe o arquivo de saída; não aceita caminho, largura, altura ou escala.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 significa que a requisição foi aceita. Execute novamente o comando de status abaixo até que `pending` seja `false` e `active` seja `true`. A verificação rejeita uma resposta para outra operação e informa falhas de captura ou de preparação do arquivo. Se uma parada automática já tiver finalizado a gravação, prossiga com a [finalização](#stop-and-wait-for-finalization) antes de baixar.

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

Deixe o jogo executar pelo período que deseja capturar e solicite a parada. Se a janela tiver sido redimensionada e a gravação já estiver concluída, pule a requisição de parada e prossiga com a finalização abaixo.

### Parando e aguardando a finalização {#stop-and-wait-for-finalization}

Pare a operação cujo ID você guardou da resposta de início:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 apenas aceita a solicitação de parada. Repita o comando de status até que `pending` seja `false`, `finalized` seja `true` e `file.state` seja `complete`. O serviço prepara o tamanho e o SHA-256 do arquivo após o término da captura nativa; portanto, `state: "complete"` e `finalized: true` sozinhos não significam que o download está pronto. Pare de aguardar se `state` ou `file.state` se tornar `failed`; não baixe um arquivo cujo estado seja `pending` ou `failed`.

Um cliente automatizado deve consultar com intervalo e limite de tempo, verificando o ID de operação guardado em cada resposta. Permita que a engine continue atualizando enquanto aguarda a captura e a finalização.

### Baixando e liberando o arquivo {#download-and-release-the-file}

Use a URL relativa do arquivo concluído na resposta de status. A verificação abaixo também garante que a resposta ainda pertence à sua operação:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Mantenha o recibo de status concluído em `capture.json` junto com o MP4. `/recording/status` descreve a operação atual; portanto, uma gravação posterior substitui a resposta de status mesmo enquanto arquivos HTTP anteriores permanecem disponíveis.

Verifique o tamanho em bytes e o SHA-256 do arquivo baixado antes de usá-lo ou excluir a cópia do serviço:

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

Um GET sem cabeçalho `Range` baixa o MP4 inteiro. O serviço também aceita intervalos fechados de bytes, como `Range: bytes=0-1023`, se um cliente precisar de downloads parciais. Verifique o arquivo remontado usando o mesmo recibo.

Após baixar e verificar o arquivo, você pode liberar a cópia mantida pelo serviço:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

Arquivos de gravação HTTP permanecem disponíveis até serem excluídos explicitamente ou a engine encerrar ou reiniciar. Baixe-os antes de fechar a engine. O serviço mantém no máximo 128 arquivos; exclua os arquivos concluídos que você já salvou para liberar espaço para novas gravações.

### Mantendo juntas as identidades das operações {#keeping-operation-identities-together}

Cada POST e DELETE exige `X-Recording-Instance`. Os exemplos também o enviam em requisições de status e download para rejeitar respostas de uma engine substituta. Mantenha `instance_id`, `operation_id` e as informações do arquivo juntos: a identidade do serviço muda ao reiniciar, e um novo processo pode reutilizar números de operação.

Uma identidade ausente retorna HTTP 400. Uma identidade desatualizada, uma operação de parada desatualizada ou um arquivo excluído retorna HTTP 410. Não obtenha uma nova identidade para reutilizá-la em uma nova tentativa de uma operação antiga. Em vez disso, descubra o novo serviço e inicie uma nova gravação.

### Tratando falhas HTTP {#handling-http-failures}

Requisições rejeitadas retornam JSON com `error.code` e `error.message`. Para solucionar problemas, execute a requisição `curl` individual com `-i` e sem `-f` para ver o status HTTP e o corpo do erro.

| Status HTTP | O que verificar |
| --- | --- |
| 409 | Outra gravação está ativa ou pendente, a gravação atual ainda não está pronta para parar ou o arquivo ainda está sendo preparado. Leia o status antes de tentar novamente. |
| 500 | A inicialização da gravação, a inicialização do armazenamento ou a preparação/leitura do arquivo falhou. Inspecione a mensagem de erro; uma captura com falha também informa `failure` no status. |
| 501 | O vídeo ou o áudio solicitado não é compatível. Inspecione as capacidades; use `audio: false` se apenas o áudio estiver indisponível. |
| 507 | O limite de arquivos mantidos pelo serviço foi atingido. Baixe e exclua arquivos concluídos antes de iniciar outra gravação. |
