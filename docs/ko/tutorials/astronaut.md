---
title: 탑다운 이동 튜토리얼
brief: 이 초보자용 튜토리얼에서는 플레이어 입력을 캡처하고 캐릭터를 움직이며 애니메이션하는 방법을 배웁니다. 또한 게임 오브젝트, 컴포넌트, 컬렉션에 대해서도 배웁니다
github: https://github.com/defold/tutorial-astronaut
difficulty: Beginner
---

# 탑다운 이동 튜토리얼

이 초보자용 튜토리얼에서는 Defold에서 간단한 탑다운 캐릭터 컨트롤러를 만드는 방법을 배웁니다. 특별히 준비된 프로젝트에서 시작하므로 에셋과 기본 설정을 걱정할 필요 없이 메커니즘에 집중할 수 있습니다.

컬렉션, 게임 오브젝트, 스프라이트, 스크립트, 타일 맵, 아틀라스, 카메라를 포함한 Defold 프로젝트의 기본 구조를 살펴봅니다. 캐릭터에 걷기 애니메이션을 추가하고, 플레이어 입력을 처리하며, Lua를 사용해 게임 오브젝트를 이동하고, 대각선 이동을 정규화하고, 이동 방향에 따라 애니메이션을 전환합니다.

마지막에는 작은 타일 맵 레벨 안에서 움직이는 애니메이션 캐릭터가 완성되며, WASD 컨트롤, 카메라 따라가기, 더 큰 맵 같은 기능으로 더 확장할 준비가 됩니다.

## Defold에서 바로 실행하기

튜토리얼은 Defold 에디터에 통합되어 있으며 Defold 시작 화면에서 쉽게 접근할 수 있습니다.

1. 왼쪽에서 *Create From* -> <kbd>Tutorials</kbd>를 선택합니다.
2. <kbd>Top-down Movement Tutorial</kbd>을 선택합니다.
3. 프로젝트의 *Title*을 입력합니다.
4. 로컬 드라이브에서 프로젝트의 *Location*을 선택합니다.
5. <kbd>Create New Project</kbd>를 클릭합니다.

![new project](images/top-down-start.webp)

에디터가 프로젝트 루트의 "README" 파일을 자동으로 엽니다. 이 파일에는 따라 할 수 있는 전체 튜토리얼 텍스트가 들어 있습니다.

![icon](images/icon-tutorial.svg){.icon} [전체 튜토리얼 텍스트를 GitHub에서도 읽을 수 있습니다](https://github.com/defold/tutorial-astronaut)

막히는 부분이 있으면 [Defold Forum](//forum.defold.com)으로 오세요. Defold 팀과 많은 친절한 사용자에게 도움을 받을 수 있습니다.

즐겁게 Defolding하세요!
