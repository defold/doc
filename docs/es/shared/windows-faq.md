#### Q: ¿Por qué los nodos caja de GUI sin textura son transparentes en el editor, pero aparecen como se espera cuando creo una build y la ejecuto?

A: Este error puede ocurrir en [computadoras con GPU AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Asegúrate de actualizar los drivers gráficos.

#### Q: ¿Por qué recibo `com.sun.jna.Native.open.class java.lang.Error: Access is denied` al abrir un atlas o una vista de escena?

A: Intenta ejecutar Defold como administrador. Haz click derecho en el ejecutable de Defold y selecciona "Run as Administrator".

#### Q: ¿Por qué mi juego no se renderiza correctamente en Windows usando una GPU integrada Intel UHD (pero mi build HTML5 funciona)?

A: Asegúrate de actualizar tu driver a una versión mayor o igual que 27.20.100.8280. Compruébalo con el [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Puedes encontrar información adicional en [esta publicación del foro](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### Q: El editor Defold se bloquea y el log muestra `AWTError: Assistive Technology not found`

A: Si el editor se bloquea y el log menciona `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, sigue estos pasos:

* Navega a `C:\Users\<username>`
* Abre el archivo llamado `.accessibility.properties` con un editor de texto estándar (Notepad está bien)
* Busca las siguientes líneas en la configuración:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Agrega un signo de numeral (`#`) delante de estas líneas
* Guarda los cambios en el archivo y reinicia Defold
