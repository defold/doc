#### Q: Chrome에서 내 HTML5 앱이 스플래시 화면에서 멈추는 이유는 무엇인가요?

A: 경우에 따라 파일 시스템에서 로컬로 브라우저에서 게임을 실행할 수 없습니다. 에디터에서 실행하면 로컬 웹 서버에서 게임이 제공됩니다. 예를 들어 Python에서 `SimpleHTTPServer`를 사용할 수 있습니다:

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: 로드 중에 내 게임이 "Unexpected data size" 오류와 함께 크래시하는 이유는 무엇인가요?

A: 이는 보통 Windows를 사용하면서 빌드를 만들고 Git에 커밋할 때 발생합니다. Git의 line-ending 설정이 잘못되어 있으면 줄 끝 문자가 변경되고 그에 따라 데이터 크기도 변경됩니다. 문제를 해결하려면 다음 지침을 따르세요: [https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
