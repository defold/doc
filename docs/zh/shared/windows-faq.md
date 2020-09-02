#### Q: 为什么编辑器中无纹理的 GUI box 节点透明显示, 但是构建运行后能正常显示?

A: 这个错误发生在 [使用 AMD Radeon GPU 的机器](https://github.com/defold/editor2-issues/issues/2723) 上. 注意更新显卡驱动.


#### Q: 编辑器无法启动, 日志显示 "Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge" 错误

A: 这个错误源于 Java 辅助技术, 比如 [NVDA screen reader](https://www.nvaccess.org/download/). 尝试删除用户文件夹下的 `.accessibility.properties` 文件. 参考 [Defold 论坛上的这个帖子](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3?u=britzl).
