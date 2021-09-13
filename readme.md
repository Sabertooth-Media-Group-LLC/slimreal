SlimReal
---------

Compile Unreal Engine for Windows in a single batch file.

This code was derived from the dockerfiles given by [Adam Rehn's repository](https://github.com/adamrehn/ue4-docker), to produce a simple batch file + patchset that can successfully compile the Unreal Engine.

Pros
----

* No full Visual Studio 2019 installation is required, saving you more disk space.  A slim install of msbuild / Visual Studio Tools with only what's needed is used.
* The installation is largely unattended, with the exception of logging into GitHub, and ticking "Yes" to register the new build in your registry.  Per Adam's request on his Wiki, github-authentication-helper.bat reliant code has been removed in this iteration.
* Nessecary DirectX / Vulkan runtime DLLs are copied automatically from official Microsoft cabinets.
* The repository you should seek out for a quick and dirty vanilla build of the Unreal Engine that works on Windows 10.

Cons
----

* Isn't docker friendly
* Can't compile on Windows Server thanks to additional missing DLLs
* Has to use chocolatey, can make a mess of the host's PATH
* Lazy, no sanity checks
