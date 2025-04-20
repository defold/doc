
## Apple 隐私清单

隐私清单是一个属性列表, 用于记录您的应用或第三方 SDK 收集的数据类型, 以及使用 API 的理由. 对于您的应用或第三方 SDK 收集的每种类型的数据以及使用 API 的理由, 需要记录在其捆绑的隐私清单文件中.

Defold 在 *game.project* 文件里的 Privacy Manifest 项提供了默认的清单文件. 创建应用程序包时, 隐私清单将与项目依赖项中的各个隐私清单合并, 包含在应用程序包中.

关于隐私清单更多详情请参考 [Apple 的官方文档](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files?language=objc).