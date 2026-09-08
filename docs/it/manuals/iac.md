---
title: Comunicazione tra applicazioni in Defold
brief: La comunicazione tra applicazioni consente di recuperare gli argomenti passati all'avvio dell'applicazione. Questo manuale spiega l'API di Defold disponibile per questa funzionalità.
---

# Comunicazione tra applicazioni {#inter-app-communication}

Nella maggior parte dei sistemi operativi, le applicazioni possono essere avviate in diversi modi:

* Dall'elenco delle applicazioni installate
* Da un collegamento specifico per l'applicazione
* Da una notifica push
* Come ultimo passaggio di un processo di installazione.

Quando l'applicazione viene avviata da un collegamento, da una notifica o al momento dell'installazione, è possibile passare argomenti aggiuntivi, come un riferimento all'origine dell'installazione (install referrer) durante l'installazione oppure un collegamento diretto (deep link) quando viene avviata da un collegamento specifico per l'applicazione o da una notifica. Defold offre un modo uniforme per ottenere informazioni su come è stata avviata l'applicazione tramite un'estensione nativa.

## Installare l'estensione {#installing-the-extension}

Per iniziare a usare l'estensione per la comunicazione tra applicazioni, devi aggiungerla come dipendenza al file *game.project*. L'ultima versione stabile è disponibile tramite questo URL di dipendenza:
```
https://github.com/defold/extension-iac/archive/master.zip
```

Consigliamo di usare un collegamento al file zip di una [release specifica](https://github.com/defold/extension-iac/releases).

## Usare l'estensione {#using-the-extension}

L'API è molto semplice da usare. Fornisci all'estensione una funzione di ascolto e gestisci le sue callback.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- This was an invocation
         print(payload.origin) -- origin may be empty string if it could not be resolved
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

La documentazione completa dell'API è disponibile sulla [pagina GitHub dell'estensione](https://defold.github.io/extension-iac/).
