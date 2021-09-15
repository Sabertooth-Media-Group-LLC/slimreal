#!/usr/bin/env python3
import os, re, subprocess, sys
import pandas as pd
from patchlib import patchlib

if __name__ == '__main__':

    # version-specific patches?  (ported from original ue4-docker)
    
    workFile = os.path.join("Engine", "Build", "Commit.gitdeps.xml")
    
    # If `Commit.gitdeps.xml` is missing the changes from CL 14469950 then inject them
    # (See: <https://github.com/EpicGames/UnrealEngine/commit/84e4ea3241c294c04fdf7d8fb63f99a3109c8edd>)

    patchlib.addInstruction({'filename': workfile, 'searchString': """<File Name=".tgitconfig" Hash="d3d7bbcf9b2fc8b6e4f2965354a5633c4f175589" />""", 'replaceString': """<File Name=".tgitconfig" Hash="d3d7bbcf9b2fc8b6e4f2965354a5633c4f175589" />
<File Name="cpp.hint" Hash="7d1daec3c6218ce9f49f9be0280091b98d7168d7" />
""", 'versionMatch': "==4.25.4", 'patchConditionString': '<File Name="cpp.hint"', 'patchConditionNot': True})
    
    patchlib.addInstruction({'filename': workfile, 'searchString': """<Blob Hash="7d1492e46d159b6979f70a415727a2be7e569e21" Size="342112" PackHash="feb61b7040721b885ad85174cfc802419600bda1" PackOffset="1545471" />""", 'replaceString': """<Blob Hash="7d1492e46d159b6979f70a415727a2be7e569e21" Size="342112" PackHash="feb61b7040721b885ad85174cfc802419600bda1" PackOffset="1545471" />
<Blob Hash="7d1daec3c6218ce9f49f9be0280091b98d7168d7" Size="456" PackHash="33e382aea05629bd179a60cf1520f77c025ac0b3" PackOffset="8" />""", 'versionMatch': "==4.25.4", 'patchConditionString': '<File Name="cpp.hint"', 'patchConditionNot': True})

    patchlib.addInstruction({'filename': workfile, 'searchString': """<Pack Hash="33d0a2949662b327b35a881192e85107ecafc8ac" Size="2097152" CompressedSize="655885" RemotePath="2369826-2acd3c361c9d4a858bd63938a2ab980e" />""", 'replaceString': """<Pack Hash="33d0a2949662b327b35a881192e85107ecafc8ac" Size="2097152" CompressedSize="655885" RemotePath="2369826-2acd3c361c9d4a858bd63938a2ab980e" />
<Pack Hash="33e382aea05629bd179a60cf1520f77c025ac0b3" Size="464" CompressedSize="235" RemotePath="UnrealEngine-14572338-da4318c3ab684bc48601f32f0b1b6fe3" />""", 'versionMatch': "==4.25.4", 'patchConditionString': '<File Name="cpp.hint"', 'patchConditionNot': True})

    pass