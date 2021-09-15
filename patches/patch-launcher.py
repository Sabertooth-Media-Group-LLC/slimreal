#!/usr/bin/env python3
import os, re, subprocess, sys
import pandas as pd
from patchlib import patchlib
    
if __name__ == '__main__':
    
    # Quality of life patch from https://www.wisengineering.com/downloads/ManagingUE4Projects.pdf , Pg. 5

    workFile = os.path.join("Engine", "Source", "Runtime", "Launch", "Private", "LaunchEngineLoop.cpp")
    
    patchlib.addInstruction({'filename': workFile, 'searchString': """			// Full game name is assumed to be the first token
                OutGameName = MoveTemp(FirstCommandLineToken);
                // Derive the project path from the game name. All games must have a uproject file, even if they are in the root folder.
                OutProjectFilePath = FPaths::Combine(*FPaths::RootDir(), *OutGameName, *FString(OutGameName + TEXT(".") + FProjectDescriptor::GetExtension()));
                return true;""", 'replaceString': """			// Full game name is assumed to be the first token
                OutGameName = MoveTemp(FirstCommandLineToken);
                // Derive the project path from the game name. All games must have a uproject file, even if they are in the root folder.
                OutProjectFilePath = FPaths::Combine(*FPaths::RootDir(), *OutGameName, *FString(OutGameName + TEXT(".") + FProjectDescriptor::GetExtension()));
                // PATCH:  Attempt to look one directory above if we can't find the uproject file normally.
                if (!FPaths::FileExists(OutProjectFilePath))
                {
                    FString Root = FPaths::RootDir() + TEXT("/..");
                    FPaths::CollapseRelativeDirectories(Root);
                    OutProjectFilePath = FPaths::Combine(*Root, *OutGameName, *FString(OutGameName + TEXT(".") +
                    FProjectDescriptor::GetExtension()));
                }
                return true;""", 'versionMatch': ">=4.0.0", 'patchConditionString': NaN, 'patchConditionNot': NaN})
    
    pass    
