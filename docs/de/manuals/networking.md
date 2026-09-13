---
title: Netzwerkverbindungen in Defold
brief: Dieses Handbuch erklärt, wie du dich mit entfernten Servern verbindest und andere Arten von Netzwerkverbindungen herstellst.
---

# Netzwerkverbindungen {#networking}

Spiele verfügen häufig über eine Verbindung zu einem Backend-Dienst, etwa um Punktestände zu übermitteln, die Spielersuche abzuwickeln oder Spielstände in der Cloud zu speichern. Viele Spiele nutzen außerdem Peer-to-Peer-Verbindungen, bei denen die Spielclients direkt miteinander kommunizieren, ohne dass ein zentraler Server beteiligt ist. Für Netzwerkverbindungen und den Datenaustausch können verschiedene Protokolle und Standards verwendet werden. Erfahre mehr über die verschiedenen Möglichkeiten, Netzwerkverbindungen in Defold zu nutzen:

* [HTTP-Anfragen](/manuals/http-requests)
* [Socket-Verbindungen](/manuals/socket-connections)
* [WebSocket-Verbindungen](/manuals/websocket-connections)
* [Online-Dienste](/manuals/online-services)


## Technische Details {#technical-details}

### IPv4 und IPv6 {#ipv4-and-ipv6}

Defold unterstützt IPv4- und IPv6-Verbindungen für Sockets und HTTP-Anfragen.

### Sichere Verbindungen {#secure-connections}

Defold unterstützt sichere SSL-Verbindungen für Sockets und HTTP-Anfragen.

Defold kann optional auch das SSL-Zertifikat jeder sicheren Verbindung überprüfen. Die SSL-Überprüfung wird aktiviert, wenn du im Feld der [Einstellung SSL Certificates](/manuals/project-settings/#network)) im Abschnitt Network von *game.project* eine PEM-Datei angibst, die öffentliche Schlüssel von CA-Stammzertifikaten oder den öffentlichen Schlüssel eines selbstsignierten Zertifikats enthält. Eine Liste von CA-Stammzertifikaten ist in `builtins/ca-certificates` enthalten. Es wird jedoch empfohlen, eine neue PEM-Datei zu erstellen und die benötigten CA-Stammzertifikate per Kopieren und Einfügen zu übernehmen, abhängig davon, mit welchen Servern sich das Spiel verbindet.


