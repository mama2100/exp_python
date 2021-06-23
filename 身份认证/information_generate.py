import itertools
list_info = []
numberList = []
specialList = []
def generate_dic():
    name=input('目标姓名全拼:')
    j_name=input('目标姓名简拼:')
    phone = input('目标手机号码:')
    birthday = input('目标生日')
    birthday_year = input('目标生日（年）:')
    birthday_day = input('目标生日(月/日)')
    qq = input('目标qq号:')
    lover_name = input("目标爱人姓名全拼:")
    lover_jname = input('目标爱人简拼:')
    lover_phone = input('目标爱人手机号码:')
    lover_birthday = input('目标爱人生日:')
    lover_birthday_year= input("目标爱人生日(年)")
    lover_birthday_day = input("目标爱人生日/月/日")
    global dict1
    dict1={
    'name':name,
    'j_name':j_name,
    'phone':phone,
    'birthday':birthday,
    'birthday_year':birthday_year,
    'birthday_day':birthday_day,
    'qq':qq,
    'lover_name':lover_name,
    'lover_jname':lover_jname,
    'lover_phone':lover_phone,
    "lover_birthday":lover_birthday,
    'lover_birthday_year':lover_birthday_year,
    "lover_birthday_day":lover_birthday_day
    }
    return dict1

def ReadInformationList():
    for i in dict1.values():
        list_info.append(i)

def CreateNuberList():
    words = "0123456789"
    itertoolsNumberList = itertools.product(words,repeat=3)
    for number in itertoolsNumberList:
        # 写入数字列表备用
        numberList.append("".join(number))

def CreateSpecialList():
    specialWords = "~!@#$%^&*()?|/><,."
    for i in specialWords:
        specialList.append("".join(i))

def AddTopPwd():
    try:
        informationFile = open('E:\demo\exp_python\身份认证\TopPwd.txt','r')
        lines = informationFile.readlines()
        for line in lines:
            dictionaryFile.write(line)
    except Exception as e:
        print(str(e)+"\n")
        print("Read TopPwd error!")

def Combination():
    for a in range(len(list_info)):
        if (len(list_info[a]) >= 8 ):
            dictionaryFile.write(list_info[a]+'\n')
        #把个人信息大于等于8位的直接输出到字典    
        else:
            needwords = 8 - len(list_info[a])
            for b in itertools.permutations('1234567890',needwords):
                dictionaryFile.write(list_info[a]+''.join(b)+'\n')
        #对于小于8位的个人信息，利用数字补全到8位输出
        for c in range(0,len(list_info)):
            if (len(list_info[a]+list_info[c])>= 8):
                dictionaryFile.write(list_info[a]+list_info[c] +'\n')
                #在两个人个人信息中加入特殊字符组合起来，大于等于八位就输出到字典
        for d in range(0,len(list_info)):
            for e in range(0,len(specialList)):
                if (len(list_info[a] + specialList[e] + list_info[d]) >= 8):
                    dictionaryFile.write(list_info[a]+list_info[d]+specialList[e]+'\n')
                    #特殊字符加在尾部
                    dictionaryFile.write(list_info[a]+specialList[e]+list_info[d]+'\n')
                    #特殊字符加在中部
                    dictionaryFile.write(specialList[e]+list_info[a]+list_info[d]+'\n')
                    #特殊字符加在头部
    dictionaryFile.close()
                
if __name__ == '__main__':
    global dictionaryFile
    dictionaryFile = open('passwords','w')
    generate_dic()
    ReadInformationList()
    CreateNuberList()
    CreateSpecialList()
    AddTopPwd()
    Combination()
    print('\n' + u"字典生成成功！" + '\n' + '\n' + u"字典文件名：passwords")


          