---
title: Gruppi di collisione in Defold
brief: Il motore fisico ti permette di raggruppare gli oggetti fisici e filtrare le collisioni tra di essi.
---

# Gruppo e maschera {#group-and-mask}

Il motore fisico ti permette di raggruppare gli oggetti fisici e filtrare le collisioni tra di essi. Ciò avviene mediante _gruppi di collisione_ identificati da un nome. Per ogni oggetto di collisione che crei, due proprietà controllano come l'oggetto collide con gli altri oggetti: *Group* e *Mask*.

Perché una collisione tra due oggetti venga rilevata, entrambi gli oggetti devono specificare nel proprio campo *Mask* i gruppi a cui appartiene l'altro.

![Gruppo di collisione fisica](images/physics/collision_group.png)

Il campo *Mask* può contenere più nomi di gruppi, consentendo scenari di interazione complessi.

## Rilevamento delle collisioni {#detecting-collisions}
Quando due oggetti di collisione con gruppi e maschere compatibili entrano in collisione, il motore fisico genera [messaggi di collisione](/manuals/physics-messages) che puoi usare nei giochi per reagire alle collisioni.
