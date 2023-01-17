# 分析各个 AOSP 版本之间的 Aidl 差别
1. 扫描android 9 的aidl，作为模板 list
2. 扫描其他版本 的aidl来对比低版本的，记录新增的接口，改动的接口，删除的接口

数据结构：
```
frameworks {
_aidl : Map<"IPackageManager", List<Method>/*接口*/>
_version : String
}

Method {
_funcName : String
_funcArgs : MethodArg[]
_funcResult : String
}

MethodArg {
_type : String
_name : String
}
```