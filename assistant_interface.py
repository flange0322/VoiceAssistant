# -*- coding: utf-8 -*-
import STT,getAPI,assignFactory,ttsReceptionist
import Master,DBgeter,ClockConfigDataBase
from time import sleep

task = []
task_id_activity = []
DBgeter.get_Clock_DB(task)
ClockConfigDataBase.ClockDataBase().search(task_id_activity)

ttsReceptionist.Reception_exe()

activity_input = False

def main():
    global activity_input
    if Master.getMasterStatus() == 'listening':
        text = STT.main()
        if text is None and Master.getMasterStatus() == 'listening':
            ttsReceptionist.Reception_add(None,1,0,'prepare.mp3')
            sleep(2)
            Master.MasterControl('ch_to_sleep')
        elif text == '關機':
            exit()
            return 'turnoff'
        elif text is not None and Master.getMasterStatus() == 'listening':
            if activity_input == True:
                fake_text = 'key'
                response = getAPI.getTTS(fake_text)
                activity_input = False
            else:
                response = getAPI.getTTS(text)
            
            if type(response) is list:
                ttsReceptionist.Reception_add(response[0],2,0,'test.mp3')
            else:
                ttsReceptionist.Reception_add(response,2,0,'test.mp3')

            assignFactory.TypeJudge(response,task,text,task_id_activity)

            if response == '要提醒您什麼事情呢':
                activity_input = True
def exit():
    Master.MasterControl('ch_to_exit')
    assignFactory.sched.shutdown()
    ttsReceptionist.Reception_exit()
    ClockConfigDataBase.ClockDataBase().cover(task_id_activity)
    print('關機完成，祝您愉快')
 
if __name__ == '__main__':
   s = main()
   print(s)
