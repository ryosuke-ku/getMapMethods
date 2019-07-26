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
    tm_count = 0
    retm_count = 0
    for i in range(len(NtPath)): 
        Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド名をすべて取得
        Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(getNicadPath[i]) #プロダクションファイル内のメソッド名をすべて取得
        Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

        file = open(getNicadPath[i] ,'r')
        line = file.readline()
        line2 = file.readline()
      
        # print('<Nicad Path> ' + getNicadPath[i])
        # print('<プロダクションPath> ' + line2[2:].replace('\n',''))
        # print('<テストコードPath> ' + 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i])
        # print('<対応するクローンペアのPath> ' + line[2:].replace('\n',''))
        # print('<テストメソッド>')
        # # print(Testmethods_list)
        # for t in Testmethods_list:
        #     if 'test' in t:
        #         print(t)
        #         tm_count += 1

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
            # print('<プロダクションメソッド>')
            # print(key)
            # print('<再利用候補のテストメソッド>')
            reusemethods = rd["^(?=.*" + key + ").*$"]
            # print(rd["^(?=.*" + key + ").*$"])
            # print(len(rd["^(?=.*" + key + ").*$"]))
            if len(reusemethods) == 0:
                notest += 1
                # print('No Reuse Test')
            else:
                hastest += 1
                print('<Production Path> ' + line2[2:].replace('\n',''))
                print('<Test Code Path> ' + 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i])
                print('<Clone Pairs Path> ' + line[2:].replace('\n',''))
                print('<Test Methods>')
                # print(Testmethods_list)
                for t in Testmethods_list:
                    if 'test' in t:
                        print(t)
                        tm_count += 1

                print('<Production Methods>')
                print(key)
                print('<Reusable Test Methods>')
                for j in reusemethods:
                    print(j[0])
                # print(len(rd["^(?=.*" + key + ").*$"][0]))
                    retm_count += 1
                print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        except IndexError:
            # print('<プロダクションメソッド>')
            print('Error')
            nodetect += 1
            pass
        
        
        count += 1
    
    print('Project Name : ' + projectname)
    print('hastest : ' + str(hastest) + '(' + str(round(hastest/count*100,1)) + ')')
    print('notest : ' + str(notest)  + '(' + str(round(notest/count*100,1)) + ')')
    print('nodetect : ' + str(nodetect)  + '(' + str(round(nodetect/count*100,1)) + ')')
    print('Total : ' + str(count))
    print('Total Test Methods : ' + str(tm_count))
    print('Total Reusable Test Methods : ' + str(retm_count))
