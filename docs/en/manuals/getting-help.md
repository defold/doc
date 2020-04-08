---
title: How to get help
brief: This manual describes how to get help if you run into a problem while using Defold.
---

# Getting help

If you run into a problem while using Defold we'd like to hear from you so that we can fix the issue and/or help you work around the problem! There are several ways to discuss and also report issues. Chose the option that works best for you:

## Report a problem on the forum

A good way to discuss and get help with a problem is to post a question on our [forum](https://forum.defold.com). Post either in the [Questions](https://forum.defold.com/c/questions) or [Bugs](https://forum.defold.com/c/bugs) category depending on the type of problem you have. When you post a support question make sure to include as much information as possible. Remember to [search](https://forum.defold.com/search) for your question/issue before asking as there may already be a solution to your problem. 


## Report a problem from the editor

The editor provides a convenient way to report issues. Select the <kbd>Help->Report Issue</kbd> menu option from within the editor to report an issue.

![](images/getting_help/report_issue.png)

Selecting this menu option will bring you to an issue tracker on GitHub. Please fill out the form and include as much information as possible. Refer to [the section below on how to extract log files](#log-files).

::: sidenote
You need a GitHub account to submit a bug report this way.
:::


## Discuss a problem on Slack

If you run into a problem while using Defold you can try to ask the question on [Slack](https://www.defold.com/slack/). We do however recommend that complex questions and in-depth discussions are posted on the forum. Also note that we do not accept bug reports submitted through Slack.


# Log files

The engine, editor and build server generates logging information that can be very valuable when asking for help and debugging an issue. Always provide log files when reporting a problem.

## Engine logs
- Android: Logs can be accessed using the `adb` command line tool (Android Debug Bridge). Read more about the `adb` command line tool in the [Android manual](/manuals/android/#android-debug-bridge).
- iOS: Logs can be accessed using XCode and the Devices and Simulators menu option.
- HTML5: Logs can be viewed in the browser developer console:
  - Chrome: Menu > More Tools > Developer Tools
  - Firefox: Tools > Web Developer > Web Console
  - Safari: Develop > Show JavaScript Console
- Desktop: Logs for desktop builds can be viewed by running the Defold application from a terminal/command prompt.

You can also write engine logs to a file and access this once the application has been shut down. You can read more about how to enable and access the log in the [Debugging manual](/manuals/debugging/#extracting-the-logtxt-file).

## Editor logs
- Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
- macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
- Linux: `~/.Defold`

## Build server logs
Build server logs are available when the project is using native extensions. The build server log (`log.txt`) is downloaded together with the custom engine when the project is built and stored inside the file `.internal/%platform%/build.zip`.
