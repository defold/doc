---
title: Mit Bibliotheksprojekten in Defold arbeiten
brief: Mit der Bibliotheksfunktion kannst du Assets zwischen Projekten teilen. Dieses Handbuch erklärt, wie sie funktioniert.
---

# Bibliotheken {#libraries}

Mit der Bibliotheksfunktion (Libraries) kannst du Assets zwischen Projekten teilen. Sie ist ein einfacher, aber sehr leistungsfähiger Mechanismus, den du auf verschiedene Weise in deinem Arbeitsablauf einsetzen kannst.

Bibliotheken sind für folgende Zwecke nützlich:

* Um Assets aus einem abgeschlossenen Projekt in ein neues zu kopieren. Wenn du eine Fortsetzung eines früheren Spiels entwickelst, erleichtert dir das den Einstieg.
* Um eine Bibliothek mit Vorlagen aufzubauen, die du in deine Projekte kopieren und anschließend anpassen oder spezialisieren kannst.
* Um eine oder mehrere Bibliotheken mit fertigen Objekten oder Skripten aufzubauen, die du direkt referenzieren kannst. Das ist sehr praktisch, um gemeinsam genutzte Skriptmodule zu speichern oder eine gemeinsame Bibliothek mit Grafik-, Audio- und Animations-Assets aufzubauen.

## Die Freigabe einer Bibliothek einrichten {#setting-up-library-sharing}

Angenommen, du möchtest eine Bibliothek mit gemeinsam genutzten Sprites und Kachelquellen (tile sources) aufbauen. Beginne damit, [ein neues Projekt einzurichten](/manuals/project-setup/). Entscheide, welche Ordner des Projekts du freigeben möchtest, und trage ihre Namen in der Eigenschaft *`include_dirs`* in den Projekteinstellungen ein. Wenn du mehrere Ordner auflisten möchtest, trenne ihre Namen durch Leerzeichen:

![Einzubeziehende Verzeichnisse](images/libraries/libraries_include_dirs.png)

Bevor wir diese Bibliothek einem anderen Projekt hinzufügen können, brauchen wir eine Möglichkeit, die Bibliothek zu finden.

## Bibliotheks-URL {#library-url}

Bibliotheken werden über eine normale URL referenziert. Bei einem auf GitHub gehosteten Projekt ist das die URL zu einer veröffentlichten Version des Projekts:

![Bibliotheks-URL auf GitHub](images/libraries/libraries_library_url_github.png)

::: important
Es wird empfohlen, immer eine bestimmte veröffentlichte Version eines Bibliotheksprojekts als Abhängigkeit zu verwenden, statt den Branch `master`. So entscheidest du bei der Entwicklung selbst, wann du Änderungen aus einem Bibliotheksprojekt übernimmst, statt immer die neuesten Änderungen aus dessen Branch `master` zu erhalten, die möglicherweise die Kompatibilität beeinträchtigen.
:::

::: important
Es wird empfohlen, Bibliotheken von Drittanbietern vor der Verwendung immer zu prüfen. Weitere Informationen findest du unter [Drittanbietersoftware sicher verwenden](https://defold.com/manuals/application-security/#securing-your-use-of-third-party-software).
:::

### Basisauthentifizierung {#basic-access-authentication}

Du kannst der Bibliotheks-URL einen Benutzernamen und ein Passwort/Token hinzufügen, um bei Bibliotheken, die nicht öffentlich verfügbar sind, eine Basisauthentifizierung durchzuführen:

```
https://username:password@github.com/defold/private/archive/main.zip
```

Die Felder `username` und `password` werden ausgelesen und als Anfrageheader `Authorization` hinzugefügt. Das funktioniert mit jedem Server, der eine grundlegende Zugriffsautorisierung unterstützt.

::: important
Achte darauf, dein erzeugtes persönliches Zugriffstoken oder dein Passwort weder weiterzugeben noch versehentlich offenzulegen, denn es kann schwerwiegende Folgen haben, wenn diese Daten in die falschen Hände geraten!
:::

Damit du Zugangsdaten nicht versehentlich offenlegst, weil sie im Klartext in der Bibliotheks-URL stehen, kannst du auch ein Ersetzungsmuster für Zeichenfolgen verwenden und die Zugangsdaten als Umgebungsvariablen speichern:

```
https://__PRIVATE_USERNAME__:__PRIVATE_TOKEN__@github.com/defold/private/archive/main.zip
```

Im obigen Beispiel werden Benutzername und Token aus den Systemumgebungsvariablen `PRIVATE_USERNAME` und `PRIVATE_TOKEN` gelesen.

#### Authentifizierung bei GitHub {#github-authentication}

Um Inhalte aus einem privaten Repository auf GitHub abzurufen, musst du [ein persönliches Zugriffstoken erzeugen](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) und es als Passwort verwenden.

```
https://github-username:personal-access-token@github.com/defold/private/archive/main.zip
```

#### Authentifizierung bei GitLab {#gitlab-authentication}

Um Inhalte aus einem privaten Repository auf GitLab abzurufen, musst du [ein persönliches Zugriffstoken erzeugen](https://docs.gitlab.com/ee/security/token_overview.html) und es als URL-Parameter senden.

```
https://gitlab.com/defold/private/-/archive/main/test-main.zip?private_token=personal-access-token
```

### Erweiterte Zugriffsauthentifizierung {#advanced-access-authentication}

Bei der Basisauthentifizierung werden das Zugriffstoken und der Benutzername eines Benutzers über jedes für das Projekt verwendete Repository geteilt. Bei einem Team mit mehr als 1 Person kann das ein Problem sein. Um dieses Problem zu lösen, muss für den Bibliothekszugriff auf das Repository ein Benutzer mit ausschließlich lesendem Zugriff verwendet werden. Auf GitHub sind dafür eine Organisation, ein Team und ein Benutzer erforderlich, der das Repository nicht bearbeiten muss und deshalb nur lesenden Zugriff hat.

Schritte auf GitHub:
* [Erstelle eine Organisation](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-new-organization-from-scratch)
* [Erstelle ein Team innerhalb der Organisation](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/creating-a-team)
* [Übertrage das gewünschte private Repository an deine Organisation](https://docs.github.com/en/github/administering-a-repository/transferring-a-repository)
* [Gib dem Team ausschließlich lesenden Zugriff auf das Repository](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/managing-team-access-to-an-organization-repository)
* [Erstelle oder wähle einen Benutzer als Mitglied dieses Teams](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/organizing-members-into-teams)
* Verwende die oben beschriebene „Basisauthentifizierung“, um ein persönliches Zugriffstoken für diesen Benutzer zu erstellen

Jetzt können die Authentifizierungsdaten des neuen Benutzers per Commit und Push in das Repository übernommen werden. So können alle, die mit deinem privaten Repository arbeiten, es als Bibliothek abrufen, ohne Bearbeitungsrechte für die Bibliothek selbst zu haben.

::: important
Das Token des Benutzers mit ausschließlich lesendem Zugriff ist für alle vollständig zugänglich, die auf die Spiel-Repositorys zugreifen können, die diese Bibliothek verwenden.
:::

Diese Lösung wurde im Defold-Forum vorgeschlagen und [in diesem Thema diskutiert](https://forum.defold.com/t/private-github-for-library-solved/67240).

## Abhängigkeiten von Bibliotheken einrichten {#setting-up-library-dependencies}

Öffne das Projekt, von dem aus du auf die Bibliothek zugreifen möchtest. Füge in den Projekteinstellungen die Bibliotheks-URL zur Eigenschaft *dependencies* hinzu. Du kannst bei Bedarf mehrere Projekte als Abhängigkeiten angeben. Füge sie einfach einzeln mit der Schaltfläche `+` hinzu und entferne sie mit der Schaltfläche `-`:

![Abhängigkeiten](images/libraries/libraries_dependencies.png)

Wähle nun <kbd>Project ▸ Fetch Libraries</kbd>, um die Abhängigkeiten von Bibliotheken zu aktualisieren. Das geschieht automatisch, wenn du ein Projekt öffnest. Du musst diesen Schritt daher nur ausführen, wenn sich die Abhängigkeiten ändern, ohne dass du das Projekt erneut öffnest. Das ist der Fall, wenn du Bibliotheken als Abhängigkeiten hinzufügst oder entfernst oder wenn jemand eines der als Abhängigkeit verwendeten Bibliotheksprojekte ändert und synchronisiert.

![Fetch Libraries](images/libraries/libraries_fetch_libraries.png)

Die freigegebenen Ordner erscheinen jetzt im Bereich *Assets*, und du kannst alle freigegebenen Inhalte verwenden. Alle synchronisierten Änderungen am Bibliotheksprojekt sind in deinem Projekt verfügbar.

![Einrichtung der Bibliothek abgeschlossen](images/libraries/libraries_done.png)

## Dateien in eingebundenen Bibliotheken bearbeiten {#editing-files-in-library-dependencies}

Dateien in Bibliotheken können nicht gespeichert werden. Du kannst Änderungen vornehmen, und der Editor kann damit einen Build erstellen, was zum Testen nützlich ist. Die Datei selbst bleibt jedoch unverändert, und alle Änderungen werden verworfen, wenn du die Datei schließt.

Wenn du Bibliotheksdateien ändern möchtest, erstelle einen eigenen Fork der Bibliothek und nimm die Änderungen dort vor. Alternativ kannst du den gesamten Bibliotheksordner in dein Projektverzeichnis kopieren und dort einfügen, um die lokale Kopie zu verwenden. In diesem Fall hat dein lokaler Ordner Vorrang vor der ursprünglichen Abhängigkeit, und die Verknüpfung zur Abhängigkeit sollte aus `game.project` entfernt werden. Vergiss nicht, anschließend <kbd>Project ▸ Fetch Libraries</kbd> zu wählen.

`builtins` ist ebenfalls eine Bibliothek, die von der Engine bereitgestellt wird. Wenn du dort Dateien bearbeiten möchtest, kopiere sie in dein Projekt und verwende diese Kopien anstelle der ursprünglichen Dateien aus `builtins`. Um beispielsweise `default.render_script` zu ändern, kopiere sowohl `/builtins/render/default.render` als auch `/builtins/render/default.render_script` als `my_custom.render` und `my_custom.render_script` in deinen Projektordner. Aktualisiere anschließend deine lokale Datei `my_custom.render`, sodass sie auf `my_custom.render_script` statt auf das integrierte Skript verweist, und lege deine angepasste Datei `my_custom.render` in `game.project` unter der Einstellung Render fest.

Wenn du ein Material kopierst und einfügst und es für alle Komponenten (components) eines bestimmten Typs verwenden möchtest, können [projektspezifische Vorlagen](/manuals/editor/#creating-new-project-files) hilfreich sein.

## Ungültige Referenzen {#broken-references}

Die Freigabe einer Bibliothek umfasst nur Dateien, die sich unterhalb der freigegebenen Ordner befinden. Wenn du etwas erstellst, das Assets außerhalb der freigegebenen Hierarchie referenziert, sind die Referenzpfade ungültig.

## Namenskonflikte {#name-collisions}

Da du in der Projekteinstellung *dependencies* mehrere Projekt-URLs angeben kannst, kann es zu einem Namenskonflikt kommen. Das passiert, wenn zwei oder mehr der als Abhängigkeit verwendeten Projekte in der Projekteinstellung *`include_dirs`* einen Ordner mit demselben Namen freigeben.

Defold löst Namenskonflikte, indem es bei gleichnamigen Ordnern alle Referenzen bis auf die letzte ignoriert. Maßgeblich ist die Reihenfolge der Projekt-URLs in der Liste *dependencies*. Wenn du beispielsweise 3 Bibliotheksprojekt-URLs als Abhängigkeiten angibst und alle einen Ordner namens *items* freigeben, wird nur ein Ordner *items* angezeigt---derjenige aus dem Projekt, das in der URL-Liste an letzter Stelle steht.
