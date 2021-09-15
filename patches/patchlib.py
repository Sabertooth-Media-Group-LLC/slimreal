import os, re, subprocess, sys, json
import pandas as pd

# Not to be confused with pleb, this is python for big sneks.
class plib:

    # private members
    __verboseOutput = False
    __patchData = pd.DataFrame(columns = ['filename', 'searchString', 'replaceString', 'versionMatch', 'patchConditionString', 'patchConditionNot'])
    
    # public members
    packageRoot = ""
    packageVersion = "1.0.0"
    
    # strings - allows for translation to other languages in verbose output at your leasure.
    __SUCCESS_SEARCH = "Succeeded for search string:"
    __SUCCESS_PATCH = "PATCHED SUCCESSFULLY"
    __FAIL_SEARCH = "Failed for search string:"
    __FAIL_PATCH = "FAILED TO PATCH"
    __SKIP_SEARCH = "Skipped for search string:"
    __SKIP_PATCH = "SKIPPED PATCH"
    __PARTIAL_SEARCH = "Patch condition string not in file:"
    __PARTIAL_PATCH = "PARTIALLY PATCHED"
    __REPLACED_SEARCH = "Replaced with:"
    
    def __init__(self, vbO):
        self.__verboseOutput = vbO
        pass
        
    def __readFile(self, filename):
        with open(filename, "rb") as f:
            return f.read().decode("utf-8")

    def __writeFile(self, filename, data):
        with open(filename, "wb") as f:
            f.write(data.encode("utf-8"))
    
    # hi.
    # i'm a template.
    # its nice to meet you.
    # use me for your pleasure.
    #
    # patchlib.addInstruction({'filename': os.path.join(patchlib.packageRoot, "rotflscssbllqqrrbrrbel.ext" ), 'searchString': """ """, 'replaceString': """ """, 'versionMatch': ">=4.0.0", 'patchConditionString': NaN})
    def addInstruction(self, matchInstruction):
        __patchData.append(data, ignore_index=True)
    
   # TODO: no removeInstruction?  probably not needed right now.
   def removeInstruction(self, matchInstruction):
        # Not implimented.
        pass

    # specific to the unreal engine.
    def getUnrealEnginePackageVersion(self):
        return "%(MajorVersion)s.%(MinorVersion).%(PatchVersion)s" % **(json.loads(readFile(os.path.join(self.packageRoot, "Engine", "Build", "Build.version"))))
        
    # aaand this commit makes it more generic.  because why the hell not?  data-driven patch management doesn't
    # exist so, i just created it, enjoy it, python community.
    def __compareVersion(self, versionComparitor):
        versions = list()
        # syntactic map
        versionRegexMatch = re.fullmatch(r`'^\s*([0-9.]*)\s*([\>\<\=]*)\s*([0-9.]*)\s*$/g', versionComparitor)
        versions.append([int(v) for v in versionRegexMatch[0].split(".")])
        versions.append([int(v) for v in versionRegexMatch[2].split(".")])
        for i in range(max(len(versions[0]),len(versions[2]))):
            v1 = versions[0][i] if i < len(versions[0]) else 0
            v2 = versions[2][i] if i < len(versions[2]) else 0
            # operator map
            if v2 > v1 and versionRegexMatch[1] ==">":
               return True
            elif v2 < v1 and versionRegexMatch[1] == "<":
               return True
            elif v2 <= v1 and versionRegexMatch[1] == "<=":
               return True
            elif v2 >= v1 and versionRegexMatch[1] == ">=":
               return True
            elif v2 == v1 and (versionRegexMatch[1] == "=" or versionRegexMatch[1] == "=="):
               return True
            elif v2 != v1 and versionRegexMatch[1] == "!=":
               return True
        return False

    def __outputSkipped(self, fileName, fileResult):
        if self.__verboseOutput == True:
            print("{} {}:\n\n{}".format(self.__SKIP_PATCH, fileName, fileResult), file=sys.stderr)
        else:
            print("{} {}".format(self.__SKIP_PATCH, fileName), file=sys.stderr)
    
    def __outputFailed(self, fileName, fileResult):
        if self.__verboseOutput == True:
            print("{} {}:\n\n{}".format(self.__FAIL_PATCH, fileName, fileResult), file=sys.stderr)
        else:
            print("{} {}".format(self.__FAIL_PATCH, fileName), file=sys.stderr)
            
    def __outputPartial(self, fileName, fileResult):
        if self.__verboseOutput == True:
            print("{} {}:\n\n{}".format(self.__PARTIAL_PATCH, fileName, fileResult), file=sys.stderr)
        else:
            print("{} {}".format(self.__PARTIAL_PATCH, fileName), file=sys.stderr)
    
    def __outputPatched(self, fileName, fileResult):
        if self.verboseOutput == True:
            print("{} {}:\n\n{}".format(self.__SUCCESS_PATCH, fileName, fileResult), file=sys.stderr)
        else:
            print("{} {}".format(self.__SUCCESS_PATCH, fileName), file=sys.stderr)

    # welp.
    def patchFiles(self):
        # perform query, filter by version match predicate.
        patchFileGrp = self.__patchData.groupby("filename", sort=False)["searchString", "replaceString", "versionMatch", "patchConditionString", "patchConditionNot"].filter(lambda x: (self.__compareVersion(self.packageVersion.join(x["versionMatch"]))).any())
        
        # loop through files
        for filename, patchGrp in patchFileGrp:

            # initialize variables for each loop
            fname = os.path.join(self.packageRoot, filename)
            contents = self.__readFile(fname)
            patched = contents
            result = ""
            
            # loop through rows grouped by this file
            for index, row in patchGrp.iterrows():
                
                # evaluate patch conditions.
                pResult = ((row["patchConditionString"] == NaN ? " " : row["patchConditionString"]) in contents)
                if (row["patchConditionNot"] == NaN ? False : row["patchConditionNot"]) == True:
                    pResult = not pResult     
                 
                # evaluate search and replace conditions.
                if pResult:
                    if row["replaceString"] not in contents:
                        if row["searchString"] in contents:
                            patched = patched.replace(row["searchString"], row["replaceString"])
                            result += "{}\n\n{}\n\n{}\n\n{}\n".format(self.__SUCCESS_SEARCH, row["searchString"], self.__REPLACED_SEARCH, row["replaceString"])
                        else:
                            result += "{}\n\n{}\n".format(self.__FAIL_SEARCH, row["searchString"])
                    else:
                        result += "{}\n\n{}\n".format(self.__SKIP_SEARCH, row["searchString"])
                else:
                    result += "{}\n\n{}\n\n\n-----\n\n{}\n\n{}".format(self.__SKIP_SEARCH, row["searchString"], self.__PARTIAL_SEARCH, row["patchConditionString"])
            
            # do operations
            if self.__SUCCESS_SEARCH in result and not self.__SKIP_SEARCH in result and not self.__FAIL_SEARCH in result:
                self.__writeFile(self, fname, patched)
                self.__outputPatched(self, fname, result)
            elif self.__SKIP_SEARCH in result and not self.__FAIL_SEARCH in result and not self.__SUCCESS_SEARCH in result:
                self.__outputSkipped(self, fname, result)
            elif self.__FAIL_SEARCH in result and not self.__SUCCESS_SEARCH in result:
                self.__outputFailed(self, fname, result)
            else:
                self.__writeFile(self, fname, patched)
                self.__outputPartial(self, fname, result)

            
patchlib = plib(False)