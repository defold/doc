---
title: Communication entre applications dans Defold
brief: La communication entre applications vous permet de récupérer les arguments de lancement utilisés au démarrage de votre application. Ce manuel explique l'API de Defold disponible pour cette fonctionnalité.
---

# Communication entre applications {#inter-app-communication}

Sur la plupart des systèmes d'exploitation, les applications peuvent être lancées de plusieurs façons :

* Depuis la liste des applications installées
* Depuis un lien propre à une application
* Depuis une notification push
* Comme dernière étape d'un processus d'installation.

Lorsque l'application est lancée depuis un lien, une notification ou lors de son installation, il est possible de transmettre des arguments supplémentaires, tels qu'un référent d'installation (install referrer) lors de l'installation ou un lien profond lors du lancement depuis un lien propre à l'application ou une notification. Defold propose une méthode unifiée pour obtenir des informations sur la façon dont l'application a été lancée, au moyen d'une extension native.

## Installation de l'extension {#installing-the-extension}

Pour commencer à utiliser l'extension Inter-app communication, vous devez l'ajouter comme dépendance à votre fichier *game.project*. La dernière version stable est disponible à l'URL de dépendance suivante :
```
https://github.com/defold/extension-iac/archive/master.zip
```

Nous vous recommandons d'utiliser un lien vers le fichier zip d'une [version précise](https://github.com/defold/extension-iac/releases).

## Utilisation de l'extension {#using-the-extension}

L'API est très simple à utiliser. Vous fournissez à l'extension une fonction d'écoute et réagissez aux appels de cette fonction.

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

La documentation complète de l'API est disponible sur la [page GitHub de l'extension](https://defold.github.io/extension-iac/).
