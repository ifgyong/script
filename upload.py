#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020-08-04 15:19
# @Author  : fgyong 简书:_兜兜转转_  https://www.jianshu.com/u/6d1254c1d145
# @Site    : http://fgyong.cn 兜兜转转的技术博客
# @File    : upload.py
# @Software: PyCharm
# 使用本脚本需要将本脚本移动至flutter项目根项目层级
#
import requests
import  os
import getopt
import sys
from enum import Enum
from requests_toolbelt.multipart import encoder


#  检查第三方包是否安装
def check_requirement(package):
    try:
        exec("import {0}".format(package))
    except ModuleNotFoundError:
        inquiry = input("This script requires {0}. Do you want to install {0}? [y/n]".format(package))
        while (inquiry != "y") and (inquiry != "n") and (inquiry != "N") and (inquiry != "Y") :
            inquiry = input("This script requires {0}. Do you want to install {0}? [y/n]".format(package))
        if inquiry == "y" or inquiry == "Y":
            import os
            print("Execute commands: pip install {0}".format(package))
            if int(sys.version.split('.')[0])==2:
                os.system("pip install {0}".format(package))
            elif int(sys.version.split('.')[0])==3:
                os.system("pip3 install {0}".format(package))
        else:
            print("{0} is missing, so the program exits!".format(package))
            exit(-1)




#  编译类型
class BuildMode(Enum):
    all=0
    debug = 1
    release =2
    @staticmethod
    def load(value):
        if value == 0:
            return BuildMode.all
        elif value == 1:
            return BuildMode.debug
        elif value ==2:
            return  BuildMode.release
#  上传类型
class UploadMode(Enum):
    all = 0
    apk = 1
    ipa = 2
    @staticmethod
    def load(value):
        if value == 0:
            return UploadMode.all
        elif value == 1:
            return UploadMode.apk
        elif value ==2:
            return  UploadMode.ipa
#  编译类别 安卓还是ios
class BuildType(Enum):
    all = 0
    apk = 1
    ipa = 2
    @staticmethod
    def load(value):
        if value == 1:
            return BuildType.apk
        elif value == 2:
            return BuildType.ipa
        elif value ==0:
            return  BuildType.all



class Runner:
    buildMode = BuildMode.release
    uploadMode = None
    buildType = None
    fileLength=1
    currentPath=''


    def main(self,argv):
        try:
            ops,args = getopt.getopt(argv,'-h-b:-u:-t:',['help','build=','upload=','type='])
        except getopt.GetoptError:
            sys.exit()
        count = 0
        for op,value in ops:
            if op in ('-h','--help'):
                count +=1
                self.pHelp()
                return
            elif op in ('-u', '--upload'):
                count += 1
                if ['all','apk','ipa'].__contains__(value) ==False:
                    self.pHelp()
                else:
                    self.uploadMode=UploadMode(['all','apk','ipa'].index(value))
            elif op in('-b','--build'):
                count += 1
                # self.p('-b:{0}'.format(value))
                if ['all','debug','release'].__contains__(value)==False:
                    self.pHelp()
                else:
                    self.buildMode=BuildMode.load(['all','debug','release'].index(value))
            elif op in('-t','--type'):
                count += 1
                # self.p('-t:{0}'.format(value))
                if ['all','apk','ipa'].__contains__(value)==False:
                    self.pHelp()
                else:
                    self.buildType=BuildType.load(['all','apk','ipa'].index(value))
        if count ==0:
            self.pHelp()
            return
        else:


            if not self.buildType:
                self.p('\n 请输入 -b buildType 参数 \n')
                self.pHelp()
                return
            if not self.uploadMode:
                self.p('\n 请输入 -u uploadMode 参数 \n')
                self.pHelp()
                return

        self.p('{0}{1}{2}'.format(self.buildMode, self.buildType,self.uploadMode))
        # 开始编译和上传ipa
        self.currentPath = os.getcwd()
        self.build()
        self.upload()


    def p(self,str):
        # 结束标示： \n\033[0m
        print('\033[0;35;48m  '+str+'')


    def pHelp(self):
        self.p('-h --help 获取帮助信息')
        self.p('-b --build 编译模式[release(default),debug,all]')
        self.p('-u --upload 上传模式[apk,ipa]')
        self.p('-t --type  编译种类[all,apk,ipa]')

    def buildAPK(self):
        try:
            if self.buildMode==BuildMode.release :
                os.system('flutter --no-color build apk'),
            if self.buildMode==BuildMode.debug :
                os.system('flutter --no-color build apk --debug'),
        except KeyError as e:
            print(e)
    def buildIPA(self,):
        try:
            if self.buildMode==BuildMode.release:
                os.system('flutter --no-color build ios --release'),
                os.chdir(self.currentPath+'/ios')
                plus='agvtool next-version -all'
                arch = 'xcodebuild -workspace Runner.xcworkspace -scheme Runner archive -archivePath ./build/Runner.xcarchive'
                export = 'xcodebuild -exportArchive -archivePath $PWD/build/Runner.xcarchive -exportOptionsPlist "./exportOptions.plist" -exportPath ./build/'
                os.system(arch)
                os.system(plus)
                os.system(export)



            elif self.buildMode==BuildMode.debug:
                os.system('flutter --no-color build ios --debug'),
        except KeyError as e:
            print(e)

    # 编译函数
    def build(self,):
        if self.buildType==BuildType.apk:
            self.buildAPK()
        elif self.buildType==BuildType.ipa:
            self.buildIPA()
        elif self.buildType==BuildType.all:
            self.buildAPK()
            self.buildIPA()
    def uploadFile(self,filePath,name='runner.ipa'):
        self.p(' 开始上传' + filePath)
        url = 'https://www.pgyer.com/apiv2/app/upload'
        file = open(filePath, 'rb')
        # dataJson = {
        #     '_api_key': '2e8571d626b9a8c8b752e59624481847',
        #     'buildInstallType': '3',
        #     'buildPassword': '',
        # }
        # 没有进度条的上传
        # fileDir = {'file': file}
        # response = requests.post(url, files=fileDir, data=dataJson)
        # jsonStr = response.json()


        e = encoder.MultipartEncoder(
            fields={
                '_api_key': '2e8571d626b9a8c8b752e59624481847',
                #     'buildInstallType': '3',
                #     'buildPassword': '',
                    'file': (name,file,'application/x-www-form-urlencoded'),
                    },
        )
        m = encoder.MultipartEncoderMonitor(e, self.my_callback)
        h = {'Content-Type': m.content_type,"enctype":"multipart/form-data"}
        self.fileLength = os.path.getsize(filePath)
        r = requests.post(url, data=m,headers=h).json()


        if int(dict(r).get('code')) != 0:
            raise Exception('上传失败:{0}'.format(dict(r).get('message')), )
        else:
            self.p(str(r).replace('u\'','\''))# 去掉前边的u
            self.p(filePath + '上传成功')

    def my_callback(self,monitor):
        total = 50
        pro =int((monitor.bytes_read *1.0)/self.fileLength * 1.0 * total)
        unit = 1000 * 1000.0
        sys.stdout.write(
            '\r' + str(pro * '\033[46;34m \033[0m') + str((total - pro) * '\033[40;30m \033[0m') + '[{0}M/{1}M]'.format( round(monitor.bytes_read/unit,2),round(self.fileLength/unit,2)))
        sys.stdout.flush()
    # 上传函数
    def upload(self,):
        currentPath=self.currentPath
        if self.uploadMode== UploadMode.apk or self.uploadMode==UploadMode.all:
            if self.buildMode==BuildMode.debug or self.buildMode==BuildMode.all:
                filePath=currentPath+'/build/app/outputs/apk/debug/app-debug.apk'

                try:
                    self.uploadFile(filePath, name='app-debug.apk')

                except Exception as e:
                    self.p(e.__str__())
                    exit()
            if self.buildMode==BuildMode.release or self.buildMode==BuildMode.all:
                filePath = currentPath+'/build/app/outputs/apk/release/app-release.apk'
                try:
                    self.uploadFile(filePath, name='app-release.apk')
                except Exception as e:
                    self.p(e.__str__())
                    exit()

        if self.uploadMode==UploadMode.ipa or self.uploadMode==UploadMode.all:
            f = os.getcwd()+'/ios/build/Runner.ipa'
            if os.path.isdir(f) or os.path.isfile(f):
                self.uploadFile(f,name='Runner.ipa')
                mv = 'mv ios/build/Runner.ipa ios/output/Runner.ipa'
                rm = 'rm -rf ios/build/'
                os.system(mv)# 移动ipa
                os.system(rm)# 删除 build文件夹
            else:
                self.p('没有发现ipa文件:'+f)



if __name__ == '__main__':
    libs = ['requests','requests_toolbelt']
    for i in libs:
        check_requirement(i)  # 检查是否安装该安装包
    Runner().main(sys.argv[1:])







