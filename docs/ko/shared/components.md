컴포넌트는 게임 오브젝트에 특정 표현 및/또는 기능을 부여하는 데 사용됩니다. 컴포넌트는 게임 오브젝트 안에 포함되어야 하며, 해당 컴포넌트를 포함하는 게임 오브젝트의 위치, 회전, 스케일의 영향을 받습니다.

![컴포넌트](../shared/images/components.png)

많은 컴포넌트에는 조작할 수 있는 타입별 프로퍼티가 있으며, 런타임에서 컴포넌트와 상호작용할 수 있는 컴포넌트 타입별 함수도 제공됩니다.

```lua
-- can "body" 스프라이트 비활성화
msg.post("can#body", "disable")

-- 1초 뒤에 "bean"에서 "hoohoo" 사운드 재생
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

컴포넌트는 게임 오브젝트 안에 내장(in-place)으로 추가하거나, 컴포넌트 파일에 대한 참조로 게임 오브젝트에 추가할 수 있습니다.

*Outline* 뷰에서 게임 오브젝트를 <kbd>Right-click</kbd>하고 <kbd>Add Component</kbd>(내장으로 추가) 또는 <kbd>Add Component File</kbd>(파일 참조로 추가)을 선택합니다.

대부분의 경우 컴포넌트를 내장으로 생성하는 것이 가장 적합하지만, 다음 컴포넌트 타입은 게임 오브젝트에 참조로 추가하기 전에 별도의 리소스 파일로 생성해야 합니다.

* Script
* GUI
* Particle FX
* Tile Map
