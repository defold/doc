#### Q: I am unable to install my Defold game using a free Apple Developer account.
A: Make sure that you are using the same bundle identifier in your Defold project as you used in the Xcode project when you generated the mobile provisioning profile.

#### Q: How can I check the entitlements of a bundled application?
A: From [Inspect the entitlements of a built app](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-APPENTITLEMENTS):

> $ codesign -d --ent :- /path/to/the.app

#### Q: How can I check the entitlements of a provisioning profile
A: From [Inspecting a profile's entitlements](https://developer.apple.com/library/archive/technotes/tn2415/_index.html#//apple_ref/doc/uid/DTS40016427-CH1-PROFILESENTITLEMENTS):

> $ security cms -D -i /path/to/iOSTeamProfile.mobileprovision
