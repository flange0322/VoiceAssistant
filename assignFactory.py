# -*- coding: utf-8 -*-
import instructionReader,clockModel,keyWordCutter,ttsReceptionist
import googleAPISock,trainT,weatherModel,newsClientModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
  'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

sched = BackgroundScheduler(jobstores = jobstores)
sched.start()

def TypeJudge(dialogMessage,taskArray,text,tia):
    iReader = instructionReader.Reader(dialogMessage)
    dataArray = iReader.getsubStringArray()
    if len(dataArray) > 1:
        if dataArray[1] == 'cron':
            dataArray.append(keyWordCutter.activityCutter(text))
            taskchecker(taskArray)
            taskcheckerforTIA(tia)
            taskArray = namer_Add(taskArray)
            tia.append([taskArray[len(taskArray)-1],dataArray[len(dataArray)-1]])

            print(taskArray)
            print(tia)

            week = ['mon','tue','wed','thu','fri','sat','sun']
            for i in range(len(week)):
                if dataArray[2] == week[i]:
                    dataArray[2] = i
                if dataArray[3] == week[i]:
                    dataArray[3] = i
            
            if dataArray[2] > dataArray[3]:
                dataArray[2],dataArray[3] = dataArray[3],dataArray[2]
                    
            clock = clockModel.clockModelClass(0,
                                               0,
                                               str(dataArray[2]) + '-' + str(dataArray[3]),
                                               0,
                                               int(dataArray[4]),
                                               int(dataArray[5]),
                                               0,
                                               sched,
                                               tia[len(tia)- 1])
            clock.add_job_cron()
        elif dataArray[1] == 'interval':
            dataArray.append(keyWordCutter.activityCutter(text))
            taskchecker(taskArray)
            taskcheckerforTIA(tia)
            taskArray = namer_Add(taskArray)
            tia.append([taskArray[len(taskArray)-1],dataArray[len(dataArray)-1]])

            print(taskArray)
            print(tia)

            clock = clockModel.clockModelClass(0,
                                               0,
                                               0,
                                               0,
                                               int(dataArray[2]),
                                               int(dataArray[3]),
                                               int(dataArray[4]),
                                               sched,
                                               tia[len(tia) - 1])
            clock.add_job_interval()
        elif dataArray[1] == 'date':
            dataArray.append(keyWordCutter.activityCutter(text))
            taskchecker(taskArray)
            taskcheckerforTIA(tia)

            gooA = googleAPISock.GoogleCalendar()
            task = gooA.add_sch(dataArray[2],
                               dataArray[3],
                               dataArray[4],
                               dataArray[5],
                               dataArray[6],
                               dataArray[7],
                               dataArray[len(dataArray)-1])
            
            taskArray.append(task[0])
            tia.append(task)

            print(taskArray)
            print(tia)

            clock = clockModel.clockModelClass(int(dataArray[2]),
                                               int(dataArray[3]),
                                               0,
                                               int(dataArray[4]),
                                               int(dataArray[5]),
                                               int(dataArray[6]),
                                               int(dataArray[7]),
                                               sched,
                                               tia[len(tia) - 1])
            clock.add_job_date()
        elif dataArray[1] == 'schedulesearch':
            clock = clockModel.clockModelClass(0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               sched,
                                               tia)
            print(dataArray)
            searchResultStr = clock.search_job(dataArray[2] + '-' + dataArray[3] + '-' + dataArray[4])
            ttsReceptionist.Reception_add(searchResultStr,
                                          2,
                                          1,
                                          'test.mp3')
        elif dataArray[1] == 'scheduledelete':
            clock = clockModel.clockModelClass(0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               0,
                                               sched,
                                               tia)
            taskchecker(taskArray)
            taskcheckerforTIA(tia)

            print(taskArray)
            print(tia)

            try:
                delete_Id = taskArray[len(taskArray) - 1]
                delete_ia = tia[len(tia) - 1][1]
                taskArray.pop()
                tia.pop()
                
                clock.delete_job(delete_Id)
                ttsReceptionist.Reception_add(delete_ia + ' ? 已刪除成功',
                                              2,
                                              1,
                                              'test.mp3')

                gooD = googleAPISock.GoogleCalendar()
                gooD.delete_sch(delete_Id)
            except IndexError:
                ttsReceptionist.Reception_add('查無任何提醒',
                                              2,
                                              1,
                                              'test.mp3')
            except:
                print('it is not in google calendar')
        elif dataArray[1] == 'trainsearch' or dataArray[1] == 'trainchangeto' or dataArray[1] == 'trainchangefrom' or dataArray[1] == 'trainchangetime':
            trainResultStr = trainT.trainData(dataArray[2][0:len(dataArray[2])-1],
                                              dataArray[3][0:len(dataArray[3])-1],
                                              dataArray[4] + '-' + dataArray[5] + '-' + dataArray[6],
                                              dataArray[7] + ':' + dataArray[8] + ':' + dataArray[9])
            
            ttsReceptionist.Reception_add(trainResultStr,
                                          2,
                                          1,
                                          'test.mp3')
        elif dataArray[1] == 'weatherspecificdate':
            weatherResultStr = weatherModel.weatherData(dateTimeY = dataArray[3],
                                                        dateTimeM = dataArray[4],
                                                        dateTimeD = dataArray[5],
                                                        select = '2',
                                                        inputcity = dataArray[2])
            ttsReceptionist.Reception_add(weatherResultStr,
                                          2,
                                          1,
                                          'test.mp3')
        elif dataArray[1] == 'weatherweek':  
            weatherResultStr = weatherModel.weatherData(select = '1',
                                                        inputcity = dataArray[2])
            ttsReceptionist.Reception_add(weatherResultStr,
                                          2,
                                          1,
                                          'test.mp3')
        elif dataArray[1] == 'government' or dataArray[1] == 'health' or dataArray[1] == 'international' or dataArray[1] == 'local' or dataArray[1] == 'sports':
            try :
                if newsClientModel.client('RespeakerTester001',dataArray[1]):
                     ttsReceptionist.Reception_add(None,
                                          2,
                                          1,
                                          'news.mp3')
            except:
                ttsReceptionist.Reception_add('連線失敗??請稍後再試',
                                          2,
                                          1,
                                          'test.mp3')

def taskchecker(taskArray):
    pos = []
    for i in range(len(taskArray)):
        if sched.get_job(job_id = taskArray[i]) is None:
            pos.append(i)
            
    if len(pos) > 0:
        for i in range(len(pos)):
            taskArray.remove(taskArray[pos[i] - i])

def taskcheckerforTIA(TIA):
    pos = []
    for i in range(len(TIA)):
        if sched.get_job(job_id = TIA[i][0]) is None:
            pos.append(i)
            
    if len(pos) > 0:
        for i in range(len(pos)):
            TIA.remove(TIA[pos[i] - i])

def namer_Add(taskArray):
    taskName = taskArray
    defaultName = 'my_job_'
    index = 1
    
    if len(taskName) == 0:
        taskName.append(defaultName + str(index))
        return taskName
    else:
       try:
           while True:
               taskName.index(defaultName + str(index))
               index = index + 1
       except:
           print(defaultName + str(index) + ' is not in list')
       taskName.append(defaultName + str(index))
       return taskName
