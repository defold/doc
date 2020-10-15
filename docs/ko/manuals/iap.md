---
title: Defold manual
---

# In-app purchases
인-앱 구매 (또는 인-앱 결제)는 유저나 플레이어에게 추가 컨텐츠나 추가 기능에 대한 비용을 청구할 수 있습니다. 이 매뉴얼은 이 기능을 위한 Defold API를 설명합니다.

Defold는 Apple의 iOS 앱 스토어의 "in-app purchases" 와 Android 장치에서 Google Play 또는 Amazon의 "in-app billing"를 위한 심플하고 통일된 인터페이스를 제공합니다.
Facebook Canvas "game payments"는 Facebook Canvas에서 지원됩니다. 이들 서비스는 다음과 같이 제품을 판매할 수 있는 기회를 제공합니다.

* 소모성 또는 비소모성의 표준 인-앱 제품 (1회 결제)
* 구독(Subscription) (반복 결제, 자동 결제)

> 현재 Defold 인터페이스는 Apple의 Storekit 기능과 완벽히 상호작용 됩니다. Google Play와 Facebook Canvas의 경우는 인터페이스는 동일하므로 각 플랫폼에서 동일한 코드를 실행할 수 있습니다. 하지만 일부 프로세스 흐름은 플랫폼 마다 다를 수 있습니다. 또한, 현재 Mac Appstore를 통핸 macOS 구매는 지원되고 있지 않습니다.

Apple, Google, Amazon, Facebook 에서 자세한 설명을 볼 수 있습니다.

* [In-App Purchase Programming Guide.](https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/StoreKitGuide/Introduction.html)
* [Google Play In-app Billing documentation.](http://developer.android.com/google/play/billing/index.html)
* [Amazon In-app Purchase documentation.](https://developer.amazon.com/public/apis/earn/in-app-purchasing)
* [Facebook game payments documentation.](https://developers.facebook.com/docs/payments)

## Testing Google Play Billing with static responses
Android 에서는 Google Play 로부터 정적 응답(static responses)을 사용하여 앱에서 IAP 구현을 시작하는 것을 추천합니다. 이렇게 하면 앱을 게시하기 전에 모든 앱의 동작이 제대로 돌아가는지 인증하는 것을 활성화 할 수 있습니다. 여기엔 정적 인앱 빌링 응답(static In-app Billing responses)을 테스트하기 위한 4개의 예약된 프로덕트 아이디가 있습니다.

#### android.test.purchased
Google Play는 아이템이 성공적으로 결제되었는지 응답합니다. 이 응답은 가짜 구매 정보 (예, 가짜 order ID)도 포함한 JSON 문자열을 포함하고 있습니다.
#### android.test.canceled
Google Play는 결제가 취소되었는지 응답하니다. 이는 유효하지 않은 신용카드이거나 결제 직전에 사용자가 주문을 취소 하는 등의 주문 과정 중 에러가 발생했을 때 나타날 수 있습니다.
#### android.test.refunded
Google Play는 결제가 환불 되었는지 응답합니다.
#### android.test.item_unavailable
Google Play는 구매중인 아이템이 사용자의 어플리케이션 제품 목록에 없을 경우 응답합니다.

## Setting up your app for purchases/billing
iOS 와 Android 의 구매 절차는 비슷합니다.

1. Apple 이나 Google Play 의 개발자로 등록되었는지 확인합니다.

2. 대상 디바이스(target device)에서 동작하도록 프로젝트를 설정합니다. [iOS development](/manuals/ios) 그리고 [Android development](/manuals/android) 가이드를 참고하세요.

3. 테스트용 앱을 설정합니다:
    * Android는 [Google Play Developer Console](https://play.google.com/apps/publish/) 에서 할 수 있습니다.
    * iOS는 [iTunes Connect](https://itunesconnect.apple.com/) 에서 할 수 있습니다. App ID (https://developer.apple.com 의 "Member Center"에서 만들었던) 에서 "In-App Purchase" 가 활성화 되어있는지 확인하십시오.
![iTunes Connect and Google Play Dev Console](images/iap/itunes_connect_google_play.png)

4. Google Play의 경우, 알파 **.apk** 파일을 업로드하고 게시(publish)해야 합니다. iTunes Connect의 경우에는 어플리케이션이 App Review 승인을 받을 때 까지는 바이너리를 업로드 하지 마십시오. iTunes Connect에 업로드 했는데 제대로 동작하지 않는다면 Apple이 이를 리젝(reject)할 수도 있습니다.

5. 앱을 위한 프로덕트를 생성합니다.
![iTunes Products](images/iap/itunes_products.png)
--
![Google Play Products](images/iap/google_play_products.png)

6. 테스트 사용자를 추가합니다.
    *  iTunes Connect 페이지의 **Users and Roles**에서는 샌드박스 환경에서 결제를 테스트할 수 있는 사용자를 추가할 수 있습니다. Developer 인증서를 앱에 서명하고 테스트 장치의 Appstore에서 샌드박스 계정을 사용해야 합니다.

    * Google Play Developer Console 에서는 **Settings > Account Details** 에서 License Testing 섹션에 사용자 이메일을 추가할 수 있습니다. 이메일은 쉼표(,)로 구분해 여러 이메일을 추가할 수 있으며, 이 사용자들은 실제 돈을 결제하지 않고 구매 절차를 테스트 할 수 있습니다.

    * 또한 Google Play 에서는 Google Group 을 설정해서 Alpha와 Beta 스토어에서 앱을 다운로드 할 수 있게 테스터 그룹을 관리할 수도 있습니다. **Alpha Testing** 탭을 클릭하고 **Manage list of testers**를 눌러서 Alpha 테스터로 Google Group을 추가한 후 나타나는 링크를 공유하면 됩니다.

![Alpha testers](images/iap/alpha_testers.png)

Facebook에서의 절차:

1. [Facebook developer](https://developers.facebook.com/) 에 등록되어 있는지 확인합니다. Facebook for developers의 "My Apps" 과 "Register as a developer" 단계를 따라 하십시오.

2. Facebook은 폭넓은 결제 기능을 가지고 있으며 동기식(synchronous)과 비동기(asynchronous)식 결제를 지원하는 것을 요구하고 있습니다. 더 많은 정보는 [Payment overview](https://developers.facebook.com/docs/payments/overview) 에서 확인 바랍니다.

3. 앱 호스팅(app hosting)과 콜백 서버(callback server)를 설정합니다:
    * 프로젝트를 호스팅하는 secure canvas URL을 설정해야 합니다. 자세한 설명은 [Games on Facebook](https://developers.facebook.com/docs/games/gamesonfacebook/hosting) 에서 볼 수 있습니다.
    * 다음으로 콜백 서버를 설정하기 위해 [Setting up your callback server](https://developers.facebook.com/docs/payments/realtimeupdates#yourcallbackserver) 단계를 수행해 주십시오.

4. [Facebook Developer Dashboard](https://developers.facebook.com/quickstarts/?platform=canvas)에서 캔버스 앱(canvas app)을 설정합니다.

5. 앱 대쉬보드의  "Canvas Payments"에서 테스트 사용자를 추가합니다.

6. [Defining products](https://developers.facebook.com/docs/payments/implementation-guide/defining-products/) 에서 프로덕트 앱을 생성합니다.

## Asynchronous transactions
IAP API는 비동기 방식입니다. 즉 프로그램이 서버로 각 요청을 보낸 후에도 프로그램을 중단하지 않은 채로 응답을 기다리는 것을 말합니다. 대신 프로그램은 정상적으로 동작하며 응답이 도착하면 이 응답 데이터에 반응하는 콜백 함수(callback function)가 호출(invoke)됩니다.

사용가능한 모든 제품 목록을 가져오려면 아래와 같이 할 수 있습니다.

```lua
local COINS_ID = "com.defold.examples.coins"
local LOGO_ID = "com.defold.examples.logo"

local function product_list(self, products, error)
    if error == nil then
        for i,p in pairs(products) do
            print(p.ident)
            print(p.title)
            print(p.description)
            print(p.currency_code)
            print(p.price_string)
        end
    else
        print(error.error)
    end
end

function init(self)
    -- Initiate a fetch of products
    iap.list({ COINS_ID, LOGO_ID }, product_list)
end
```

실제 트랜잭션을 수행하려면, 먼저 트랜잭션 결과를 수신하는 함수를 등록하고 적당한 때에 이 함수를 호출하면 됩니다.

```lua
    local function iap_listener(self, transaction, error)
        if error == nil then
            if transaction.state == iap.TRANS_STATE_PURCHASING then
                print("Purchasing...")
            elseif transaction.state == iap.TRANS_STATE_PURCHASED then
                print("Purchased!")
            elseif transaction.state == iap.TRANS_STATE_UNVERIFIED then
                print("Unverified!")
            elseif transaction.state == iap.TRANS_STATE_FAILED then
                print("Failed!")
            elseif transaction.state == iap.TRANS_STATE_RESTORED then
                print("Restored")
            end
        else
            print(error.error)
        end
    end

    function on_message(self, message_id, message, sender)

        ...
        -- IAP 트래잭션을 수신하는 함수를 등록하기
        iap.set_listener(iap_listener)
        -- 코인 구매 초기화하기
        iap.buy(COINS_ID)
        ...

    end
```

장치의 운영체제는 사용자가 구매를 할 수 있는 팝업창을 자동으로 띄워줍니다. 이 인터페이스는 테스트/샌드박스 환경에서 실행중인지 여부를 보여줍니다.

![Confirm purchase](images/iap/ios_confirm_purchase.png)

![Android purchase](images/iap/android_purchase.png)

![Confirm purchase](images/iap/ios_purchase_done.png)

## Synchronous payments
대부분의 결제 제공자(payment providers)는 동기식 결제만을 지원합니다. 즉 클라이언트(당신의 어플리케이션)은 결제가 완료될 때 TRANS_STATE_PURCHASED 와 같은 알림을 받는다는 것을 뜻합니다. 이는 결제의 마지막 상태(final state)이며 이 트랜잭션에서 더 이상의 콜백을 제공하지 않습니다.

## Asynchronous payments
일부 결제 제공자는 비동기 결제를 지원할 것을 요구하고 있습니다. 즉 클라이언트(당신의 어플리케이션)은 결제가 초기화 될 때만 알림을 받을 수 있습니다. 결제 완료를 확인하기 위해서는 개발자 서버(또는 클라이언트)와 통신하여 결제가 유효한지 확인해야 합니다. 비동기 결제를 초기화 했을 경우 iap 수신자(iap listener)는 TRANS_STATE_UNVERIFIED 또는 TRANS_STATE_PURCHASED 를 받을 수 있습니다. 이는 결제의 마지막 상태(final state)이므로 이 트랜잭션에서 더 이상의 콜백을 제공하지 않습니다.

## Purchase fulfillment
결제 제공자로부터 구매를 완료하기 위해서는, 어플리케이션은 구매 이행서(purchase fulfillment)를 결제 제공자에게 알릴 필요가 있습니다.(예: 개발자 서버 사이드에서 확인).
Iap는 구매가 완료될 경우(기본 동작) 공급자에게 자동으로 이행서(fulfillment)를 알려주는 자동-완성 기능을 지원합니다. 또한 game project 설정에서 이 기능을 비활성화 할 수도 있습니다. 그러면 트랜잭션이 완료될 때 iap.finish()를 호출해서 구매 이행서를 제공자에게 넘길 수 있습니다.

## Transaction receipt
영수증(receipt)은 결제가 성공적으로 처리되었는지 확인하기 위해서 App Store로 전송하는 서명된 데이터의 묶음(chunk)입니다. 이는 별도의 서버를 사용하여 결제 진행을 확인하는 상점을 설계할 때 매우 유용합니다.

## Troubleshooting
### Android iap.list()가 "failed to fetch product"를 리턴합니다.
Google Play Developer Console 의 alpha나 beta 채널에 **.apk**를 업로드하고 게시(publish)해야 합니다. 또한 당신의 장치의 시간이나 날짜가 정확한지 확인해 보세요.

### iOS iap.list() 가 아무것도 리턴하지 않습니다.
iOS Paid Applications 계정을 요청해서 올바른 문서가 제출되었는지 확인합니다. 적절한 승인(authorization) 없이는 iOS 앱 구매(테스트 구매도)가 제대로 동작하지 않습니다.

"Member Center" 의 AppId에서 in-app purchases가 활성화(activated)되어 있는지 확인하고 앱(또는 dev-app)에 프로비져닝 프로파일이 AppId와 올바른 날짜로 서명되어 있는지 확인합니다. ("Member Center"의 "Certificates, Identifiers & Profiles"에서 provisioning profile details 의 "Enabled Services:" 필드 확인)

여기서 In-App product ID가 샌드박스 환경으로 전파되는데 몇 시간이 걸릴 수도 있습니다.

### iOS iap.list() fails logging error "Unexpected callback set"
iap.list는 중첩 호출(nested calls)를 지원하지 않습니다. iap.list 콜백함수에서 iap.list 를 호출하는 것은 이 에러를 수집하는 엔진에서 무시하게 됩니다.

### On iOS, the "price_string" field contains ~ characters
~ 문자는 폰트 파일에서 일치하는 문자를 찾을 수 없는 placeholders입니다. iap.list()를 사용하는 경우 제품 목록에서 반환된 "price_string" 필드는 이 값과 화폐 분모(currency denominator) 사이에서 줄 바꿈 없는 공백(non breaking space (\u00a0))으로 형식화 됩니다. 만약 GUI에서 이 문자열을 렌더링하려면, 폰트의 **extra_characters** 필드에 이 문자를 추가할 필요가 있습니다. macOS에서는 줄 바꿈 없는 공백(non breaking spaces)을 **Option-\<SPACE>** 를 눌러서 입력할 수 있습니다. 자세한 정보는  [https://ko.wikipedia.org/wiki/줄 바꿈 없는 공백](https://ko.wikipedia.org/wiki/줄%20바꿈%20없는%20공백) 를 확인 바랍니다.
