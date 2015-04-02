# -*- coding: utf-8 -*-


from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

from CustomRunner import CustomRunner

class TestClass(ApplicationSession):
    def __init__(self, config=None):
        print("TestClass:init")
        ApplicationSession.__init__(self, config)

    def onOpen(self, transport):
        print("TestClass:onOpen")
        ApplicationSession.onOpen(self, transport)

    def bob(self):
        print("Une fonction!!!")

if __name__ == '__main__':
    print("Hello world")
    #runner = CustomRunner("ws://localhost:8080/ws","realm1",debug=True,debug_app=True,debug_wamp=True)

    runner = CustomRunner("ws://localhost:8080/ws","realm1")
    runner.run(TestClass)