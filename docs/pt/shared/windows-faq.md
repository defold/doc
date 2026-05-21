#### P: Por que nós box de GUI sem uma textura ficam transparentes no editor, mas aparecem como esperado quando compilo e executo?

R: Esse erro pode acontecer em [computadores que usam GPUs AMD Radeon](https://github.com/defold/editor2-issues/issues/2723). Certifique-se de atualizar seus drivers gráficos.

#### P: Por que recebo `com.sun.jna.Native.open.class java.lang.Error: Access is denied` ao abrir um atlas ou uma visualização de cena?

R: Tente executar o Defold como administrador. Clique com o botão direito no executável do Defold e selecione "Run as Administrator".

#### P: Por que meu jogo não renderiza corretamente no Windows usando uma GPU integrada Intel UHD (mas minha build HTML5 funciona)?

R: Certifique-se de atualizar seu driver para uma versão maior ou igual a 27.20.100.8280. Verifique com o [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D). Informações adicionais podem ser encontradas [nesta postagem do fórum](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl).

#### P: O editor Defold está travando e o log mostra `AWTError: Assistive Technology not found`

Se o editor travar com um log mencionando `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`, siga estes passos:

* Navegue até `C:\Users\<username>`
* Abra o arquivo chamado `.accessibility.properties` usando um editor de texto padrão (Notepad serve)
* Encontre as seguintes linhas na configuração:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* Adicione uma cerquilha (`#`) na frente dessas linhas
* Salve suas alterações no arquivo e reinicie o Defold
