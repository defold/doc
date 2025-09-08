
## Apple 隐私清单

隐私清单是一个属性列表，用于记录您的应用程序或第三方 SDK 收集的数据类型，以及您的应用程序或第三方 SDK 使用的必需原因 API。对于您的应用程序或第三方 SDK 收集的每种数据类型以及使用的必需原因 API 类别，应用程序或第三方 SDK 需要在其捆绑的隐私清单文件中记录这些原因。

Defold 通过 *game.project* 文件中的隐私清单字段提供了一个默认的隐私清单。创建应用程序包时，隐私清单将与项目依赖项中的任何隐私清单合并，并包含在应用程序包中。

有关隐私清单的更多信息，请参阅 [Apple 的官方文档](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc)。