## Tamanho da heap (HTML5)
O tamanho da heap de um jogo Defold HTML5 pode ser configurado pelo [campo `heap_size`](/manuals/project-settings/#heap-size) em *game.project*. Certifique-se de otimizar o uso de memória do seu jogo e definir um tamanho mínimo de heap.

Para jogos pequenos, 32 MB é um tamanho de heap viável. Para jogos maiores, mire em 64-128 MB. Se, por exemplo, você estiver em 58 MB e não for viável otimizar mais, pode ficar com 64 MB sem pensar demais. Não há um tamanho-alvo rígido; isso depende do jogo. Apenas mire em tamanhos menores, de preferência em passos de potências de dois.

Para verificar o uso atual da heap, você pode iniciar seu jogo, jogar o nível ou seção mais pesado em recursos e monitorar o uso de memória:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

Você também pode abrir as ferramentas de desenvolvedor do seu navegador e escrever o seguinte no console:

```js
HEAP8.length / 1024 / 1024
```

Se o uso de memória permanecer em 32 MB, ótimo! Caso contrário, siga os passos para [otimizar o tamanho da própria engine e de assets grandes, como sons e texturas](/manuals/optimization-size).
