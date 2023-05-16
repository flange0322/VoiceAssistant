# -*- coding: utf-8 -*-
from gtts import gTTS
from pygame import mixer
from evdev import InputDevice,ecodes
import Master,MicroSoftSpeech,threading

#api key放置處
key = "your_key"
 
statusClick = 'keeping'

#語音輸出
def wordToSound(*args):
    global statusClick
    while True :
        queue = args[0]
        if queue.qsize() > 0:
            if Master.getMasterStatus() != 'sleeping' and Master.getMasterStatus() != 'dreamSpeaking':
                Master.MasterControl('ch_to_speak')
            else:
                Master.MasterControl('ch_to_dreamSpeak')
            ttsTgroup = queue.get()
            ttsT = ttsTgroup[2]
            if ttsT.getPri() == 0:
                break

            file_name = ttsT.getMus()
            if ttsT.getRes() is not None and ttsT.getRes() != '':
                word = ttsT.getRes() 
                
                #google TTS
                try:
                    tts = gTTS(word, lang='zh-tw')
                    tts.save(file_name)
                except AssertionError:
                    continue
                
                #MicroSoft TTS
                ''' 需申請microsoft api key才能使用
                speech = MicroSoftSpeech.TextToSpeech(key,file_name,word)
                speech.get_token()
                speech.save_audio()
                '''

            if (ttsT.getRes() is not None and ttsT.getRes() != '') or file_name != 'test.mp3':
                threadClick = threading.Thread(target = clickButton)
                threadClick.setDaemon(True)
                threadClick.start()

                mixer.init()
                mixer.music.load(file_name)
                mixer.music.play()
                while mixer.music.get_busy() == True:
                    if statusClick == 'out':
                       statusClick = 'keeping'
                       break
                    else:
                       continue
                mixer.music.stop()
                mixer.quit()
            if Master.getMasterStatus() == 'speaking':
                Master.MasterControl('ch_to_listen')
            elif Master.getMasterStatus() == 'dreamSpeaking':
                Master.MasterControl('ch_to_sleep')

def clickButton():
    global statusClick
    key = InputDevice("/dev/input/event0")
    for event in key.read_loop():
        if event.type == ecodes.EV_KEY:
            statusClick = 'out'
            break

