# -*-coding:utf-8-*-
  
#===============================================================================
# 目录对比工具(包含子目录 )，并列出
# 1、A比B多了哪些文件
# 2、B比A多了哪些文件
# 3、二者相同的文件: md5比较
#===============================================================================
  
import os
import sys
import time
import difflib
import hashlib

# 获取md5值，如果文件不是MD5值要先获取MD5值
def getFileMd5(filename):
    if not os.path.isfile(filename):
        print('file not exist: ' + filename)
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

# 获取所有文件的路径,这里实现内部文件夹路径
def getAllFiles(path):
    flist=[]
    for root, dirs , fs in os.walk(path):
        for f in fs:
            f_fullpath = os.path.join(root, f)
            f_relativepath = f_fullpath[len(path):]
            flist.append(f_relativepath)
    return flist

def dirCompare(apath,bpath):
    afiles = getAllFiles(apath)
#    print(afiles)
    bfiles = getAllFiles(bpath)
#    print(bfiles)
    setA = set(afiles)
    setB = set(bfiles)

    commonfiles = setA & setB  # 处理共有文件
    for f in sorted(commonfiles):
        amd=getFileMd5(apath+f)
#        print(apath+""+f)
#        print(amd)
        bmd=getFileMd5(bpath+f)
#        print(bpath+""+f)
#        print(bmd)
        if amd != bmd:
            print("dif file: %s文件名相同，文件的MD5值不相等,进行替换。。。" % (f))
            os.remove(bpath+""+f)
            #time.sleep(5)
            #file_01=open(apath+""+f,encoding='gbk')
            #file_02=open(bpath+""+f,"w")
            #file_02.write(file_01.read())
            #file_01.close()
            #file_02.close()
            file_01=apath+""+f
            file_02=bpath+""+f
            os.popen("copy %s %s" %(file_01,file_02))
            print("替换完成!")
#        else:
#            print("dif file: %s,文件名相同，文件的MD5值相等，不处理！" % (f))

    # 处理仅出现在一个目录中的文件
    onlyFiles = setA ^ setB
    onlyInA = []
    onlyInB = []
    for of in onlyFiles:
        if of in afiles:
            onlyInA.append(of)
        elif of in bfiles:
            onlyInB.append(of)
    # 取A每一个文件，逐一与B的每一个文件进行对比，输出两文件MD5不相同的A文件
    if len(onlyInA) > 0:
        print ('-' * 20,"only in '"+apath+"' copy to '"+bpath+"'" ,'-' * 20)
        for of in sorted(onlyInA):
            print (of)
            #os.path.basename(of) #获取带后缀的文件名
            pt=os.path.split(of)    #输出为文件目录路径和文件名，元组
            if not os.path.exists(bpath+""+pt[0]):   #判断目录是否存在
                os.makedirs(bpath+""+pt[0])
            #file_01=open(apath+""+of,encoding='gbk')
            #file_02=open(bpath+""+of,"w")
            #file_02.write(file_01.read())
            #file_01.close()
            #file_02.close()
            file_01=apath+""+of
            file_02=bpath+""+of
            os.popen("copy %s %s" %(file_01,file_02))
            print("copy done!")
            
    if len(onlyInB) > 0:
        print ('-' * 20,"only in '"+bpath+"' Don't do processing!" ,'-' * 20)
        for of in sorted(onlyInB):
            print(of)
            if "\\app\\src\\main\\res" in of:   #此处Windows系统必须使用\对\进行转义
            	#os.popen("del /s/q %s" %of)
                os.remove(bpath+""+of)
                print ("del file...%s" %of)
            
#直接比较
def compare_a_b(apath, bpath):
    afiles = getAllFiles(apath)
    # print(afiles)
    bfiles = getAllFiles(bpath)
    # print(bfiles)
    for a in afiles:
        amd5=getFileMd5(apath + '/' + a)
        for b in bfiles :
            bmd5=getFileMd5(bpath + '/' + b)
            if amd5 == bmd5:
                print("a的文件名（直接比较）",a)
            
if __name__ == '__main__':
    #aPath = os.getcwd()+'/a'
    #bPath = os.getcwd()+'/b'
    aPath = sys.argv[1]
    bPath = sys.argv[2]
    dirCompare(aPath, bPath)
    #compare_a_b(aPath, bPath)
    print("\ndone!")
