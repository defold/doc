
## Manifeste de confidentialité Apple {#apple-privacy-manifest}

Le manifeste de confidentialité est une liste de propriétés qui consigne les types de données collectées par votre application ou un SDK tiers, ainsi que les API dont l'utilisation doit être justifiée et auxquelles votre application ou un SDK tiers fait appel. Pour chaque type de données collectées et chaque catégorie d'API utilisée nécessitant une justification, votre application ou le SDK tiers doit consigner les raisons dans le fichier de manifeste de confidentialité inclus dans son bundle.

Defold fournit un manifeste de confidentialité par défaut via le champ Privacy Manifest du fichier *game.project*. Lors de la création d'un bundle d'application, le manifeste de confidentialité est fusionné avec les éventuels manifestes de confidentialité des dépendances du projet, puis inclus dans le bundle d'application.

Pour en savoir plus sur les manifestes de confidentialité, consultez la [documentation officielle d'Apple](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).
