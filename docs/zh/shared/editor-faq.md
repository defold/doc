
#### Q: 编辑器的系统要求是什么？
A: 编辑器将使用系统最多 75% 的可用内存。在具有 4 GB RAM 的计算机上，这应该足以满足较小的 Defold 项目。对于中型或大型项目，建议使用 6 GB 或更多的 RAM。


#### Q: Defold 测试版会自动更新吗？
A: 是的。Defold 测试版编辑器会在启动时检查更新，就像 Defold 稳定版一样。


#### Q: 为什么启动编辑器时会出现 `java.awt.AWTError: Assistive Technology not found` 错误？
A: 此错误与 Java 辅助技术（如 [NVDA 屏幕阅读器](https://www.nvaccess.org/download/)）相关的问题有关。您的主文件夹中可能有一个 `.accessibility.properties` 文件。删除该文件并尝试重新启动编辑器。（注意：如果您确实使用任何辅助技术并且需要该文件存在，请通过 info@defold.se 与我们联系以讨论替代解决方案）。

在 [Defold 论坛上讨论过](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3)。


#### Q: 为什么启动编辑器时会出现 `sun.security.validator.ValidatorException: PKIX path building failed` 错误？
A: 当编辑器尝试建立 https 连接但服务器提供的证书链无法验证时，会发生此异常。

有关此错误的详细信息，请参阅[此链接](https://github.com/defold/defold/blob/master/editor/README_TROUBLESHOOTING_PKIX.md)。


#### Q: 为什么执行某些操作时会出现 `java.lang.OutOfMemoryError: Java heap space` 错误？
A: Defold 编辑器是使用 Java 构建的，在某些情况下，Java 的默认内存配置可能不够。如果发生这种情况，您可以通过编辑编辑器配置文件手动配置编辑器分配更多内存。配置文件名为 `config`，在 macOS 上位于 `Defold.app/Contents/Resources/` 文件夹中。在 Windows 上，它位于 `Defold.exe` 可执行文件旁边，在 Linux 上位于 `Defold` 可执行文件旁边。打开 `config` 文件，并在以 `vmargs` 开头的行中添加 `-Xmx6gb`。添加 `-Xmx6gb` 会将最大堆大小设置为 6 GB（默认通常为 4GB）。它应该看起来像这样：

```
vmargs = -Xmx6gb,-Dfile.encoding=UTF-8,-Djna.nosys=true,-Ddefold.launcherpath=${bootstrap.launcherpath},-Ddefold.resourcespath=${bootstrap.resourcespath},-Ddefold.version=${build.version},-Ddefold.editor.sha1=${build.editor_sha1},-Ddefold.engine.sha1=${build.engine_sha1},-Ddefold.buildtime=${build.time},-Ddefold.channel=${build.channel},-Ddefold.archive.domain=${build.archive_domain},-Djava.net.preferIPv4Stack=true,-Dsun.net.client.defaultConnectTimeout=30000,-Dsun.net.client.defaultReadTimeout=30000,-Djogl.texture.notexrect=true,-Dglass.accessible.force=false,--illegal-access=warn,--add-opens=java.base/java.lang=ALL-UNNAMED,--add-opens=java.desktop/sun.awt=ALL-UNNAMED,--add-opens=java.desktop/sun.java2d.opengl=ALL-UNNAMED,--add-opens=java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED
```
