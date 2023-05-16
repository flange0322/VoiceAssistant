# -*- coding: utf-8 -*-
import threading,queue,TTS,Master
class ttsType:     
    def attach(self,res,pri,mus):
        self.response = res
        self.priority = pri
        self.music_name = mus
    
    def getRes(self):
        return self.response
    
    def getPri(self):
        return self.priority
    
    def getMus(self):
        return self.music_name

que = queue.PriorityQueue()

def Reception_add(response,priority,priorityIndex,music_name):
    temp = ttsType()
    temp.attach(response,priority,music_name)
    que.put((temp.getPri(),priorityIndex,temp))
    if Master.getMasterStatus() != 'sleeping' and Master.getMasterStatus() != 'dreamSpeaking':
        Master.MasterControl('ch_to_speak')
    else:
        Master.MasterControl('ch_to_dreamSpeak')
    
def Reception_exe():
    t = threading.Thread(target = TTS.wordToSound,args=(que,))
    t.start()
    
def Reception_exit():
    Reception_add(None,0,0,None)
