# -*- coding: utf-8 -*-
import sqlite3,datetime,time
def get_Clock_DB(taskArray):
    mydb = sqlite3.connect('jobs.sqlite')

    cursor = mydb.cursor()

    cursor.execute("SELECT id FROM apscheduler_jobs;")

    Tables = cursor.fetchall()
    
    if(len(Tables) > 0):
        for i in range(len(Tables)):
            taskArray.append(Tables[i][0])

#type datetime          
def get_Clock_DB_time_today():
    mydb = sqlite3.connect('jobs.sqlite')
    
    cursor = mydb.cursor()
    
    #當前時間
    now_dateTime = datetime.datetime.now()
    #起始、終點時間
    datehTime_Start = now_dateTime.strftime('%Y-%m-%d %H:%M:%S')
    datehTime_End_datetime = now_dateTime + datetime.timedelta(hours = 24)
    datehTime_End = datehTime_End_datetime.strftime('%Y-%m-%d')
    
    timeArray_Start = time.strptime(datehTime_Start,'%Y-%m-%d %H:%M:%S')
    timestamp_Start = time.mktime(timeArray_Start)
    timeArray_End = time.strptime(datehTime_End + ' 00:00:00','%Y-%m-%d %H:%M:%S')
    timestamp_End = time.mktime(timeArray_End)
    
    cursor.execute("SELECT id,next_run_time FROM apscheduler_jobs WHERE next_run_time >= " + str(timestamp_Start) + " AND next_run_time < " + str(timestamp_End) + ";")
    
    Tables = cursor.fetchall()
    
    if(len(Tables) > 0):
        #tuple to list
        for i in range(len(Tables)):
            Tables[i] = list(Tables[i])
        
        # 時間戳 to String
        for i in range(len(Tables)):
            Tables[i][1] = time.strftime('%H:%M:%S',time.localtime(int(Tables[i][1])))     
    return Tables

#type string
def get_Clock_DB_time(dateforuserString):
    mydb = sqlite3.connect('jobs.sqlite')
    
    cursor = mydb.cursor()
    
    #起始時間
    datehTime_Start = dateforuserString + ' 00:00:00'
    datehTime_Start_datetime = datetime.datetime.strptime(datehTime_Start,'%Y-%m-%d %H:%M:%S')
    datehTime_End_datetime = datehTime_Start_datetime + datetime.timedelta(hours = 24)
    #終點時間
    datehTime_End = datehTime_End_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    #轉成時間戳
    timeArray_Start = time.strptime(datehTime_Start,'%Y-%m-%d %H:%M:%S')
    timestamp_Start = time.mktime(timeArray_Start)
    timeArray_End = time.strptime(datehTime_End,'%Y-%m-%d %H:%M:%S')
    timestamp_End = time.mktime(timeArray_End)
    
    cursor.execute("SELECT id,next_run_time FROM apscheduler_jobs WHERE next_run_time >= " + str(timestamp_Start) + " AND next_run_time < " + str(timestamp_End) + ";")
    
    Tables = cursor.fetchall()
        
    if(len(Tables) > 0):
        #tuple to list
        for i in range(len(Tables)):
            Tables[i] = list(Tables[i])
        
        # 時間戳 to String
        for i in range(len(Tables)):
            Tables[i][1] = time.strftime('%H:%M:%S',time.localtime(int(Tables[i][1])))     
    return Tables
