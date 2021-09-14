Installing
==========

1. Ensure proper repository permissions
---------------------------------------

Ensure that your Git for Windows installation has proper permissions to access (EpicGames/UnrealEngine)[https://github.com/EpicGames/UnrealEngine] 

If clicking this link gives a 404 error message, your GitHub account does not have access to the repository.  You should test that a simple clone command works. We recommend forking the repository to a private repository on your own GitHub account, and then granting Git for Windows access.

You can use SSH keys, via the ssh-add command, and ssh-agent to accomplish the task of authentication.

This should work before you run the script.  Per the original code's author, he would like the GitHub authentication helper functionality left out to make this project independent of its source, and we won't do it for you with a personal access token.

------

If you are able to access Epic Games repository, you should be able to access this one without authenticating.  Move onto the next step.

2. Clone the repository
-----------------------

Clone this repository, by using the green "code" button at the top of the repository to download a zip file and extract it to the appropriate location, or by using git

  We recommend a drive with approximately 110 GB free space.  An SSD 
  is recommended.  You will need an additional 6 GB of free space on 
  your OS drive (C:) to accomidate the Microsoft Visual Studio Build 
  Tools that are automatically downloaded by the script, along with 
  the packages that chocolatey needs for the script to function 
  correctly.  Keep in mind that this is SIGNIFICANTLY LESS than the
  amount required to build the engine traditionally, which does
  require a hefty 300 GB.

2. (Optional) Configure the script
----------------------------------

The following lines in the script can be adjusted to your liking:

```bat
set VISUAL_STUDIO_BUILD_NUMBER=16
set WINDOWS_SDK_VERSION=20348
set "GIT_BRANCH=release"
set "GIT_REPO=https://github.com/EpicGames/UnrealEngine.git"
```

------

```bat
set "GIT_REPO=https://github.com/MyAccount/UnrealEngine.git"
```

Say that you have a forked version of the repository, you would adjust ``GIT_REPO`` accordingly with the clone URL like so.

------

```bat
set VISUAL_STUDIO_BUILD_NUMBER=15
```

If you'd like to use Visual Studio 2017 (not recommended, but possible, and not gaurenteed to work) you can by changing the ``VISUAL_STUDIO_BUILD_NUMBER`` to 15, like so.

The package configuration is a bit different for the 2017 packages.  The visual studio 2019 installer is hard-coded, and I do not recommend changing that line, because it will cause a build failure.  You are however still free to use the 2017 PACKAGES, using the 2019 installer, by changing this line as-mentioned.

------

```bat
set "GIT_BRANCH=release"
```

Use the ``GIT_BRANCH`` line to specify a branch for a specific version of the Unreal Engine.  The release branch downloads by default.  At the time of writing, this is version 4.27.

------

```bat
set WINDOWS_SDK_VERSION=20348
```

You can adjust this line to select an appropriate Windows SDK.  The most recent SDK at the time of making the script has been selected, tested, and works with the current release branch.

You should not set the SDK version to ANYTHING LESS than 18093 .  This will cause a build failure.  Older versions of the SDK are no longer supported by Epic Games.

------

  Do not ask, I am NOT implimenting command line arguments
  in Windows batch.  There is no possibility of security and
  safe argument sanitization when using Windows batch.
  Because this script runs as Administrator, what you can
  change is given to you at the top of the script.  This
  batch will not respond to given arguments for its own
  security.  DO NOT submit a PR request implimenting command
  line arguments.  I will reject that.  If this was a binary
  build or a python script, absolutely, but no.  Its by
  default shady because it needs to work on System32 for
  build dependencies.  NO!

3. Run the script
-----------------

Open the command prompt as Administrator, and then navigate to where you cloned the repository using the ``cd`` command, for example:

```bat
cd "F:\git\work\ue4-docker"
f:
.\slimreal.cmd
```

Why Administrator?
------------------

Running the command prompt as Administrator is important to chocolately, the package manager that helps this script work.  Chocolatey runs in Powershell.  Powershell permissions are bypassed by process so that the script can run mostly unattended (with minimal user input, other than accepting "Yes" to install the filetype associations from the popup that appears)  In order to do this, the script needs to run as a priviledged user.

This script also modifies files in ``C:\Windows\System32`` , which also requires priviledged user (Administrator) permission.  This works by downloading some additional dependencies **directly from Microsoft** to resolve missing dependency problems commonly encountered when running the build.

We sourced winehq for these.  They are links directly from Microsoft's Azure endpoint, and download area.

Here is a list of what is installed there, for transparency and your own security:

xinput1_3.dll
D3DCompiler_43.dll 
X3DAudio1_7.dll 
XAPOFX1_5.dll 
XAudio2_7.dll 
dxcompiler.dll
dxil.dll
vulkan-1.dll

These files are copied to system32 to ensure the build is allowed to succeed, from the official Microsoft cabinets, and directly from lunarg for the vulkan shader compiler.  You can view the source code of the script to see the source URLs of the cabinets running on curl, if you are curious.

We work with the temp directly, which is also cleared.  Nothing in temp is usable beyond a single run of a process.  Running processes that need to keep handles open on files do, so its safe to run:

```bat
rmdir /S /Q \\?\%TEMP%
mkdir %TEMP%
```

Everything that is stored in temp is considered non-volitile by Microsoft standard.  This script runs these commands to clear its downloaded cabinets off from curl after its done, and help to clean up more behind itself.

Enjoy!
------------------

Thank you for using the script.  Please look for future updates, like using BuildGraph and the XML files with the Automation tool to create Installed builds!
