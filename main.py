from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
from sGen import sGen
from emailmanager import sendmail,readmail
import threading
import time
import inspect



    


    
    



#list of commands
Commands = ['wakepc','sleeppc', 'snap', 'downfiles']

#logic for any commands
class CommandHandler():
    def __init__(self,Command,LineNum,Pass):
        self.Command = Command
        self.LineNum = LineNum
        self.Pass = Pass


    def wakepc(self):
        if self.Command == 'wakepc':
            subjects = 'wakepc'
            message = sGen(self.LineNum,self.Pass)

            sendmail(message,subjects)
            

    def sleeppc(self):
        if self.Command == 'sleeppc':
            subjects = 'sleeppc'
            message = sGen(self.LineNum,self.Pass)

            sendmail(message,subjects)
            

    def snap(self):
        if self.Command == 'snap':
            subjects = 'snap'
            message = sGen(self.LineNum,self.Pass)

            sendmail(message,subjects)
            

    def sendfiles(self):
        if self.Command == 'downfiles':
            subjects = 'sendfiles'
            message = sGen(self.LineNum,self.Pass)


            
            # sendmail(message,subjects)
            

            
            
            
            
            






    def run(self): 
        methods = inspect.getmembers(CommandHandler, predicate=inspect.isfunction) #gets list of all methods in the class
        for method in methods: #runs each method in the list for the exception of the init run
            if method[0] != '__init__' and method[0] != 'run': 
                method[1](self)
                



class MyLayout(Widget):
    Commands = Commands

    def press(self):
        self.Command = self.ids.Commands_Drop.text
        self.LineNum = int(self.ids.Lines_Drop.text)
        self.Pass = self.ids.Pass_Input.text

        self.ids.Submit_Button.text = "Processing..."
        print(f'{self.Command} , {self.LineNum} , {self.Pass}')
        
        
        t=threading.Thread(target=self.commandHandleInit, daemon=True)
        t.start()
        pass

    def commandHandleInit(self):
        cH = CommandHandler(self.Command,self.LineNum,self.Pass)
        cH.run()


        # self.ids.Submit_Button.text = "Sent!"
        # time.sleep(2)
        # self.ids.Submit_Button.text = "Submit"
        

    def subbuttonlabel():

        print(MyLayout().ids.Submit_Button.text)
        time.sleep(2)
        print(MyLayout().ids.Submit_Button.text)
buildkv = Builder.load_file("Command_UI.kv")

class CommandApp(App):
    def build(self):
        self.Commands = Commands
        return buildkv

if __name__ == '__main__':
    CommandApp().run()
    
    
