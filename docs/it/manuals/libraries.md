---
title: Lavorare con i progetti libreria in Defold
brief: La funzionalità delle librerie consente di condividere asset tra progetti. Questo manuale ne spiega il funzionamento.
---

# Librerie {#libraries}

La funzionalità delle librerie consente di condividere asset tra progetti. È un meccanismo semplice ma molto potente che puoi usare nel tuo flusso di lavoro in diversi modi.

Le librerie sono utili per i seguenti scopi:

* Copiare asset da un progetto completato a uno nuovo. Se stai realizzando il seguito di un gioco precedente, è un modo semplice per iniziare.
* Creare una libreria di modelli da copiare nei tuoi progetti e poi personalizzare o adattare a esigenze specifiche.
* Creare una o più librerie di oggetti o script già pronti a cui puoi fare riferimento direttamente. È molto comodo per conservare moduli script di uso comune o creare una libreria condivisa di asset grafici, sonori e di animazione.

## Configurare la condivisione di una libreria {#setting-up-library-sharing}

Supponiamo che tu voglia creare una libreria contenente sprite e sorgenti di tile (tile source) condivisi. Inizia [configurando un nuovo progetto](/manuals/project-setup/). Decidi quali cartelle del progetto vuoi condividere e aggiungi i loro nomi alla proprietà *`include_dirs`* nelle impostazioni del progetto. Se vuoi elencare più cartelle, separa i nomi con spazi:

![Directory da includere](images/libraries/libraries_include_dirs.png)

Prima di poter aggiungere questa libreria a un altro progetto, serve un modo per individuarla.

## URL della libreria {#library-url}

Alle librerie si fa riferimento tramite un normale URL. Per un progetto ospitato su GitHub, si tratta dell'URL di una release del progetto:

![URL della libreria su GitHub](images/libraries/libraries_library_url_github.png)

::: important
È consigliabile usare sempre una release specifica di un progetto libreria come dipendenza, anziché il branch `master`. In questo modo puoi decidere, in qualità di sviluppatore, quando incorporare le modifiche di un progetto libreria, invece di ricevere sempre le ultime modifiche dal suo branch `master`, che potrebbero compromettere la compatibilità.
:::

::: important
È consigliabile esaminare sempre le librerie di terze parti prima di usarle. Per saperne di più, consulta [come rendere sicuro l'uso di software di terze parti](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Autenticazione di accesso di base {#basic-access-authentication}

Puoi aggiungere un nome utente e una password o un token all'URL della libreria per eseguire l'autenticazione di accesso di base quando usi librerie che non sono disponibili pubblicamente:

```
https://username:password@github.com/defold/private/archive/main.zip
```

I campi `username` e `password` vengono estratti e aggiunti come intestazione `Authorization` della richiesta. Questo metodo funziona con qualsiasi server che supporti l'autorizzazione di accesso di base.

::: important
Assicurati di non condividere o divulgare accidentalmente il token di accesso personale che hai generato o la tua password: se cadessero nelle mani sbagliate, le conseguenze potrebbero essere gravi!
:::

Per evitare di divulgare accidentalmente le credenziali lasciandole in chiaro nell'URL della libreria, puoi anche usare uno schema di sostituzione delle stringhe e conservare le credenziali in variabili d'ambiente:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

Nell'esempio precedente, il nome utente e il token vengono letti dalle variabili d'ambiente di sistema `PRIVATE_USERNAME` e `PRIVATE_TOKEN`.

#### Autenticazione con GitHub {#github-authentication}

Per recuperare una libreria da un repository privato su GitHub devi [generare un token di accesso personale](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) e usarlo come password.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Autenticazione con GitLab {#gitlab-authentication}

Per recuperare una libreria da un repository privato su GitLab devi [generare un token di accesso personale](https://docs.gitlab.com/ee/security/token_overview.html) e inviarlo come parametro dell'URL.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Autenticazione di accesso avanzata {#advanced-access-authentication}

Quando usi l'autenticazione di accesso di base, il token di accesso e il nome utente vengono condivisi in ogni repository usato per il progetto. In un team di più persone questo può essere un problema. Per risolverlo, occorre usare un utente con accesso in "sola lettura" per accedere al repository della libreria. Su GitHub sono necessari un'organizzazione, un team e un utente che non debba modificare il repository (quindi con accesso in sola lettura).

Passaggi su GitHub:
* [Crea un'organizzazione](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Crea un team all'interno dell'organizzazione](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Trasferisci il repository privato desiderato alla tua organizzazione](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Concedi al team l'accesso in "sola lettura" al repository](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Crea o seleziona un utente da aggiungere a questo team](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Usa l'"autenticazione di accesso di base" descritta sopra per creare un token di accesso personale per questo utente

A questo punto puoi includere i dati di autenticazione del nuovo utente in un commit ed eseguire il push al repository. In questo modo chiunque lavori con il tuo repository privato potrà recuperarlo come libreria senza avere i permessi per modificare la libreria stessa.

::: important
Il token dell'utente con accesso in sola lettura è completamente accessibile a chiunque possa accedere ai repository dei giochi che usano la libreria.
:::

Questa soluzione è stata proposta sul forum di Defold e [discussa in questo thread](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Configurare le dipendenze da librerie {#setting-up-library-dependencies}

Apri il progetto da cui vuoi accedere alla libreria. Nelle impostazioni del progetto, aggiungi l'URL della libreria alla proprietà *dependencies*. Se vuoi, puoi specificare più progetti come dipendenze. Aggiungili uno alla volta con il pulsante `+` e rimuovili con il pulsante `-`:

![Dipendenze](images/libraries/libraries_dependencies.png)

Ora seleziona <kbd>Project ▸ Fetch Libraries</kbd> per aggiornare le dipendenze da librerie. Questo avviene automaticamente ogni volta che apri un progetto, quindi devi farlo soltanto se le dipendenze cambiano senza che tu riapra il progetto. Succede quando aggiungi o rimuovi librerie dalle dipendenze, oppure quando qualcuno modifica e sincronizza uno dei progetti libreria da cui dipendi.

![Recupero delle librerie](images/libraries/libraries_fetch_libraries.png)

Ora le cartelle che hai condiviso compaiono nel *pannello Assets* e puoi usare tutto ciò che hai condiviso. Qualsiasi modifica sincronizzata del progetto libreria sarà disponibile nel tuo progetto.

![Configurazione della libreria completata](images/libraries/libraries_done.png)

## Modificare i file nelle librerie usate come dipendenze {#editing-files-in-library-dependencies}

I file delle librerie non possono essere salvati. Puoi modificarli e l'editor potrà creare una build con le modifiche, il che è utile per i test. Il file stesso, però, rimane invariato e tutte le modifiche vengono scartate quando lo chiudi.

Se vuoi modificare i file di una libreria, assicurati di creare un tuo fork della libreria e di apportare lì le modifiche. Un'altra possibilità è copiare e incollare l'intera cartella della libreria nella directory del progetto e usare la copia locale. In questo caso la cartella locale avrà la precedenza sulla dipendenza originale e dovrai rimuovere il link della dipendenza da `game.project` (ricorda di selezionare <kbd>Project ▸ Fetch Libraries</kbd> in seguito).

Anche `builtins` è una libreria fornita dal motore. Se vuoi modificare i suoi file, assicurati di copiarli nel tuo progetto e di usare le copie al posto dei file originali di `builtins`. Per esempio, per modificare `default.render_script`, copia sia `/builtins/render/default.render` sia `/builtins/render/default.render_script` nella cartella del progetto con i nomi `my_custom.render` e `my_custom.render_script`. Poi aggiorna il file locale `my_custom.render` affinché faccia riferimento a `my_custom.render_script` anziché a quello integrato, e imposta il tuo `my_custom.render` personalizzato nell'impostazione Render di `game.project`.

Se copi e incolli un materiale e vuoi usarlo in tutti i componenti di un certo tipo, può essere utile usare [modelli specifici del progetto](/manuals/editor/#creating-new-project-files).

## Riferimenti non validi {#broken-references}

La condivisione di una libreria include soltanto i file che si trovano nelle cartelle condivise. Se crei qualcosa che fa riferimento ad asset situati al di fuori della gerarchia condivisa, i percorsi dei riferimenti non saranno validi.

## Conflitti di nomi {#name-collisions}

Poiché puoi elencare gli URL di più progetti nell'impostazione *dependencies* del progetto, potresti incontrare un conflitto di nomi. Questo avviene se due o più progetti da cui dipendi condividono una cartella con lo stesso nome nell'impostazione *`include_dirs`* del progetto.

Defold risolve i conflitti di nomi ignorando tutti i riferimenti alle cartelle con lo stesso nome tranne l'ultimo, nell'ordine in cui gli URL dei progetti sono specificati nell'elenco *dependencies*. Per esempio, se elenchi gli URL di 3 progetti libreria nelle dipendenze e tutti condividono una cartella chiamata *items*, comparirà una sola cartella *items*---quella del progetto che si trova per ultimo nell'elenco degli URL.
