from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from ast.JavaLexer import JavaLexer
from ast.JavaParser import JavaParser
from pprint import pformat
from ast.ast_processor_pt_test import AstProcessorTest
from ast.basic_info_listener_pt import BasicInfoListener
import re
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

class AstProcessor:

    def __init__(self, logging, listener):
        # self.logging = logging
        # self.logger = logging.getLogger(self.__class__.__name__)
        self.listener = listener

    # ★ポイント２
    def execute(self, input_source):
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        walker = ParseTreeWalker()
        walker.walk(self.listener, parser.compilationUnit())

        cnt = 1
        listmethods = [] #テストメソッドを格納するリスト
        listcallmethods = [] #テストメソッド内で呼び出されているメソッド呼び出しを格納するリスト

        ProductionPath = 'C:/Users/ryosuke-ku/Desktop/NiCad-5.1/systems/maven/maven-model-builder/src/main/java/org/apache/maven/model/interpolation/StringSearchModelInterpolator.java'
        methods_list = AstProcessorTest(None, BasicInfoListener()).execute(ProductionPath) #プロダクションファイルから取得したメソッド名(リスト)
        for method in self.listener.methods:
            num = len(self.listener.called_methods[method][0]) #メソッド呼び出しの個数
            # print(num)

            for i in range(num):
                # print(method + '/' + self.listener.called_methods[method][0][i])
                listmethods.append(method) #listmethodsにテストメソッド名をメソッド呼び出しの数だけ格納する
                listcallmethods.append(str(cnt) + ' ' + self.listener.called_methods[method][0][i]) #テストメソッド内で呼び出されているメソッド呼び出しを格納する、同じ名前のメソッド呼び出しを区別するためのcntのつける
                cnt +=1

        d = dict(zip(listcallmethods,listmethods)) #テストメソッド名とテストメソッド内で呼び出されているメソッド呼び出しを １：リスト(複数) で対応付ける
        # print(d)

        rd = rdict(d)
        

        # print(listmethods)
        # print(len(listmethods))
        # print(listcallmethods)
        # print(len(listcallmethods))
       
        # print(methods_list)
        # print('------------------------')

        dicMethods = defaultdict(list) #プロダクションファイルのすべてのメソッド名とテストファイルのすべてのメソッド名を対応付け
        for key in methods_list:
            # print(key)
            
            if rd["^(?=.*" + key + ").*$"] == []: #keyを正規表現で与えて、valueが空の時
                pass
            
            else:
                dicMethods[key].append(rd["^(?=.*" + key + ").*$"]) #プロダクションファイルのすべてのメソッド名とテストファイルのすべてのメソッド名を 1:リスト(複数) で対応付ける
                # print(key)
                # print(rd["^(?=.*" + key + ").*$"])
                # print(len(rd["^(?=.*" + key + ").*$"]))
        
        # print(dicMethods)
        # return self.listener.ast_info