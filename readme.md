# 做一个分析脚本，分析各个aosp版本之间的aidl差别
1. 扫描android 9 的aidl，作为模板 list
2. 扫描其他版本 的aidl来对比低版本的，记录新增的接口，改动的接口，删除的接口

数据结构：
FrameworkAidl {
Map<"IPackageManager", List<Method>/*接口*/>
versionName : String
}



Method {
函数名 ：String
参数名 ：String[]
返回值 ：String
}

# 写脚本拉取独立包，获取base.apk