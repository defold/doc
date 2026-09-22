## Taille du tas (HTML5) {#heap-size-html5}
La taille du tas d'un jeu HTML5 Defold peut être configurée à partir du [champ `heap_size`](/manuals/project-settings/#heap-size) dans *game.project*. Veillez à optimiser l'utilisation de la mémoire de votre jeu et à définir une taille minimale du tas.

Pour les petits jeux, il est possible d'atteindre une taille de tas de 32 Mo. Pour les jeux plus volumineux, visez 64–128 Mo. Si, par exemple, vous êtes à 58 Mo et qu'une optimisation supplémentaire n'est pas réalisable, vous pouvez vous en tenir à 64 Mo sans trop vous poser de questions. Il n'y a pas de taille cible stricte : elle dépend du jeu. Visez simplement des tailles plus petites, idéalement par paliers correspondant à des puissances de deux. 

Pour vérifier l'utilisation actuelle du tas, vous pouvez lancer votre jeu et surveiller l'utilisation de la mémoire pendant que vous jouez dans le niveau ou la section qui consomme le plus de ressources :

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

Vous pouvez aussi ouvrir les outils de développement de votre navigateur et saisir ce qui suit dans la console :

```js
HEAP8.length / 1024 / 1024
```

Si l'utilisation de la mémoire reste à 32 Mo, c'est parfait ! Sinon, suivez les étapes pour [optimiser la taille du moteur lui-même et des ressources volumineuses telles que les sons et les textures](/manuals/optimization-size).
