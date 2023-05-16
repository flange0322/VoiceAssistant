from datetime import datetime, date
import urllib.request as request
import json

#需至open weather data平台申請id
appid = 'your_app_id'
#----------------自訂函式---------------------
def sortD(arr):#
    sT=sorted(arr)#從小到大
    for i in range(0, len(sT), +1):
        for j in range(i, len(sT), +1):
            if(j>i):
                if(sT[i]==sT[j]):
                    sT[j]=100
    sTr=[]#不重複從小到大排序
    for i in range(0, len(sT), +1):
        if(sT[i]!=100):
            sTr.append(sT[i])
    return(sTr)
    
def rainD(dwArr,arr,int,rainArr):
    if(len(arr)!=0):
        rainArr=rainArr+"??在週"
        for i in range(0, len(arr), +1):
            rainArr=rainArr+dict[dwArr[arr[i]]-1]+"?"
        if(int==30):
            rainArr=rainArr+"的降雨機率低"
        elif(int==50):
            rainArr=rainArr+"的降雨機率中"
        else:
            rainArr=rainArr+"的降雨機率高"
        return(rainArr)

def UVI(dwArr,arr,int,UvArr):
    if(len(arr)!=0):
        UvArr=UvArr+"??週"
        for i in range(0, len(arr), +1):
            UvArr=UvArr+dict[dwArr[arr[i]]-1]+"?"
        if(int==3):
            UvArr=UvArr+"的紫外線為低量級"
        elif(int==5):
            UvArr=UvArr+"的紫外線為中量級"
        elif(int==8):
            UvArr=UvArr+"的紫外線為高量級"
        elif(int==10):
            UvArr=UvArr+"的紫外線為過量級"
        else:
            UvArr=UvArr+"的紫外線為危險級"
        return(UvArr)

#--------------------遞增遞減---------------------
class LCS():
    def input(self, x, y,maxL,rT):
    #讀入待匹配的兩個字串
        if type(x) != str or type(y) != str:
            print('input error')
            return None
        self.x = x
        self.y = y
        self.m = maxL
        self.r=rT

    def Compute_LCS(self):
        xlength = len(self.x)
        ylength = len(self.y)
        self.direction_list = [None] * xlength #這個二維列表存著回溯方向
        for i in range(xlength):
            self.direction_list[i] = [None] * ylength
        self.lcslength_list = [None] * (xlength + 1)      
        #這個二維列表存著當前最長公共子序列長度
        for j in range(xlength + 1):
            self.lcslength_list[j] = [None] * (ylength + 1)

        for i in range(0, xlength + 1):
            self.lcslength_list[i][0] = 0
        for j in range(0, ylength + 1):
            self.lcslength_list[0][j] = 0
        #下面是進行回溯方向和長度表的賦值
        for i in range(1, xlength + 1):
            for j in range(1, ylength + 1):
                if self.x[i - 1] == self.y[j - 1]:
                    self.lcslength_list[i][j] = self.lcslength_list[i - 1][j - 1] + 1
                    self.direction_list[i - 1][j - 1] = 0  # 左上
                elif self.lcslength_list[i - 1][j] > self.lcslength_list[i][j - 1]:
                    self.lcslength_list[i][j] = self.lcslength_list[i - 1][j]
                    self.direction_list[i - 1][j - 1] = 1  # 上
                elif self.lcslength_list[i - 1][j] < self.lcslength_list[i][j - 1]:
                    self.lcslength_list[i][j] = self.lcslength_list[i][j - 1]
                    self.direction_list[i - 1][j - 1] = -1  # 左
                else:
                    self.lcslength_list[i][j] = self.lcslength_list[i - 1][j]
                    self.direction_list[i - 1][j - 1] = 2  # 左或上
        self.lcslength = self.lcslength_list[-1][-1]
        return self.direction_list, self.lcslength_list

    def printLCS(self, curlen, i, j, s):
        if i == 0 or j == 0:
            return None
        if self.direction_list[i - 1][j - 1] == 0:
            if curlen == self.lcslength:
                s += self.x[i - 1]
                for i in range(len(s)-1,-1,-1):
                    self.m.append(s[i])
                self.r.append(0)
                #print('\n')
            elif curlen < self.lcslength:
                s += self.x[i-1]
                self.printLCS(curlen + 1, i - 1, j - 1, s)
        elif self.direction_list[i - 1][j - 1] == 1:
            self.printLCS(curlen,i - 1, j,s)
        elif self.direction_list[i - 1][j - 1] == -1:
            self.printLCS(curlen,i, j - 1,s)
        else:
            self.printLCS(curlen,i - 1, j,s)
            self.printLCS(curlen,i, j - 1,s)
    def returnLCS(self):
        #回溯的入口
        self.printLCS(1,len(self.x), len(self.y),'')
#==============建表=====================

dict={"宜蘭縣":'003',"桃園市":'007',"新竹縣":'011',"苗栗縣":'015',
      "彰化縣":'019',"南投縣":'023',"雲林縣":'027',"嘉義縣":'031',
      "屏東縣":'035',"臺東縣":'039',"花蓮縣":'043',"澎湖縣":'047',
      "基隆縣":'051',"新竹市":'055',"嘉義市":'059',"臺北市":'063',
      "高雄市":'067',"新北市":'071',"臺中市":'075',"臺南市":'079',
      "連江縣":'083',"金門縣":'087',"臺灣":'091',0:'一',1:'二',
      2:'三',3:'四',4:'五',5:'六',6:'日'}
#============搜尋日期======================
def weatherData(dateTimeY = 0,dateTimeM = 0,dateTimeD = 0,select = None,inputcity = None):
    DT = False;
    if(select != '2'):
        DT=True;
#============輸入城市======================
    print('')
    city=dict[inputcity]
#==============設定參數======================
    src1='https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-'
    app_id = '?Authorization=' + appid
    src2='&limit=1&format=JSON'
    src=src1+city+app_id+src2
    with request.urlopen(src) as response:
        data=response.read().decode('utf-8')
        mis=json.loads(data)
     
#=============撈資料======================
    mist1=[]#特定日期紫外線強度
    mist2=[]#天氣資訊
    mist3=[]#天氣時間
    mist4=[]#紫外線時間
    mist5=[]#七天資訊的紫外線
    for i in range(0, 7, +1):
        mist5.append(mis['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][i]['elementValue'][0]['value'])
        mist1.append(mis['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][i]['elementValue'][1]['value'])
    for i in range(0, 7, +1):
        mist4.append(mis['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][i]['startTime'])
    for i in range(0, 14, +1):
        mist2.append(mis['records']['locations'][0]['location'][0]['weatherElement'][10]['time'][i]['elementValue'][0]['value'])
    for i in range(0, 14, +1):
        mist3.append(mis['records']['locations'][0]['location'][0]['weatherElement'][10]['time'][i]['startTime'])
#===============輸出========================
    if(DT==True):#這個區塊都在抓資料
        test=[]#天氣資訊切割
        cutDay=[]#日期切割
        j=0;
        Temperature=[]#每日平均溫
        rain=[]
        for i in range(0, 14, +1):
            test.append(mist2[i].split('。'))#天氣資訊切割
            cutDay.append(mist3[i].split(' '))
        #print(mist3[i])
            if(j<7):
                if(mist3[i]==mist4[j]):
                    if(test[i][2][0]=='溫'):#抓資料中的溫度
                        TemperatureC1=(int)(test[i][2][4]+test[i][2][5])
                        TemperatureC2=(int)(test[i][2][7]+test[i][2][8])
                        maT=TemperatureC1+TemperatureC2#溫度平均
                        if(maT%2==1):
                            maT=maT+1
                        maT=maT/2
                        Temperature.append((int)(maT))
                        if(test[i][1][6]=='%'):#抓資料中的降雨機率(test[i][1][6]這個位置%代表他是個位數的降雨機率
                            rain.append((int)(test[i][1][5]))
                        else:
                            tR=(int)(test[i][1][5]+(test[i][1][6]))
                            rain.append(tR)
                        j=j+1
                    else:
                        TemperatureC1=(int)(test[i][1][4]+test[i][1][5])
                        TemperatureC2=(int)(test[i][1][7]+test[i][1][8])
                        maT=TemperatureC1+TemperatureC2
                        if(maT%2==1):
                            maT=maT+1
                        maT=maT/2
                        Temperature.append((int)(maT))
                        rain.append(0)
                        j=j+1
    #--------------------禮拜X-------------------
    #例如今天是禮拜二dwArr=[ 2,3,4,5,6,7,1]就會有這樣的七天出來
        dwArr=[]
        dayOfWeek = datetime.today().weekday()
        for i in range(0, 7, +1):
            dayOfWeek=dayOfWeek+1
            if(dayOfWeek>7):#超過週日要變成週一開始
                dayOfWeek=dayOfWeek-7
                dwArr.append(dayOfWeek)
            else:
                dwArr.append(dayOfWeek)
        #-------------------------------------------
        
        sorT=sorted(Temperature)
        sTr=sortD(Temperature)#數字位置(用來恢復溫度的)
        #遞增最長子序列
        str1=""#Temperature
        str2=""#sorT
        for i in range(0, len(Temperature), +1):
            for j in range(0, len(sTr), +1):
                if(Temperature[i]==sTr[j]):
                    str1=str1+str(j)
        for i in range(0, len(Temperature), +1):
            for j in range(0, len(sTr), +1):
                if(sorT[i]==sTr[j]):
                        str2=str2+str(j)
    
        choseUD=[]#選擇遞增或是遞減
        controlUD=False
        Lup=[]#遞增的序列
        mathArr=[]
        p1 = LCS()
        p1.input(str1,str2,Lup,mathArr)
        p1.Compute_LCS()
        p1.returnLCS()
        
        check7=False
    #把多餘的遞增序列去除
        #mathArr是用來記住有多少組相同長度的最長子序列
        mathLong=int(len(Lup)/len(mathArr))#mathLong來限制長度
    
        for i in range(0, mathLong, +1):
            choseUD.append(Lup[i])
        rT=len(Lup)#最長子序列的長度
        controlUD=True
           
        for i in range(0, rT, +1):
            for j in range(0, len(sTr), +1):
                if(int(choseUD[0])==j):
                    del choseUD[0]
                    choseUD.append(sTr[j])

        minT=sorT[0]#本周平均最低溫
        maxT=sorT[len(sorT)-1]#本周平均最高溫
        messPri=[]
        detection=[0,0,0,0,0,0,0]
        runC=False
        printOut=""
        #這下面開始就是單純輸出了
        if(controlUD==True):
            if((maxT-minT)<2):
                printOut="未來七天內溫度會略有起伏，但是溫差不大?"
            elif((maxT-minT)>=2):
                for i in range(0, len(choseUD), +1):
                    runC=True
                    for j in range(i, len(Temperature), +1):
                        if(runC==True):
                            if(int(choseUD[i])==int(Temperature[j])and(detection[j]==0)):
                                messPri.append(j)
                                runC=False
                                detection[j]=1
                maxMes1=False#羧高溫度是否在範圍內
                for i in range(len(Temperature)-1, -1, -1):#遞增從尾找最高溫
                    if(maxT==Temperature[i]):
                        messPri.append(i)
                        break;
                            
                if(len(messPri)==2):
                    printOut="從週"+dict[dwArr[messPri[1]-1]]+"開始溫度持續下降到下週"
                elif(messPri[len(messPri)-1] <  messPri[len(messPri)-2] and messPri[len(messPri)-1] > messPri[0]):
                    printOut=dict[dwArr[messPri[0]]]+"開始平均溫度會持續上升到週"+dict[dwArr[messPri[len(messPri)-2]]-1]
                elif(messPri[len(messPri)-1] < messPri[0]):
                    c=int(Temperature[messPri[len(messPri)-1]])-int(Temperature[messPri[len(messPri)-1]+1])
                    printOut="平均溫度在週"+dict[dwArr[messPri[len(messPri)-1]]-1]+"為最高的"+str(maxT)+"度，並開始下降約"+str(c)+"度，在週"+dict[dwArr[messPri[0]]-1]+"開始趨於平衡"
                elif(messPri[len(messPri)-1]==messPri[len(messPri)-2]):
                    printOut="從今天起平均溫度會持續上升到週"+dict[dwArr[messPri[len(messPri)-2]]-1]
            #return(printOut)
            #print(printOut)
                

    #降雨機率
        light=[]
        medium=[]
        strong=[]
        for i in range(0, 7, +1):
            if(rain[i]<30):
                light.append(i)
            elif(rain[i]<50):
                medium.append(i)
            else:
                strong.append(i)
        putRainArr=""
        rainArr1=rainD(dwArr,light,30,putRainArr)
        rainArr2=rainD(dwArr,medium,50,putRainArr)
        rainArr3=rainD(dwArr,strong,100,putRainArr)
        rainArr=""
        if(rainArr1!=None):
            rainArr=rainArr+rainArr1
        if(rainArr2!=None):
            rainArr=rainArr+rainArr2
        if(rainArr3!=None):
            rainArr=rainArr+rainArr3
        #print(rainArr)
    #紫外線
        Low=[]
        Middle=[]
        High=[]
        Excessive=[]
        Dangerous=[]
        for i in range(0,7,+1):
            if(int(mist5[i])<3):
                Low.append(i)
            elif(int(mist5[i])>2 and int(mist5[i])<6):
                Middle.append(i)
            elif(int(mist5[i])>5 and int(mist5[i])<8):
                High.append(i)
            elif(int(mist5[i])>7 and int(mist5[i])<11):
                Excessive.append(i)
            else:
                Dangerous.append(i)
        putUvArr=""
        putUvArr1=UVI(dwArr,Low,3,putUvArr)
        putUvArr2=UVI(dwArr,Middle,5,putUvArr)  
        putUvArr3=UVI(dwArr,High,8,putUvArr)
        putUvArr4=UVI(dwArr,Excessive,10,putUvArr)
        putUvArr5=UVI(dwArr,Dangerous,11,putUvArr)
        if(putUvArr1!=None):
            putUvArr=putUvArr+putUvArr1
        if(putUvArr2!=None):
            putUvArr=putUvArr+putUvArr2
        if(putUvArr3!=None):
            putUvArr=putUvArr+putUvArr3
        if(putUvArr4!=None):
            putUvArr=putUvArr+putUvArr4
        if(putUvArr5!=None):
            putUvArr=putUvArr+putUvArr5
        #print(putUvArr)
        printOut=printOut+rainArr+putUvArr
        return(printOut)
    else:
        printOut=""
        test=[]
        testDate=dateTimeY+'-'+dateTimeM+'-'+dateTimeD
        #print(testDate)
        printOut=printOut+testDate
        cutDate=[]
        err=False
        for i in range(0, 14, +1):
            test.append(mist2[i].split('。'))
            cutDate.append(mist3[i].split(' '))
            if(cutDate[i][0]==testDate):
                #print(cutDate[i][1],'?')#時間
                printOut=printOut+" "+cutDate[i][1]
                for j in range(0, 7, +1):
                    if(mist3[i]==mist4[j]):
                        #print("?紫外線強度 : "+mist1[j]+"?")#紫外線
                        printOut=printOut+"紫外線強度:"+mist1[j]
                #print(test[i][0]+"?"+test[i][1]+"?"+test[i][2]+"??")#資訊
                printOut=printOut+"?"+test[i][0]+"?"+test[i][1]+"?"+test[i][2]+"??"
                err=True
        if(err==False):
            return("查無資料..超過七日內的資料")
        return(printOut)

print(weatherData(dateTimeY = '2019',dateTimeM = '11',dateTimeD = '21',select = '2',inputcity = '臺南市'))