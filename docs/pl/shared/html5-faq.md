#### P: Dlaczego moja aplikacja HTML5 zawiesza się na ekranie startowym w Chrome?

O: W niektórych przypadkach nie da się uruchomić gry w przeglądarce lokalnie z systemu plików. Uruchamianie z edytora udostępnia grę z lokalnego serwera WWW. Możesz na przykład użyć `SimpleHTTPServer` w Pythonie:

```sh
$ python -m SimpleHTTPServer [port]
```


#### P: Dlaczego moja gra kończy się błędem "Unexpected data size" podczas wczytywania?

O: Zwykle zdarza się to, gdy używasz Windows, tworzysz build i zatwierdzasz go w repozytorium Git. Jeśli konfiguracja końców linii w Git jest nieprawidłowa, Git zmieni końce linii, a więc także rozmiar danych. Postępuj zgodnie z tymi instrukcjami, aby rozwiązać problem: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
