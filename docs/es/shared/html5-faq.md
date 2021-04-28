#### Q: ¿Por qué mi aplicación HTML5 se congela en la pantalla splash en Chrome?

A: En algunos casos no es posible correr un juego en el navegador de manera local desde el sistema de archivos. Correr desde el editor sirve el juego desde un servidor web local. Puedes, por ejemplo, utilizar SimpleHTTPServer en Python:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: ¿Por qué mi juego crashea con el error "Unexpected data size" mientras carga?

A: Esto usualmente pasa cuando estás usando Windows y creas una build y lo cometes en Git. Si tienes la configuración line-ending equivocada en Git puede cambiar tus finales de líneas y por lo tanto el tamaño de la data. Sigue estas instrucciones para resolver el problema: https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings
