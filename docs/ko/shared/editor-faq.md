#### Q: 에디터의 시스템 요구사항은 무엇인가요?
A: 에디터는 시스템에서 사용 가능한 메모리의 최대 75%를 사용합니다. RAM이 4 GB인 컴퓨터에서는 작은 Defold 프로젝트에 충분합니다. 중간 규모 또는 대형 프로젝트에는 6 GB 이상의 RAM을 사용하는 것이 권장됩니다.


#### Q: Defold beta 버전은 자동 업데이트되나요?
A: 예. Defold stable 버전과 마찬가지로 Defold beta 에디터는 시작할 때 업데이트를 확인합니다.


#### Q: 에디터를 실행할 때 `java.awt.AWTError: Assistive Technology not found` 오류가 표시되는 이유는 무엇인가요?
A: 이 오류는 [NVDA 스크린 리더](https://www.nvaccess.org/download/) 같은 Java 보조 기술 문제와 관련이 있습니다. 홈 폴더에 `.accessibility.properties` 파일이 있을 가능성이 높습니다. 이 파일을 삭제하고 에디터를 다시 실행해 보세요. (참고: 보조 기술을 사용하고 있어서 해당 파일이 반드시 있어야 한다면 대체 해결 방법을 논의할 수 있도록 info@defold.se로 연락해 주세요).

이 내용은 [Defold 포럼의 이 글](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3)에서 논의되었습니다.


#### Q: 에디터를 실행할 때 `sun.security.validator.ValidatorException: PKIX path building failed` 오류가 표시되는 이유는 무엇인가요?
A: 이 예외는 에디터가 https 연결을 시도하지만 서버에서 제공한 인증서 체인을 확인할 수 없을 때 발생합니다.

이 오류에 대한 자세한 내용은 [이 링크](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md)를 참조하세요.


#### Q: 특정 작업을 수행할 때 `java.lang.OutOfMemoryError: Java heap space` 오류가 표시되는 이유는 무엇인가요?
A: Defold 에디터는 Java로 빌드되어 있으며, 경우에 따라 Java의 기본 메모리 설정이 충분하지 않을 수 있습니다. 이런 경우 에디터 설정 파일을 편집하여 에디터가 더 많은 메모리를 할당하도록 수동으로 설정할 수 있습니다. `config`라는 이름의 설정 파일은 macOS에서는 `Defold.app/Contents/Resources/` 폴더에 있습니다. Windows에서는 `Defold.exe` 실행 파일 옆에 있고 Linux에서는 `Defold` 실행 파일 옆에 있습니다. `config` 파일을 열고 `vmargs`로 시작하는 줄에 `-Xmx6gb`를 추가하세요. `-Xmx6gb`를 추가하면 최대 힙 크기가 6기가바이트로 설정됩니다(기본값은 보통 4Gb입니다). 다음과 비슷한 형태여야 합니다:

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
