#### P: Por que meu aplicativo HTML5 congela na tela inicial no Chrome?

R: Em alguns casos, não é possível rodar um jogo localmente no navegador a partir do sistema de arquivos. Ao rodar pelo editor, o jogo é servido a partir de um servidor web local. Você pode, por exemplo, usar `SimpleHTTPServer` em Python:

```sh
$ python -m SimpleHTTPServer [port]
```


#### P: Por que meu jogo trava com o erro "Unexpected data size" durante o carregamento?

R: Isso geralmente acontece quando você está usando Windows, faz uma build e a commita no Git. Se você tiver uma configuração errada de finais de linha no Git, ele mudará seus finais de linha e, portanto, também o tamanho dos dados. Siga estas instruções para resolver o problema: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
