#!/usr/bin/env python3
import os, re, subprocess, sys
import pandas as pd
from patchlib import patchlib

if __name__ == '__main__':

    # morph setup into an unattended version of itself.
    
    workFile = os.path.join("Setup.bat")
    
    patchlib.addInstruction({'filename': workFile , 'searchString': """echo Installing prerequisites...""", 'replaceString': """echo (Skipping installation of prerequisites)""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': False})
    
    patchlib.addInstruction({'filename': workfile, 'searchString': """start /wait Engine\Extras\Redist\en-us\UE4PrereqSetup_x64.exe""", 'replaceString': """@rem start /wait Engine\Extras\Redist\en-us\UE4PrereqSetup_x64.exe""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': False})
    
    patchlib.addInstruction({'filename': workfile, 'searchString': """.\Engine\Binaries\Win64\UnrealVersionSelector-Win64-Shipping.exe /register""", 'replaceString': """@rem .\Engine\Binaries\Win64\UnrealVersionSelector-Win64-Shipping.exe /register""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': False})
    
    patchlib.addInstruction({'filename': workfile, 'searchString': """rem Done!""", 'replaceString': """echo Done!
exit /b 0""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': False})

    patchlib.addInstruction({'filename': workfile, 'searchString': """pause""", 'replaceString': """@rem pause""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': False})
 
    pass
