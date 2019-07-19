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
    getNicadPath = []
    for n in range(351):
        name = 'C:/Users/ryosuke-ku/Desktop/SCRAPING/Method_Scraping/xml_scraping/NicadOutputFile/Nicad_' + str(n+1) + '.java'
        getNicadPath.append(name)

    # print(getNicadPath)

    NicadTest = open(r'TestPath.txt','r',encoding="utf-8_sig")
    NicadTestPath = NicadTest.readlines()
    NtPath = [Ntline.replace('\n', '') for Ntline in NicadTestPath]

    # print(NtPath)

    Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[203]) #target_file_path(テストファイル)内のメソッド名をすべて取得
    Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(getNicadPath[203]) #プロダクションファイル内のメソッド名をすべて取得
    Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[203]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

    # print(Testmethodcalls_list)
    # print('---------------------------------------------------------------------------------------------------------------------')
    print(Productionmethods_list)
    print('---------------------------------------------------------------------------------------------------------------------')
    print(Testmethods_list)

    # print(Testmethodcalls_list.keys())
    # print(Testmethodcalls_list['testShouldAppendRecessivePluginGroupIds'])
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
    print(len(methodmapcall))
    # print(methodmapcall['137:clone.getRepositories()'][0])
    rd = rdict(methodmapcall)
    

    try:
        key = Productionmethods_list[0]
        print(Productionmethods_list[0])
        print(rd["^(?=.*" + key + ").*$"])
    except IndexError:
        print('Error')
        pass
     
        



    notest = 0
    hastest = 0
    count = 0
    for i in range(351): 
        Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド名をすべて取得
        Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(getNicadPath[i]) #プロダクションファイル内のメソッド名をすべて取得
        Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

        # print(Testmethodcalls_list)
        # print('---------------------------------------------------------------------------------------------------------------------')
        # print(Productionmethods_list)
 
        print('<プロダクションコードPath>' + getNicadPath[i])
        print('<テストコードPath>' + 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i])
        print('<テストメソッド>')
        print(Testmethods_list)

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
            print('<プロダクションメソッド>')
            print(key)
            print(rd["^(?=.*" + key + ").*$"])
            # print(len(rd["^(?=.*" + key + ").*$"]))
            if len(rd["^(?=.*" + key + ").*$"]) == 0:
                notest += 1
            else:
                hastest += 1

        except IndexError:
            print('<プロダクションメソッド>')
            print('Error')
            pass
        
        print('---------------------------------------------------------------------------------------------------------------------')
        count += 1
    
    print('hastest : ' + str(hastest))
    print('notest : ' + str(notest))
    print('Total : ' + str(count))









    




    # for i in range(351):
    #     Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド名をすべて取得
    #     Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(getNicadPath[i]) #プロダクションファイル内のメソッド名をすべて取得
    #     Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + NtPath[i]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

    #     print(Testmethodcalls_list)
    #     print('---------------------------------------------------------------------------------------------------------------------')
    #     print(Productionmethods_list)
    #     print('---------------------------------------------------------------------------------------------------------------------')
    #     print(Testmethods_list)


    # production = open(r'AvaiProductionPaths.txt','r',encoding="utf-8_sig")
    # ProductionPath = production.readlines()
    # PPath = [Pline.replace('\n', '') for Pline in ProductionPath]
    # # print(len(PPath))
    # # print(PPath[0])

    # Test = open(r'AvaiTestPaths.txt','r',encoding="utf-8_sig")
    # TestPath = Test.readlines()
    # TPath = [Tline.replace('\n', '') for Tline in TestPath]
    # # print(len(TPath))

    # ProductionPath = 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/maven/maven-model-builder/src/main/java/org/apache/maven/model/interpolation/StringSearchModelInterpolator.java'

    # findmethod = 0
    # allcount = 0
    # for i in range(555):
    #     Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + TPath[i]) #target_file_path(テストファイル)内のメソッド名をすべて取得
    #     Productionmethods_list = AstProcessorProduction(None, BasicInfoListener()).execute(ProductionPaths[i]) #プロダクションファイル内のメソッド名をすべて取得
    #     Testmethods_list = AstProcessorTest(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + TPath[i]) #target_file_path(テストファイル)内のメソッド呼び出しをすべて取得

    #     # for productionmethod in Productionmethods_list:
    #     #     print(productionmethod)

    #     # print('\n')
        
    #     # for testmethod in Testmethods_list:
    #     #     print(testmethod)
    #     #     print(Testmethodcalls_list[testmethod][0])

    #     cnt = 1
    #     listmethods = [] #テストメソッドを格納するリスト
    #     listcallmethods = [] #テストメソッド内で呼び出されているメソッド呼び出しを格納するリスト

    #     for method in Testmethods_list:
    #         num = len(Testmethodcalls_list[method][0]) #メソッド呼び出しの個数
    #         # print(num)

    #         for i in range(num):
    #             # print(method + '/' + Testmethodcalls_list[method][0][i])
    #             listmethods.append(method) #listmethodsにテストメソッド名をメソッド呼び出しの数だけ格納する
    #             listcallmethods.append(str(cnt) + ' ' + Testmethodcalls_list[method][0][i]) #テストメソッド内で呼び出されているメソッド呼び出しを格納する、同じ名前のメソッド呼び出しを区別するためのcntのつける
    #             cnt +=1

    #     d = dict(zip(listcallmethods,listmethods)) #テストメソッド名とテストメソッド内で呼び出されているメソッド呼び出しを １：リスト(複数) で対応付ける
    #     # print(d)
    #     rd = rdict(d)

    #     dicMethods = defaultdict(list) #プロダクションファイルのすべてのメソッド名とテストファイルのすべてのメソッド名を対応付け
    #     for key in Productionmethods_list: #プロダクションファイルから取得できたメソッド名をキーとして辞書で検索をかける
    #         # print(key) 
    #         if rd["^(?=.*" + key + ").*$"] == []: #keyを正規表現で与えて、valueが空の時
    #             # print('見つかりませんでした')
    #             allcount+=1
    #         else:
    #             dicMethods[key].append(rd["^(?=.*" + key + ").*$"]) #プロダクションファイルのすべてのメソッド名とテストファイルのすべてのメソッド名を 1:リスト(複数) で対応付ける
    #             # print(key)
    #             # print(rd["^(?=.*" + key + ").*$"])
    #             # print(len(rd["^(?=.*" + key + ").*$"]))
    #             findmethod+=1
    #             allcount+=1

    # print(findmethod)
    # print(allcount)
    # print(findmethod/allcount)
    #     # print(rd)



    # # print(Testmethodcalls_list)
    # # Testmethodcalls_list = AstProcessorTestMethodCall(None, BasicInfoListener()).execute(target_file_path)
    # # for testmethodcall in Testmethodcalls_list:
    # #     print(testmethodcall)

    # # ast_info = AstProcessor2(None, BasicInfoListener()).execute(ProductionPath)
    # # AvaiTestPathsfile = open(r'AvaiTestPaths.txt','r',encoding="utf-8_sig")
    # # readAvaiTestPathsfile = AvaiTestPathsfile.readlines()
    # # AvaiTestPaths = [readAvaiTestPath.replace('\n', '') for readAvaiTestPath in readAvaiTestPathsfile]
    # # print(AvaiTestPaths)

    # # for AvaiTestPath in AvaiTestPaths:
    # #     ast_info = AstProcessor(None, BasicInfoListener()).execute('C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/' + AvaiTestPath)
    