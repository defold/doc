#### D: Perché la mia applicazione HTML5 si blocca alla schermata iniziale in Chrome? {#q-why-does-my-html5-app-freeze-at-the-splash-screen-in-chrome}

R: In alcuni casi non è possibile eseguire un gioco nel browser direttamente dal file system locale. Quando lo avvii dall'editor, il gioco viene servito da un server web locale. Puoi usare, per esempio, `SimpleHTTPServer` di Python:

```sh
$ python -m SimpleHTTPServer [port]
```


#### D: Perché il mio gioco si arresta con l'errore "Unexpected data size" durante il caricamento? {#q-why-does-my-game-crash-with-error-unexpected-data-size-while-loading}

R: Questo accade solitamente quando usi Windows, crei una build e la aggiungi a un commit Git. Se la configurazione delle terminazioni di riga in Git è errata, Git le modifica, cambiando così anche la dimensione dei dati. Segui queste istruzioni per risolvere il problema: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
