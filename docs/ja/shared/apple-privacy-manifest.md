
## Apple のプライバシーマニフェスト {#apple-privacy-manifest}

プライバシーマニフェスト（privacy manifest）は、アプリまたはサードパーティ SDK が収集するデータの種類と、使用する API のうち理由の宣言が求められるものを記録するプロパティリストです。アプリまたはサードパーティ SDK は、収集するデータの種類ごとに、また、理由の宣言が求められる API を使用する場合はそのカテゴリごとに、理由を同梱のプライバシーマニフェストファイルに記録する必要があります。

Defold では、*game.project* ファイルの Privacy Manifest フィールドを通じて、デフォルトのプライバシーマニフェストが提供されます。アプリケーションバンドル（application bundle）の作成時に、このプライバシーマニフェストはプロジェクトの依存関係に含まれるすべてのプライバシーマニフェストとマージされ、アプリケーションバンドルに含められます。

プライバシーマニフェストについて詳しくは、[Apple の公式ドキュメント](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc)を参照してください。
