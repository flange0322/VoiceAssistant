# -*- coding: utf-8 -*-
import requests
import json
import collections

clientAccessTokenKey = 'your_key'

def getTTS(text):
    query = text
    lang = 'zh-tw'
    session_id = '6cd6236b-a29e-5b07-d287-f4ceb7ab060b'
    timezone = 'Asia/Taipei'
    authorization = 'Bearer ' + clientAccessTokenKey
    
    headers = {
            "accept":"application/json",
            "authorization":authorization
            }
    url = 'https://api.dialogflow.com/v1/query?v=20170712'
    params = {'query':str(query),'lang':lang,'sessionId':session_id,'timezone':timezone}
    response = requests.request("GET",url,headers=headers,params=params)
    
    data = json.loads(response.text)
    print(data)
    
    status = data['status']['code']
   # print("Status: {}".format(status))
    
    if status == 200:
        resolveQuery = data['result']['resolvedQuery']
        parameters = data['result']['parameters']
        list_parameters = list(parameters.values())
        fulfillment = data['result']['fulfillment']['speech']

        print("Query: {}".format(resolveQuery))
        print("Response: {}".format(fulfillment))
        
        try:
            if list_parameters.index('') > -1:
                return fulfillment
        except ValueError:
            list_or_text = contextsReader(parameters)
            if list_or_text == 'justResponse':
                return fulfillment
            else:
                list_or_text.insert(0,fulfillment)
                return list_or_text

def contextsReader(category):
    scheduleCron = collections.OrderedDict()
    scheduleCron['schedule_cron'] = None
    scheduleCron['schedule_weekstart'] = None
    scheduleCron['schedule_weekend'] = None
    scheduleCron['time'] = None
    
    scheduleDate = collections.OrderedDict()
    scheduleDate['schedule_date'] = None
    scheduleDate['date'] = None
    scheduleDate['time'] = None
    
    scheduleInterval = collections.OrderedDict()
    scheduleInterval['schedule_interval'] = None
    scheduleInterval['hour'] = None
    scheduleInterval['minute'] = None
    scheduleInterval['sec'] = None

    scheduleSearch = collections.OrderedDict()
    scheduleSearch['schedule_search'] = None
    scheduleSearch['date'] = None

    scheduleDelete = collections.OrderedDict()
    scheduleDelete['schedule_delete'] = None
    
    trainSearch = collections.OrderedDict()
    trainSearch['train_search'] = None
    trainSearch['city_from'] = None
    trainSearch['city_to'] = None
    trainSearch['date'] = None
    trainSearch['time'] = None
                   
    trainChangeTo = collections.OrderedDict()
    trainChangeTo['train_changeto'] = None
    trainChangeTo['city_from'] = None
    trainChangeTo['city_to'] = None
    trainChangeTo['date'] = None
    trainChangeTo['time'] = None

    trainChangeFrom = collections.OrderedDict()
    trainChangeFrom['train_changefrom'] = None
    trainChangeFrom['city_from'] = None
    trainChangeFrom['city_to'] = None
    trainChangeFrom['date'] = None
    trainChangeFrom['time'] = None
   
    trainChangeTime = collections.OrderedDict()
    trainChangeTime['train_changetime'] = None
    trainChangeTime['city_from'] = None
    trainChangeTime['city_to'] = None
    trainChangeTime['date'] = None
    trainChangeTime['time'] = None

    weatherSpecificDate = collections.OrderedDict()
    weatherSpecificDate['weather_specificdate'] = None
    weatherSpecificDate['weather_address'] = None
    weatherSpecificDate['date'] = None
    
    weatherWeek = collections.OrderedDict()
    weatherWeek['weather_week'] = None
    weatherWeek['weather_address'] = None

    newsSearch = collections.OrderedDict()
    newsSearch['news_type'] = None
    
    container = None
    Jumper = False
    for i in category.keys():
        if i == 'schedule_cron':
            container = scheduleCron
            Jumper = True
        elif i == 'schedule_date':
            container = scheduleDate
            Jumper = True
        elif i == 'schedule_interval':
            container = scheduleInterval
            Jumper = True
        elif i == 'schedule_search':
            container = scheduleSearch
            Jumper = True
        elif i == 'schedule_delete':
            container = scheduleDelete
            Jumper = True
        elif i == 'train_search':
            container = trainSearch
            Jumper = True
        elif i == 'train_changeto':
            container = trainChangeTo
            Jumper = True
        elif i == 'train_changefrom':
            container = trainChangeFrom
            Jumper = True
        elif i == 'train_changetime':
            container = trainChangeTime
            Jumper = True
        elif i == 'weather_specificdate':
            container = weatherSpecificDate
            Jumper = True
        elif i == 'weather_week':
            container = weatherWeek
            Jumper = True
        elif i == 'news_type':
            container = newsSearch
            Jumper = True
    
    if Jumper is not True:
        return 'justResponse'
    
    for i in container.keys():
        if category[i] != '':
            container[i] = category[i]
        else:
            return 'justResponse'
    try:    
        Datalist = list(container.values())
        if Datalist[2] == '$schedule_weekstart':
            Datalist[2] = Datalist[1]
    except:
        print('not Cron')

    return Datalist
    
if __name__ == '__main__':
    while True:
        x = input()
        if x == 'bye':
            break
        print(getTTS(str(x)))
