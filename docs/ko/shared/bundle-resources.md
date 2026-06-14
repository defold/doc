번들 리소스는 *game.project*의 [*Bundle Resources* 필드](/manuals/project-settings/#bundle-resources)를 사용해 어플리케이션 번들의 일부로 배치되는 추가 파일과 폴더입니다.

*Bundle Resources* 필드에는 번들링할 때 결과 패키지에 그대로 복사해야 하는 리소스 파일과 폴더가 들어 있는 디렉토리의 쉼표로 구분된 목록을 입력해야 합니다. 디렉토리는 프로젝트 루트 기준의 절대 경로로 지정해야 하며, 예를 들면 `/res`입니다. 리소스 디렉토리에는 `platform` 또는 `architecture-platform` 이름의 서브폴더가 있어야 합니다.

지원되는 플랫폼은 `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`입니다. 모든 플랫폼에 공통으로 쓰이는 리소스 파일을 담는 `common`이라는 이름의 서브폴더도 허용됩니다. 예:

```
res
├── win32
│   └── mywin32file.txt
├── common
│   └── mycommonfile.txt
└── android
    ├── myandroidfile.txt
    └── res
        └── xml
            └── filepaths.xml
```

어플리케이션이 저장된 위치의 경로를 얻으려면 [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:)를 사용할 수 있습니다. 이 어플리케이션 기본 경로를 사용해 액세스해야 하는 파일의 최종 절대 경로를 만드세요. 이 파일들의 절대 경로를 얻은 뒤에는 `io.*`와 `os.*` 함수를 사용해 파일에 액세스할 수 있습니다.
