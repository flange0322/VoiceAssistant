# -*- coding: utf-8 -*-
status = 'sleeping'
def MasterControl(action):
    global status
    if action == 'ch_to_sleep':
        status = 'sleeping'
        print('sleeping success')
    elif action == 'ch_to_speak':
        status = 'speaking'
        print('speaking success')
    elif action == 'ch_to_listen':
        status = 'listening'
        print('listening success')
    elif action == 'ch_to_exit':
        status = 'turnoff'
        print('exit success')
    elif action == 'ch_to_dreamSpeak':
        status = 'dreamSpeaking'
        print('dreamSpeaking success')
        
def getMasterStatus():
    global status
    return status
    
