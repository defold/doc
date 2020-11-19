
#### 问: 运行编辑器需要什么硬件系统?

答: 编辑器最多占用 75% 的空闲系统内存. 一般 4 GB 内存的电脑就可以运行 Defold 小项目了. 中大型项目建议配备 6 GB 或更多内存.


#### 问: Defold 测试版会自动更新吗?

答: Defold 测试版编辑器会在启动时检查并自动更新, 正式版也是.

#### 问: 编辑器不启动, 项目不加载?

答: 检查 Defold 安装路径里是否有空格. 比如, 把编辑器放在mac系统 *Applications* 中的 *Defold-macosx* 文件夹里, 就能运行.  改成 *Defold macosx* 就无法运行. 在 Windows 上, 像 *C:\\Program Files\\* 这样的路径都不行. 这归因于 Eclipse 框架的一个已知 bug.


#### 问: 启动 Defold 时报了 "sun.security.validator.ValidatorException: PKIX path building failed" 的错?

答: 这个错是由于编辑器尝试建立 https 连接而服务器证书无法验证导致.

详情请见 [这里](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md).
