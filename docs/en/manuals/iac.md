---
title: Inter-app communication in Defold
brief: Inter-app communication allows you to pick up on the launch arguments used when starting your application. This manual explains Defold's API available for this functionality.
---

# Inter-app communication

Applications can on most operating systems be launched in several ways:

* From the list of installed applications
* From an application specific link
* From a push notification
* As the final step of an installation process.

In the case when the application is launched from a link, notification or when installed it is possible to pass additional arguments such as an install referrer when installing or a deep-link when launching from an application specific link or notification. Defold provides a unified way to get the information about how the application was invoked using a native extensions.

## Installing the extension

To start using the Inter-app communication extension you need to add it as a dependency to your `game.project` file. The latest stable version is available with the dependency URL:
```
https://github.com/defold/extension-iac/archive/master.zip
```

We recommend using a link to a zip file of a [specific release](https://github.com/defold/extension-iac/releases).

## Using the extension

The API is very easy to use. You provide the extension with a listener function and react to listener callbacks.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- This was an invocation
         print(payload.origin) -- origin may be empty string if it could not be resolved
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

Full documentation of the API is available on the [extension GitHub page](https://defold.github.io/extension-iac/).
