import re


print(re.match(r" ([a-zA-Z0-9]+)", '    void cancelAllNotifications(String pkg, int userId);'))  # 在起始位置匹配

print(re.findall(r" ([a-zA-Z0-9]+)\(", '    void cancelAllNotifications(String pkg, int userId);')[0])  # 在起始位置匹配



funcName = re.findall(r" ([a-zA-Z0-9]+)\(", '    void cancelAllNotifications(String pkg, int userId);')
if funcName and len(funcName) > 0:
    funcName = funcName[0]
    print("funcNAme = " + funcName)
    
    
    
class Employee:
   '所有员工的基类'
   empCount = 0
 
   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
      
"创建 Employee 类的第一个对象"
emp1 = Employee("Zara", 2000)
"创建 Employee 类的第二个对象"
emp2 = Employee("Manni", 5000)

print("Total Employee %d %s" % (Employee.empCount, emp1.name))
