# 导入模块，分配内存进行读写操作
from ctypes import *
from ctypes.wintypes import *

PAGE_EXECUTE_READWRITE = 0X00000040 #区域可执行代码，可读可写
MEM_COMMIT = 0x3000 #分配内存
PROCESS_ALL_ACCESS = (0X000f0000 | 0X00100000 | 0XFFF)#给予进程所有权限

# 调用windows api，以便于后续调用
# api
VirtalAlloc = windll.kernel32.VirtualAlloc