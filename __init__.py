from mycroft import MycroftSkill, intent_file_handler
import subprocess
import time
from time import monotonic

class CurrentUser(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        firstMessages = []
        secondMessages  = []
        self.stt_messages = []
        self.last_stt_time = (0, 0)


    def initialize(self):
        """Setup handlers for catching user sentences and Mycroft utterances.
        """
        def on_utterance(message):
            self.stt_messages.append(message.data['utterances'][0])
            self.stt_messages = self.stt_messages[-2:]
            self.last_stt_time = self.last_stt_time[1], monotonic()


        self.add_event('recognizer_loop:utterance', on_utterance)

        nothing = self.translate('nothing')
        self.stt_messages = [nothing]
        firstMessages = self.stt_messages
        time.sleep(30)
        secondMessages = self.stt_messages
        if firstMessages == secondMessages:
            subprocess.call(["/home/pi/logoutcommands.sh","Arguments"],shell=True)

    @intent_file_handler('user.current.intent')
    def handle_user_current(self):
        File_output = open("/home/pi/login.txt","r")
        user = File_output.read()
        File_output.close()
        self.speak_dialog('user.current', data = { 
            'user' : user
        })

    @intent_file_handler('user.logout.intent')
    def handle_user_logout(self):
        File_output = open("/home/pi/login.txt","w")
        File_output.write(" ")
        File_output.close()
        subprocess.call(["/home/pi/logoutcommands.sh","Arguments"],shell=True)
        self.speak_dialog('user.logout')

def create_skill():
    return CurrentUser()

