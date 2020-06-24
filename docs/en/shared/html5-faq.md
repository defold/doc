### Q: Why does my HTML5-app freeze at the splash screen in Chrome?

A: In some cases it is not possible to run a game in the browser locally from the filesystem. Running from the editor serves the game from a local web server. You can, for instance, use SimpleHTTPServer in Python:

```sh
$ python -m SimpleHTTPServer [port]
```
