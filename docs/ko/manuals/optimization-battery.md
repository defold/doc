---
title: Defold 게임의 배터리 사용량 최적화
brief: 이 매뉴얼은 Defold 게임의 배터리 사용량을 최적화하는 방법을 설명합니다.
---

# 배터리 사용량 최적화
모바일/휴대용 기기를 타겟으로 하는 경우 배터리 사용량은 주요 고려 사항입니다. CPU나 GPU 사용량이 높으면 배터리가 빠르게 소모되고 기기가 과열됩니다.

CPU와 GPU 사용량을 줄이는 방법은 게임의 [런타임 성능 최적화](/manuals/optimization-speed) 매뉴얼을 참조하세요.

## 가속도계 비활성화
기기의 가속도계를 사용하지 않는 모바일 게임을 만드는 경우 생성되는 입력 이벤트 수를 줄이기 위해 [*game.project*에서 비활성화](/manuals/project-settings/#use-accelerometer)하는 것이 좋습니다.

# 플랫폼별 최적화

## Android Device Performance Framework

Android Dynamic Performance Framework는 게임이 Android 기기의 전력 및 발열 시스템과 더 직접적으로 상호작용할 수 있게 해 주는 API 집합입니다. Android 시스템에서 동적 동작을 모니터링하고 기기를 과열시키지 않는 지속 가능한 수준으로 게임 성능을 최적화할 수 있습니다. Android 기기용 Defold 게임에서 성능을 모니터링하고 최적화하려면 [Android Dynamic Performance Framework extension](https://defold.com/extension-adpf/)을 사용하세요.
