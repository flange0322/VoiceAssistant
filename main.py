# -*- coding: UTF-8 -*-
import snowboydecoder
import sys
import signal
import assistant_interface
import Master

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def main():
    model = 'snowboy.pmdl'

    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.4)
    print('Listening... Press Ctrl+C to exit')

    #loop
    while True:
        if Master.getMasterStatus() == 'sleeping':
             detector.start(detected_callback=snowboydecoder.play_audio_file,
                            interrupt_check=interrupt_callback,
                            sleep_time=0.03)
             if Master.getMasterStatus() != 'dreamSpeaking':
                 Master.MasterControl('ch_to_listen')
        try:
            close_order = assistant_interface.main()
        except Exception as e:
            print('Error Generate!')
            print(e)
            assistant_interface.exit()
            break
        if close_order == 'turnoff':
            break

if __name__ == '__main__':
    main()
