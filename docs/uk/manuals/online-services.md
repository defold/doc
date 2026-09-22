---
title: Онлайн-сервіси
brief: У цьому посібнику пояснюється, як підключатися до різних ігрових і серверних сервісів.
---
# Ігрові сервіси {#game-services}

HTTP-запити та з’єднання через сокети дають змогу підключатися до тисяч різних сервісів в інтернеті та взаємодіяти з ними, але в більшості випадків для цього потрібно більше, ніж просто надіслати HTTP-запит. Зазвичай потрібна певна автентифікація, дані запиту може знадобитися відформатувати певним чином, а відповідь — розібрати, перш ніж її можна буде використати. Усе це, звісно, можна зробити вручну, але є також розширення й бібліотеки, які виконають такі завдання за вас. Нижче наведено список деяких розширень, що спрощують взаємодію з конкретними серверними сервісами:

## Загального призначення {#general-purpose}
* [Colyseus](https://defold.com/assets/colyseus/) — Клієнт для багатокористувацької гри
* [Nakama](https://defold.com/assets/nakama/) — Додайте до своєї гри автентифікацію, підбір гравців, аналітику, хмарне збереження, багатокористувацький режим, чат і багато іншого
* [Photon Realtime](https://defold.com/assets/photon-realtime/) — Photon Realtime пропонує масштабовані рішення для таких основних можливостей, як автентифікація, підбір гравців і швидкий та надійний зв’язок.
* [PlayFab](https://defold.com/assets/playfabsdk/) — Додайте до своєї гри автентифікацію, підбір гравців, аналітику, хмарне збереження й багато іншого
* [AWS SDK](https://github.com/britzl/aws-sdk-lua) — Використовуйте Amazon Web Services у своїй грі

## Автентифікація, таблиці лідерів, досягнення {#authentication-leaderboards-achievements}
* [Google Play Game Services](https://defold.com/assets/googleplaygameservices/) — Використовуйте Google Play Game Services для автентифікації та хмарного збереження у своїй грі
* [Steamworks](https://defold.com/assets/steamworks/) — Додайте підтримку Steam до своєї гри
* [Apple GameKit Game Center](https://defold.com/assets/gamekit/)

## Аналітика {#analytics}
* [Firebase Analytics](https://defold.com/assets/googleanalyticsforfirebase/) — Додайте Firebase Analytics до своєї гри
* [Game Analytics](https://gameanalytics.com/docs/item/defold-sdk) — Додайте GameAnalytics до своєї гри
* [Google Analytics](https://defold.com/assets/gameanalytics/) — Додайте Google Analytics до своєї гри

Ще більше розширень шукайте на [порталі ресурсів](https://www.defold.com/assets/)!
