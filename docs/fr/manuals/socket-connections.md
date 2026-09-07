---
title: Connexions socket
brief: Ce manuel explique comment créer des connexions socket.
---

## Connexions socket {#socket-connections}

Defold inclut la [bibliothèque LuaSocket](https://lunarmodules.github.io/luasocket/) pour créer des connexions socket TCP et UDP. Voici un exemple de création d'une connexion socket, d'envoi de données et de lecture d'une réponse :

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

Cet exemple crée un socket TCP et le connecte à l'adresse IP 127.0.0.1 (localhost) sur le port 8123. Il définit le délai d'expiration à 0 pour rendre le socket non bloquant et envoie la chaîne "foobar" via le socket. Il lit également une ligne de données (des octets se terminant par un caractère de saut de ligne) depuis le socket. Notez que l'exemple ci-dessus ne contient aucune gestion des erreurs.

### Référence de l'API et exemples {#api-reference-and-examples}

Consultez la [référence de l'API](/ref/socket/) pour en savoir plus sur les fonctionnalités disponibles via LuaSocket. La [documentation officielle de LuaSocket](https://lunarmodules.github.io/luasocket/) contient également de nombreux exemples d'utilisation de la bibliothèque. Vous trouverez aussi quelques exemples et modules utilitaires dans la [bibliothèque DefNet](https://github.com/britzl/defnet/).
