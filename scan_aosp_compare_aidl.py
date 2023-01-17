# 
import os
import re



class frameworks:
    def __init__(self, aidl, version):
        self._aidl = aidl
        self._version = version


class stMethod:
    def __init__(self, funcName, funcArgs, funcResult):
        self._funcName = funcName
        self._funcArgs = funcArgs
        self._funcResult = funcResult
        
    def toString(self):
        argsStr = ""
        for arg in self._funcArgs:
            argsStr += arg.toString() + ", "
        return "stMethod:{[%s] [%s] [%s]}" %(self._funcResult, self._funcName, argsStr)
    
class stMethodArg:
    def __init__(self, type, name):
        self._type = type
        self._name = name
        
    def toString(self):
        return "arg:{%s : %s}" %(self._type, self._name)


# curpath = "/home/eason/sad/android-12.0.0_r3/frameworks"
curpath = "/home/eason/workspace/scripts/scan_aosp"
os.chdir(curpath)

def reFindFirstMatch(line, pattern):
    funcName = re.findall(pattern, line)
    if not funcName or len(funcName) <= 0:
        return ""
    funcName = funcName[0]
    return funcName

def parseLineToArgs(line):
    argsResult = []
    if line :
        # print("parseLineToArgs:line " + line)
        argsArr = line.split(", ")
        for arg in argsArr:
            m = arg.split(" ")
            if m and len(m) == 2:
                # print("type = " + m[0] + " name = " + m[1])
                argSt = stMethodArg(m[0], m[1])
                argsResult.append(argSt)
            elif m and len(m) == 3:
                argSt = stMethodArg(m[1], m[2])
                argsResult.append(argSt)
                
    return argsResult
    

def parseLineToMethod(line):
    print("parseLineToMethod:line " + line)
    funcName = reFindFirstMatch(line, r" ([a-zA-Z0-9]+)\(")
    funcArgsStr = reFindFirstMatch(line, r"\((.+)\)")
    funcArgs = parseLineToArgs(funcArgsStr)
    funcResult = line.replace(funcName, "").replace("("+funcArgsStr+");", "").strip()
    
    # print("parseLineToMethod:funcName " + funcName)
    # print("parseLineToMethod:funcArgs " + str(funcArgs))
    # print("parseLineToMethod:funcResult " + funcResult)
    method1 = stMethod(funcName, funcArgs, funcResult)
    print("method: " + method1.toString())
    return True
    
def isMethodLine(line):
    ret = True
    methodNotIncludePattern = ["interface", "@", "{", "/", "*/", "*"]
    
    for pattern in methodNotIncludePattern:
        if line.startswith(pattern):
            ret = False
            break
    # print("isMethodLine : line = " + line + " return " + str(ret))
    return ret
    

for root, dirs, files in os.walk(curpath, topdown=False):
    for f in files:
        if f.endswith(".aidl"):
            f_abs = "%s/%s"%(root, f)
            f = open(f_abs, "r")
            
            methodLineArr = []
            
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().replace('\n', '').replace('\r', '').replace('\r\n', '')
                if line and isMethodLine(line) :
                    methodLineArr.append(line)
                    if not line.endswith(';'):
                        continue
                    
                    methodLine = ""
                    for itLine in methodLineArr:
                        methodLine += itLine + " "
                        
                    parseLineToMethod(methodLine)
                    methodLineArr.clear()
                
            
