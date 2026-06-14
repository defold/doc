## Apple 개인정보 보호 메니페스트

개인정보 보호 메니페스트는 앱 또는 서드파티 SDK가 수집하는 데이터 유형과 앱 또는 서드파티 SDK가 사용하는 필수 사유 API(required reasons API)를 기록하는 프로퍼티 리스트입니다. 앱 또는 서드파티 SDK가 수집하는 각 데이터 유형과 사용하는 필수 사유 API 카테고리마다, 앱 또는 서드파티 SDK는 번들에 포함된 개인정보 보호 메니페스트 파일에 그 사유를 기록해야 합니다.

Defold는 *game.project* 파일의 Privacy Manifest 필드를 통해 기본 개인정보 보호 메니페스트를 제공합니다. 어플리케이션 번들을 만들 때 개인정보 보호 메니페스트는 프로젝트 종속성에 있는 모든 개인정보 보호 메니페스트와 병합되어 어플리케이션 번들에 포함됩니다.

개인정보 보호 메니페스트에 대한 자세한 내용은 [Apple 공식 문서](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc)를 읽어보세요.
