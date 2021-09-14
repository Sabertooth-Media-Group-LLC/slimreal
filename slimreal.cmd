@if (@CodeSection == @Batch) @then
@echo off
setlocal enableextensions

@rem you can adjust these as you like
set MYPATH=%~dp0
set MYPATH=%MYPATH:~0,-1%
set VISUAL_STUDIO_BUILD_NUMBER=16
set WINDOWS_SDK_VERSION=20348
set "GIT_BRANCH=release"
set "GIT_REPO=https://github.com/EpicGames/UnrealEngine.git"

@rem enable long paths
reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f

@rem install chocolatey
powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

@rem install prereqs
choco install -y python choco-cleaner curl vcredist-all windows-sdk-10-version-1809-windbg
python -m pip install --upgrade pip

@rem download and install DirectX, XInput, and XAudio prerequisites.
if not exist "\\?\%TEMP%\directx_redist.exe" curl --progress-bar -L "https://download.microsoft.com/download/8/4/A/84A35BF1-DAFE-4AE8-82AF-AD2AE20B6B14/directx_Jun2010_redist.exe" --output \\?\%TEMP%\directx_redist.exe
if not exist "\\?\%TEMP%\directx_redist\" (
	mkdir "\\?\%TEMP%\directx_redist\"
	start /wait \\?\%TEMP%\directx_redist.exe /Q /T:\\?\%TEMP%\directx_redist\
)
if not exist "C:\Windows\System32\xinput1_3.dll" expand \\?\%TEMP%\directx_redist\APR2007_xinput_x64.cab -F:xinput1_3.dll C:\Windows\System32\
if not exist "C:\Windows\System32\D3DCompiler_43.dll" expand \\?\%TEMP%\directx_redist\\Jun2010_D3DCompiler_43_x64.cab -F:D3DCompiler_43.dll C:\Windows\System32\
if not exist "C:\Windows\System32\X3DAudio1_7.dll" expand \\?\%TEMP%\directx_redist\Feb2010_X3DAudio_x64.cab -F:X3DAudio1_7.dll C:\Windows\System32\
if not exist "C:\Windows\System32\XAPOFX1_5.dll" expand \\?\%TEMP%\directx_redist\Jun2010_XAudio_x64.cab -F:XAPOFX1_5.dll C:\Windows\System32\
if not exist "C:\Windows\System32\XAudio2_7.dll" expand \\?\%TEMP%\directx_redist\Jun2010_XAudio_x64.cab -F:XAudio2_7.dll C:\Windows\System32\ 

@rem download and install Direct 3D shader compiler prerequisites.
if not exist "\\?\%TEMP%\dxc.zip" curl --progress -L "https://github.com/microsoft/DirectXShaderCompiler/releases/download/v1.6.2104/dxc_2021_04-20.zip" --output \\?\%TEMP%\dxc.zip
if not exist "\\?\%TEMP%\dxc\" (
	mkdir "\\?\%TEMP%\dxc\"
	powershell -Command "Expand-Archive -Path \"$env:TEMP\dxc.zip\" -DestinationPath $env:TEMP\dxc\"
)
if not exist "C:\Windows\System32\dxcompiler.dll" xcopy /y \\?\%TEMP%\dxc\bin\x64\dxcompiler.dll C:\Windows\System32\
if not exist "C:\Windows\System32\dxil.dll" xcopy /y \\?\%TEMP%\dxc\bin\x64\dxil.dll C:\Windows\System32\

@rem download and install vulkan runtime prerequisites.
if not exist "\\?\%TEMP%\vulkan-runtime-components.zip" curl --progress-bar -L "https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-runtime-components.zip?u=" --output \\?\%TEMP%\vulkan-runtime-components.zip
if not exist "\\?\%TEMP%\vulkan-runtime-components\" (
	mkdir "\\?\%TEMP%\vulkan-runtime-components\"
	powershell -Command "Expand-Archive -Path \"$env:TEMP\vulkan-runtime-components.zip\" -DestinationPath \"$env:TEMP\vulkan-runtime-components\""
)
if not exist "C:\Windows\System32\vulkan-1.dll" powershell -Command "Copy-Item -Path \"\\?\%TEMP%\vulkan-runtime-components\*\x64\vulkan-1.dll\" -Destination C:\Windows\System32"

@rem download and install visual studio build tools prerequisites.
if not exist "\\?\%TEMP%\vs_buildtools.exe" curl --progress-bar -L "https://aka.ms/vs/16/release/vs_buildtools.exe" --output \\?\%TEMP%\vs_buildtools.exe
if not exist "\\?\%MYPATH%\vs_buildtools\buildtools-%VISUAL_STUDIO_BUILD_NUMBER%_%WINDOWS_SDK_VERSION%\" (
	mkdir "\\?\%MYPATH%\vs_buildtools\buildtools-%VISUAL_STUDIO_BUILD_NUMBER%_%WINDOWS_SDK_VERSION%\"
	call \\?\%TEMP%\vs_buildtools.exe --quiet --wait --norestart --nocache ^
	--installPath \\?\%MYPATH%\vs_buildtools\buildtools-%VISUAL_STUDIO_BUILD_NUMBER%_%WINDOWS_SDK_VERSION%\ ^
	--channelUri "https://aka.ms/vs/%VISUAL_STUDIO_BUILD_NUMBER%/release/channel" ^
	--installChannelUri "https://aka.ms/vs/%VISUAL_STUDIO_BUILD_NUMBER%/release/channel" ^
	--channelId VisualStudio.%VISUAL_STUDIO_BUILD_NUMBER%.Release ^
	--productId Microsoft.VisualStudio.Product.BuildTools ^
	--locale en-US ^
	--add Microsoft.VisualStudio.Workload.VCTools ^
	--add Microsoft.VisualStudio.Workload.MSBuildTools ^
	--add Microsoft.VisualStudio.Component.NuGet ^
	--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
	--add Microsoft.VisualStudio.Component.Windows10SDK.%WINDOWS_SDK_VERSION% ^
	--add Microsoft.Net.Component.4.5.TargetingPack ^
	--add Microsoft.Net.ComponentGroup.4.6.2.DeveloperTools ^
	--add Microsoft.NetCore.Component.SDK
)

@rem cleanups
start "Chocolatey Cleanup" /wait cmd.exe /c "choco-cleaner"
if exist %APPDATA%\NuGet rmdir /s /q %APPDATA%\NuGet

@rem clone repository
if not exist %MYPATH%\ue4_%GIT_BRANCH% mkdir %MYPATH%\ue4_%GIT_BRANCH%
git clone --progress --depth=1 -b %GIT_BRANCH% "%GIT_REPO%" %MYPATH%\ue4_%GIT_BRANCH%

@rem debug (broken for now)
goto :EOF

@rem apply patches
python %MYPATH%\patches\patch-setup-win.py %MYPATH%\ue4_%GIT_BRANCH%\Setup.bat
python %MYPATH%\patches\patch-broken-releases.py %MYPATH%\ue4_%GIT_BRANCH%

@rem perform initial setup.
pushd %MYPATH%\ue4_%GIT_BRANCH%
call %MYPATH%\ue4_%GIT_BRANCH%\Setup.bat -no-cache

@rem run version selector (automated)
start %MYPATH%\ue4_%GIT_BRANCH%\Engine\Binaries\Win64\UnrealVersionSelector-Win64-Shipping.exe /register
powershell -c "Start-Sleep -s 2"
powershell -c "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('^{ENTER}')"

@rem delete bogus example platform directory that causes build issues.
rmdir /s /q %MYPATH%\ue4_%GIT_BRANCH%\Engine\Platforms\XXX
popd && popd

@rem run last patchset
python %MYPATH%\patches\patch-ubt.py %MYPATH%\ue4_%GIT_BRANCH%\Engine\Source\Programs\UnrealBuildTool

@rem build the engine (grab a coffee!)
pushd %MYPATH%\ue4_%GIT_BRANCH%
call %MYPATH%\ue4_%GIT_BRANCH%\GenerateProjectFiles.bat
call %MYPATH%\ue4_%GIT_BRANCH%\Engine\Build\BatchFiles\Build.bat UE4Editor Win64 Development -WaitMutex
call %MYPATH%\ue4_%GIT_BRANCH%\Engine\Build\BatchFiles\Build.bat ShaderCompileWorker Win64 Development -WaitMutex
call %MYPATH%\ue4_%GIT_BRANCH%\Engine\Build\BatchFiles\Build.bat UnrealPak Win64 Development -WaitMutex
popd

endlocal
goto :EOF
@end