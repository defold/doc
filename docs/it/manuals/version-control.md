---
title: Controllo di versione
brief: Questo manuale spiega come usare Git con i progetti Defold ed esaminare le modifiche locali nell'editor.
---

# Controllo di versione {#version-control}

I progetti Defold funzionano bene con [Git](https://git-scm.com), ma la sincronizzazione viene gestita al di fuori dell'editor. Usa il client Git che preferisci o la riga di comando per clonare repository, eseguire fetch, pull, commit e push, creare rami e risolvere conflitti.

## File modificati {#changed-files}

Quando la directory del progetto è la radice di un worktree Git con almeno un commit, Defold elenca nel pannello *Changed Files* dell'editor i file non ignorati rilevati come aggiunti, modificati, eliminati o rinominati. Queste voci vengono ricavate confrontando i file su disco direttamente con il commit corrente (`HEAD`), quindi aggiungere una modifica all'indice non cambia l'elenco. Risolvi i conflitti di fusione in un client Git esterno.

![file modificati](images/workflow/changed_files.png)

Seleziona un solo file modificato o rinominato e fai clic su <kbd>Diff</kbd> per visualizzarne le differenze testuali. Fai clic su <kbd>Revert</kbd> per scartare le modifiche selezionate nel worktree e nell'indice. I file tracciati vengono ripristinati a `HEAD`; i file assenti da `HEAD` vengono eliminati, indipendentemente dal fatto che siano stati aggiunti all'indice come nuovi file; per i file rinominati, il nuovo percorso viene eliminato e quello precedente viene ripristinato. Questa operazione non può essere annullata nell'editor, quindi esegui un commit o una copia di backup del lavoro che potrebbe servirti.

## Git

Git archivia in modo efficiente i file di progetto testuali di Defold. Gli asset binari di grandi dimensioni che cambiano di frequente, come i file PSD o quelli di produzione audio, possono comunque far crescere rapidamente la cronologia del repository. Valuta Git LFS o una soluzione separata di archiviazione e backup per i file di lavoro di grandi dimensioni.

Il pannello *Changed Files* offre soltanto operazioni locali per visualizzare lo stato e le differenze e annullare le modifiche. Non rileva se i commit sono stati inviati a un repository remoto e non esegue fetch, pull, commit o push delle modifiche. Esegui queste operazioni in un client Git esterno o dalla riga di comando. Per impostazione predefinita, Defold ricarica le modifiche esterne e aggiorna il pannello quando riacquista il focus. Se *Load External Changes on App Focus* è disabilitata, scegli *File ▸ Load External Changes*.
