# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendar():
    def __init__(self):
        self.creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json',SCOPES)
                self.creds = flow.run_local_server()
                
            with open('token.pickle','wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('calendar', 'v3', credentials = self.creds)
    
    def search_sch_now(self):
        hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15']
        
        now_g_dateTime = datetime.datetime.utcnow()
        datehTime_End_g_dateTime = now_g_dateTime + datetime.timedelta(hours = 24)
        for i in range(len(hours)):  
            if now_g_dateTime.strftime('%H') == hours[i]:
                datehTime_End_g_dateTime = now_g_dateTime               
                
        datehTime_End_g = datehTime_End_g_dateTime.strftime('%Y-%m-%d')
        datehTime_End_g_dateTime = datetime.datetime.strptime(datehTime_End_g + ' 16:00:00','%Y-%m-%d %H:%M:%S')
        
        now_g = now_g_dateTime.isoformat() + 'Z'
        datehTime_End_g = datehTime_End_g_dateTime.isoformat() + 'Z'

        events_result = self.service.events().list(calendarId = 'primary',
                                                   timeMin = now_g,
                                                   timeMax = datehTime_End_g,
                                                   maxResults = 100, 
                                                   singleEvents = True,
                                                   orderBy = 'startTime').execute()
        events = events_result.get('items', [])
        #print(events)
        if not events:
            print('No upcoming events found.')
        dataList = []
        for event in events:
            tempList = []
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start.replace('T',' ')
            start = start[11:19]
            tempList.append(start)
            tempList.append(event['summary'])
            dataList.append(tempList)
            
        return dataList
    
    def search_sch(self,dateforuserString):
        datehTime_Start_g = dateforuserString + ' 16:00:00'
        datehTime_Start_g_datetime = datetime.datetime.strptime(datehTime_Start_g,'%Y-%m-%d %H:%M:%S')
        datehTime_Start_g_datetime = datehTime_Start_g_datetime - datetime.timedelta(hours = 24)
        
        datehTime_End_g_datetime = datehTime_Start_g_datetime + datetime.timedelta(hours = 24)
        
        datehTime_Start_g = datehTime_Start_g_datetime.isoformat() + 'Z'
        datehTime_End_g = datehTime_End_g_datetime.isoformat() + 'Z'
        
        events_result = self.service.events().list(calendarId = 'primary',
                                                   timeMin = datehTime_Start_g,
                                                   timeMax = datehTime_End_g,
                                                   maxResults = 100, 
                                                   singleEvents = True,
                                                   orderBy = 'startTime').execute()
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            
        dataList = []
        for event in events:
            tempList = []
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start.replace('T',' ')
            start = start[11:19]
            tempList.append(start)
            tempList.append(event['summary'])
            dataList.append(tempList)
            
        return dataList
        
    def add_sch(self,year,mouth,date,hour,minute,second,activity):
        dateStr = year + '-' +  mouth + '-' + date + ' ' + hour + ':' + minute + ':' + second
        dateStart = datetime.datetime.strptime(dateStr,'%Y-%m-%d %H:%M:%S') 
        dateEnd = dateStart + datetime.timedelta(hours = 1)
        event = {
          'summary': activity,
          'description': 'Adding From ReSpeaker',
          'start': {
             'dateTime': dateStart.isoformat(),
             'timeZone': 'Asia/Taipei',
          },
          'end': {
             'dateTime': dateEnd.isoformat(),
             'timeZone': 'Asia/Taipei',
          },
          'recurrence': [
             'RRULE:FREQ=DAILY;COUNT=1'
          ],
          'reminders': {
             'useDefault': False,
             'overrides': [
               {'method': 'email', 'minutes': 24 * 60}
            ],
          },
        }
        
        events_add = self.service.events().insert(calendarId = 'primary',
                                                  body = event).execute()
        dataList = []
        dataList.append(events_add['id'])
        dataList.append(events_add['summary'])
        return dataList
        
    def delete_sch(self,id):
        events_delete = self.service.events().delete(calendarId = 'primary',
                                                eventId = id).execute()
                                        
    #查詢指定事件(需要對應ID)
    #events_search = service.events().instances(calendarId = 'primary',
                                              # eventId = id).execute()
    #events_get_search = events_search.get('items', [])
    #if not events_get_search:
    #    print('No upcoming events found.')
    #for event in events_get_search:
        #start = event['start'].get('dateTime',event['start'].get('date'))
       # print(start,event['summary'],event['id'])

if __name__ == '__main__':
    goo = GoogleCalendar()
    #goo.delete_sch('76lkpioh4dk1jnusrc0mpfl98c')
    #test2 = goo.add_sch('2019','5','26','10','0','0','剪頭髮')
    #print(test2)
    test = goo.search_sch_now()
    print(test)
