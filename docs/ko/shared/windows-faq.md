#### Q: 텍스쳐가 없는 GUI box 노드는 에디터에서는 투명하지만 빌드하고 실행하면 예상대로 표시되는 이유는 무엇인가요?

A: 이 오류는 [AMD Radeon GPU를 사용하는 컴퓨터](https://github.com/defold/editor2-issues/issues/2723)에서 발생할 수 있습니다. 그래픽 드라이버를 업데이트했는지 확인하세요.

#### Q: 아틀라스나 씬 뷰를 열 때 `com.sun.jna.Native.open.class java.lang.Error: Access is denied`가 표시되는 이유는 무엇인가요?

A: Defold를 관리자 권한으로 실행해 보세요. Defold 실행 파일을 마우스 오른쪽 버튼으로 클릭하고 "Run as Administrator"를 선택합니다.

#### Q: Windows에서 Intel UHD 통합 GPU를 사용할 때 게임이 제대로 렌더링되지 않는 이유는 무엇인가요(HTML5 빌드는 작동합니다)?

A: 드라이버를 27.20.100.8280 이상 버전으로 업데이트했는지 확인하세요. [Intel Driver Support Assistant](https://www.intel.com/content/www/us/en/search.html?ws=text#t=Downloads&layout=table&cf:Downloads=%5B%7B%22actualLabel%22%3A%22Graphics%22%2C%22displayLabel%22%3A%22Graphics%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20Family%22%7D%2C%7B%22actualLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%2C%22displayLabel%22%3A%22Intel%C2%AE%20UHD%20Graphics%20630%22%7D%5D)에서 확인하세요. 추가 정보는 [이 포럼 게시물](https://forum.defold.com/t/sprite-game-object-is-not-rendering/69198/35?u=britzl)에서 확인할 수 있습니다.

#### Q: Defold 에디터가 크래시하고 로그에 `AWTError: Assistive Technology not found`가 표시됩니다

에디터가 크래시하면서 로그에 `Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge`가 언급된다면 다음 단계를 따르세요:

* `C:\Users\<username>`로 이동합니다
* 표준 텍스트 에디터로 `.accessibility.properties` 파일을 엽니다(Notepad를 사용해도 됩니다)
* 설정 파일에서 다음 줄을 찾습니다:

```
assistive_technologies=com.sun.java.accessibility.AccessBridge
screen_magnifier_present=true
```

* 이 줄들 앞에 해쉬 기호(`#`)를 추가합니다
* 파일에 변경 사항을 저장하고 Defold를 다시 시작합니다
