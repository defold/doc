#### Q: Почему моё HTML5-приложение зависает на splash screen в Chrome?

A: В некоторых случаях невозможно запустить игру в браузере локально прямо из файловой системы. При запуске из редактора игра раздаётся через локальный web server. Например, можно использовать `SimpleHTTPServer` в Python:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: Почему моя игра падает с ошибкой "Unexpected data size" во время загрузки?

A: Обычно это происходит, если вы используете Windows, делаете сборку и коммитите её в Git. Если в Git неправильно настроены окончания строк, он изменит line endings и, как следствие, размер данных. Чтобы решить проблему, следуйте этим инструкциям: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
