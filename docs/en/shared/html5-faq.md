#### Q: Why does my HTML5-app freeze at the splash screen in Chrome?

A: In some cases it is not possible to run a game in the browser locally from the filesystem. Running from the editor serves the game from a local web server. You can, for instance, use SimpleHTTPServer in Python:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: Why does my game crash with error "Unexpected data size" while loading?

A: This usually happens when you are using Windows and make a build and commit it to Git. If you have the wrong line-ending configuration in Git it will change your line endings and thus also the data size. Follow these instructions to solve the problem: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
