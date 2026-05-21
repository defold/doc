---
title: Resolvendo colisões cinemáticas no Defold
brief: Este manual explica como resolver colisões de física cinemáticas.
---

# Resolvendo colisões cinemáticas

Usar objetos de colisão cinemáticos exige que você resolva colisões por conta própria e mova os objetos como reação. Uma implementação ingênua para separar dois objetos em colisão se parece com isto:

```lua
function on_message(self, message_id, message, sender)
  -- Trata colisão
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Esse código separará seu objeto cinemático de outro objeto de física que ele penetra, mas a separação frequentemente passa do ponto e você verá jitter em muitos casos. Para entender melhor o problema, considere o seguinte caso em que um personagem do jogador colidiu com dois objetos, *A* e *B*:

![Physics collision](images/physics/collision_multi.png)

A engine de física enviará várias mensagens `"contact_point_response"`, uma para o objeto *A* e uma para o objeto *B*, no frame em que a colisão ocorre. Se você mover o personagem em resposta a cada penetração, como no código ingênuo acima, a separação resultante seria:

- Mover o personagem para fora do objeto *A* de acordo com sua distância de penetração (a seta preta)
- Mover o personagem para fora do objeto *B* de acordo com sua distância de penetração (a seta preta)

A ordem dessas operações é arbitrária, mas o resultado é o mesmo de qualquer forma: uma separação total que é a *soma dos vetores de penetração individuais*:

![Physics separation naive](images/physics/separation_naive.png)

Para separar corretamente o personagem dos objetos *A* e *B*, você precisa tratar a distância de penetração de cada ponto de contato e verificar se separações anteriores já resolveram a separação, total ou parcialmente.

Suponha que a primeira mensagem de ponto de contato venha do objeto *A* e que você mova o personagem para fora pelo vetor de penetração de *A*:

![Physics separation step 1](images/physics/separation_step1.png)

Então o personagem já foi parcialmente separado de *B*. A compensação final necessária para realizar a separação completa do objeto *B* é indicada pela seta preta acima. O comprimento do vetor de compensação pode ser calculado projetando o vetor de penetração de *A* sobre o vetor de penetração de *B*:

![Projection](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

O vetor de compensação pode ser encontrado reduzindo o comprimento de *B* por *l*. Para calcular isso para um número arbitrário de penetrações, você pode acumular a correção necessária em um vetor para cada ponto de contato, começando com um vetor de correção de comprimento zero:

1. Projete a correção atual contra o vetor de penetração do contato.
2. Calcule qual compensação resta do vetor de penetração (conforme a fórmula acima).
3. Mova o objeto pelo vetor de compensação.
4. Adicione a compensação à correção acumulada.

Uma implementação completa se parece com isto:

```lua
function init(self)
  -- vetor de correção
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- redefine a correção
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Trata colisão
  if message_id == hash("contact_point_response") then
    -- Obtém as informações necessárias para sair da colisão. Podemos
    -- receber vários pontos de contato de volta e ter que calcular
    -- como sair de todos eles acumulando um
    -- vetor de correção para este frame:
    if message.distance > 0 then
      -- Primeiro, projeta a correção acumulada sobre
      -- o vetor de penetração
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Considera apenas projeções que não passam do ponto.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Aplica compensação
        go.set_position(go.get_position() + comp)
        -- Acumula a correção feita
        self.correction = self.correction + comp
      end
    end
  end
end
```
