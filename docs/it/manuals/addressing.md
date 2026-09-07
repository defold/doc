---
title: Indirizzamento in Defold
brief: Questo manuale spiega come Defold ha risolto il problema dell'indirizzamento.
---

# Indirizzamento {#addressing}

Il codice che controlla un gioco in esecuzione deve poter raggiungere ogni oggetto e componente per spostare, ridimensionare, animare, eliminare e manipolare ciò che il giocatore vede e sente. Il meccanismo di indirizzamento di Defold lo rende possibile.

## Identificatori {#identifiers}

Defold usa indirizzi (o URL, ma per ora lasciamoli da parte) per fare riferimento a oggetti di gioco (game object) e componenti. Questi indirizzi sono composti da identificatori. Quelli che seguono sono tutti esempi di come Defold usa gli indirizzi. In questo manuale esamineremo nel dettaglio come funzionano:

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Cominciamo con un esempio molto semplice. Supponi di avere un oggetto di gioco con un solo componente sprite. Hai anche un componente script per controllare l'oggetto di gioco. Nell'editor, la configurazione sarebbe simile a questa:

![bean nell'editor](images/addressing/bean_editor.png)

Ora vuoi disabilitare lo sprite all'avvio del gioco, così da poterlo far apparire in seguito. Per farlo basta inserire il codice seguente in "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Non preoccuparti se il carattere '#' ti lascia perplesso. Ci arriveremo tra poco.

Il codice funzionerà come previsto. All'avvio del gioco, il componente script *indirizza* il componente sprite tramite il suo identificatore "body" e usa quell'indirizzo per inviargli un *messaggio* "disable". L'effetto di questo messaggio speciale del motore è che il componente sprite nasconde la grafica dello sprite. Schematicamente, la configurazione è questa:

![Personaggio bean](images/addressing/bean.png)

Gli identificatori nella configurazione sono definiti dallo sviluppatore e devono essere univoci all'interno del loro contesto di denominazione. Qui abbiamo scelto di assegnare all'oggetto di gioco l'identificatore "bean", al suo componente sprite il nome "body" e al componente script che controlla il personaggio il nome "controller". Gli identificatori usati negli indirizzi URL espressi come stringhe non devono contenere `:` o `#`, perché la sintassi degli URL riserva `:` come separatore del socket e `#` come separatore tra oggetto di gioco e componente. Per il resto, il parser degli URL non rifiuta i segni di punteggiatura.

::: sidenote
Se non scegli un nome, lo farà l'editor. Ogni volta che crei un nuovo oggetto di gioco o componente nell'editor, viene impostata automaticamente una proprietà *Id* univoca.

- Agli oggetti di gioco viene assegnato automaticamente un ID "go" con un numero progressivo ("go2", "go3" ecc.).
- Ai componenti viene assegnato un ID corrispondente al tipo di componente ("sprite", "sprite2" ecc.).

Se vuoi, puoi mantenere questi nomi assegnati automaticamente, ma ti consigliamo di sostituire gli identificatori con nomi chiari e descrittivi.
:::

Ora aggiungiamo un altro componente sprite e diamo uno scudo al fagiolo:

![Personaggio bean](images/addressing/bean_shield_editor.png)

Il nuovo componente deve essere identificato in modo univoco all'interno dell'oggetto di gioco. Se gli assegnassi il nome "body", il codice dello script non potrebbe distinguere a quale sprite inviare il messaggio "disable". Scegliamo quindi l'identificatore univoco (e descrittivo) "shield". Ora possiamo abilitare e disabilitare a piacere gli sprite "body" e "shield".

![Personaggio bean](images/addressing/bean_shield.png)

::: sidenote
Se provi a usare lo stesso identificatore più di una volta, l'editor segnala un errore, quindi nella pratica questo non è mai un problema:

![Personaggio bean](images/addressing/name_collision.png)
:::

Ora vediamo cosa succede se aggiungi altri oggetti di gioco. Supponi di voler abbinare due "fagioli" per formare una piccola squadra. Decidi di chiamare uno degli oggetti di gioco "bean" e l'altro "buddy". Inoltre, quando "bean" è rimasto inattivo per un po', deve dire a "buddy" di iniziare a ballare. Per farlo, si invia un messaggio personalizzato chiamato "dance" dal componente script "controller" di "bean" allo script "controller" di "buddy":

![Personaggio bean](images/addressing/bean_buddy.png)

::: sidenote
Ci sono due componenti distinti chiamati "controller", uno in ciascun oggetto di gioco, ma questo è perfettamente valido perché ogni oggetto di gioco crea un nuovo contesto di denominazione.
:::

Poiché il destinatario del messaggio si trova all'esterno dell'oggetto di gioco che lo invia ("bean"), il codice deve specificare quale "controller" deve riceverlo. Deve indicare sia l'ID dell'oggetto di gioco di destinazione sia l'ID del componente. L'indirizzo completo del componente diventa `"buddy#controller"` ed è composto da due parti distinte.

- Prima viene l'identificatore dell'oggetto di gioco di destinazione ("buddy"),
- poi il carattere separatore tra oggetto di gioco e componente ("#"),
- infine l'identificatore del componente di destinazione ("controller").

Tornando all'esempio precedente con un solo oggetto di gioco, vediamo che, omettendo l'identificatore dell'oggetto di gioco dall'indirizzo di destinazione, il codice può indirizzare i componenti dell'*oggetto di gioco corrente*.

Per esempio, `"#body"` indica l'indirizzo del componente "body" nell'oggetto di gioco corrente. È molto utile perché questo codice funziona in *qualsiasi* oggetto di gioco, purché sia presente un componente "body".

## Collezioni {#collections}

Le collezioni (collection) permettono di creare gruppi, o gerarchie, di oggetti di gioco e di riutilizzarli in modo controllato. Nell'editor usi i file di collezione come modelli (o "prototipi" o "prefab") quando aggiungi contenuti al gioco.

Supponi di voler creare molte squadre formate da bean e buddy. Un buon modo per farlo è creare un modello in un nuovo *file di collezione* (chiamalo "team.collection"). Crea gli oggetti di gioco della squadra nel file di collezione e salvalo. Poi inserisci un'istanza del contenuto di quel file nella collezione di bootstrap principale e assegna un identificatore all'istanza (chiamala "team_1"):

![Personaggio bean](images/addressing/team_editor.png)

Con questa struttura, l'oggetto di gioco "bean" può ancora fare riferimento al componente "controller" di "buddy" tramite l'indirizzo `"buddy#controller"`.

![Personaggio bean](images/addressing/collection_team.png)

Se aggiungi una seconda istanza di "team.collection" (chiamala "team_2"), il codice in esecuzione nei componenti script di "team_2" funzionerà altrettanto bene. L'istanza dell'oggetto di gioco "bean" nella collezione "team_2" può ancora indirizzare il componente "controller" di "buddy" tramite l'indirizzo `"buddy#controller"`.

![Personaggio bean](images/addressing/teams_editor.png)

## Indirizzamento relativo {#relative-addressing}

L'indirizzo `"buddy#controller"` funziona per gli oggetti di gioco di entrambe le collezioni perché è un indirizzo *relativo*. Ciascuna delle collezioni "team_1" e "team_2" crea un nuovo contesto di denominazione, o "spazio dei nomi". Defold evita i conflitti tra nomi tenendo conto del contesto di denominazione creato da una collezione quando risolve gli indirizzi:

![ID relativo](images/addressing/relative_same.png)

- Nel contesto di denominazione "team_1", gli oggetti di gioco "bean" e "buddy" sono identificati in modo univoco.
- Analogamente, anche nel contesto di denominazione "team_2" gli oggetti di gioco "bean" e "buddy" sono identificati in modo univoco.

L'indirizzamento relativo funziona anteponendo automaticamente il contesto di denominazione corrente quando risolve un indirizzo di destinazione. Anche questo è estremamente utile e potente, perché puoi creare gruppi di oggetti di gioco con il relativo codice e riutilizzarli in modo efficiente in tutto il gioco.

### Forme abbreviate {#shorthands}

Defold offre due comode forme abbreviate che puoi usare per inviare messaggi senza specificare un URL completo:

:[Shorthands](../shared/url-shorthands.md)

## Percorsi degli oggetti di gioco {#game-object-paths}

Per comprendere correttamente il meccanismo di denominazione, vediamo cosa succede quando crei una build del progetto e lo esegui:

1. L'editor legge la collezione di bootstrap ("main.collection") e tutto il suo contenuto (oggetti di gioco e altre collezioni).
2. Per ogni oggetto di gioco statico, il compilatore crea un identificatore. Questi identificatori vengono costruiti come "percorsi" che partono dalla radice della collezione di bootstrap e scendono lungo la gerarchia delle collezioni fino all'oggetto. A ogni livello viene aggiunto un carattere '/'.

Nel nostro esempio, il gioco verrà eseguito con i seguenti 4 oggetti di gioco:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Gli identificatori vengono memorizzati come valori hash. Il runtime memorizza anche lo stato dell'hash per l'identificatore di ogni collezione, che viene usato per proseguire il calcolo dell'hash di una stringa relativa e ottenere un ID assoluto.
:::

Durante l'esecuzione, il raggruppamento in collezioni non esiste. Non è possibile risalire alla collezione a cui apparteneva un determinato oggetto di gioco prima della compilazione. Non è nemmeno possibile manipolare contemporaneamente tutti gli oggetti di una collezione. Se hai bisogno di queste operazioni, puoi facilmente tenere traccia degli oggetti nel tuo codice. L'identificatore di ciascun oggetto è statico: è garantito che rimanga invariato per tutta la vita dell'oggetto. Questo significa che puoi memorizzare l'identificatore di un oggetto e usarlo in seguito senza problemi.

## Indirizzamento assoluto {#absolute-addressing}

Per l'indirizzamento è possibile usare gli identificatori completi descritti sopra. Nella maggior parte dei casi è preferibile l'indirizzamento relativo, perché consente di riutilizzare i contenuti, ma in alcuni casi diventa necessario l'indirizzamento assoluto.

Per esempio, supponi di volere un gestore dell'IA che tenga traccia dello stato di ogni oggetto fagiolo. Vuoi che i fagioli comunichino il loro stato di attività al gestore e che quest'ultimo prenda decisioni tattiche e impartisca ordini in base al loro stato. In questo caso avrebbe perfettamente senso creare un unico oggetto di gioco gestore con un componente script e inserirlo nella collezione di bootstrap, accanto alle collezioni delle squadre.

![Oggetto gestore](images/addressing/manager_editor.png)

Ogni fagiolo ha quindi il compito di inviare messaggi di stato al gestore: "contact" se avvista un nemico oppure "ouch!" se viene colpito e subisce danni. Per farlo, lo script di controllo del fagiolo usa l'indirizzamento assoluto per inviare messaggi al componente "controller" di "manager".

Qualsiasi indirizzo che inizia con '/' viene risolto a partire dalla radice del mondo di gioco. Questa corrisponde alla radice della *collezione di bootstrap* caricata all'avvio del gioco.

L'indirizzo assoluto dello script del gestore è `"/manager#controller"` e questo indirizzo viene risolto nel componente corretto, indipendentemente da dove venga usato.

![Squadre e gestore](images/addressing/teams_manager.png)

![Indirizzamento assoluto](images/addressing/absolute.png)

## Identificatori hash {#hashed-identifiers}

Il motore memorizza tutti gli identificatori come valori hash. Tutte le funzioni che ricevono come argomento un componente o un oggetto di gioco accettano una stringa, un hash o un oggetto URL. Sopra abbiamo visto come usare le stringhe per l'indirizzamento.

Quando ottieni l'identificatore di un oggetto di gioco, il motore restituisce sempre l'hash di un identificatore con percorso assoluto:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Puoi usare un identificatore di questo tipo al posto di un ID stringa oppure costruirne uno tu stesso. Ricorda però che un ID hash corrisponde al percorso dell'oggetto, cioè a un indirizzo assoluto:

::: sidenote
Gli indirizzi relativi devono essere forniti come stringhe perché il motore calcola un nuovo ID hash a partire dallo stato dell'hash del contesto di denominazione corrente (collezione), aggiungendo la stringa fornita al calcolo dell'hash.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL {#urls}

Per completare il quadro, esaminiamo il formato completo degli indirizzi di Defold: l'URL.

Un URL è un oggetto, di solito scritto come una stringa con un formato particolare. Un URL generico è composto da tre parti:

`[socket:][path][#fragment]`

socket
: Identifica il mondo di gioco della destinazione. È importante quando lavori con i [proxy di collezione](/manuals/collection-proxy) e in quel caso viene usato per identificare la _collezione caricata dinamicamente_.

path
: Questa parte dell'URL contiene l'ID completo dell'oggetto di gioco di destinazione.

fragment
: L'identificatore del componente di destinazione all'interno dell'oggetto di gioco specificato.

Come abbiamo visto sopra, nella maggior parte dei casi puoi omettere alcune di queste informazioni, o anche la maggior parte. Quasi mai è necessario specificare il socket, mentre spesso, ma non sempre, devi specificare il percorso. Quando devi indirizzare elementi in un altro mondo di gioco, devi specificare la parte socket dell'URL. Per esempio, la stringa URL completa dello script "controller" nell'oggetto di gioco "manager" visto sopra è:

`"main:/manager#controller"`

e quella del controller di buddy in team_2 è:

`"main:/team_2/buddy#controller"`

Possiamo inviare loro dei messaggi:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Costruire oggetti URL {#constructing-url-objects}

Gli oggetti URL possono anche essere costruiti in modo programmatico nel codice Lua:

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
