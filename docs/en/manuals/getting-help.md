---
title: How to get help
brief: This manual describes how to get help if you run into a problem while using Defold.
---

# Getting help

If you run into a problem while using Defold we'd like to hear from you so that we can fix the issue and/or help you work around the problem! There are several ways to discuss and also report issues. Chose the option that works best for you:

## Report a problem on the forum

A good way to discuss and get help with a problem is to post a question on our [forum](https://forum.defold.com). Post either in the [Questions](https://forum.defold.com/c/questions) or [Bugs](https://forum.defold.com/c/bugs) category depending on the type of problem you have. Remember to [search](https://forum.defold.com/search) for your question/issue before asking as there may already be a solution to your problem.

If you have several questions, create multiple posts. Do not ask unrelated questions in the same post.

### Required information
We will not be able to provide support unless you provide the information needed:

**Title**
Make sure to use a short and descriptive title. A good title would be "How do I move a game object in the direction it is rotated?" or "How do I fade out a sprite?". A bad title would be "I need some help using Defold!" or "My game is not working!".

**Describe the bug (REQUIRED)**
A clear and concise description of what the bug is.

**To Reproduce (REQUIRED)**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior (REQUIRED)**
A clear and concise description of what you expected to happen.

**Defold version (REQUIRED):**
  - Version [e.g. 1.2.155]

**Platforms (REQUIRED):**
 - Platforms: [e.g. iOS, Android, Windows, macOS, Linux, HTML5]
 - OS: [e.g. iOS8.1, Windows 10, High Sierra]
 - Device: [e.g. iPhone6]

**Minimal repro case project (OPTIONAL):**
Please attach a minimal project where the bug is reproduced. This will greatly help the person trying to investigate and fix the bug.

**Logs (OPTIONAL):**
Please provide relevant logs from engine, editor or build server. Learn where the logs are stored [here](#log-files).

**Workaround (OPTIONAL):**
If there is a workaround, please describe it here.

**Screenshots (OPTIONAL):**
If applicable, add screenshots to help explain your problem.

**Additional context (OPTIONAL):**
Add any other context about the problem here.

## Report a problem from the editor

The editor provides a convenient way to report issues. Select the <kbd>Help->Report Issue</kbd> menu option from within the editor to report an issue.

![](images/getting_help/report_issue.png)

Selecting this menu option will bring you to an issue tracker on GitHub. Provide [log files](#log-files), information about your operating system, steps to reproduce the problem, possible workarounds etc.

::: sidenote
You need a GitHub account to submit a bug report this way.
:::


## Discuss a problem on Slack

If you run into a problem while using Defold you can try to ask the question on [Slack](https://www.defold.com/slack/). We do however recommend that complex questions and in-depth discussions are posted on the forum. Also note that we do not accept bug reports submitted through Slack.


# Log files

The engine, editor and build server generates logging information that can be very valuable when asking for help and debugging an issue. Always provide log files when reporting a problem:

* [Engine logs](/manuals/debugging-game-and-system-logs)
* Editor logs
  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` or `~/Library/Application Support/Defold`
  * Linux: `~/.Defold`
* [Build server logs](/manuals/extensions#build-server-logs)
