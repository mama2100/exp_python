from ctypes import *  #C语言函数库
from ctypes.wintypes import *  #导入windows的底层函数
import sys #python 中的解释器模块

PAGE_EXECUTE_READWRITE = 0x00000040     # 区域可执行代码，可读可写
MEM_COMMIT = 0x3000                 # 分配内存
PROCESS_ALL_ACCESS = ( 0x000F0000 | 0x00100000 | 0xFFF )  #给予进程所有权限
