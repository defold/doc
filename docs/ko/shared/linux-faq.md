#### Q: 4k 또는 HiDPI 모니터에서 실행할 때 Defold 에디터가 매우 작게 보이는 이유는 무엇인가요?

A: GNOME을 사용 중이라면 Defold를 실행하기 전에 스케일링 배율을 변경할 수 있습니다. [출처](https://unix.stackexchange.com/a/552411)

```bash
$ gsettings set org.gnome.desktop.interface scaling-factor 2
$ ./Defold
```

A: 특히 일부 비율만큼 확대하고 싶을 때 사용할 수 있는 다른 해결 방법은 `Defold/config` 파일을 수정하고 `vmargs` 줄에 `glass.gtk.uiScale`을 추가하는 것입니다. [출처](https://forum.defold.com/t/4k-hidpi-monitor-support-solved/64108/12?u=britzl)

```
vmargs = -Dglass.gtk.uiScale=1.5,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=175%,-Dfile.encoding=UTF-8,...
vmargs = -Dglass.gtk.uiScale=192dpi,-Dfile.encoding=UTF-8,...
```

이 값에 대한 자세한 내용은 [Arch Linux HiDPI wiki 문서](https://wiki.archlinux.org/title/HiDPI#JavaFX)를 참고하세요.

A: KDE를 사용 중이라면 `GDK_SCALE`을 설정할 수 있습니다.

```bash
$ GDK_SCALE=2 ./Defold
```

#### Q: Elementary OS에서 마우스 클릭이 에디터를 통과해 그 아래에 있는 항목으로 전달되는 이유는 무엇인가요?

A: 다음과 같이 에디터를 시작하세요.

```bash
$ GTK_CSD=0 ./Defold
```


#### Q: 컬렉션 또는 게임 오브젝트를 열 때 Defold 에디터가 충돌하고 충돌 정보에서 `com.jogamp.opengl`을 참조합니다.

A: 특정 배포판(예: Ubuntu 18)에서는 Defold가 사용하는 `jogamp`/`jogl` 버전과 시스템의 [Mesa](https://docs.mesa3d.org/) 버전 사이에 문제가 있습니다. `MESA_GL_VERSION_OVERRIDE`를 2.1 또는 그래픽 드라이버 버전 이하의 더 큰 값으로 설정하여 `glGetString(GL_VERSION)` 호출 시 보고되는 GL 버전을 재정의할 수 있습니다. `glxinfo`를 사용해 드라이버가 지원하는 최대 OpenGL 버전을 확인할 수 있습니다.

```bash
glxinfo | grep version
```

예시 출력("OpenGL version string: x.y"를 확인하세요):

```
server glx version string: 1.4
client glx version string: 1.4
GLX version: 1.4
Max core profile version: 4.6
Max compat profile version: 4.6
Max GLES1 profile version: 1.1
Max GLES[23] profile version: 3.2
OpenGL core profile version string: 4.6 (Core Profile) Mesa 20.2.6
OpenGL core profile shading language version string: 4.60
OpenGL version string: 4.6 (Compatibility Profile) Mesa 20.2.6
OpenGL shading language version string: 4.60
OpenGL ES profile version string: OpenGL ES 3.2 Mesa 20.2.6
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20
GL_EXT_shader_implicit_conversions, GL_EXT_shader_integer_mix,
```

버전 2.1 또는 그래픽 드라이버와 일치하는 버전을 사용하세요.

```bash
$ MESA_GL_VERSION_OVERRIDE=2.1 ./Defold
```

```bash
$ MESA_GL_VERSION_OVERRIDE=4.6 ./Defold
```


#### Q: Defold를 시작할 때 "`com.jogamp.opengl.GLException: Graphics configuration failed`"가 표시되는 이유는 무엇인가요?

A: 특정 배포판(예: Ubuntu 20.04)에서는 Defold를 실행할 때 새로운 [Mesa](https://docs.mesa3d.org/) 드라이버(Iris)와 관련된 문제가 있습니다. Defold를 실행할 때 이전 드라이버 버전 사용을 시도할 수 있습니다.

```bash
$ MESA_LOADER_DRIVER_OVERRIDE=i965 ./Defold
```


#### Q: 컬렉션 또는 게임 오브젝트를 열 때 Defold 에디터가 충돌하고 충돌 정보에서 `libffi.so`를 참조합니다.

A: 배포판의 [libffi](https://sourceware.org/libffi/) 버전과 Defold에 필요한 버전(버전 6 또는 7)이 일치하지 않습니다. `libffi.so.6` 또는 `libffi.so.7`이 `/usr/lib/x86_64-linux-gnu` 아래에 설치되어 있는지 확인하세요. 다음과 같이 `libffi.so.7`을 다운로드할 수 있습니다.

```bash
$ wget http://ftp.br.debian.org/debian/pool/main/libf/libffi/libffi7_3.3-6_amd64.deb
$ sudo dpkg -i libffi7_3.3-6_amd64.deb
```

그다음 Defold를 실행할 때 이 버전의 경로를 `LD_PRELOAD` 환경 변수에 지정합니다.

```bash
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libffi.so.7 ./Defold
```


#### Q: OpenGL 드라이버가 오래되었습니다. 그래도 Defold를 사용할 수 있나요?

A: 예. 소프트웨어 렌더링(software rendering)을 활성화하면 Defold를 사용할 수 있을 수도 있습니다. `LIBGL_ALWAYS_SOFTWARE` 환경 변수를 1로 설정하여 소프트웨어 렌더링을 활성화할 수 있습니다.

```bash
$ LIBGL_ALWAYS_SOFTWARE=1 ./Defold
```


#### Q: Linux에서 Defold 게임을 실행하려고 할 때 게임이 시작되지 않는 이유는 무엇인가요?

A: 에디터의 콘솔 출력을 확인하세요. 다음 메세지가 표시된다면:

```
dmengine: error while loading shared libraries: libopenal.so.1: cannot open shared object file: No such file or directory
```

그러면 *`libopenal1`*을 설치해야 합니다. 패키지 이름은 배포판마다 다르며, 경우에 따라 *`openal`* 및 *`openal-dev`* 또는 *`openal-devel`* 패키지를 설치해야 할 수도 있습니다.

```bash
$ apt-get install libopenal-dev
```

#### Q: 무언가를 선택하기 전에 상단 메뉴가 닫히는 이유는 무엇인가요?

A: 사용 중인 윈도우 매니저(예: `Qtile` 또는 i3)가 원인일 가능성이 큽니다. 이는 [JavaFX의 알려진 이슈](https://bugs.openjdk.org/browse/JDK-8251240?focusedCommentId=14362084&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-14362084)이며, `GDK_DISPLAY` 환경 변수를 1로 설정하여 해결할 수 있습니다.¨

```bash
$ GDK_DISPLAY=1 ./Defold

D=2

```

또는 `Defold/config` 파일을 수정하고 `vmargs` 줄에 `-Djdk.gtk.version=2`를 추가하여 해결할 수 있습니다.

```
vmargs = -Djdk.gtk.version=2,-Dfile.encoding=UTF-8,...
```


#### Q: Open From Disk를 선택할 때 사용 가능한 모든 파일 위치를 탐색할 수 없는 이유는 무엇인가요?

A: [Flatpak을 사용해 Steam](https://flathub.org/apps/com.valvesoftware.Steam)에서 Defold를 실행 중이라면 Steam에 다른 드라이브에 액세스할 권한을 부여해야 합니다. [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) 또는 비슷한 도구를 사용하여 Flatpak 어플리케이션의 권한을 수정할 수 있습니다.


#### Q: 웹 프로파일러(web profiler) 또는 브라우저가 필요한 다른 메뉴 옵션을 열 수 없는 이유는 무엇인가요?

A: Gnome이 아닌 시스템에서 브라우저가 감지되지 않아 `Desktop.getDesktop().browse(new URI(url));` 내부 호출이 실패했을 가능성이 큽니다. `libgnome` 설치를 시도해 보세요.

```bash
$ apt-get install libgnome
```
