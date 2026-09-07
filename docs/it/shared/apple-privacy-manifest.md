
## Manifesto sulla privacy di Apple {#apple-privacy-manifest}

Il manifesto sulla privacy è un elenco di proprietà che registra i tipi di dati raccolti dalla tua applicazione o da un SDK di terze parti e le API utilizzate dall'applicazione o dall'SDK per le quali è obbligatorio dichiarare una motivazione d'uso. Per ogni tipo di dato raccolto e per ogni categoria di API utilizzata che richiede una motivazione, l'applicazione o l'SDK di terze parti deve registrare le motivazioni nel file del manifesto sulla privacy incluso nel proprio bundle.

Defold fornisce un manifesto sulla privacy predefinito tramite il campo Privacy Manifest nel file *game.project*. Quando crei un bundle dell'applicazione, il manifesto sulla privacy viene unito agli eventuali manifesti sulla privacy presenti nelle dipendenze del progetto e incluso nel bundle dell'applicazione.

Per saperne di più sui manifesti sulla privacy, consulta la [documentazione ufficiale di Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).