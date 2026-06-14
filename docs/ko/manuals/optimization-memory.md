---
title: Defold 게임의 메모리 사용량 최적화
brief: 이 매뉴얼은 Defold 게임의 메모리 사용량을 최적화하는 방법을 설명합니다.
---

# 메모리 사용량 최적화

## 텍스쳐 압축
텍스쳐 압축을 사용하면 게임 아카이브 안의 리소스 크기가 줄어들 뿐만 아니라, 압축된 텍스쳐는 필요한 GPU 메모리 양도 줄일 수 있습니다.

## 동적 로딩
대부분의 게임에는 드물게 사용되는 컨텐츠가 어느 정도 있습니다. 메모리 사용량 관점에서는 이런 컨텐츠를 항상 메모리에 로드해 두기보다, 필요할 때 로드하고 언로드하는 것이 좋습니다. 이는 런타임 메모리를 사용하는 대신 컨텐츠를 즉시 사용할 수 있게 할지, 로딩 시간이 들더라도 필요할 때 컨텐츠를 로드할지 사이의 절충입니다.

Defold는 컨텐츠를 동적으로 로드하는 여러 방법을 제공합니다:

* [컬렉션 프록시](/manuals/collection-proxy/)
* [동적 컬렉션 팩토리](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [동적 팩토리](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## 컴포넌트 카운터 최적화
Defold는 메모리 단편화를 줄이기 위해 컬렉션이 생성될 때 컴포넌트와 리소스용 메모리를 한 번에 할당합니다. 할당되는 메모리 양은 *game.project*의 다양한 컴포넌트 카운터 설정값에 따라 달라집니다. [프로파일러](/manuals/profiling/)를 사용해 정확한 컴포넌트 및 리소스 사용량을 파악하고, 게임이 실제 컴포넌트와 리소스 개수에 더 가까운 최대값을 사용하도록 구성하세요. 이렇게 하면 게임이 사용하는 메모리 양을 줄일 수 있습니다(컴포넌트 [max count optimizations](/manuals/project-settings/#component-max-count-optimizations)에 대한 정보를 참고하세요).

## GUI 노드 수 최적화
GUI 파일의 최대 노드 수를 필요한 만큼만 설정하여 GUI 노드 수를 최적화하세요. [GUI 컴포넌트 프로퍼티](https://defold.com/manuals/gui/#gui-properties)의 `Current Nodes` 필드는 GUI 컴포넌트가 사용하는 노드 수를 보여줍니다.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)
