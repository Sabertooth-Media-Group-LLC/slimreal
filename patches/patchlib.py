import os, re, subprocess, sys, json
import pandas as pd

# Not to be confused with pleb, this is advanced python.
class plib:

    __verboseOutput = False
    __patchData = pd.DataFrame(columns = ['filename', 'searchString', 'replaceString', 'versionMatch'])
    engineRoot = ""
    
    def __init__(self, vbO):
        self.__verboseOutput = vbO
        pass
        
    def __readFile(self, filename):
        with open(filename, "rb") as f:
            return f.read().decode("utf-8")

    def __writeFile(self, filename, data):
        with open(filename, "wb") as f:
            f.write(data.encode("utf-8"))

    # You *could* make this more generic if you wanted.  But
    # this is specific to the Unreal Engine source code, so
    # thats your job if you want patch management for your game.
    def __compareVersion(self, versionComparitor):
        versions = list()
        versions.append([int(v) for v in ("%(MajorVersion)s.%(MinorVersion).%(PatchVersion)s" % **(json.loads(readFile(join(engineRoot, "Engine", "Build", "Build.version"))))).split(".")])
        versionRegexMatch = re.fullmatch(r`'^\s*([\>\<\=]*)\s*([0-9.]*)\s*$/g', versionComparitor)
        versions.append([int(v) for v in versionRegexMatch[1].split(".")])
        for i in range(max(len(versions[0]),len(versions[1]))):
            v1 = versions[0][i] if i < len(versions[0]) else 0
            v2 = versions[1][i] if i < len(versions[1]) else 0
            if v2 > v1 and versionRegexMatch[0].contains(">"):
               return True
            elif v2 < v1 and versionRegexMatch[0].contains("<"):
               return True
            elif v2 <= v1 and versionRegexMatch[0].contains("<="):
               return True
            elif v2 >= v1 and versionRegexMatch[0].contains(">="):
               return True
            elif v2 == v1 and versionRegexMatch[0].contains("="):
               return True
        return False

    def __outputSkipped(self, fileName, fileResult):
        if self.__verboseOutput == True:
            print("SKIPPED PATCH {}:\n\n{}".format(fileName, fileResult), file=sys.stderr)
        else:
            print("SKIPPED PATCH {}".format(fileName), file=sys.stderr)
    
    def __outputFailed(self, fileName, fileResult):
        if self.__verboseOutput == True:
            print("FAILED TO PATCH {}:\n\n{}".format(fileName, fileResult), file=sys.stderr)
        else:
            print("FAILED TO PATCH {}".format(fileName), file=sys.stderr)
            
    def __outputPartial(self, fileName, fileResult):
        if self.__verboseOutput == True:
            print("PARTIALLY PATCHED {}:\n\n{}".format(fileName, fileResult), file=sys.stderr)
        else:
            print("PARTIALLY PATCHED {}".format(fileName), file=sys.stderr)
    
    def __outputPatched(self, fileName, fileResult):
        if self.verboseOutput == True:
            print("PATCHED {}:\n\n{}".format(fileName, fileResult), file=sys.stderr)
        else:
            print("PATCHED {}".format(fileName), file=sys.stderr)

    def patchFiles(self):
        patchFileGrp = self.__patchData.groupby("filename", sort=False)["searchString", "replaceString", "versionMatch"].filter(lambda x: (self.__compareVersion(x["versionMatch"])).any())
        for filename, patchGrp in patchFileGrp:

            contents = self.__readFile(filename)
            patched = contents
            result = ""

            for index, row in patchGrp.iterrows():
                if row["replaceString"] not in contents:
                    if row["searchString"] in contents:
                        patched = patched.replace(row["searchString"], row["replaceString"])
                        result += "Succeeded for search string:\n\n{}\n\nReplaced with:\n\n{}\n".format(row["searchString"], row["replaceString"])
                    else:
                        result += "Failed for search string:\n\n{}\n".format(row["searchString"])
                else:
                    result += "Skipped for search string:\n\n{}\n".format(row["searchString"])

            if "Succeeded for search string:" in result and not "Skipped for search string:" in result and not "Failed for search string:" in result:
                self.__writeFile(self, filename, patched)
                self.__outputPatched(self, filename, result)
            elif "Skipped for search string:" in result and not "Failed for search string:" in result and not "Succeeded for search string:" in result:
                self.__outputSkipped(self, filename, result)
            elif "Failed for search string:" in result and not "Succeeded for search string:" in result:
                self.__outputFailed(self, filename, result)
            else:
                self.__writeFile(self, filename, patched)
                self.__outputPartial(self, filename, result)

            
patchlib = plib(False)