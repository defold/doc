## Variantes de build {#build-variants}

Lorsque vous créez un bundle de jeu, vous devez choisir le type de moteur que vous souhaitez utiliser. Vous disposez de trois options de base :

  * Debug
  * Release
  * Headless

Ces différentes versions sont également appelées `Build variants`

::: sidenote
Lorsque vous choisissez <kbd>Project ▸ Build</kbd>, vous obtenez toujours la version Debug.
:::


### Debug {#debug}

Ce type d'exécutable est généralement utilisé pendant le développement d'un jeu, car il intègre plusieurs fonctionnalités de débogage utiles :

* Profileur - Sert à recueillir des compteurs de performances et d'utilisation. Découvrez comment utiliser le profileur dans le [manuel de profilage](/manuals/profiling/).
* Journalisation - Le moteur consigne les informations système, les avertissements et les erreurs lorsque la journalisation est activée. Le moteur affiche également les journaux issus de la fonction Lua `print()` et des extensions natives qui utilisent `dmLogInfo()`, `dmLogError()`, etc. Découvrez comment lire ces journaux dans le [manuel des journaux du jeu et du système](https://defold.com/manuals/debugging-game-and-system-logs/).
* Rechargement à chaud - Le rechargement à chaud est une fonctionnalité puissante qui permet à un développeur de recharger une ressource pendant l'exécution du jeu. Découvrez comment l'utiliser dans le [manuel du rechargement à chaud](https://defold.com/manuals/hot-reload/).
* Services du moteur - Il est possible de se connecter à une version Debug d'un jeu et d'interagir avec elle via différents ports TCP ouverts et services. Ces services comprennent le rechargement à chaud, l'accès à distance aux journaux et le profileur mentionnés ci-dessus, mais aussi d'autres services permettant d'interagir à distance avec le moteur. Pour en savoir plus sur les services du moteur, consultez la [documentation pour les développeurs](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release {#release}

Les fonctionnalités de débogage sont désactivées dans cette variante. Vous devriez choisir cette option lorsque le jeu est prêt à être publié dans un magasin d'applications ou partagé avec les joueurs d'une autre manière. Il est déconseillé de publier un jeu avec les fonctionnalités de débogage activées pour plusieurs raisons :

* Les fonctionnalités de débogage occupent un peu de place dans le binaire, et [une bonne pratique consiste à garder le binaire d'un jeu publié aussi petit que possible](https://defold.com/manuals/optimization/#optimize-application-size).
* Les fonctionnalités de débogage consomment également un peu de temps processeur. Cela peut nuire aux performances du jeu si l'utilisateur dispose de matériel peu puissant. Sur les téléphones mobiles, l'utilisation accrue du processeur contribue aussi à l'échauffement et à la décharge de la batterie.
* Les fonctionnalités de débogage peuvent exposer des informations sur le jeu qui ne sont pas destinées aux joueurs, pour des raisons de sécurité, de triche ou de fraude.


### Headless {#headless}

Cet exécutable fonctionne sans interface graphique ni son. Cela signifie que vous pouvez exécuter les tests unitaires ou de bon fonctionnement du jeu sur un serveur d'intégration continue (CI), ou même l'utiliser comme serveur de jeu dans le cloud.
