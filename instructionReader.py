# -*- coding: utf-8 -*-
#指令解析、指定資料存取位置
class Reader:
    def __init__(self,dialog_Message):

        if type(dialog_Message) == list:
            self.subStringArray = []
            temp_Array = []
            for i in range(len(dialog_Message)):
               if dialog_Message[i].find(':') >= 0 and i != 0:
                   temp_Text = dialog_Message[i].replace(':','/').split('/')
                   temp_Array = temp_Array + temp_Text
               elif dialog_Message[i].find('-') >= 0 and i != 0:
                   temp_Text = dialog_Message[i].replace('-','/').split('/')
                   temp_Array = temp_Array + temp_Text
               else:
                   self.subStringArray.append(dialog_Message[i])
            
            for i in range(len(temp_Array)):
                self.subStringArray.append(temp_Array[i])
        else:
            temp_Text = dialog_Message
            self.subStringArray = []
            self.subStringArray.append(temp_Text)
    
    def getsubStringArray(self):
        return self.subStringArray

if __name__ == '__main__':
    lists = ['好的，已經有幫你記了，但是吉娃娃會看心情選擇要不要提醒你', 'date', '2019-05-21', '09:00:00']
    iReader = Reader(lists)
    print(iReader.getsubStringArray())