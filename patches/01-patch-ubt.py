#!/usr/bin/env python3
import os, re, subprocess, sys
import pandas as pd
from patchlib import patchlib

if __name__ == '__main__':

    # ubt quality-of-life patch 
    
    workFile = os.path.join("Configuration", "UEBuildTarget.cs")
    
    patchlib.addInstruction({'filename': workFile , 'searchString': """Module.ExportJson(Module.Binary?.OutputDir, GetExecutableDir(), Writer);""", 'replaceString': """Module.ExportJson((Module.Binary != null || Binaries.Count == 0) ? Module.Binary?.OutputDir : Binaries[0].OutputDir, GetExecutableDir(), Writer);""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': False})

    pass
