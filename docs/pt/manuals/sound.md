---
title: Som no Defold
brief: Este manual explica como trazer sons para o seu projeto Defold, reproduzi-los e controlá-los.
---

# Som

A implementação de som do Defold é simples, mas poderosa. Há apenas dois conceitos que você precisa conhecer:

Componentes de som
: Esses componentes contêm um som real que deve ser tocado e são capazes de reproduzi-lo.

Grupos de som
: Cada componente de som pode ser designado para pertencer a um _grupo_. Grupos oferecem uma forma fácil de gerenciar sons relacionados de maneira intuitiva. Por exemplo, um grupo "sound_fx" pode ser configurado e qualquer som pertencente a esse grupo pode sofrer ducking com uma simples chamada de função.

## Criando um componente de som

Componentes de som só podem ser instanciados no local em um objeto de jogo. Crie um novo objeto de jogo, clique com o botão direito nele, selecione <kbd>Add Component ▸ Sound</kbd> e pressione *OK*.

![Select component](images/sound/sound_add_component.jpg)

O componente criado tem um conjunto de propriedades que devem ser configuradas:

![Select component](images/sound/sound_properties.png)

*Sound*
: Deve ser definido para um arquivo de som no seu projeto. O arquivo deve estar no formato _Wave_, _Ogg Vorbis_ ou _Ogg Opus_. O Defold suporta arquivos de som salvos com profundidade de 16 bits.

*Looping*
: Se marcado, o som será reproduzido _Loopcount_ vezes ou até ser explicitamente interrompido.

*Loopcount*
: O número de vezes que um som em loop será reproduzido antes de parar (0 significa que o som deve repetir até ser explicitamente interrompido).

*Group*
: O nome do grupo de som ao qual o som deve pertencer. Se essa propriedade ficar vazia, o som será atribuído ao grupo integrado "master".

*Gain*
: Você pode definir o ganho do som diretamente no componente. Isso permite ajustar facilmente o ganho de um som sem voltar ao seu programa de áudio e reexportá-lo. Veja abaixo detalhes sobre como o ganho é calculado.

*Pan*
: Você pode definir o valor de pan do som diretamente no componente. O pan deve ser um valor entre -1 (45 graus à esquerda) e 1 (45 graus à direita).

*Speed*
: Você pode definir o valor de velocidade do som diretamente no componente. Um valor de 1.0 é velocidade normal, 0.5 é metade da velocidade e 2.0 é o dobro da velocidade.


## Reproduzindo o som

Quando você tiver um componente de som configurado corretamente, pode fazê-lo tocar chamando [`sound.play()`](/ref/sound/#sound.play:url-[play_properties]-[complete_function]):

```lua
sound.play("go#sound", {delay = 1, gain = 0.5, pan = -1.0, speed = 1.25})
```

::: sidenote
Um som continuará tocando mesmo que o objeto de jogo ao qual o componente de som pertencia seja excluído. Você pode chamar [`sound.stop()`](/ref/sound/#sound.stop:url) para parar o som (veja abaixo).
:::
Cada mensagem enviada a um componente fará com que ele reproduza outra instância do som, até que o buffer de som disponível fique cheio e a engine imprima erros no console. Recomenda-se implementar algum tipo de mecanismo de bloqueio e agrupamento de som.

## Parando o som

Se quiser parar a reprodução de um som, você pode chamar [`sound.stop()`](/ref/sound/#sound.stop:url):

```lua
sound.stop("go#sound")
```

## Ganho

![Gain](images/sound/sound_gain.png)

O sistema de som tem 4 níveis de ganho:

- O ganho definido no componente de som.
- O ganho definido ao iniciar o som por uma chamada a `sound.play()` ou ao alterar o ganho na voz por uma chamada a `sound.set_gain()`.
- O ganho definido no grupo por uma chamada à função [`sound.set_group_gain()`](/ref/sound#sound.set_group_gain).
- O ganho definido no grupo "master". Isso pode ser alterado com `sound.set_group_gain(hash("master"))`.

O ganho de saída é o resultado da multiplicação desses 4 ganhos. O ganho padrão é 1.0 em todos os lugares (0 dB).

## Grupos de som

Qualquer componente de som com um nome de grupo de som especificado será colocado em um grupo de som com esse nome. Se você não especificar um grupo, o som será atribuído ao grupo "master". Você também pode definir explicitamente o grupo de um componente de som como "master", o que tem o mesmo efeito.

Há algumas funções disponíveis para obter todos os grupos disponíveis, obter o nome em string, obter e definir ganho, rms (veja http://en.wikipedia.org/wiki/Root_mean_square) e pico de ganho. Também há uma função que permite testar se o player de música do dispositivo-alvo está em execução:

```lua
-- Se houver som tocando neste dispositivo iPhone/Android, silencia tudo
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

Os grupos são identificados com um valor hash. O nome em string pode ser recuperado com [`sound.get_group_name()`](/ref/sound#sound.get_group_name), que pode ser usado para exibir nomes de grupos em ferramentas de desenvolvimento, por exemplo um mixer para testar níveis de grupos.

![Sound group mixer](images/sound/sound_mixer.png)

::: important
Você não deve escrever código que dependa do valor em string de um grupo de som, pois esses valores não estão disponíveis em builds release.
:::

Todos os valores são lineares entre 0 e 1.0 (0 dB). Para converter para decibel, basta usar a fórmula padrão:

```math
db = 20 \times \log \left( gain \right)
```

```lua
for i, group_hash in ipairs(sound.get_groups()) do
    -- A string do nome só está disponível em debug. Retorna "unknown_*" em release.
    local name = sound.get_group_name(group_hash)
    local gain = sound.get_group_gain(group_hash)

    -- Converte para decibel.
    local db = 20 * math.log10(gain)

    -- Obtém RMS (ganho Root Mean Square). Canal esquerdo e direito separadamente.
    local left_rms, right_rms = sound.get_rms(group_hash, 2048 / 65536.0)
    left_rmsdb = 20 * math.log10(left_rms)
    right_rmsdb = 20 * math.log10(right_rms)

    -- Obtém pico de ganho. Esquerda e direita separadamente.
    left_peak, right_peak = sound.get_peak(group_hash, 2048 * 10 / 65536.0)
    left_peakdb = 20 * math.log10(left_peak)
    right_peakdb = 20 * math.log10(right_peak)
end

-- Define o ganho master como +6 dB (math.pow(10, 6/20)).
sound.set_group_gain("master", 1.995)
```

## Bloqueando sons

Se o seu jogo toca o mesmo som em um evento e esse evento é disparado com frequência, você corre o risco de tocar o mesmo som duas vezes ou mais quase ao mesmo tempo. Se isso acontecer, os sons ficarão _defasados_, o que pode resultar em artefatos bastante perceptíveis.

![Phase shift](images/sound/sound_phase_shift.png)

A forma mais simples de lidar com esse problema é criar um gate que filtre mensagens de som e não permita que o mesmo som seja reproduzido mais de uma vez dentro de um intervalo definido:

```lua
-- Não permite que o mesmo som seja tocado dentro do intervalo "gate_time".
local gate_time = 0.3

function init(self)
    -- Armazena temporizadores de sons tocados em uma tabela e faz contagem regressiva a cada frame
    -- até que tenham ficado na tabela por "gate_time" segundos. Depois os remove.
    self.sounds = {}
end

function update(self, dt)
    -- Faz contagem regressiva dos temporizadores armazenados
    for k,_ in pairs(self.sounds) do
        self.sounds[k] = self.sounds[k] - dt
        if self.sounds[k] < 0 then
            self.sounds[k] = nil
        end
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("play_gated_sound") then
        -- Toca apenas sons que não estão atualmente na tabela de gating.
        if self.sounds[message.soundcomponent] == nil then
            -- Armazena temporizador do som na tabela
            self.sounds[message.soundcomponent] = gate_time
            -- Toca o som
            sound.play(message.soundcomponent, { gain = message.gain })
        else
            -- Uma tentativa de tocar um som foi bloqueada
            print("gated " .. message.soundcomponent)
        end
    end
end
```

Para usar o gate, basta enviar a ele uma mensagem `play_gated_sound` e especificar o componente de som alvo e o ganho do som. O gate chamará `sound.play()` com o componente de som alvo se o gate estiver aberto:

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1", gain = 1.0 })
```

::: important
Não funciona fazer o gate escutar mensagens `play_sound`, pois esse nome é reservado pela engine Defold. Você terá comportamento inesperado se usar nomes de mensagens reservados.
:::


## Manipulação em tempo de execução
Você pode manipular sons em tempo de execução por meio de várias propriedades diferentes (consulte a [documentação da API para uso](/ref/sound/)). As seguintes propriedades podem ser manipuladas usando `go.get()` e `go.set()`:

`gain`
: O ganho do componente de som (`number`).

`pan`
: O pan do componente de som (`number`). O pan deve ser um valor entre -1 (45 graus à esquerda) e 1 (45 graus à direita).

`speed`
: A velocidade do componente de som (`number`). Um valor de 1.0 é velocidade normal, 0.5 é metade da velocidade e 2.0 é o dobro da velocidade.

`sound`
: O caminho do recurso para o som (`hash`). Você pode usar o caminho do recurso para alterar o som usando `resource.set_sound(path, buffer)`. Exemplo:

```lua
local boom = sys.load_resource("/sounds/boom.wav")
local path = go.get("#sound", "sound")
resource.set_sound(path, boom)
```


## Configuração do projeto

O arquivo *game.project* tem algumas [configurações do projeto](/manuals/project-settings#sound) relacionadas a componentes de som.

## Streaming de som

Também é possível oferecer suporte a [streaming de sons](/manuals/sound-streaming)
