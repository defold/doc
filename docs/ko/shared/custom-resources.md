커스텀 리소스는 *game.project*의 [*Custom Resources* 필드](https://defold.com/manuals/project-settings/#custom-resources)를 사용해 메인 게임 아카이브에 번들됩니다.

*Custom Resources* 필드에는 메인 게임 아카이브에 포함할 리소스의 쉼표로 구분된 목록을 넣어야 합니다. 디렉토리를 지정하면 해당 디렉토리 안의 모든 파일과 디렉토리가 재귀적으로 포함됩니다. 파일은 [`sys.load_resource()`](/ref/sys/#sys.load_resource)를 사용해 읽을 수 있습니다.
