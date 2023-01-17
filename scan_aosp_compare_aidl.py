# 
import os
import re



class stFrameworks:
    def __init__(self, aidl, version, aidl_count):
        self._aidl = aidl # dict<filename, list<stMethod>>
        self._version = version
        self._aidl_count = aidl_count
        
    def toString(self):
        return "stFrameworks:{[%d] [%d]}" %(self._version, self._aidl_count)
    
    def printAidls(self):
        for name,methods in self._aidl.items():
            print("name[%s]: count[%d]" %(name, len(methods)))
            for m in methods:
                print(m.toString())
            

class stMethod:
    def __init__(self, name, args, _result):
        self._name = name
        self._args = args
        self._result = _result
        
    def toString(self):
        argsStr = ""
        for arg in self._args:
            argsStr += arg.toString() + ", "
        if argsStr.endswith(", "):
            argsStr = argsStr[:argsStr.rfind(",")]
        return "stMethod:{%s %s [%s]}" %(self._result, self._name, argsStr)
    
class stMethodArg:
    def __init__(self, type, name):
        self._type = type
        self._name = name
        
    def toString(self):
        return "{%s : %s}" %(self._type, self._name)

def reFindFirstMatch(line, pattern):
    res = re.findall(pattern, line)
    if not res or len(res) <= 0:
        return ""
    res = res[0]
    return res

def parseLineToArgs(line):
    args_res = []
    if line :
        # print("parseLineToArgs:line " + line)
        args_arr = line.split(", ")
        for arg in args_arr:
            m = arg.split(" ")
            if m and len(m) == 2:
                # print("type = " + m[0] + " name = " + m[1])
                arg_st = stMethodArg(m[0], m[1])
                args_res.append(arg_st)
            elif m and len(m) == 3:
                arg_st = stMethodArg(m[1], m[2])
                args_res.append(arg_st)
                
    return args_res
    

def parseLineToMethod(line):
    # print("parseLineToMethod: [%s]" %line)
    name = reFindFirstMatch(line, r" ([a-zA-Z0-9]+)\(")
    args_str = reFindFirstMatch(line, r"\((.+)\)")
    args = parseLineToArgs(args_str)
    result = line.replace(name, "").replace("("+args_str+");", "").replace("oneway", "").strip()
    
    # print("parseLineToMethod:funcName " + funcName)
    # print("parseLineToMethod:funcArgs " + str(funcArgs))
    # print("parseLineToMethod:funcResult " + funcResult)
    method1 = stMethod(name, args, result)
    # print("method: [%s]" %method1.toString())
    return method1
    
def isMethodLine(line):
    ret = True
    method_not_include_pattern = ["interface", "@", "{", "/", "*/", "*", "package", "const", "import"]
    
    for pattern in method_not_include_pattern:
        if line.startswith(pattern):
            ret = False
            break
    # print("isMethodLine : line = " + line + " return " + str(ret))
    return ret
    
def scanFrameworksAndParse(curpath, version):
    os.chdir(curpath)
    aidl = {}
    aidl_count = 0
    for root, dirs, files in os.walk(curpath, topdown=False):
        for f in files:
            if f.endswith(".aidl"):
                f_abs = "%s/%s"%(root, f)
                f = open(f_abs, "r")
                
                all_content = f.read()
                f.seek(0, 0)
                
                i1 = f.name.rfind('/')
                i2 = f.name.rfind('.')
                aidl_name = f.name[i1 + 1:i2]
                
                # print("filename = " + filename)
                if "interface " + aidl_name not in all_content:
                    # print("interface %s not in file" % filename)
                    continue

                methods = []
                method_line_arr = []
                
                while True:
                    line = f.readline()
                    if not line:
                        break
                    line = line.strip().replace('\n', '').replace('\r', '').replace('\r\n', '')
                    if line and isMethodLine(line) :
                        method_line_arr.append(line)
                        if not line.endswith(';'):
                            continue
                        
                        method_line = ""
                        for it_line in method_line_arr:
                            method_line += it_line + " "
                            
                        m = parseLineToMethod(method_line)
                        if m:
                            methods.append(m)
                        method_line_arr.clear()
                
                aidl[aidl_name] = methods
                aidl_count += 1
    framework = stFrameworks(aidl, version, aidl_count)
    return framework


if __name__ == "__main__":
    framework = scanFrameworksAndParse("/home/eason/sad/android-12.0.0_r3/frameworks", 12)
    print(framework.toString())
    framework.printAidls()