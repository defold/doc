---
title: Comment obtenir de l'aide
brief: Ce manuel explique comment obtenir de l'aide si vous rencontrez un problème en utilisant Defold.
---

# Obtenir de l'aide {#getting-help}

Si vous rencontrez un problème en utilisant Defold, faites-le-nous savoir pour que nous puissions le corriger et/ou vous aider à le contourner ! Il existe plusieurs façons de discuter des problèmes et de les signaler. Choisissez l'option qui vous convient le mieux :

## Signaler un problème sur le forum {#report-a-problem-on-the-forum}

Pour discuter d'un problème et obtenir de l'aide, vous pouvez poser une question sur notre [forum](https://forum.defold.com). Publiez-la dans la catégorie [Questions](https://forum.defold.com/c/questions) ou [Bugs](https://forum.defold.com/c/bugs), selon le type de problème que vous rencontrez. Pensez à [rechercher](https://forum.defold.com/search) votre question ou votre problème avant de poser votre question, car une solution existe peut-être déjà.

Si vous avez plusieurs questions, créez plusieurs publications. Ne posez pas de questions sans rapport entre elles dans une même publication.

### Informations requises {#required-information}
Nous ne pourrons pas vous aider si vous ne fournissez pas les informations nécessaires :

**Titre**
Utilisez un titre court et descriptif. Un bon titre serait « Comment déplacer un objet de jeu (game object) dans la direction vers laquelle il est orienté ? » ou « Comment faire disparaître progressivement un sprite ? ». Un mauvais titre serait « J'ai besoin d'aide pour utiliser Defold ! » ou « Mon jeu ne fonctionne pas ! ».

**Description du bug (OBLIGATOIRE)**
Une description claire et concise du bug.

**Étapes de reproduction (OBLIGATOIRE)**
Étapes permettant de reproduire le comportement :
1. Accédez à '...'
2. Cliquez sur '....'
3. Faites défiler jusqu'à '....'
4. Constatez l'erreur

**Comportement attendu (OBLIGATOIRE)**
Une description claire et concise de ce que vous vous attendiez à voir se produire.

**Version de Defold (OBLIGATOIRE) :**
  - Version [p. ex. 1.2.155]

**Plateformes (OBLIGATOIRE) :**
 - Plateformes : [p. ex. iOS, Android, Windows, macOS, Linux, HTML5]
 - Système d'exploitation : [p. ex. iOS8.1, Windows 10, High Sierra]
 - Appareil : [p. ex. iPhone6]

**Projet minimal de reproduction (FACULTATIF) :**
Veuillez joindre un projet minimal dans lequel le bug se reproduit. Cela aidera grandement la personne qui cherche à comprendre et à corriger le bug.

**Journaux (FACULTATIF) :**
Veuillez fournir les journaux pertinents du moteur, de l'éditeur ou du serveur de build. Découvrez où les journaux sont stockés [ici](#log-files).

**Solution de contournement (FACULTATIF) :**
S'il existe une solution de contournement, veuillez la décrire ici.

**Captures d'écran (FACULTATIF) :**
Le cas échéant, ajoutez des captures d'écran pour mieux expliquer votre problème.

**Contexte supplémentaire (FACULTATIF) :**
Ajoutez ici tout autre élément de contexte concernant le problème.


### Partager du code {#sharing-code}
Lorsque vous partagez du code, il est recommandé de le faire sous forme de texte, et non de captures d'écran. Le format texte facilite les recherches, la mise en évidence des erreurs ainsi que la proposition et la réalisation de modifications. Partagez le code en l'entourant de trois \`\`\` ou en le mettant en retrait de quatre espaces.

Exemple :

\`\`\`
print("Hello code!")
\`\`\`

Résultat :

```
print("Hello code!")
```


## Signaler un problème depuis l'éditeur {#report-a-problem-from-the-editor}

L'éditeur propose un moyen pratique de signaler des problèmes. Sélectionnez l'option de menu <kbd>Help->Report Issue</kbd> dans l'éditeur pour signaler un problème.

![](images/getting_help/report_issue.png)

Cette option de menu vous mène à un outil de suivi des problèmes sur GitHub. Fournissez les [fichiers journaux](#log-files), des informations sur votre système d'exploitation, les étapes permettant de reproduire le problème, les solutions de contournement possibles, etc.

::: sidenote
Vous devez disposer d'un compte GitHub pour soumettre un rapport de bug de cette manière.
:::


## Discuter d'un problème sur Discord {#discuss-a-problem-on-discord}

Si vous rencontrez un problème en utilisant Defold, vous pouvez essayer de poser votre question sur [Discord](https://www.defold.com/discord/). Nous vous recommandons toutefois de publier les questions complexes et les discussions approfondies sur le forum. Notez également que nous n'acceptons pas les rapports de bugs soumis via Discord.


# Fichiers journaux {#log-files}

Le moteur, l'éditeur et le serveur de build génèrent des informations de journalisation qui peuvent être très utiles pour demander de l'aide et déboguer un problème. Fournissez toujours les fichiers journaux lorsque vous signalez un problème :

* [Journaux du moteur](/manuals/debugging-game-and-system-logs)
* [Journaux de l'éditeur](/manuals/editor#editor-logs)
* [Journaux du serveur de build](/manuals/extensions#build-server-logs)
