---
title: Defold에서의 네트워킹
brief: 이 매뉴얼은 원격 서버에 연결하고 다른 종류의 네트워크 연결을 수행하는 방법을 설명합니다.
---

# 네트워킹

게임에서 백엔드 서비스와 어떤 식으로든 연결하는 것은 드문 일이 아닙니다. 예를 들어 점수를 게시하거나, 매치메이킹을 처리하거나, 저장된 게임을 클라우드에 보관할 수 있습니다. 또한 많은 게임은 중앙 서버의 개입 없이 게임 클라이언트가 서로 직접 통신하는 피어 투 피어 연결도 사용합니다. 네트워크 연결과 데이터 교환은 여러 프로토콜과 표준을 사용해 수행할 수 있습니다. Defold에서 네트워크 연결을 사용하는 다양한 방법에 대해 자세히 알아보세요.

* [HTTP 요청](/manuals/http-requests)
* [소켓 연결](/manuals/socket-connections)
* [WebSocket 연결](/manuals/websocket-connections)
* [온라인 서비스](/manuals/online-services)


## 기술 세부 정보

### IPv4 및 IPv6

Defold는 소켓과 HTTP 요청에서 IPv4 및 IPv6 연결을 지원합니다.

### 보안 연결

Defold는 소켓과 HTTP 요청에서 보안 SSL 연결을 지원합니다.

Defold는 선택적으로 모든 보안 연결의 SSL 인증서도 검증할 수 있습니다. 공개 CA 루트 인증서 키가 포함된 PEM 파일이나 자체 서명 인증서 공개 키가 *game.project*의 Network 섹션에 있는 [SSL Certificates 설정](/manuals/project-settings/#network)) 필드에 제공되면 SSL 검증이 활성화됩니다. CA 루트 인증서 목록은 `builtins/ca-certificates`에 포함되어 있지만, 게임이 연결하는 서버에 따라 필요한 CA 루트 인증서를 복사해 붙여 넣은 새 PEM 파일을 만드는 것을 권장합니다.
