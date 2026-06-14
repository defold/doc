---
title: Defold 리소스 관리
brief: 이 매뉴얼은 Defold가 리소스를 자동으로 관리하는 방식과, 메모리 사용량 및 번들 크기 제약을 지키기 위해 리소스 로딩을 수동으로 관리하는 방법을 설명합니다.
---

# 리소스 관리

아주 작은 게임을 만든다면 타겟 플랫폼의 제한 사항(메모리 사용량, 번들 크기, 연산 성능, 배터리 소모)이 문제가 되지 않을 수 있습니다. 하지만 더 큰 게임을 만들 때, 특히 휴대용 기기에서는 메모리 사용량이 가장 큰 제약 중 하나가 될 가능성이 높습니다. 경험 있는 팀은 플랫폼 제약에 맞춰 리소스 예산을 신중하게 세웁니다. Defold는 메모리와 번들 크기를 관리하는 데 도움이 되는 여러 기능을 제공합니다. 이 매뉴얼은 이러한 기능의 개요를 설명합니다.

## 정적 리소스 트리

Defold에서 게임을 빌드할 때는 리소스 트리를 정적으로 선언합니다. 게임의 모든 개별 부분은 부트스트랩(bootstrap) 컬렉션(보통 "main.collection"이라고 함)에서 시작해 트리에 연결됩니다. 리소스 트리는 모든 참조를 따라가며 해당 참조와 관련된 모든 리소스를 포함합니다.

- 게임 오브젝트 및 컴포넌트 데이터(아틀라스, 사운드 등).
- 팩토리 컴포넌트 프로토타입(게임 오브젝트 및 컬렉션).
- 컬렉션 프록시 컴포넌트 참조(컬렉션).
- *game.project*에 선언된 [커스텀 리소스](/manuals/project-settings/#custom-resources).

![Resource tree](images/resource/resource_tree.png)

::: sidenote
Defold에는 [번들 리소스](/manuals/project-settings/#bundle-resources) 개념도 있습니다. 번들 리소스는 어플리케이션 번들에 포함되지만 리소스 트리의 일부는 아닙니다. 번들 리소스는 플랫폼별 지원 파일부터 [파일 시스템에서 로드되어](/manuals/file-access/#how-to-access-files-bundled-with-the-application) 게임에서 사용되는 외부 파일(예: FMOD 사운드 뱅크)까지 무엇이든 될 수 있습니다.
:::

게임을 *번들링*할 때는 리소스 트리에 있는 항목만 포함됩니다. 트리에서 참조하지 않는 항목은 제외됩니다. 번들에 포함하거나 제외할 항목을 수동으로 선택할 필요가 없습니다.

게임을 *실행*하면 엔진은 트리의 부트스트랩 루트에서 시작해 리소스를 메모리로 가져옵니다.

- 참조된 모든 컬렉션과 그 컨텐츠.
- 게임 오브젝트 및 컴포넌트 데이터.
- 팩토리 컴포넌트 프로토타입(게임 오브젝트 및 컬렉션).

하지만 엔진은 런타임에 다음 유형의 참조된 리소스를 자동으로 로드하지 않습니다.

- 컬렉션 프록시를 통해 참조된 게임 월드 컬렉션. 게임 월드는 비교적 크기 때문에 코드에서 직접 로드와 언로드를 트리거해야 합니다. 자세한 내용은 [컬렉션 프록시 매뉴얼](/manuals/collection-proxy)을 참고하세요.
- *game.project*의 *Custom Resources* 설정을 통해 추가된 파일. 이러한 파일은 [`sys.load_resource()`](/ref/sys/#sys.load_resource) 함수로 수동 로드합니다.

Defold가 리소스를 번들링하고 로드하는 기본 방식은 리소스가 메모리에 들어오는 방식과 시점을 세밀하게 제어하도록 변경할 수 있습니다.

![Resource loading](images/resource/loading.png)

## 팩토리 리소스 동적 로드

팩토리 컴포넌트가 참조하는 리소스는 일반적으로 컴포넌트가 로드될 때 메모리로 로드됩니다. 그러면 런타임에 팩토리가 존재하는 즉시 해당 리소스를 게임 안에 스폰할 준비가 됩니다. 기본 동작을 변경하고 팩토리 리소스 로딩을 미루려면 팩토리의 *Load Dynamically* 체크박스를 선택하면 됩니다.

![Load dynamically](images/resource/load_dynamically.png)

이 박스를 체크하면 엔진은 참조된 리소스를 게임 번들에 계속 포함하지만 팩토리 리소스를 자동으로 로드하지는 않습니다. 대신 두 가지 옵션이 있습니다.

1. 오브젝트를 스폰하려는 시점에 [`factory.create()`](/ref/factory/#factory.create) 또는 [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create)를 호출합니다. 이 호출은 리소스를 동기적으로 로드한 다음 새 인스턴스를 스폰합니다.
2. [`factory.load()`](/ref/factory/#factory.load) 또는 [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load)를 호출해 리소스를 비동기적으로 로드합니다. 리소스를 스폰할 준비가 되면 콜백을 받습니다.

이 동작 방식에 대한 자세한 내용은 [팩토리 매뉴얼](/manuals/factory)과 [컬렉션 팩토리 매뉴얼](/manuals/collection-factory)을 참고하세요.

## 동적으로 로드된 리소스 언로드

Defold는 모든 리소스의 참조 카운터를 유지합니다. 리소스의 카운터가 0이 되면 더 이상 아무것도 해당 리소스를 참조하지 않는다는 뜻입니다. 그러면 그 리소스는 메모리에서 자동으로 언로드됩니다. 예를 들어 팩토리에서 스폰한 모든 오브젝트를 삭제하고 팩토리 컴포넌트를 가진 오브젝트도 삭제하면, 이전에 팩토리가 참조하던 리소스가 메모리에서 언로드됩니다.

*Load Dynamically*로 표시된 팩토리의 경우 [`factory.unload()`](/ref/factory/#factory.unload) 또는 [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload) 함수를 호출할 수 있습니다. 이 호출은 리소스에 대한 팩토리 컴포넌트의 참조를 제거합니다. 해당 리소스를 참조하는 다른 항목이 없으면(예를 들어 스폰된 모든 오브젝트가 삭제된 경우) 리소스가 메모리에서 언로드됩니다.

## 번들에서 리소스 제외

컬렉션 프록시를 사용하면 컴포넌트가 참조하는 모든 리소스를 번들링 과정에서 제외할 수 있습니다. 이는 번들 크기를 최소로 유지해야 할 때 유용합니다. 예를 들어 HTML5로 웹에서 게임을 실행할 경우, 브라우저는 게임을 실행하기 전에 전체 번들을 다운로드합니다.

![Exclude](images/resource/exclude.png)

컬렉션 프록시를 *Exclude*로 표시하면 참조된 리소스가 게임 번들에서 제외됩니다. 대신 제외된 컬렉션을 선택한 클라우드 스토리지에 저장할 수 있습니다. [Live update 매뉴얼](/manuals/live-update/)은 이 기능의 동작 방식을 설명합니다.
