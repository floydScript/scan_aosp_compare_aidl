import os
import re



def read_first_line(f, f_abs):
    first_line = f.readline()
    if not first_line.startswith("#ifndef"):
        print("error : %s 第一行为 \"%s\""%(f_abs, first_line.strip()))
        first_line = read_first_line(f, f_abs)
    return first_line



curpath = "/home/eason/sad/vmos_kernel/libos_kernel_20201201"
os.chdir(curpath)


header_list = []

for root, dirs, files in os.walk(curpath, topdown=False):
    for f in files:
        if f.endswith(".h"):
            if f == "list_head.h" or f == "rbtree.h" or f == "__get_tls.h" or f == "rbtree_augmented.h":
                continue

            
            # h_map = {""}
            f_abs = "%s/%s"%(root, f)
            f = open(f_abs, "r")
            # first_line = f.readline()
            # if not first_line.startswith("#ifndef"):
            #     print("error :第一行为 %s"%first_line)
            first_line = read_first_line(f, f_abs)
            # print(f_abs)
            h_macro = first_line.replace("#ifndef", "").strip()
            
            f_rel = f_abs.replace(curpath, "")

            for h_dict in header_list:
                if h_macro == h_dict['macro']:
                    print(".%s  ::  .%s"%(h_dict["path"], f_rel))

            header_list.append({"path":f_rel, "macro":h_macro})
            f.close()



# file_mk = open("/home/eason/sad/Libos_kernel/Android.mk", "r")


# mk_content = file_mk.read()
# i = 0
# for cpp_path in cpp_list:
#     if mk_content.find(cpp_path) != -1:
#         i += 1
#     else:
#         print("FALSE : %s\n"%cpp_path)

# print("总共有cpp文件 %d 个, 在 /home/eason/sad/Libos_kernel/Android.mk 中找到 %d 个"%(len(cpp_list), i))