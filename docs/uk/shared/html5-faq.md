#### П: Чому мій застосунок HTML5 зависає на заставці в Chrome? {#q-why-does-my-html5-app-freeze-at-the-splash-screen-in-chrome}

В: У деяких випадках гру неможливо запустити в браузері безпосередньо з локальної файлової системи. Під час запуску з редактора гра обслуговується локальним вебсервером. Ви можете, наприклад, скористатися `SimpleHTTPServer` у Python:

```sh
$ python -m SimpleHTTPServer [port]
```


#### П: Чому моя гра аварійно завершується з помилкою "Unexpected data size" під час завантаження? {#q-why-does-my-game-crash-with-error-unexpected-data-size-while-loading}

В: Зазвичай це трапляється, коли ви створюєте збірку у Windows і додаєте її до Git. Якщо завершення рядків у Git налаштовано неправильно, Git змінюватиме їх, а отже, і розмір даних. Щоб розв’язати проблему, дотримуйтеся цих інструкцій: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
