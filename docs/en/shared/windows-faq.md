Q: Why are GUI box nodes without a texture transparent in the editor but show up as expected when I build and run?

: A: This error can happen on [computers using AMD Radeon GPUs](https://github.com/defold/editor2-issues/issues/2723). Make sure to update your graphics drivers.

Q: The editor doesn't start and the editor log shows "Caused by: java.awt.AWTError: Assistive Technology not found: com.sun.java.accessibility.AccessBridge"

: A: This error is related to problems with Java assistive technology such as the [NVDA screen reader](https://www.nvaccess.org/download/). Try removing any `.accessibility.properties` file in your user's home folder. Discussed [here on the Defold forum](https://forum.defold.com/t/editor-endless-loading-windows-10-1-2-169-solved/65481/3?u=britzl).
