#### Q: Warum bleibt meine HTML5-App in Chrome beim Startbildschirm hängen? {#q-why-does-my-html5-app-freeze-at-the-splash-screen-in-chrome}

A: In manchen Fällen lässt sich ein Spiel nicht lokal aus dem Dateisystem im Browser ausführen. Wenn du das Spiel aus dem Editor startest, wird es von einem lokalen Webserver bereitgestellt. Du kannst beispielsweise `SimpleHTTPServer` in Python verwenden:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: Warum stürzt mein Spiel beim Laden mit dem Fehler "Unexpected data size" ab? {#q-why-does-my-game-crash-with-error-unexpected-data-size-while-loading}

A: Das passiert normalerweise, wenn du unter Windows einen Build erstellst und ihn in Git committest. Wenn die Zeilenenden in Git falsch konfiguriert sind, ändert Git deine Zeilenenden und damit auch die Datengröße. Befolge diese Anleitung, um das Problem zu beheben: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
