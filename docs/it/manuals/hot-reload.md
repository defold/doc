---
title: Hot reload
brief: Questo manuale spiega la funzionalità di hot reload di Defold.
---

# Hot reload delle risorse {#hot-reloading-resources}

Defold consente di eseguire l'hot reload delle risorse. Durante lo sviluppo di un gioco, questa funzionalità permette di velocizzare enormemente alcune attività. Puoi modificare il codice e i contenuti di un gioco mentre è in esecuzione. Alcuni casi d'uso comuni sono:

- Regolare i parametri del gameplay negli script Lua.
- Modificare e perfezionare gli elementi grafici (come gli effetti particellari o gli elementi GUI) e visualizzare i risultati nel contesto appropriato.
- Modificare e perfezionare il codice degli shader e visualizzare i risultati nel contesto appropriato.
- Facilitare i test del gioco riavviando i livelli, impostando lo stato e così via---senza interrompere il gioco.

## Come eseguire l'hot reload {#how-to-hot-reload}

Avvia il gioco dall'editor (<kbd>Project ▸ Build</kbd>).

Per ricaricare una risorsa aggiornata, seleziona la voce di menu <kbd>File ▸ Hot Reload</kbd> oppure premi la combinazione di tasti corrispondente:

![Ricaricamento delle risorse](images/hot-reload/menu.png)

## Hot reload su dispositivo {#hot-reloading-on-device}

L'hot reload funziona sia sui dispositivi mobili sia su desktop. Per usarlo su un dispositivo mobile, esegui una build di debug del gioco o l'[app di sviluppo](/manuals/dev-app) sul dispositivo, quindi selezionalo come destinazione nell'editor:

![Dispositivo di destinazione](images/hot-reload/target.png)

Ora, quando crei la build ed esegui il gioco, l'editor carica tutti gli asset nell'app in esecuzione sul dispositivo e avvia il gioco. Da quel momento, ogni file di cui esegui l'hot reload viene aggiornato sul dispositivo.

Per esempio, per aggiungere un paio di pulsanti a una GUI visualizzata in un gioco in esecuzione sul telefono, basta aprire il file GUI:

![Ricaricamento della GUI](images/hot-reload/gui.png)

Aggiungi i nuovi pulsanti, salva ed esegui l'hot reload del file GUI. Ora puoi vedere i nuovi pulsanti sullo schermo del telefono:

![GUI ricaricata](images/hot-reload/gui-reloaded.png)

Quando esegui l'hot reload di un file, il motore stampa nella console il nome di ogni file di risorsa ricaricato.

## Ricaricamento degli script {#reloading-scripts}

Ogni file di script Lua ricaricato viene eseguito nuovamente nell'ambiente Lua in esecuzione.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

Impostare `my_value` a 11 ed eseguire l'hot reload del file ha un effetto immediato:

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

Tieni presente che l'hot reload non modifica l'esecuzione delle funzioni del ciclo di vita. Per esempio, durante l'hot reload non viene chiamata `init()`. Se però ridefinisci le funzioni del ciclo di vita, vengono utilizzate le nuove versioni.

## Ricaricamento dei moduli Lua {#reloading-lua-modules}

Se aggiungi variabili all'ambito globale in un file di modulo, ricaricare il file modifica queste variabili globali:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- hot reload "my_module.lua" and the new value will print
end
```

Un modello comune per i moduli Lua consiste nel creare una tabella locale, popolarla e poi restituirla:

```lua
--- my_module.lua
local M = {} -- a new table object is created here
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- will print 10 even if you change and hot reload "my_module.lua"
end
```

Modificare e ricaricare `my_module.lua` _non_ cambia il comportamento di `user.script`. Consulta [il manuale sui moduli](/manuals/modules) per scoprire il motivo e come evitare questo problema.

## La funzione on_reload() {#the-on_reload-function}

Ogni componente script può definire una funzione `on_reload()`. Se presente, viene chiamata ogni volta che lo script viene ricaricato. È utile per ispezionare o modificare dati, inviare messaggi e così via:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## Ricaricamento del codice degli shader {#reloading-shader-code}

Quando ricarichi vertex shader e fragment shader, il driver grafico ricompila il codice GLSL e lo carica sulla GPU. Se il codice dello shader provoca un crash, cosa che può accadere facilmente dato che GLSL è scritto a un livello molto basso, anche il motore va in crash.
