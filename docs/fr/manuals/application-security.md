---
title: Manuel de sécurité des applications
brief: Ce manuel aborde plusieurs domaines liés aux pratiques de développement sécurisé.
---

# Sécurité des applications {#application-security}

La sécurité des applications est un vaste sujet qui va des pratiques de développement sécurisé à la protection du contenu de votre jeu après sa publication. Ce manuel aborde plusieurs domaines et les replace dans le contexte de la sécurité des applications utilisant le moteur, les outils et les services Defold :

* Protection de la propriété intellectuelle
* Solutions contre la triche
* Communications réseau sécurisées
* Utilisation de logiciels tiers
* Utilisation de serveurs de build dans le cloud
* Contenu téléchargeable


## Protéger votre propriété intellectuelle contre le vol {#securing-your-intellectual-property-from-theft}
La plupart des développeurs se préoccupent de la protection de leurs créations contre le vol. Sur le plan juridique, le droit d'auteur, les brevets et les marques peuvent servir à protéger les différents aspects de la propriété intellectuelle des jeux vidéo. Le droit d'auteur donne à son titulaire le droit exclusif de distribuer l'œuvre, les brevets protègent les inventions et les marques protègent les noms, les symboles et les logos.

Il peut également être souhaitable de prendre des précautions techniques pour protéger le travail créatif d'un jeu. Il est toutefois important de garder à l'esprit qu'une fois le jeu entre les mains du joueur, il est possible de trouver des moyens d'en extraire les ressources. Cela peut se faire par rétro-ingénierie de l'application et des fichiers du jeu, mais aussi à l'aide d'outils permettant d'extraire les textures et les modèles lors de leur envoi au GPU, ou d'autres ressources lors de leur chargement en mémoire.

C'est pourquoi nous considérons, de manière générale, que les utilisateurs déterminés à extraire les ressources d'un jeu parviendront à le faire.

Les développeurs peuvent ajouter leurs propres protections pour rendre l'extraction des ressources plus difficile, __mais pas impossible__. Cela comprend généralement différents moyens de chiffrement et d'obfuscation pour protéger et masquer les ressources du jeu.

### Obfuscation du code source {#source-code-obfuscation}
L'obfuscation du code source est un processus automatisé qui rend délibérément le code source difficile à comprendre pour un humain, sans modifier les résultats du programme. Elle vise généralement à protéger le code contre le vol, mais aussi à rendre la triche plus difficile.

Dans Defold, il est possible d'appliquer une obfuscation du code source soit avant le build, soit dans le cadre du processus de build Defold. Dans le premier cas, le code source est transformé à l'aide d'un outil d'obfuscation avant le démarrage du processus de build Defold.

L'obfuscation pendant le build, quant à elle, est intégrée au processus de build à l'aide d'un plugin de build Lua. Ce plugin prend le code source brut en entrée et renvoie une version obfusquée du code source en sortie. L'[extension Prometheus](https://github.com/defold/extension-prometheus) fournit un exemple d'obfuscation pendant le build, fondé sur l'outil d'obfuscation Lua Prometheus disponible sur GitHub. Vous trouverez ci-dessous un exemple d'utilisation de Prometheus pour appliquer une obfuscation poussée à un extrait de code (notez qu'une obfuscation aussi importante aura un effet sur les performances du code Lua à l'exécution) :

Exemple :

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Résultat obfusqué :

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Chiffrement des ressources {#resource-encryption}
Pendant le processus de build Defold, les ressources du jeu sont traitées et transformées en formats adaptés à leur utilisation par le moteur Defold à l'exécution. Les textures sont compilées au format Basis Universal, les collections, les objets de jeu (game object) et les composants (component) sont convertis de leur représentation textuelle lisible par un humain en leur équivalent binaire, et le code source Lua est traité puis compilé en bytecode. D'autres ressources, comme les fichiers audio, sont utilisées telles quelles.

Une fois ce processus terminé, les ressources sont ajoutées une par une à l'archive du jeu. L'archive du jeu est un gros fichier binaire et l'emplacement de chaque ressource dans l'archive est stocké dans un fichier d'index d'archive. Le format est documenté [ici](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md).

Avant d'être ajoutés à l'archive, les fichiers source Lua peuvent également être chiffrés. Le chiffrement fourni par défaut dans Defold est un simple chiffrement par blocs, destiné à empêcher que les chaînes de caractères du code soient immédiatement visibles lors de l'inspection de l'archive du jeu avec un outil de visualisation de fichiers binaires. Il ne doit pas être considéré comme sûr sur le plan cryptographique, car le code source de Defold est disponible sur GitHub et la clé de chiffrement y est visible.

Il est possible d'appliquer un chiffrement personnalisé aux fichiers source Lua en implémentant un plugin de chiffrement des ressources. Ce plugin comprend une partie qui chiffre les ressources pendant le processus de build et une partie qui les déchiffre à l'exécution, lors de leur lecture dans l'archive du jeu. Un plugin de chiffrement des ressources de base, que vous pouvez utiliser comme point de départ pour votre propre chiffrement, est [disponible sur GitHub](https://github.com/defold/extension-resource-encryption).


### Encodage des valeurs de configuration du projet {#encoding-project-configuration-values}
Le fichier *game.project* sera inclus tel quel dans le bundle de votre application. Vous pouvez parfois souhaiter stocker des clés d'accès à des API publiques ou des valeurs similaires, qui sont sensibles sans être nécessairement privées. Pour renforcer la sécurité de ces valeurs, vous pouvez les inclure dans le binaire de l'application au lieu de les stocker dans *game.project*, tout en les gardant accessibles aux fonctions de l'API Defold, comme `sys.get_config_string()` et les fonctions similaires. Pour cela, ajoutez une extension native dans votre fichier *game.project* et utilisez la macro `DM_DECLARE_CONFIGFILE_EXTENSION` pour fournir vos propres implémentations de la récupération des valeurs de configuration par les fonctions de l'API Defold. Un exemple de projet que vous pouvez utiliser comme point de départ est [disponible sur GitHub](https://github.com/defold/example-configfile-extension/tree/master).


## Protéger votre jeu contre les tricheurs {#securing-your-game-against-cheaters}
La triche dans les jeux vidéo existe depuis les débuts de l'industrie du jeu. Les codes de triche étaient partagés dans les magazines de jeux vidéo populaires et des cartouches de triche spéciales étaient vendues pour les premiers ordinateurs domestiques. Les tricheurs et leurs méthodes ont évolué en même temps que l'industrie et les jeux. Parmi les mécanismes de triche les plus répandus, on trouve :

* Le reconditionnement du contenu du jeu pour y injecter une logique personnalisée
* La modification de la vitesse d'exécution pour faire fonctionner un jeu plus vite ou plus lentement que la normale
* L'automatisation et l'analyse visuelle pour la visée automatique et les robots de jeu
* L'injection de code et l'injection en mémoire pour modifier les scores, les vies, les munitions, etc.

Se protéger contre les tricheurs est difficile, voire presque impossible. Même le jeu dans le cloud, où les jeux s'exécutent sur des serveurs distants et sont diffusés directement sur l'appareil de l'utilisateur, n'est pas totalement épargné par les tricheurs.

Defold ne fournit aucune solution contre la triche dans le moteur ou les outils et laisse ce travail à l'une des nombreuses entreprises spécialisées dans les solutions contre la triche pour les jeux.


## Sécuriser vos communications réseau {#securing-your-network-communication}
Les communications par socket et HTTP de Defold prennent en charge les connexions sécurisées par socket. Il est recommandé d'utiliser des connexions sécurisées pour toute communication avec un serveur, afin d'authentifier ce serveur et de protéger la confidentialité et l'intégrité des données échangées pendant leur transit du client vers le serveur et inversement. Defold utilise [Mbed TLS](https://github.com/Mbed-TLS/mbedtls), une implémentation open source populaire et largement adoptée des protocoles TLS et SSL. Mbed TLS est développé par ARM et ses partenaires technologiques.

### Validation des certificats SSL {#ssl-certificate-validation}
Pour empêcher les attaques de l'homme du milieu contre vos communications réseau, il est possible de valider la chaîne de certificats pendant la négociation SSL lors de l'établissement d'une connexion avec un serveur. Pour cela, vous pouvez fournir une liste de clés publiques au client réseau dans Defold. Pour en savoir plus sur la sécurisation de vos communications réseau, consultez la section sur la vérification SSL dans le [manuel sur les communications réseau](https://defold.com/manuals/networking/#secure-connections).


## Sécuriser votre utilisation de logiciels tiers {#securing-your-use-of-third-party-software}
Bien qu'il ne soit pas nécessaire d'utiliser des bibliothèques tierces ou des extensions natives pour créer un jeu, il est devenu très courant pour les développeurs d'utiliser des ressources de l'[Asset Portal](https://defold.com/assets/) officiel pour accélérer le développement. L'Asset Portal contient une vaste sélection de ressources, allant des intégrations de SDK tiers aux gestionnaires d'écrans, en passant par les bibliothèques d'interface utilisateur, les caméras et bien d'autres éléments.

Aucune des ressources de l'Asset Portal n'a été examinée par la Defold Foundation et nous déclinons toute responsabilité en cas de dommage à votre système informatique ou à tout autre appareil, ou de perte de données résultant de l'utilisation d'une ressource obtenue par l'intermédiaire de l'Asset Portal. Vous pouvez consulter les dispositions détaillées dans nos [conditions générales](https://defold.com/terms-and-conditions/#3-no-warranties).

Nous vous recommandons d'examiner toute ressource avant de l'utiliser puis, une fois que vous avez jugé qu'elle convient à votre projet, d'en créer un fork ou une copie pour vous assurer qu'elle ne change pas à votre insu.


## Sécuriser votre utilisation des serveurs de build dans le cloud {#securing-your-use-of-cloud-build-servers}
Les serveurs de build Defold dans le cloud (également appelés serveurs extender) ont été créés pour aider les développeurs à ajouter de nouvelles fonctionnalités au moteur Defold sans nécessiter de recompilation du moteur lui-même. Lorsqu'un projet Defold contenant du code natif est compilé pour la première fois, le code natif et toutes les ressources associées sont envoyés aux serveurs de build dans le cloud, où une version personnalisée du moteur Defold est créée puis renvoyée au développeur. Le même processus s'applique lorsqu'un projet est compilé à l'aide d'un manifeste d'application personnalisé pour supprimer les composants inutilisés du moteur.

Les serveurs de build dans le cloud sont hébergés chez AWS et créés conformément aux bonnes pratiques de sécurité. La Defold Foundation ne garantit toutefois pas que ces serveurs répondront à vos exigences, qu'ils seront exempts de défauts, de virus ou d'erreurs, qu'ils seront sécurisés, ni que votre utilisation des serveurs sera ininterrompue ou sécurisée. Vous pouvez consulter les dispositions détaillées dans nos [conditions générales](https://defold.com/terms-and-conditions/#3-no-warranties).

Si la sécurité et la disponibilité des serveurs de build vous préoccupent, nous vous recommandons de mettre en place vos propres serveurs de build privés. Vous trouverez les instructions de configuration de votre propre serveur dans le [fichier readme principal](https://github.com/defold/extender) du dépôt extender sur GitHub.


## Sécuriser votre contenu téléchargeable {#securing-your-downloadable-content}
Le système Live Update de Defold permet aux développeurs d'exclure du contenu du bundle principal du jeu pour le télécharger et l'utiliser ultérieurement. Un cas d'utilisation typique consiste à télécharger des niveaux, des cartes ou des mondes supplémentaires à mesure que le joueur progresse dans le jeu.

Lorsque le contenu exclu est téléchargé et préparé pour être utilisé dans un jeu, le moteur le vérifie avant son utilisation. Cette vérification comprend plusieurs contrôles :

* Le format binaire est-il correct ?
* Le contenu téléchargé est-il pris en charge par la version du moteur en cours d'exécution ?
* Le contenu téléchargé est-il complet, sans fichier manquant ?

Vous pouvez en savoir plus sur ce processus dans le [manuel Live Update](https://defold.com/manuals/live-update/#content-verification).
