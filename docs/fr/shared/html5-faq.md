#### Q : Pourquoi mon application HTML5 se fige-t-elle sur l'écran de démarrage dans Chrome ? {#q-why-does-my-html5-app-freeze-at-the-splash-screen-in-chrome}

R : Dans certains cas, il n'est pas possible d'exécuter un jeu localement dans le navigateur à partir du système de fichiers. Lorsque vous lancez le jeu depuis l'éditeur, un serveur web local le sert au navigateur. Vous pouvez, par exemple, utiliser `SimpleHTTPServer` en Python :

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q : Pourquoi mon jeu plante-t-il avec l'erreur « Unexpected data size » pendant le chargement ? {#q-why-does-my-game-crash-with-error-unexpected-data-size-while-loading}

R : Cela se produit généralement lorsque vous utilisez Windows, créez un build et l'enregistrez dans un commit Git. Si la configuration des fins de ligne dans Git est incorrecte, Git modifiera vos fins de ligne et donc également la taille des données. Suivez ces instructions pour résoudre le problème : [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
