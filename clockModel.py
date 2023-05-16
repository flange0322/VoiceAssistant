# -*- coding: utf-8 -*-
import time
from datetime import datetime,timedelta,date
import ttsReceptionist,DBgeter
from threading import Lock

index = 0
lock = Lock()

def my_job(activity,tasksize):
    global index
    lock.acquire()
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        ttsReceptionist.Reception_add(None,1,index,'Tip.mp3')
        if activity != '':
            ttsReceptionist.Reception_add(activity,1,index + 1,'test.mp3')
        if index >= (tasksize + 1) * 2 - 1:
            index = 0
        else:
            index = index + 2
    finally:
        lock.release()
    
class clockModelClass:
    def __init__(self,y,mon,dow,dat,h,m,s,sc,ia):
        self.year = y
        self.month = mon
        self.dayofweek = dow
        self.date = dat
        self.hour = h
        self.min = m
        self.sec = s
        self.sched = sc
        self.id_act = ia

    def add_job_cron(self):
        self.sched.add_job(my_job, 
                           'cron', 
                           day_of_week = self.dayofweek,
                           hour = self.hour,
                           minute = self.min,
                           id = self.id_act[0],
                           args = (self.id_act[1],len(self.sched.get_jobs()),))
    
    def add_job_interval(self):
        start = datetime.now() + timedelta(hours = self.hour,minutes = self.min,seconds = self.sec)
        self.sched.add_job(my_job, 
                           'interval',
                           hours = self.hour,
                           minutes = self.min,
                           seconds = self.sec,
                           id = self.id_act[0],
                           start_date = start.strftime('%Y-%m-%d %H:%M:%S'),
                           end_date = start.strftime('%Y-%m-%d %H:%M:%S'),
                           args = (self.id_act[1],len(self.sched.get_jobs()),))
        
    def add_job_date(self):
        self.sched.add_job(my_job, 
                           'date', 
                           run_date = datetime(self.year,
                                               self.month,
                                               self.date,
                                               self.hour,
                                               self.min,
                                               self.sec),
                                               id = self.id_act[0],
                           args = (self.id_act[1],len(self.sched.get_jobs()),))
        
    def delete_job(self,delId):
        self.sched.remove_job(delId)
        
    def search_job(self,dateForUser):
        todayDate = date.today().strftime('%Y-%m-%d')
            
        TimeList = None
        if todayDate == dateForUser:
            TimeList = DBgeter.get_Clock_DB_time_today()
        else:
            TimeList = DBgeter.get_Clock_DB_time(dateForUser)
        
        ResponseSchSearchStr = None
        if len(TimeList) > 0:
            ResponseSchSearchStr = '您有' + str(len(TimeList)) + '個提醒事件'

            nameActivity = ''
            for i in range(len(TimeList)):
                for j in range(len(self.id_act)):
                    if self.id_act[j][0] == TimeList[i][0]:
                        nameActivity = self.id_act[j][1]
                        break
                ResponseSchSearchStr = ResponseSchSearchStr + '?' + TimeList[i][1] + '?' + nameActivity
        else:
            ResponseSchSearchStr = '您尚未添加任何提醒事件'
            
        return ResponseSchSearchStr
