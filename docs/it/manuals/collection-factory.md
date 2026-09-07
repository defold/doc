---
title: Manuale delle fabbriche di collezioni
brief: Questo manuale spiega come usare i componenti fabbrica di collezioni per generare gerarchie di oggetti di gioco.
---

# Fabbriche di collezioni {#collection-factories}

Il componente fabbrica di collezioni (collection factory) permette di generare in un gioco in esecuzione gruppi e gerarchie di oggetti di gioco salvati in file di collezione.

Le collezioni offrono un potente meccanismo per creare modelli riutilizzabili, o "prefab", in Defold. Per una panoramica delle collezioni, consulta la [documentazione sugli elementi costitutivi](/manuals/building-blocks#collections). Le collezioni possono essere posizionate nell'editor oppure inserite dinamicamente nel gioco.

Con un componente fabbrica di collezioni puoi generare il contenuto di un file di collezione in un mondo di gioco. È un'operazione analoga alla generazione tramite fabbrica (factory) di tutti gli oggetti di gioco all'interno della collezione, seguita dalla costruzione della gerarchia genitore-figlio tra gli oggetti. Un caso d'uso tipico è la generazione di nemici composti da più oggetti di gioco (per esempio, nemico + arma).

## Generare una collezione {#spawning-a-collection}

Supponi di voler creare un oggetto di gioco per un personaggio e un oggetto di gioco separato per uno scudo, figlio del personaggio. Crea la gerarchia degli oggetti di gioco in un file di collezione e salvalo come `bean.collection`.

::: sidenote
Il componente *proxy di collezione* viene usato per creare un nuovo mondo di gioco, con un mondo fisico separato, a partire da una collezione. Al nuovo mondo si accede tramite un nuovo socket. Tutti gli asset contenuti nella collezione vengono caricati tramite il proxy quando gli invii un messaggio per avviare il caricamento. Questo rende i proxy molto utili, per esempio, per cambiare livello in un gioco. I nuovi mondi di gioco comportano però un costo aggiuntivo piuttosto elevato, quindi non usarli per caricare dinamicamente piccoli elementi. Per ulteriori informazioni, consulta la [documentazione sui proxy di collezione](/manuals/collection-proxy).
:::

![Collezione da generare](images/collection_factory/collection.png)

Aggiungi quindi un componente *Collection factory* a un oggetto di gioco che si occuperà della generazione e imposta `bean.collection` come *Prototype* del componente:

![Fabbrica di collezioni](images/collection_factory/factory.png)

Per generare `bean` e lo scudo, ora basta chiamare la funzione `collectionfactory.create()`:

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

La funzione accetta 5 parametri:

`url`
: L'ID del componente fabbrica di collezioni che deve generare il nuovo insieme di oggetti di gioco.

`[position]`
: (facoltativo) La posizione nel mondo degli oggetti di gioco generati. Deve essere un `vector3`. Se non specifichi una posizione, gli oggetti vengono generati nella posizione del componente fabbrica di collezioni.

`[rotation]`
: (facoltativo) La rotazione nel mondo dei nuovi oggetti di gioco. Deve essere un `quat`.

`[properties]`
: (facoltativo) Una tabella Lua con coppie `id`-`table` usate per inizializzare gli oggetti di gioco generati. Più avanti viene spiegato come costruire questa tabella.

`[scale]`
: (facoltativo) La scala degli oggetti di gioco generati. La scala può essere espressa come un `number` (maggiore di 0), che specifica una scala uniforme lungo tutti gli assi. Puoi anche fornire un `vector3` in cui ogni componente specifica la scala lungo l'asse corrispondente.

`collectionfactory.create()` restituisce gli identificatori degli oggetti di gioco generati sotto forma di tabella. Le chiavi della tabella associano l'hash dell'ID locale alla collezione di ciascun oggetto al relativo ID a runtime:

::: sidenote
La relazione genitore-figlio tra `bean` e `shield` *non* si riflette nella tabella restituita. Questa relazione esiste soltanto nel grafo della scena a runtime, ovvero determina come gli oggetti vengono trasformati insieme. Cambiare il genitore di un oggetto non ne modifica mai l'ID.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. All'ID viene aggiunto un prefisso `/collection[N]/`, dove `[N]` è un contatore, per identificare in modo univoco ogni istanza:

## Proprietà {#properties}

Quando generi una collezione, puoi passare i parametri delle proprietà a ogni oggetto di gioco costruendo una tabella in cui le chiavi sono gli ID degli oggetti e i valori sono tabelle con le proprietà dello script da impostare.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

Questo presuppone che l'oggetto di gioco `bean` in `bean.collection` definisca la proprietà `shield`. [Il manuale delle proprietà degli script](/manuals/script-properties) contiene informazioni sulle proprietà degli script.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## Caricamento dinamico delle risorse della fabbrica {#dynamic-loading-of-factory-resources}

Selezionando la casella *Load Dynamically* nelle proprietà della fabbrica di collezioni, il motore rimanda il caricamento delle risorse associate alla fabbrica.

![Caricamento dinamico](images/collection_factory/load_dynamically.png)

Se la casella non è selezionata, il motore carica le risorse del prototipo quando viene caricato il componente fabbrica di collezioni, rendendole subito disponibili per la generazione.

Se la casella è selezionata, hai due possibilità:

Caricamento sincrono
: Chiama [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) quando vuoi generare gli oggetti. Le risorse verranno caricate in modo sincrono, il che potrebbe causare una breve interruzione, poi verranno generate le nuove istanze.

  ```lua
  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling create without
      -- having called load will create the resources synchronously.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the collection
      -- factory component holds no reference.
      go.delete(self.go_ids)

      -- Calling unload will do nothing since factory holds
      -- no references
      collectionfactory.unload("#factory")
  end
  ```

Caricamento asincrono
: Chiama [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) per caricare esplicitamente le risorse in modo asincrono. Quando le risorse sono pronte per la generazione, viene chiamata una callback.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling load will load the resources.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the collection factory
      -- component still holds a reference.
      go.delete(self.go_ids)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      collectionfactory.unload("#factory")
  end
  ```


## Prototipo dinamico {#dynamic-prototype}

Puoi cambiare il *Prototype* che una fabbrica di collezioni può creare selezionando la casella *Dynamic Prototype* nelle proprietà della fabbrica di collezioni.

![Prototipo dinamico](images/collection_factory/dynamic_prototype.png)

Quando l'opzione *Dynamic Prototype* è selezionata, il componente fabbrica di collezioni può cambiare prototipo tramite la funzione `collectionfactory.set_prototype()`. Esempio:

```lua
collectionfactory.unload("#factory") -- unload the previous resources
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
Quando l'opzione *Dynamic Prototype* è attiva, il numero di componenti della collezione non può essere ottimizzato e la collezione che contiene il componente userà i conteggi predefiniti dei componenti del file *game.project*.
:::
