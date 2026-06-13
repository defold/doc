---
title: Mensagens de colisão no Defold
brief: Quando dois objetos colidem, a engine chamará o callback de evento ou transmitirá mensagens.
---

# Mensagens de colisão

Quando dois objetos colidem, a engine enviará um evento para o callback de evento ou transmitirá mensagens para ambos os objetos.

## Filtragem de eventos

Os tipos de eventos gerados podem ser controlados usando as flags de cada objeto:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Todas elas são `true` por padrão.
Quando dois objetos de colisão interagem, verificamos se devemos enviar uma mensagem ao usuário, dadas essas caixas de seleção.

Por exemplo, considerando as caixas de seleção "Generate Contact Events":

Ao usar `physics.set_event_listener()`:

| Componente A | Componente B | Enviar mensagem |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | Sim          |
| ❌          | ✅︎          | Sim          |
| ✅︎          | ❌          | Sim          |
| ❌          | ❌          | Não          |

Ao usar o tratador de mensagens padrão:

| Componente A | Componente B | Enviar mensagem(ns) |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Sim (A,B) + (B,A) |
| ❌          | ✅︎          | Sim (B,A)         |
| ✅︎          | ❌          | Sim (A,B)         |
| ❌          | ❌          | Não               |

## Resposta de colisão

A mensagem `"collision_response"` é enviada quando um dos objetos em colisão é do tipo "dynamic", "kinematic" ou "static". Ela tem os seguintes campos definidos:

`other_id`
: o id da instância com a qual o objeto de colisão colidiu (`hash`)

`other_position`
: a posição mundial da instância com a qual o objeto de colisão colidiu (`vector3`)

`other_group`
: o grupo de colisão do outro objeto de colisão (`hash`)

`own_group`
: o grupo de colisão do objeto de colisão (`hash`)

A mensagem `collision_response` só é adequada para resolver colisões em que você não precisa de detalhes sobre a interseção real dos objetos, por exemplo, se quiser detectar se uma bala atinge um inimigo. Apenas uma dessas mensagens é enviada para qualquer par de objetos em colisão a cada frame.

```Lua
function on_message(self, message_id, message, sender)
    -- verifica a mensagem
    if message_id == hash("collision_response") then
        -- executa uma ação
        print("I collided with", message.other_id)
    end
end
```

## Resposta de ponto de contato

A mensagem `"contact_point_response"` é enviada quando um dos objetos em colisão é do tipo "dynamic" ou "kinematic" e o outro é do tipo "dynamic", "kinematic" ou "static". Ela tem os seguintes campos definidos:

`position`
: posição mundial do ponto de contato (`vector3`).

`normal`
: normal em espaço mundial do ponto de contato, que aponta do outro objeto em direção ao objeto atual (`vector3`).

`relative_velocity`
: a velocidade relativa do objeto de colisão conforme observada a partir do outro objeto (`vector3`).

`distance`
: a distância de penetração entre os objetos, não negativa (`number`).

`applied_impulse`
: o impulso resultante do contato (`number`).

`life_time`
: (*não usado atualmente!*) tempo de vida do contato (`number`).

`mass`
: a massa do objeto de colisão atual em kg (`number`).

`other_mass`
: a massa do outro objeto de colisão em kg (`number`).

`other_id`
: o id da instância com a qual o objeto de colisão está em contato (`hash`).

`other_position`
: a posição mundial do outro objeto de colisão (`vector3`).

`other_group`
: o grupo de colisão do outro objeto de colisão (`hash`).

`own_group`
: o grupo de colisão do objeto de colisão (`hash`).

Para um jogo ou aplicação em que você precisa separar objetos perfeitamente, a mensagem `"contact_point_response"` fornece todas as informações necessárias. No entanto, observe que, para qualquer par de colisão específico, várias mensagens `"contact_point_response"` podem ser recebidas a cada frame, dependendo da natureza da colisão. Consulte [Resolvendo colisões para mais informações](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- verifica a mensagem
    if message_id == hash("contact_point_response") then
        -- executa uma ação
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Resposta de gatilho

A mensagem `"trigger_response"` é enviada quando um dos objetos em colisão é do tipo "trigger". A mensagem será enviada uma vez quando a colisão for detectada pela primeira vez e mais uma vez quando os objetos deixarem de colidir. Ela tem os seguintes campos:

`other_id`
: o id da instância com a qual o objeto de colisão colidiu (`hash`).

`enter`
: `true` se a interação foi uma entrada no gatilho, `false` se foi uma saída. (`boolean`).

`other_group`
: o grupo de colisão do outro objeto de colisão (`hash`).

`own_group`
: o grupo de colisão do objeto de colisão (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- verifica a mensagem
    if message_id == hash("trigger_response") then
        if message.enter then
            -- executa ação de entrada
            print("I am now inside", message.other_id)
        else
            -- executa ação de saída
            print("I am now outside", message.other_id)
        end
    end
end
```
