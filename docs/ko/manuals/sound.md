# Sound
이 메뉴얼은 Defold 프로젝트로 사운드를 가져와 재생하고 제어하는 방법에 대하 성멸합니다.

Defold의 사운드 구현은 간단하지만 강력합니다.  알아 두어야 할 개념은 두 가지 뿐입니다.

#### Sound components
이 컴포넌트는 소리를 재생하기 위한 실제 사운드를 포함하고 있습니다.

#### Sound groups
각 사운드 컴포넌트를 그룹에 속하도록 지정할 수도 있습니다. 그룹을 사용하여 소속된 사운드들을 직관적인 방법으로 쉽게 관리할 수 있습니다. 예를 들어, "sound_fx" 같은 그룹을 만들어 간단한 함수 호출로 다른 그룹의 사운드들을 소리가 작아지게 할 수 있습니다.

## Creating a sound component
사운드 컴포넌트는 게임 오브젝트의 내장 오브젝트로만 만들 수 있습니다. 새 게임 오브젝트를 만들고 오른쪽 클릭하고 **Add Component**를 선택합니다. **Sound**를 선택하고 **OK**를 누르세요.

![Select component](images/sound/sound_select_component.png)

생성된 컴포넌트에는 아래와 같은 속성들이 있습니다.

#### Sound
Sound는 프로젝트에 있는 사운드 파일로 설정되며 Wave나 Ogg Vorbis 포멧을 지원합니다. (자세한 내용은  http://en.wikipedia.org/wiki/WAV 와 http://en.wikipedia.org/wiki/Vorbis 참고)

#### Looping
체크되어 있다면 직접적으로 중단 시킬때 까지 재생이 반복됩니다.

#### Gain
이 컴포넌트에서 사운드의 게인(gain)을 직접 설정할 수 있습니다. 이를 통해 사운드 편집 프로그램으로 되돌아가서 재작업하고 다시 익스포트하는 과정없이 쉽게 게인(gain)을 조절하게 해 줍니다. 어떻게 게인(gain)이 계산되는지 자세히 알려면 아래를 참고하십시오.

#### Group
사운드가 속할 사운드 그룹의 이름입니다. 이 속성값이 비어있다면, 사운드는 기본적으로 "master" 그룹에 할당됩니다.

![Create component](images/sound/sound_create_component.png)

## Gain
![Gain](images/sound/sound_gain.png)

사운드 시스템은 4가지 단계로 게인(gain)을 계산하여 처리합니다.

1. 사운드 컴포넌트에서 셋팅된 게인(gain)
2. "play_sound" 메세지를 통해 셋팅되거나 "set_gain" 메세지를 통해 변경되는 게인(gain)
3. sound.set_group_gain() 함수를 호출해서 그룹에 셋팅되는 게인(gain)
4. "master" 그룹에 셋팅된 게인(gain). 이는 sound.set_group_gain(hash("master")) 로 변경 가능

위의 4단계의 게인(gain)을 곱하여 최총 출력 게인(gain)을 계산합니다. 기본 게인(gain)은 어디에서나 1.0입니다. (0 dB)

## Sound groups
사운드 그룹의 이름이 지정된 사운드 컴포넌트는 해당 이름의 사운드 그룹에 속하게 됩니다. 만약 그룹을 지정하지 않았다면 기본적으로 "master" 그룹에 할당됩니다. 또한 사운드 컴포넌트의 그룹을 명시적으로 "master" 그룹을 지정해도 됩니다.

몇 함수는 사용가능한 모든 그룹을 가져와 그룹의 이름을 알아내고 게인(gain), rms( http://en.wikipedia.org/wiki/Root_mean_square 참고), 피크 게인(peak gain)을 얻거나 설정할 수 있습니다. 또한 대상 디바이스의 음악 플레이어가 실행중인지 테스트하는 함수도 있습니다.

```lua
-- 아이폰이나 안드로이드 디바이스에서 사운드가 플레이 중이라면, 모든 소리를 줄여버림
if sound.is_music_playing() then
    for i, group_hash in ipairs(sound.get_groups()) do
        sound.set_group_gain(group_hash, 0)
    end
end
```

이 그룹들은 해쉬(hash) 값으로 식별됩니다. 문자열로 된 이름은 sound.get_group_name() 을 사용하여 가져올 수 있으며 이 이름은 개발도구에서 사운드 그룹 이름을 표시해야할 경우 사용될 수 있습니다. (예들 들어 사운드를 조절하는 믹서 등)

![Sound group mixer](images/sound/sound_mixer.png)

> 릴리즈된 빌드에서는 사용할 수 없으므로 사운드 그룹의 문자열값에 의존하는 코드를 작성하면 안됩니다.

모든 값은 0과 1.0(0 dB) 사이의 값입니다. 데시벨로 변환하려면, 간단하게 db = 20 * math.log10(gain) 표준공식을 사용하면 됩니다.

```lua
for i, group_hash in ipairs(sound.get_groups()) do
    -- 문자열 이름은 디버그 빌드에서만 사용가능함. 릴리즈빌드에선 "unknown_*"라고 반환됨
    local name = sound.get_group_name(group_hash)
    local gain = sound.get_group_gain(group_hash)

    -- 데시벨로 변환하기
    local db = 20 * math.log10(gain)

    -- RMS (gain Root Mean Square) 얻기. 왼쪽 오른쪽 채널 분리
    local left_rms, right_rms = sound.get_rms(group_hash, 2048 / 65536.0)
    left_rmsdb = 20 * math.log10(left_rms)
    right_rmsdb = 20 * math.log10(right_rms)

    -- gain peak 얻기. 왼쪽 오른쪽으로 분리
    left_peak, right_peak = sound.get_peak(group_hash, 2048 * 10 / 65536.0)
    left_peakdb = 20 * math.log10(left_peak)
    right_peakdb = 20 * math.log10(right_peak)
end

-- master gain을 +6 dB 로 설정하기 (math.pow(10, 6/20))
sound.set_group_gain("master", 1.995)
```

## Gating sounds
만약 게임이 특정 이벤트마다 동일한 사운드로 재생되고 이 이벤트가 자주 트리거 된다면, 동일 사운드를 거의 동시에 재생되어 버리는 문제가 발생합니다. 눈에 띄는 현상으로는 위상 변이(phase-shift ) 현상이 생기는 문제가 있습니다.

![Phase shift](images/sound/sound_phase_shift.png)

이 문제를 해결하는 가장 쉬운 방법은 사운드 메세지를 필터링하는 기능(gate)을 만들어 특정 시간 간격 내에서는 동일한 사운드가 재생되는 것을 막는 방법이 있습니다.

```lua
-- gate_time 시간 내에서 동일한 사운드가 재생되는걸 막자
local gate_time = 0.3

function init(self)
    -- 재생된 사운드의 타이머들을 테이블로 관리하고 매 프레임마다 "gate_time" 초가 될 때까지 카운트 다운함. 그리고 나서 삭제
    self.sounds = {}
end

function update(self, dt)
    -- 저장된 타이머들을 카운트 다운 함
    for k,_ in pairs(self.sounds) do
        self.sounds[k] = self.sounds[k] - dt
        if self.sounds[k] < 0 then
            self.sounds[k] = nil
        end
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("play_gated_sound") then
        -- 현재 게이팅 테이블(gating table)에 없는 사운드만 재생하자
        if self.sounds[message.soundcomponent] == nil then
            -- 테이블에 사운드 타이머를 저장함
            self.sounds[message.soundcomponent] = gate_time
            sound.play(message.soundcomponent, { gain = message.gain })
        else
            -- 재생하려는 사운드를 막았음
            print("gated " .. message.soundcomponent)
        end
    end
end
```

게이트(gate)를 사용하려면, 간단히 "play_gated_sound" 메세지에 타겟 사운드 컴포넌트와 사운드 게인(gain)을 지정해서 전송하면 됩니다. 이 게이트는 게이트가 열려 있다면 "play_sound" 메세지를 타겟 사운드 컴포넌트로 보내게 됩니다.

```lua
msg.post("/sound_gate#script", "play_gated_sound", { soundcomponent = "/sounds#explosion1, gain = 1.0 })
```

> "play_sound"는 Defold 엔진에 의해 예약된 이름이므로 게이트는 이 메세지를 들을 수 없습니다. 예약된 메세지 이름을 사용하면 예기치 않은 동작이 발생할 수 있습니다.
