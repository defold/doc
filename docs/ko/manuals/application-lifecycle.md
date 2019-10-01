# Application lifecycle
이 문서는 Defold의 게임과 어플리케이션의 라이프사이클에 대해 자세히 알아봅니다.

Defold의 어플리케이션이나 게임의 라이프사이클은 매우 단순합니다. 엔진은 초기화(initialization), 업데이트 루프(update loop: 여기서 대부분의 시간이 소비됨), 마무리(finalization) 세 단계로 진행합니다.

![Lifecycle overview](images/application_lifecycle/application_lifecycle_overview.png)

대부분의 경우엔 Defold 내부 동작의 기본적인 이해만 해도 되지만, 이 작업의 정확한 순서를 이해하지 못하면 난관에 빠질 수도 있습니다. 이 문서는 게임엔진이 어떻게 어플리케이션을 시작부터 끝까지 실행하는지 설명합니다

어플리케이션은 엔진을 실행하는데 필요한 모든 것을 초기화(initialization)하면서 시작합니다. main 컬렉션을 로드하고 init() Lua 함수가 존재하는 로드된 모든 컴포넌트(스크립트 컴포넌트나 GUI스크립트가 있는 GUI 컴포넌트)들의 init() 함수를 호출합니다. 이를 통해 커스텀하게 초기화를 할 수 있습니다.

다음으로 어플리케이션은 업데이트 루프(update loop)에 진입해서 어플리케이션 생명주기 대부분을 머물게 됩니다. 매 프레임마다, 추가된 게임 오브젝트와 컴포넌트들이 업데이트 되며 스크립트나 GUI 스크립트에서는 update() 함수가 호출됩니다. 업데이트가 반복되는 동안 메세지는 수신자 측에 발송되며, 사운드를 플레이하고 그래픽을 렌더링 합니다.

어플리케이션 라이프사이클을 종료해야 하는 특정 시점에서는 어플리케이션을 종료하기 직전에 엔진은 업데이트 루프 단계를 빠져나와 마무리(finalization) 단계로 진입합니다. 여기서 로드된 모든 게임 오브젝트의 삭제를 준비하게 됩니다. 모든 오브젝트 컴포넌트의 final() 함수가 호출되므로 여기서 커스텀한 리소스 해제 작업을 할 수 있습니다. 모든 오브젝트가 삭제된 후 main 컬렉션도 언로드 됩니다.

## Initialization

![Lifecycle overview](images/application_lifecycle/application_lifecycle_init.png)

이 다이어그램은 초기화 단계를 더 자세히 설명하고 있습니다. 이 단계의 더 정확한 설명을 위해 라이프 사이클과 관련이 있는 "dispatch messages" 단계("spawn dynamic objects"단계 바로 직전에 호출됨)에 대한 자세한 설명을 오른쪽 블록에 배치했습니다.

사실, main컬렉션이 로드되기 전 초기화 동안 엔진이 내부적으로 수행하는 단계는 훨씬 많습니다. 메모리 프로파일러, 소켓, 그래픽, HID(인풋 디바이스), 사운드, 물리 등등의 많은 것들을 설정하고 "game.project" 같은 어플리케이션 설정값을 또한 로드 후 처리하는 작업을 수행합니다.

엔진의 초기화가 끝난 후 사용자가 맨처음으로 직접 제어할 수 있는 진입점은 렌더 스크립트의 init() 함수입니다.

main 컬렉션이 로드되고 초기화 되면 컬렉션의 모든 게임 오브젝트는 자신의 transform 정보(위치(position), 이동(movement), 회전(rotation), 확대축소(scaling))를 자식들에게 반영합니다. 컴포넌트에 init() 함수가 있다면 호출됩니다.

> 게임오브젝트 컴포넌트의 init() 함수가 호출되는 순서는 정해진 것이 없으므로 게임엔진이 동일한 컬렉션에 속한 오브젝트들을 특정한 순서로 초기화 할거라고 미리 예측하여 개발하지 않는 것이 좋습니다.

init() 함수 이후에는 새 메세지를 보낼 수도 있고, 팩토리가 새 오브젝트를 스폰되게 할 수도 있고, 삭제하려는 오브젝트에 마킹 작업을 하기도 하고 엔진이 다음 "post-update" 단계를 수행하기 위해 정리 작업을 할 수도 있습니다.  여기서는 메세지를 디스패치하고 팩토리를 사용하여 게임 오브젝트를 스폰하고 오브젝트를 삭제하는 작업을 합니다.

post-update 단계에는 메세지 큐를 보낼 뿐만아니라 또한 메세지가 컬렉션 프록시로 전송되는 일을 다루는 "dispatch messages" 단계를 포함하고 있다는 것을 알아두기 바랍니다. 이 단계가 수행되는 동안은 proxy를 통하여(활성화, 비활성화, 로딩, 언로딩을 위한 마킹작업 등) 하위 작업들이 업데이트 됩니다.

위의 다이어그램을 살펴보면, init() 하는 동안에 [컬렉션 프록시(Collection proxy)](/manuals/collection-proxy)를 로드하고 프록시의 모든 오브젝트들을 초기화하고 프록시의 컬렉션을 언로드하는 것이 가능하다는 것을 알 수 있습니다. 이 모든 것이 컴포넌트의 update()가 처음 호출되기 이전에 발생합니다. 즉 엔진이 모든 초기화(initialization) 단계를 빠져나가서 업데이트 반복(update loop) 단계로 진입하기 이전입니다:

```lua
function init(self)
        print("init()")
        msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- 이 코드까지 도달하기 전에 프록시 컬렉션이 언로드됨
    print("update()")
end

function on_message(self, message_id, message, sender)
        if message_id == hash("proxy_loaded") then
                print("proxy_loaded. Init, enable and then unload.")
                msg.post("#collectionproxy", "init")
                msg.post("#collectionproxy", "enable")
                msg.post("#collectionproxy", "unload")
                -- 이 오브젝트의 update()가 호출되기 이전에
                -- 프록시컬렉션의 init()과 final()이 호출됨
          end
end
```

## The update loop
업데이트 루프는 매 프레임 마다 한 번씩 긴 시퀀스로 실행됩니다. 명확한 이해를 위해 아래 그림에선 이 업데이트 시퀀스를 논리적인 시퀀스 블록으로 구분했습니다. 또한 "Dispatch messages" 블록도 같은 이유로 분리해서 보여줍니다:

![Update loop](images/application_lifecycle/application_lifecycle_update.png)

#### Input
입력(input)은 사용 가능한 디바이스로부터 읽혀지며, [인풋 바인딩(input binding)](/manuals/input)에 대해 매핑되어 디스패치 됩니다. 입력 포커스를 획득한 게임 오브젝트는 사용자의 입력을 받아 on_input() 함수가 있는 모든 컴포넌트에게 전송합니다. 스크립트 컴포넌트와 GUI스크립트가 있는 GUI컴포넌트를 사용하는 게임 오브젝트가 입력을 받아 이들 컴포넌트의 on_input() 함수로 보냅니다.

입력 포커스를 획득하고 컬렉션 프록시 컴포넌트를 포함하고 있는 게임오브젝트는 프록시 컬렉션에 있는 컴포넌트들에게 까지 입력을 전달합니다. 이 프로세스는 활성화된 컬렉션 프록시들을 따라 재귀적으로 반복되어 전달됩니다.

#### Update
main 컬렉션의 각 게임 오브젝트 컴포넌트 순환하며 수행됩니다. 만약 컴포넌트의 스크립트에 update()함수를 선언했다면 이 함수를 호출해 줍니다. 또한 컴포넌트가 컬렉션 프록시라면 이 프록시의 컬렉션 안에 있는 각 컴포넌트는 재귀적으로 업데이트 되어 위 다이어그램의 "update" 시퀀스의 모든 단계를 수행합니다.

> 게임오브젝트 컴포넌트의 update() 함수가 호출되는 순서는 정해진 것이 없으므로 게임엔진이 동일한 컬렉션에 속한 오브젝트들을 특정한 순서로 초기화 할거라고 미리 예측하여 개발하지 않는 것이 좋습니다.

다음 단계에선 게시된 모든 메세지가 전달(dispatch)됩니다. 수신 컴포넌트의 on_message() 코드는 추가적인 메세지를 게시할 수 있으므로 메세지 전달자(message dispatcher)는 메세지 큐가 다 비워질 때 까지 게시된 메세지를 전달하는 작업을 지속합니다. 그러나 메세지 전달자가 수행 가능한 횟수에는 성능상 한계가 있습니다. [메세지 전달(Message passing)](/manuals/message-passing) 문서의 "Advanced topics" 섹션을 참고 바랍니다.

충돌(collision) 오브젝트 컴포넌트의 경우엔, 물리 메세지(collisions, triggers, ray_cast 등을 처리함)가 게임오브젝트가 영향을 주는 주변 오브젝트의 스크립트에 쓰인 on_message() 함수로 전달됩니다.

다음으로는 게임 오브젝트의 이동, 회전, 확대/축소 작업을 각기 컴포넌트와 자식 게임 오브젝트의 컴포넌트 들에게 반영시키는 것으로 변형(transform)을 완료합니다.

#### Render update
렌더 업데이트 블록은 메세지들을 @render 소켓(오브젝트 URL의 socket, 네트워크 소켓 아님)으로 전달합니다(카메라 컴포넌트의 "set_view_projection" 메세지나 "set_clear_color" 메세지 등). 다음으로는 렌더 스크립트의 update() 함수가 호출됩니다.

#### Post update
업데이트 작업 후엔, 포스트 업데이트(post update) 시퀀스가 실행됩니다. 여기선 언로드를 위해 예약된 컬렉션 프록시의 메모리를 언로드합니다(이는 "dispatch messages" 시퀀스 수행 중에도 발생함). 삭제가 예약된 게임 오브젝트는 모든 소속 컴포넌트들의 final() 함수를 호출합니다. final()함수의 코드에서 메세지큐로 새 메세지를 보내는 경우엔 "dispatch messages"가 이를 나중에 처리하게 됩니다.

다음으로는 게임오브젝트를 스폰하도록 지시받은 팩토리 컴포넌트가 작업을 시작하고, 마지막으로는 삭제가 예약된 게임오브젝트들이 실제로 삭제 됩니다.

업데이트 루프의 마지막 단계는 @system 메세지("exit", "reboot" 메세지, 프로파일러 토글하기, 비디오 캡쳐를 시작하거나 멈추기 등등)를 전달하는 것을 포함하고 있습니다. 다음으로 그래픽을 렌더링합니다. 그래픽이 렌더링 되는 동안, 비디오 캡쳐 작업과 비주얼 프로필러(visual profiler)의 렌더링 작업도 수행됩니다. ( [Debugging](/manuals/debugging) 문서를 참고 바랍니다.)

#### Frame rate and collection time step
초당 프레임 업데이트의 수(FPS, 즉 update-loop의 실행 수와 동일함)는 프로젝트 설정(project settings)에서 셋팅할 수 있으며 프로그래밍 방식으로 @system 소켓에 "set_update_frequency" 메세지를 보내서 셋팅할 수도 있습니다. 그리고 프록시로 "set_time_step" 메세지를 보내서 컬렉션 프록시의 시간 흐름(time step)을 개별적으로 설정하는 것도 가능합니다. 컬렉션의 시간 흐름을 변경해도 프레임 레이트에 영향을 주지는 않습니다. 대신, 물리 업데이트(physics update)의 시간 흐름과, update() 함수로 전달되는 "dt" 인자값에 영향을 줍니다. 또한, 시간 흐름을 변경하는 것은 각 프레임에 호출되는 update()의 횟수를 변경하는 것은 아닙니다. update()는 프레임당 한번씩만 호출됩니다.

(자세한 것은 [Collection proxy](/manuals/collection-proxy) 와 [set_time_step](/ref/collectionproxy/#set-time-step) 를 참고하세요.)

## Finalization
어플리케이션이 종료되는 시점에는, 마지막 업데이트 루프 시퀀스를 끝내고, 컬렉션 프록시들을 언로드하여 프록시 컬렉션의 모든 게임오브젝트의 마무리(finalizing)와 삭제(deleting)를 수행합니다.

엔진은 마지막으로 main 컬렉션과 오브젝트들을 다루기 위한 마무리(finalization) 시퀀스에 진입합니다.

![Finalization](images/application_lifecycle/application_lifecycle_final.png)

먼저 컴포넌트의 final() 함수를 호출한 후, 남은 메세지들을 전달합니다. 마지막으로, 모든 게임 오브젝트가 삭제되고 main 컬렉션이 언로드 됩니다.

다음으로 엔진은 서브시스템을 종료하고, 프로젝트 설정을 삭제하고, 메모리 프로파일러를 종료하는 등의 작업을 백그라운드에서 수행합니다.

이제 어플리케이션은 완전히 종료되었습니다.
