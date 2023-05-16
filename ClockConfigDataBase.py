# -*- coding: utf-8 -*-
import sqlite3

class ClockDataBase():
    def __init__(self):
        self.dbName = 'ClockDataBase.sqlite'
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()
        
        Create_Table = '''CREATE TABLE ClockId_Activity (id varchar(191) PRIMARY KEY,activity varchar(100))'''
        
        try:
            self.cursor.execute(Create_Table)
        except Exception:
            print('Table Read OK')
            
    def cover(self,listArray):
        self.cursor.execute('DELETE FROM ClockId_Activity')
        self.db.commit()
        
        for i in range(len(listArray)):
            self.db.execute("INSERT INTO ClockId_Activity VALUES (?,?)",(listArray[i][0],listArray[i][1]))
            self.db.commit()
            
    def search(self,listArray):
        self.cursor.execute('SELECT * FROM ClockId_Activity')
        Tables = self.cursor.fetchall()
        
        if len(Tables) > 0:
            for i in range(len(Tables)):
                tempList = []
                tempList.append(Tables[i][0])
                tempList.append(Tables[i][1])
                listArray.append(tempList)
        
if __name__ == '__main__':
    database = ClockDataBase()
    
    List = []
    #List = [['my_job_2','奶奶記得吃藥'],['my_job_1','爸爸去吃飯']]
    #database.cover(List)
    database.search(List)
    print(List)
            
            
        