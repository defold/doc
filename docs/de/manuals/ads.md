---
title: Werbung in Defold anzeigen
brief: Verschiedene Arten von Werbung anzuzeigen, ist eine gängige Möglichkeit, Web- und Mobilspiele zu monetarisieren. Dieses Handbuch zeigt mehrere Möglichkeiten, dein Spiel mit Werbung zu monetarisieren.
---

# Werbung {#ads}

Werbung ist zu einer sehr verbreiteten Möglichkeit geworden, Web- und Mobilspiele zu monetarisieren, und hat sich zu einer Milliarden-Dollar-Branche entwickelt. Als Entwickler wirst du danach bezahlt, wie viele Menschen die Werbung ansehen, die du in deinem Spiel zeigst. Meist gilt ganz einfach: Je mehr Zuschauer, desto mehr Geld. Aber auch andere Faktoren beeinflussen, wie viel du erhältst:

* Die Qualität der Werbung - relevante Werbeanzeigen erhalten eher Aufmerksamkeit von deinen Spielern und regen sie eher zur Interaktion an.
* Das Werbeformat - Banneranzeigen bringen in der Regel weniger ein, während Vollbildanzeigen, die von Anfang bis Ende angesehen werden, mehr einbringen.
* Das Werbenetzwerk - der Betrag, den du erhältst, unterscheidet sich von Werbenetzwerk zu Werbenetzwerk.

::: sidenote
CPM = Cost per mille (Kosten pro tausend Aufrufe). Der Betrag, den ein Werbetreibender für tausend Aufrufe bezahlt. Der CPM unterscheidet sich je nach Werbenetzwerk und Werbeformat.
:::

## Formate {#formats}

Es gibt viele verschiedene Werbeformate, die in Spielen verwendet werden können. Zu den gängigeren gehören Banneranzeigen, Interstitial-Anzeigen und Werbung gegen Belohnung:

### Banneranzeigen {#banner-ads}

Banneranzeigen basieren auf Text, Bildern oder Videos und bedecken einen relativ kleinen Teil des Bildschirms, normalerweise am oberen oder unteren Bildschirmrand. Banneranzeigen lassen sich sehr leicht implementieren und passen sehr gut zu Casual-Spielen, die auf einem einzigen Bildschirm stattfinden und bei denen sich leicht ein Bildschirmbereich für Werbung reservieren lässt. Banneranzeigen maximieren die Sichtbarkeit der Werbung, während die Nutzer dein Spiel ohne Unterbrechung spielen.

### Interstitial-Anzeigen {#interstitial-ads}

Interstitial-Anzeigen sind großflächige Vollbildanzeigen mit Animationen und manchmal auch interaktiven *Rich-Media*-Inhalten. Interstitial-Anzeigen werden üblicherweise zwischen Leveln oder Spielsitzungen eingeblendet, da dies eine natürliche Pause im Spielerlebnis ist. Interstitial-Anzeigen erzielen üblicherweise weniger Aufrufe als Banneranzeigen, aber die Kosten (CPM) sind deutlich höher als bei Banneranzeigen, was insgesamt zu erheblichen Werbeeinnahmen führt.

### Werbung gegen Belohnung {#rewarded-ads}

Werbung gegen Belohnung (auch als Incentivized Ads bekannt) ist optional und daher weniger aufdringlich als viele andere Werbeformen. Werbung gegen Belohnung besteht in der Regel aus Vollbildanzeigen wie Interstitial-Anzeigen. Der Nutzer kann sich dafür entscheiden, im Austausch für das Ansehen der Werbung eine Belohnung zu erhalten - beispielsweise *Beute*, Münzen, Leben, Zeit oder eine andere Spielwährung oder einen Vorteil im Spiel. Werbung gegen Belohnung hat in der Regel die höchsten Kosten (CPM), aber die Anzahl der Aufrufe hängt direkt davon ab, wie viele Nutzer sich dafür entscheiden. Werbung gegen Belohnung erzielt nur dann sehr gute Ergebnisse, wenn die Belohnungen wertvoll genug sind und zum richtigen Zeitpunkt angeboten werden.


## Werbenetzwerke {#ad-networks}

Das [Defold Asset Portal](/tags/stars/ads/) enthält mehrere Assets zur Integration von Werbeanbietern:

* [AdMob](https://defold.com/assets/admob-defold/) - Zeige Werbung über das Netzwerk von Google AdMob an.
* [AppLovin MAX](https://defold.com/extension-applovin/) - Zeige Werbung über die Werbevermittlung von AppLovin MAX an.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Zeige Werbung in deinem Facebook Instant Game an.
* [LevelPlay](https://defold.com/extension-levelplay/) - Zeige Werbung über die Werbevermittlung von Unity LevelPlay an.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Zeige Werbung über das Netzwerk von Unity Ads an.


# Werbung in dein Spiel integrieren {#how-to-integrate-ads-in-your-game}

Wenn du dich für ein Werbenetzwerk entschieden hast, das du in dein Spiel integrieren möchtest, musst du die Installations- und Nutzungsanweisungen des jeweiligen *Assets* befolgen. Üblicherweise fügst du die Erweiterung zunächst als [Projektabhängigkeit](/manuals/libraries/#setting-up-library-dependencies) hinzu. Sobald du das Asset zu deinem Projekt hinzugefügt hast, kannst du mit der Integration fortfahren und die Funktionen des jeweiligen Assets aufrufen, um Werbung zu laden und anzuzeigen.


# Werbung und In-App-Käufe kombinieren {#combining-ads-and-in-app-purchases}

In Mobilspielen ist es recht üblich, einen [In-App-Kauf](/manuals/iap) anzubieten, mit dem sich Werbung dauerhaft entfernen lässt.


## Mehr erfahren {#learn-more}

Es gibt viele Online-Ressourcen, aus denen du lernen kannst, wie du deine Werbeeinnahmen optimierst:

* Google AdMob [Mobilspiele mit Werbung monetarisieren](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Beliebte Werbeformate und ihre Verwendung](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Werbeeinblendungen in Spielen: 10 Expertentipps](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
