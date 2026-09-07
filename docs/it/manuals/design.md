---
title: La progettazione di Defold
brief: La filosofia alla base della progettazione di Defold
---

# La progettazione di Defold {#the-design-of-defold}

Defold è stato creato con i seguenti obiettivi:

- Essere una piattaforma di produzione completa, professionale e pronta all'uso per i team di sviluppo di giochi.
- Essere semplice e chiaro, offrendo soluzioni esplicite ai problemi comuni di architettura e flusso di lavoro nello sviluppo di giochi.
- Essere una piattaforma di sviluppo estremamente veloce, ideale per lo sviluppo iterativo di giochi.
- Offrire prestazioni elevate durante l'esecuzione.
- Essere davvero multipiattaforma.

L'editor e il motore sono progettati con cura per raggiungere questi obiettivi. Se hai esperienza con altre piattaforme, alcune delle nostre scelte di progettazione potrebbero differire da ciò a cui sei abituato, per esempio:

- Richiediamo che l'albero delle risorse e tutti i nomi siano dichiarati staticamente. Questo richiede un certo impegno iniziale da parte tua, ma agevola enormemente il processo di sviluppo nel lungo periodo.
- Incoraggiamo lo scambio di messaggi tra entità semplici e incapsulate.
- Non è prevista l'ereditarietà della programmazione orientata agli oggetti.
- Le nostre API sono asincrone.
- La pipeline di rendering è controllata dal codice ed è completamente personalizzabile.
- Tutti i nostri file di risorse usano semplici formati di testo, strutturati in modo ottimale per le operazioni di merge con Git, oltre che per l'importazione e l'elaborazione con strumenti esterni.
- Le risorse possono essere modificate e ricaricate a caldo in un gioco in esecuzione, consentendo iterazioni e sperimentazioni estremamente rapide.
