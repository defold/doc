---
title: Afficher des publicités dans Defold
brief: Afficher différents types de publicités est un moyen courant de monétiser les jeux web et mobiles. Ce manuel présente plusieurs façons de monétiser votre jeu grâce aux publicités.
---

# Publicités {#ads}

La publicité est devenue un moyen très courant de monétiser les jeux web et mobiles, et le secteur pèse désormais des milliards de dollars. En tant que développeur, vous êtes rémunéré en fonction du nombre de personnes qui regardent les publicités affichées dans votre jeu. En général, plus il y a de spectateurs, plus vous gagnez d'argent, mais d'autres facteurs influent aussi sur votre rémunération :

* La qualité des publicités - les publicités pertinentes sont plus susceptibles de susciter des interactions et de retenir l'attention de vos joueurs.
* Le format des publicités - les bannières publicitaires rapportent généralement moins, tandis que les publicités en plein écran regardées du début à la fin rapportent davantage.
* Le réseau publicitaire - le montant de votre rémunération varie d'un réseau publicitaire à l'autre.

::: sidenote
CPM = Coût pour mille. Le montant qu'un annonceur paie pour mille vues. Le CPM varie selon les réseaux publicitaires et les formats de publicité.
:::

## Formats {#formats}

De nombreux formats de publicité peuvent être utilisés dans les jeux. Parmi les plus courants figurent les bannières, les publicités interstitielles et les publicités avec récompense :

### Bannières publicitaires {#banner-ads}

Les bannières publicitaires contiennent du texte, des images ou des vidéos et occupent une partie relativement petite de l'écran, généralement en haut ou en bas. Les bannières publicitaires sont très faciles à mettre en œuvre et conviennent très bien aux jeux occasionnels qui se jouent sur un seul écran, où il est facile de réserver une zone aux publicités. Les bannières publicitaires maximisent l'exposition pendant que les utilisateurs jouent à votre jeu sans interruption.

### Publicités interstitielles {#interstitial-ads}

Les publicités interstitielles proposent des expériences en plein écran avec des animations et parfois aussi du *contenu multimédia enrichi* interactif. Elles sont généralement affichées entre les niveaux ou les sessions de jeu, car il s'agit d'une pause naturelle dans l'expérience de jeu. Les publicités interstitielles génèrent généralement moins de vues que les bannières publicitaires, mais leur coût (CPM) est beaucoup plus élevé, ce qui se traduit par des revenus publicitaires globaux importants.

### Publicités avec récompense {#rewarded-ads}

Les publicités avec récompense (également appelées publicités incitatives) sont facultatives et donc moins intrusives que de nombreuses autres formes de publicité. Elles proposent généralement des expériences en plein écran, comme les publicités interstitielles. L'utilisateur peut choisir une récompense en échange du visionnage de la publicité, par exemple du *butin*, des pièces, des vies, du temps ou une autre monnaie ou un autre avantage dans le jeu. Les publicités avec récompense ont généralement le coût (CPM) le plus élevé, mais le nombre de vues est directement lié à la proportion d'utilisateurs qui choisissent de les regarder. Elles ne donnent de très bons résultats que si les récompenses ont suffisamment de valeur et sont proposées au bon moment.


## Réseaux publicitaires {#ad-networks}

Le [Defold Asset Portal](/tags/stars/ads/) contient plusieurs ressources qui s'intègrent à des fournisseurs de publicités :

* [AdMob](https://defold.com/assets/admob-defold/) - Affichez des publicités à l'aide du réseau Google AdMob.
* [AppLovin MAX](https://defold.com/extension-applovin/) - Affichez des publicités à l'aide de la médiation publicitaire AppLovin MAX.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Affichez des publicités dans votre Facebook Instant Game.
* [LevelPlay](https://defold.com/extension-levelplay/) - Affichez des publicités à l'aide de la médiation publicitaire Unity LevelPlay.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Affichez des publicités à l'aide du réseau Unity Ads.


# Comment intégrer des publicités dans votre jeu {#how-to-integrate-ads-in-your-game}

Une fois que vous avez choisi un réseau publicitaire à intégrer dans votre jeu, vous devez suivre les instructions d'installation et d'utilisation de la *ressource* correspondante. En général, vous commencez par ajouter l'extension en tant que [dépendance du projet](/manuals/libraries/#setting-up-library-dependencies). Une fois la ressource ajoutée à votre projet, vous pouvez poursuivre l'intégration et appeler les fonctions propres à la ressource pour charger et afficher des publicités.


# Combiner publicités et achats intégrés {#combining-ads-and-in-app-purchases}

Il est assez courant dans les jeux mobiles de proposer un [achat intégré](/manuals/iap) pour supprimer définitivement les publicités.


## En savoir plus {#learn-more}

De nombreuses ressources en ligne permettent d'apprendre à optimiser les revenus publicitaires :

* Google AdMob [Monétiser les jeux mobiles avec des publicités](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Formats de publicité populaires et comment les utiliser](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Diffusion de publicités dans les jeux : 10 conseils d'experts](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
