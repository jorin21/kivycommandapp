import re
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
from sGen import sGen
from emailmanager import sendmail,readmail
import threading
import time
import inspect



    

global Reply
Reply = False

#list of commands
Commands = ['wakepc','sleeppc', 'snap', 'downfiles', 'change']

#logic for any commands
class CommandHandler():
    def __init__(self,Command,LineNum,Pass):
        self.Command = Command
        self.LineNum = LineNum
        self.Pass = Pass
        self.wait_for_reply = 0

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
            if Reply == False:
                subjects = 'sendfiles'
                message = sGen(self.LineNum,self.Pass)
                time.sleep(2)
                
                self.wait_for_reply = 1
                
                sendmail(message,subjects)
            else:
                
                self.Pass = self.Pass.split('\n')
                
                subjects = 'Re: DropBox API Call'
                message = self.Pass[1]

                sendmail(message,subjects)


            
           
            

            
            
            
            
            






    def run(self):
        methods = inspect.getmembers(CommandHandler, predicate=inspect.isfunction) #gets list of all methods in the class
        for method in methods: #runs each method in the list for the exception of the init run
            if method[0] != '__init__' and method[0] != 'run': 
                method[1](self)
                
                



    


class MyLayout(Widget):
    Commands = Commands

    stop = threading.Event()

    def press(self):
        self.Command = self.ids.Commands_Drop.text
        self.LineNum = int(self.ids.Lines_Drop.text)
        self.Pass = self.ids.Pass_Input.text

        self.ids.Submit_Button.text = "Processing..."
        print(f'{self.Command} , {self.LineNum} , {self.Pass}')
        
        
        th1 = threading.Thread(target=self.commandHandleInit, daemon=True)
        th1.start()
        pass

    def commandHandleInit(self):
        self.cH = CommandHandler(self.Command,self.LineNum,self.Pass)
        self.cH.run()

        global t
        t = True


        if self.cH.wait_for_reply == 1:
            self.waiting()
                
        
        

        

    def waiting(self):
        
        th2 = threading.Thread(target=self.replyhandler, daemon=True)
        th2.start()
        while t:
            if th2.is_alive():
                wait = 'Waiting.'
                for i in range(3):
                    self.update_but(wait)
                    time.sleep(1)
                    wait += '.'
            else:
                th2 = threading.Thread(target=self.replyhandler, daemon=True)
                th2.start()
                


    def replyhandler(self):
        r = readmail()
        if self.cH.Command == 'downfiles':
            if r['Subject'] == 'Download Files':
                self.update_inp(reverse=True)
                self.update_but('Submit')
                global t
                t = False
                
                

            if r['Subject'] == 'DropBox API Call':
                self.update_inp()
                self.update_but('Submit')
                t = False

                global Reply
                Reply = True

            
               


               
            else:
                print('No API Call yet')
                
                
            
    
    @mainthread
    def update_but(self, wait):
        self.ids.Submit_Button.text = wait

    @mainthread
    def update_inp(self, reverse=False):
        if reverse:
            self.ids.Pass_Input.size = (self.ids.Commands_Drop.width , self.ids.Commands_Drop.height)
        else:
            self.ids.Pass_Input.size = (self.ids.Commands_Drop.width , self.ids.Commands_Drop.height * 2)
            

    def infinite_loop(self):
        iteration = 0
        while True:
            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                return
            iteration += 1
            print('Infinite loop, iteration {}.'.format(iteration))
            time.sleep(1)

        
buildkv = Builder.load_file("Command_UI.kv")

class CommandApp(App):
    def on_stop(self):
        self.root.stop.set()

    def build(self):
        self.Commands = Commands
        return buildkv

if __name__ == '__main__':
    CommandApp().run()
    
    
