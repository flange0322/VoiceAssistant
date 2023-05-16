# -*- coding: utf-8 -*-
keyword = ['提醒我','提醒','叫我','叫']

def checkKeyWord(text):
    for i in range(len(keyword)):
        if text.find(keyword[i]) >= 0:
            return 1
    return 0
    
def activityCutter(text):
    activityContent = text
    for i in range(len(keyword)):
        if text.find(keyword[i]) >= 0:
            activityContent = text[text.find(keyword[i]) + len(keyword[i]):len(text)]
            break
    return activityContent

def timeCutter(text):
    timeContent = text
    for i in range(len(keyword)):
        if text.find(keyword[i]) >= 0:
            timeContent = text[0:text.find(keyword[i]) + len(keyword[i])]
            break
    return timeContent

if __name__ == '__main__':
    print(timeCutter('今天早上9點叫我起床'))
            
