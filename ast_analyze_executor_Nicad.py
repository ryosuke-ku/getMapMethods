import logging.config
from ast.ast_processor_Production import AstProcessorProduction
from ast.ast_processor_Test import AstProcessorTest
from ast.ast_processor_TestMethodCall import AstProcessorTestMethodCall
from ast.basic_info_listener_pt import BasicInfoListener
import glob
import re
import os
from collections import defaultdict

class rdict(dict):
    def __getitem__(self, key):
        try:
            return super(rdict, self).__getitem__(key)
        except:
            try:
                ret=[]
                for i in self.keys():
                    m= re.match("^"+key+"$",i)
                    if m:ret.append( super(rdict, self).__getitem__(m.group(0)) )
            except:raise(KeyError(key))
        return ret


if __name__ == '__main__':
    t = 't1'
    projectname = 'maven_0726'

    NicadTest = open(r'TestPath_' + t + '_' + projectname + '.txt','r',encoding="utf-8_sig")
    NicadTestPath = NicadTest.readlines()
    NtPath = [Ntline.replace('\n', '') for Ntline in NicadTestPath]

    getNicadPath = []
    for n in range(len(NtPath)):
        name = 'C:/Users/ryosuke-ku/Desktop/SCRAPING/Method_Scraping/xml_scraping/NicadOutputFile_' + t + '_' + projectname + '/Nicad_' + t + '_' + projectname + str(n+1) + '.java'
        getNicadPath.append(name)

    notest = 0
    hastest = 0
    nodetect = 0
    count = 0
    for i in range(len(NtPath)): 
        Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド名をすべて取得
        Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(getNicadPath[i]) #プロダクションファイル内のメソッド名をすべて取得
        Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

        file = open(getNicadPath[i],'r')
        line = file.readline()
        line2 = file.readline()
        print('<Production Code Path> ' + line2[2:].replace('\n',''))

        # print('<プロダクションコードPath>' + getNicadPath[i])
        print('<Test Code Path> ' + 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i])
        print('<Clone Pairs Path> ' + line[2:].replace('\n',''))
        print('<Test Methods>')
        # print(Testmethods_list)
        for t in Testmethods_list:
            print(t)

        cnt = 1
        methodmapcall = defaultdict(list)
        for k in Testmethodcalls_list:
            # print(k)
            for l in Testmethodcalls_list[k]:
                for m in l:
                    methodcall = str(cnt) + ':' + m
                    # print(methodcall)
                    methodmapcall[methodcall].append(k)
                    cnt+=1


        # print(methodmapcall)
        # print(methodmapcall['137:clone.getRepositories()'][0])
        rd = rdict(methodmapcall)
        

        try:
            key = Productionmethods_list[0]
            print('<Production Methods>')
            print(key)
            print('<Reusable Test Methods>')
            print(rd["^(?=.*" + key + ").*$"])
            # print(len(rd["^(?=.*" + key + ").*$"]))
            if len(rd["^(?=.*" + key + ").*$"]) == 0:
                notest += 1
            else:
                hastest += 1

        except IndexError:
            print('<Production Methods>')
            print('Error')
            nodetect += 1
            pass
        
        print('---------------------------------------------------------------------------------------------------------------------')
        count += 1
    
    print('hastest : ' + str(hastest) + '(' + str(round(hastest/count*100,1)) + ')')
    print('notest : ' + str(notest)  + '(' + str(round(notest/count*100,1)) + ')')
    print('nodetect : ' + str(nodetect)  + '(' + str(round(nodetect/count*100,1)) + ')')
    print('Total : ' + str(count))
