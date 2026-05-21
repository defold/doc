---
title: Eventos de colisão no Defold
brief: O tratamento de eventos de colisão pode ser centralizado usando `physics.set_event_listener()` para direcionar todas as mensagens de colisão e interação a uma única função especificada.
---

# Tratamento de eventos de física no Defold

Anteriormente, interações de física no Defold eram tratadas transmitindo mensagens para todos os componentes dos objetos em colisão. No entanto, a partir da versão 1.6.4, o Defold oferece uma abordagem mais centralizada por meio da função `physics.set_event_listener()`. Essa função permite definir um listener personalizado para tratar todos os eventos de interação de física em um único lugar, simplificando seu código e melhorando a eficiência.

## Definindo o listener do mundo de física

No Defold, cada proxy de coleção cria seu próprio mundo de física separado. Portanto, ao trabalhar com vários proxies de coleção, é essencial gerenciar os mundos de física distintos associados a cada um. Para garantir que os eventos de física sejam tratados corretamente em cada mundo, você deve definir um listener de mundo de física especificamente para o mundo de cada proxy de coleção.

Essa configuração significa que o listener de eventos de física deve ser definido de dentro do contexto da coleção que o proxy representa. Ao fazer isso, você associa o listener diretamente ao mundo de física relevante, permitindo que ele processe eventos de física com precisão.

Aqui está um exemplo de como definir um listener de mundo de física dentro de um proxy de coleção:

```lua
function init(self)
    -- Supondo que este script esteja anexado a um objeto de jogo dentro da coleção carregada pelo proxy
    -- Define o listener do mundo de física para o mundo de física deste proxy de coleção
    physics.set_event_listener(physics_world_listener)
end
```

Ao implementar esse método, você garante que cada mundo de física gerado por um proxy de coleção tenha seu listener dedicado. Isso é crucial para tratar eventos de física de forma eficaz em projetos que utilizam vários proxies de coleção.

::: important
Se um listener for definido, [mensagens de física](/manuals/physics-messages) não serão mais enviadas para o mundo de física onde esse listener está definido.
:::

## Estrutura de dados dos eventos

Cada evento de física fornece uma tabela `data` contendo informações específicas relevantes para o evento.

1. **Evento de ponto de contato (`contact_point_event`):**
Este evento relata um ponto de contato entre dois objetos de colisão. Ele é útil para tratamento detalhado de colisões, como calcular forças de impacto ou respostas de colisão personalizadas.

   - `applied_impulse`: O impulso resultante do contato.
   - `distance`: A distância de penetração entre os objetos.
   - `a` e `b`: Objetos que representam as entidades em colisão, cada um contendo:
     - `position`: Posição mundial do ponto de contato (`vector3`).
     - `instance_position`: Posição mundial da instância do objeto de jogo (`vector3`).
     - `id`: ID da instância (`hash`).
     - `group`: Grupo de colisão (`hash`).
     - `relative_velocity`: Velocidade relativa ao outro objeto (`vector3`).
     - `mass`: Massa em quilogramas (`number`).
     - `normal`: Normal de contato, apontando a partir do outro objeto (`vector3`).

2. **Evento de colisão (`collision_event`):**
Este evento indica que ocorreu uma colisão entre dois objetos. É um evento mais geral em comparação ao evento de ponto de contato, ideal para detectar colisões sem precisar de informações detalhadas sobre os pontos de contato.

   - `a` e `b`: Objetos que representam as entidades em colisão, cada um contendo:
     - `position`: Posição mundial (`vector3`).
     - `id`: ID da instância (`hash`).
     - `group`: Grupo de colisão (`hash`).

3. **Evento de gatilho (`trigger_event`):** 
Este evento é enviado quando um objeto interage com um objeto gatilho. Ele é útil para criar áreas no seu jogo que fazem algo acontecer quando um objeto entra ou sai.

   - `enter`: Indica se a interação foi uma entrada (`true`) ou uma saída (`false`).
   - `a` e `b`: Objetos envolvidos no evento de gatilho, cada um contendo:
     - `id`: ID da instância (`hash`).
     - `group`: Grupo de colisão (`hash`).

4. **Resposta de ray cast (`ray_cast_response`):**
Este evento é enviado em resposta a um raycast, fornecendo informações sobre o objeto atingido pelo raio.

   - `group`: Grupo de colisão do objeto atingido (`hash`).
   - `request_id`: Identificador da requisição de raycast (`number`).
   - `position`: Posição atingida (`vector3`).
   - `fraction`: A fração do comprimento do raio em que o acerto ocorreu (`number`).
   - `normal`: Normal na posição atingida (`vector3`).
   - `id`: ID da instância do objeto atingido (`hash`).

5. **Ray cast sem acerto (`ray_cast_missed`):**
Este evento é enviado quando um raycast não atinge nenhum objeto.

   - `request_id`: Identificador da requisição de raycast que não acertou (`number`).

## Exemplo de uso

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Trata dados detalhados de ponto de contato
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Trata dados gerais de colisão
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Trata dados de interação de gatilho
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Trata dados de acerto de raycast
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Trata dados de raycast sem acerto
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Limitações

O listener é chamado de forma síncrona no momento em que o evento ocorre. Isso acontece no meio de um timestep, o que significa que o mundo de física está bloqueado. Isso torna impossível usar funções que possam afetar simulações do mundo de física, por exemplo, `physics.create_joint()`.

Aqui está um pequeno exemplo de como evitar essas limitações:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- preenche a mensagem da mesma forma como os argumentos devem ser passados para `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- envia mensagem para o próprio objeto
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- desempacota a mensagem com os argumentos da função
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
