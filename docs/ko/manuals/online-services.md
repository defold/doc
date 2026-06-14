---
title: 온라인 서비스
brief: 이 매뉴얼에서는 다양한 게임 및 백엔드 서비스에 연결하는 방법을 설명합니다.
---
# 게임 서비스

HTTP 요청과 소켓 연결을 사용하면 인터넷의 수많은 서비스에 연결하고 상호작용할 수 있습니다. 하지만 대부분의 경우 단순히 HTTP 요청을 보내는 것만으로는 충분하지 않습니다. 보통 어떤 형태의 인증을 사용해야 하고, 요청 데이터는 특정 방식으로 포멧되어야 할 수 있으며, 응답은 사용하기 전에 파싱해야 할 수 있습니다. 물론 이러한 작업을 직접 처리할 수도 있지만, 이런 종류의 작업을 대신 처리해 주는 익스텐션과 라이브러리도 있습니다. 아래에는 특정 백엔드 서비스와 더 쉽게 상호작용하는 데 사용할 수 있는 익스텐션 목록이 있습니다:

## 범용
* [Colyseus](https://defold.com/assets/colyseus/) - 멀티플레이어 게임 클라이언트
* [Nakama](https://defold.com/assets/nakama/) - 게임에 인증, 매치메이킹, 분석, 클라우드 저장, 멀티플레이어, 채팅 등을 추가합니다
* [Photon Realtime](https://defold.com/assets/photon-realtime/) - Photon Realtime은 인증, 매치메이킹, 빠르고 안정적인 통신 같은 핵심 기능을 위한 확장 가능한 솔루션을 제공합니다.
* [PlayFab](https://defold.com/assets/playfabsdk/) - 게임에 인증, 매치메이킹, 분석, 클라우드 저장 등을 추가합니다
* [AWS SDK](https://github.com/britzl/aws-sdk-lua) - 게임 안에서 아마존 웹 서비스(AWS)를 사용합니다

## 인증, 리더보드, 업적
* [Google Play Game Services](https://defold.com/assets/googleplaygameservices/) - Google Play Game Services를 사용해 게임에서 인증하고 클라우드 저장을 사용합니다
* [Steamworks](https://defold.com/assets/steamworks/) - 게임에 Steam 지원을 추가합니다
* [Apple GameKit Game Center](https://defold.com/assets/gamekit/)

## 분석
* [Firebase Analytics](https://defold.com/assets/googleanalyticsforfirebase/) - 게임에 Firebase Analytics를 추가합니다
* [Game Analytics](https://gameanalytics.com/docs/item/defold-sdk) - 게임에 GameAnalytics를 추가합니다
* [Google Analytics](https://defold.com/assets/gameanalytics/) - 게임에 Google Analytics를 추가합니다

더 많은 익스텐션은 [Asset Portal](https://www.defold.com/assets/)에서 확인하세요!
