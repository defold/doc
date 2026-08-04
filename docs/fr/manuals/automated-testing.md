---
title: Tests et vérification automatisés
brief: Ce manuel explique comment concevoir, exécuter et documenter des tests Defold déterministes en local, dans un jeu en cours d'exécution, dans des navigateurs et dans un environnement d'intégration continue.
---

# Tests et vérification automatisés {#automated-testing-and-verification}

Les tests automatisés vérifient le code et le contenu Defold à l'aide de preuves explicites et lisibles par une machine. Utilisez ce manuel pour concevoir des tests qui fonctionnent aussi bien avec des scripts locaux, des exécuteurs CI (intégration continue) et des agents de programmation. Il couvre les tests de modules, l'exécution de collections, les tests dans un navigateur, l'automatisation à l'exécution, les contrôles visuels et les builds headless, et présente des bonnes pratiques utiles.

## Niveaux de vérification {#verification-levels}

Une bonne organisation des tests automatisés suit le principe de la pyramide des tests, qui répartit les tests en trois couches principales : tests unitaires, tests d'intégration et tests de bout en bout (E2E). Dans Defold, vous pouvez séparer les tests dans des collections particulières qui peuvent être chargées au démarrage. En règle générale, commencez par le contrôle le plus ciblé et le plus rapide capable de détecter le problème, puis ajoutez des tests d'exécution ou de plateforme lorsque cela est nécessaire.

| Niveau | Preuves appropriées |
| --- | --- |
| Validation statique | Analyseur, outil de formatage, validateur de ressources ou comparaison de fichiers générés |
| Test de module | Résultats d'assertions pour une logique Lua réutilisable avec un minimum de dépendances au moteur |
| Collection en cours d'exécution | Messages, composants, entrées, physique, cycle de vie et comportement du moteur |
| Automatisation à l'exécution | État en direct de la scène, entrées injectées, état de l'application et captures d'écran à l'exécution |
| Test HTML5 dans un navigateur | Entrées du canvas, intégration au navigateur, comportement de la fenêtre d'affichage et sortie web |
| Test de plateforme | Comportement et rendu sur la plateforme cible réelle |
| Build et bundle | État de sortie de Bob, rapport de build, archive et artefacts du bundle |

Une compilation réussie prouve que le projet peut être compilé, mais pas que le comportement du jeu est correct. Une capture d'écran ne prouve pas les transitions, les animations, les interactions ou le déroulement complexe du jeu, mais les solutions multimodales modernes peuvent l'utiliser pour examiner l'apparence d'une image et vérifier que les shaders et la disposition visuelle sont corrects. Pour les tests automatisés, préférez toutefois les assertions déterministes dès que la condition peut être exprimée directement.

## Code Lua réutilisable et testable {#reusable-and-testable-lua-code}

Conservez la logique réutilisable dans des modules Lua qui dépendent le moins possible du moteur. Les transformations de données pures, les règles, les machines à états et les calculs peuvent ainsi être exercés sans construire un univers de jeu complet.

Séparez le code qui interagit avec le moteur de la logique qu'il appelle. Un script peut traduire les messages et l'état des composants en appels à un module, tandis que les tests appellent directement le module avec des entrées contrôlées.

Pour plus de détails, consultez le [manuel sur l'écriture du code](/manuals/writing-code).

## Tests dans une collection en cours d'exécution {#tests-in-a-running-collection}

Utilisez une collection de test dédiée lorsque le comportement dépend d'objets de jeu, de composants, de messages, d'entrées, de la physique ou d'autres systèmes du moteur.

Chaque test doit :

1. établir un état connu ;
2. exécuter un comportement ;
3. vérifier et évaluer le résultat attendu ;
4. nettoyer les ressources créées ;
5. émettre une description structurée du résultat.

Préférez des collections de test isolées. Un projet peut sélectionner une collection bootstrap de test au moyen d'un paramètre temporaire du projet dans `game.project` :

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Ne laissez pas un bootstrap de test temporaire dans la configuration normale du projet. Dans la CI, préférez un fichier de paramètres dédié transmis à Bob. La CI ne doit pas modifier l'état du dépôt ; elle doit uniquement effectuer des modifications temporaires lorsque cela est nécessaire.

Pour les jeux complexes, vous pouvez créer de petites collections de « salles de développement » avec des scénarios prédéfinis et de simples prototypes visuels. Elles rendent les mécaniques reproductibles et facilitent les tests pendant le développement sans avoir à parcourir des états et des sections sans rapport du jeu.

### Frameworks de test {#test-frameworks}

Les projets peuvent implémenter un petit exécuteur ou utiliser une [bibliothèque de test communautaire](https://defold.com/assets/?tag=testing).

Par exemple, [DefTest](https://defold.com/assets/deftest/) est une bibliothèque de tests unitaires fondée sur Telescope. Elle prend en charge les suites, les fonctions de préparation et de nettoyage, les assertions, le filtrage par nom, les mocks pour certaines API Defold et, facultativement, la couverture LuaCov. Les tests peuvent s'exécuter à partir d'une collection bootstrap dédiée, y compris dans un bundle headless créé avec Bob.

## Résultats de test structurés {#structured-test-results}

Le résumé dans la console ou le journal d'un framework peut être utile aux développeurs, mais un contrôleur automatique sans supervision a toujours besoin d'un résultat de fin explicite. Si nécessaire, ajoutez un petit adaptateur autour du callback ou du résumé du framework afin que le contrôleur traite facilement les résultats des tests.

Une description simple des résultats peut utiliser un préfixe unique suivi d'un objet JSON sur chaque ligne physique de la console :

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Un collecteur doit traiter chaque ligne indépendamment, rechercher le préfixe `TEST`, analyser le JSON qui suit et ignorer les sorties sans rapport du moteur.

Incluez un identifiant d'exécution unique afin que la sortie d'un processus ancien ou simultané ne puisse pas terminer l'exécution actuelle. Chaque suite doit émettre un événement final sans ambiguïté (comme `Pass`, `Failure`, `Crash`, `Timeout`, etc.).

### Collecte de la sortie de la console {#collecting-console-output}

Lorsqu'un jeu s'exécute depuis l'éditeur, celui-ci fournit à la fois l'historique actuel de la console et un flux continu. Fermez le flux après un événement de fin de suite correspondant, l'arrêt du processus, une erreur, ou lorsqu'un délai d'expiration ou une limite de lignes configurés sont atteints.

Pour en savoir plus, consultez le [manuel de l'API HTTP de l'éditeur](/manuals/editor-http-api/#reading-console-output).

### Journaux persistants {#persisted-logs}

Defold peut également conserver le journal du jeu en activant `Write Log File` dans `game.project`. Consultez [Journaux du jeu et du système](/manuals/debugging-game-and-system-logs/). La journalisation dans un fichier est utile pour les applications empaquetées et pour tester des appareils cibles sur lesquels la console de l'éditeur n'est pas disponible.

Le projet peut utiliser les fonctions intégrées `print()` et `pprint()`, ou par exemple toute autre [bibliothèque de journalisation](https://defold.com/assets/?tag=logging) de notre Asset Portal.

## Tester un jeu en cours d'exécution au moyen d'une API d'exécution {#testing-a-running-game-through-a-runtime-api}

Une API d'automatisation à l'exécution peut inspecter et contrôler un moteur de débogage actif. Elle peut être utilisée lorsque les tests doivent rechercher des objets à l'exécution, injecter des entrées, attendre un état visible ou capturer le résultat rendu.

Pour plus de détails, consultez le [manuel du service du moteur](/manuals/engine-service/#automation-bridge-extension).

L'exemple suivant utilise la structure des utilitaires Python de l'[Automation Bridge](https://github.com/defold/extension-automation-bridge). Le projet doit inclure une version compatible de l'extension de débogage, exposer un élément avec l'identifiant d'automatisation indiqué et publier l'état d'application `screen` :

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Les états définis par l'application et les identifiants d'automatisation utilisent l'API Lua facultative d'Automation Bridge, réservée au débogage, que le projet doit activer et alimenter. Une pause fixe est vulnérable à la vitesse de la machine et à la synchronisation des images ; une interrogation limitée d'un état défini est plus fiable.

Automation Bridge est une extension et ne fait pas partie du moteur principal. Consultez sa [référence de l'API Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) pour connaître les sélecteurs, les attentes, les états, les événements, les captures d'écran et les diagnostics de la version installée.

## Tests HTML5 dans un navigateur {#browser-tests-for-html5}

L'éditeur peut créer et servir un build HTML5 au moyen de sa commande actuelle `build-html5`, comme indiqué dans le [manuel de l'API HTTP de l'éditeur](/manuals/editor-http-api/#building-html5). Bob peut également créer un bundle HTML5 sans l'éditeur.

Des outils externes d'automatisation des navigateurs tels que Playwright, Puppeteer, Selenium, WebdriverIO ou Cypress peuvent :

* attendre que le canvas Defold et l'application soient prêts ;
* envoyer des entrées clavier, souris et tactiles émulées ;
* redimensionner la fenêtre d'affichage ;
* recueillir la sortie de la console du navigateur et les erreurs JavaScript ;
* prendre des captures d'écran et comparer les artefacts.

Les entrées destinées au canvas sont traitées par les liaisons d'entrée normales du projet et les callbacks `on_input()`. Testez à la fois la réponse du jeu et les points d'intégration propres au navigateur.

L'approche la plus fiable consiste à exposer un bridge de test JavaScript explicite dans le fichier `index.html` personnalisé. Du côté de Defold, les builds HTML5 peuvent exécuter du JavaScript avec `html5.run()`, ce qui permet de communiquer avec ce bridge côté navigateur. Pour les commandes qui vont de JavaScript vers Defold, utilisez un bridge dédié entre JavaScript et le moteur.

Limitez les tests dans le navigateur. Distinguez dans le rapport final l'échec du chargement de la page, l'absence du canvas, une erreur JavaScript, l'expiration du test et l'échec d'une assertion du jeu.

## Aperçus de l'éditeur et captures d'écran à l'exécution pour l'inspection visuelle {#editor-previews-and-runtime-screenshots}

Il est possible de créer une capture d'écran des fichiers de ressources dans la vue de scène par défaut de l'éditeur ouvert ou d'un jeu en cours d'exécution.

| Méthode | Objectif |
| --- | --- |
| [Aperçu de l'éditeur](/manuals/editor-http-api/#rendering-scene-previews) | Disposition d'une ressource chargée, par exemple un niveau ou une interface graphique, composition d'un atlas, inspection d'une tilemap, composition d'une scène statique, exactitude du rendu et des shaders de l'éditeur ou création de miniatures pour la documentation |
| [Capture d'écran à l'exécution](/manuals/engine-service) | État rendu d'un build en cours d'exécution dans un scénario contrôlé |

Vous pouvez utiliser la comparaison d'images, par exemple pour les tests de régression. Stockez l'image des différences et les métriques de comparaison lorsqu'un contrôle échoue.

Un modèle multimodal peut évaluer lors de l'inspection visuelle des conditions sémantiques difficiles à exprimer autrement, telles qu'un texte tronqué, des contrôles qui se chevauchent, des états de sélection peu clairs ou du contenu hors d'une zone de sécurité. Il est conseillé de considérer cette évaluation comme un signal supplémentaire associé à des critères explicites, et non comme un remplacement des contrôles logiques déterministes ou de la comparaison d'images.

## Tests headless et CI {#headless-tests-and-ci}

Utilisez Bob, l'outil de build en ligne de commande, pour une CI indépendante de l'éditeur.

Vous pouvez l'utiliser pour résoudre les dépendances, créer un build, une archive ou un bundle autonome, et générer un rapport JSON :

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Créez un bundle de test headless avec des paramètres dédiés :

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Exécutez le fichier exécutable obtenu avec un contrôleur de processus adapté à la plateforme. Capturez son état de sortie et ses journaux, imposez un délai d'expiration et exigez l'événement structuré de fin de suite.

Le [manuel de Bob](/manuals/bob) décrit les plateformes, les fichiers de paramètres, les bundles, les caches, les extensions natives et les rapports de build.

## Rapports d'échec et artefacts {#failure-reports-and-artifacts}

De bons résultats de test doivent conserver suffisamment d'éléments pour reproduire et diagnostiquer un échec :

* le nom du test, l'identifiant d'exécution et les détails de l'assertion ;
* le temps écoulé et le résultat classifié ;
* le journal complet de la console ou du processus ;
* la version de Defold, la plateforme cible et la configuration pertinente ;
* le rapport de build de Bob et l'état de sortie du processus ;
* l'état d'exécution ou l'instantané de la scène lorsqu'ils sont disponibles ;
* les captures d'écran, les différences par rapport à la référence, les enregistrements ou les traces du navigateur ;
* les chemins ou liens vers tous les artefacts générés.

Le même format doit pouvoir être utilisé par un développeur, un script local, un service CI ou un [agent de programmation IA](/manuals/ai-agents). La vérification reste ainsi déterministe, même lorsque le diagnostic ou la réparation sont délégués.
