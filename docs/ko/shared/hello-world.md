## Hello World

Defold에서 무언가를 빠르게 만들어 보는 간단한 방법입니다. 단계를 따라 한 뒤 이 매뉴얼의 나머지를 계속 읽어 보세요.

1. `Templates`에서 빈 프로젝트를 선택하고, `Title`에 이름을 입력하고, 위치를 선택한 뒤 `Create New Project`를 클릭해 생성합니다. 프로젝트가 Defold Editor에서 열립니다.
![Hello World Step 1](../manuals/images/unity/helloworld_1.png)
2. 왼쪽의 `Assets` 창에서 `main` 폴더를 열고 `main.collection`을 더블 클릭해 엽니다.
3. 오른쪽의 `Outline` 창에서 `Collection`을 마우스 오른쪽 버튼으로 클릭하고 `Add Game Object`를 선택합니다.
![Hello World Step 2](../manuals/images/unity/helloworld_2.png)
4. 생성된 `go` 게임 오브젝트를 마우스 오른쪽 버튼으로 클릭하고 `Add Component`, 그다음 `Label`을 선택합니다.
![Hello World Step 3](../manuals/images/unity/helloworld_3.png)
5. 아래쪽 왼쪽의 `Properties` 창에서 `Text` 프로퍼티에 텍스트를 입력합니다.
6. 중앙의 메인 씬 뷰에서 라벨을 드래그하고 이동해 `(480,320,0)` 근처에 놓거나, `Properties`의 `Position`에서 변경합니다.
![Hello World Step 4](../manuals/images/unity/helloworld_4.png)
7. 라벨 위치를 변경한 뒤 `File` -> `Save All`을 클릭하거나 단축키 <kbd>Ctrl</kbd>+<kbd>S</kbd>(Mac에서는 <kbd>Cmd</kbd>+<kbd>S</kbd>)로 프로젝트를 저장합니다.
8. `Project` -> `Build`를 클릭하거나 단축키 <kbd>Ctrl</kbd>+<kbd>B</kbd>(Mac에서는 <kbd>Cmd</kbd>+<kbd>B</kbd>)로 프로젝트를 빌드합니다.
![Hello World Step 5](../manuals/images/unity/helloworld_5.png)

이제 Defold에서 첫 프로젝트를 빌드했으며, 창에서 입력한 텍스트를 볼 수 있을 것입니다. 게임 오브젝트와 컴포넌트 개념은 익숙할 것입니다. 컬렉션, Outline, Properties, 그리고 왜 라벨을 오른쪽 위 방향으로 조금 이동해야 했는지는 아래에서 설명합니다.
