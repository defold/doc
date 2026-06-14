---
title: 에디터 템플릿
brief: New Project 창에 직접 만든 커스텀 프로젝트 템플릿을 추가할 수 있습니다.
---

# 에디터 템플릿

New Project 창에 직접 만든 커스텀 프로젝트 템플릿을 추가할 수 있습니다:

![커스텀 프로젝트 템플릿](images/editor/custom_project_templates.png)

커스텀 프로젝트 템플릿이 있는 새 탭을 하나 이상 추가하려면 사용자 홈 디렉토리의 `.defold` 폴더에 `welcome.edn` 파일을 추가해야 합니다:

* 사용자 홈 디렉토리에 `.defold`라는 이름의 폴더를 만듭니다.
  * Windows의 경우 `C:\Users\**Your Username**\.defold`
  * macOS의 경우 `/Users/**Your Username**/.defold`
  * Linux의 경우 `~/.defold`
* `.defold` 폴더에 `welcome.edn` 파일을 만듭니다.

`welcome.edn` 파일은 Extensible Data Notation 포멧을 사용합니다. 예:

```
{:new-project
  {:categories [
    {:label "My Templates"
     :templates [
          {:name "My project"
           :description "My template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-project/archive/master.zip"
           :skip-root? true},
          {:name "My other project"
           :description "My other template with everything set up the way I want it."
           :image "empty.svg"
           :zip-url "https://github.com/britzl/template-other-project/archive/master.zip"
           :skip-root? true}]
    }]
  }
}
```

그러면 위 스크린샷에 보이는 템플릿 목록이 생성됩니다.

::: sidenote
[에디터에 번들된](https://github.com/defold/defold/tree/dev/editor/resources/welcome/images) 템플릿 이미지만 사용할 수 있습니다.
:::
