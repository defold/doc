---
title: Connexions réseau dans Defold
brief: Ce manuel explique comment vous connecter à des serveurs distants et établir d'autres types de connexions réseau.
---

# Connexions réseau {#networking}

Il n'est pas rare que les jeux disposent d'une connexion à un service côté serveur, par exemple pour publier des scores, gérer la mise en relation des joueurs ou stocker des sauvegardes de parties dans le cloud. De nombreux jeux utilisent aussi des connexions de pair à pair, où les clients du jeu communiquent directement entre eux, sans l'intervention d'un serveur central. Les connexions réseau et l'échange de données peuvent s'appuyer sur différents protocoles et normes. Découvrez les différentes façons d'utiliser les connexions réseau dans Defold :

* [Requêtes HTTP](/manuals/http-requests)
* [Connexions par socket](/manuals/socket-connections)
* [Connexions WebSocket](/manuals/websocket-connections)
* [Services en ligne](/manuals/online-services)


## Détails techniques {#technical-details}

### IPv4 et IPv6 {#ipv4-and-ipv6}

Defold prend en charge les connexions IPv4 et IPv6 pour les sockets et les requêtes HTTP.

### Connexions sécurisées {#secure-connections}

Defold prend en charge les connexions sécurisées SSL pour les sockets et les requêtes HTTP.

Defold peut également, de manière facultative, vérifier le certificat SSL de toute connexion sécurisée. La vérification SSL est activée lorsqu'un fichier PEM contenant les clés publiques de certificats d'autorités de certification racines ou la clé publique d'un certificat autosigné est fourni dans le champ du [paramètre SSL Certificates](/manuals/project-settings/#network)) de la section Network de *game.project*. Une liste de certificats d'autorités de certification racines est incluse dans `builtins/ca-certificates`, mais il est recommandé de créer un nouveau fichier PEM et d'y copier-coller les certificats racines nécessaires en fonction du ou des serveurs auxquels le jeu se connecte.

