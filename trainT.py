from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import time
import json
from requests import request

#需到公共運輸整合平台申請對應之id以及key才能使用
app_id = 'your_id'
app_key = 'your_key'

#==============函式======================
       
#=========================================
class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
    
def trainData(start_st,target_st,train_date,train_time):
    dict={"基隆":'0900',"三坑":'0910',"八堵":'0920',"七堵":'0930',"百福":'0940',"五堵":'0950',"汐止":'0960',"汐科":'0970',"南港":'0980',"松山":'0990',"臺北":'1000',"萬華":'1010',"板橋":'1020',"浮洲":'1030',"樹林":'1040',"南樹林":'1050',"山佳":'1060',"鶯歌":'1070',"桃園":'1080',"內壢":'1090',"中壢":'1100',"埔心":'1110',"楊梅":'1120',"富岡":'1130',"新富":'1140',"北湖":'1150',"湖口":'1160',"新豐":'1170',"竹北":'1180',"北新竹":'1190',"新竹":'1210',"三姓橋":'1220',"香山":'1230',"崎頂":'1240',"竹南":'1250',"談文":'2110',"大山":'2120',"後龍":'2130',"龍港":'2140',"白沙屯":'2150',"新埔":'2160',"通霄":'2170',"苑裡":'2180',"日南":'2190',"大甲":'2200',"臺中港":'2210',"清水":'2220',"沙鹿":'2230',"龍井":'2240',"大肚":'2250',"追分":'2260',"彰化":'3360',"花壇":'3370',"大村":'3380',"員林":'3390',"永靖":'3400',"社頭":'3410',"田中":'3420',"二水":'3430',"林內":'3450',"石榴":'3460',"斗六":'3470',"斗南":'3480',"石龜":'3490',"大林":'4050',"民雄":'4060',"嘉北":'4070',"嘉義":'4080',"水上":'4090',"南靖":'4100',"後壁":'4110',"新營":'4120',"柳營":'4130',"林鳳營":'4140',"隆田":'4150',"拔林":'4160',"善化":'4170',"南科":'4180',"新市":'4190',"永康":'4200',"大橋":'4210',"臺南":'4220',"保安":'4250',"仁德":'4260',"中洲":'4270',"大湖":'4290',"路竹":'4300',"岡山":'4310',"橋頭":'4320',"楠梓":'4330',"新左營":'4340',"左營":'4350',"內惟":'4360',"美術館":'4370',"鼓山":'4380',"三塊厝":'4390',"高雄":'4400',"海科館":'7361',"八斗子":'7362',"大華":'7331',"十分":'7332',"望古":'7333',"嶺腳":'7334',"平溪":'7335',"菁桐":'7336',"千甲":'1191',"新莊":'1192',"竹中":'1193',"上員":'1201',"榮華":'1202',"竹東":'1203',"橫山":'1204',"九讚頭":'1205',"合興":'1206',"富貴":'1207',"內灣":'1208',"六家":'1194',"勝興":'3192',"舊泰安":'3194',"造橋":'3140',"豐富":'3150',"苗栗":'3160',"南勢":'3170',"銅鑼":'3180',"三義":'3190',"泰安":'3210',"后里":'3220',"豐原":'3230',"栗林":'3240',"潭子":'3250',"頭家厝":'3260',"松竹":'3270',"太原":'3280',"精武":'3290',"臺中":'3300',"五權":'3310',"大慶":'3320',"烏日":'3330',"新烏日":'3340',"成功":'3350',"源泉":'3431',"濁水":'3432',"龍泉":'3433',"集集":'3434',"水里":'3435',"車埕":'343c6',"長榮大學":'4271',"沙崙":'4272',"暖暖":'7390',"四腳亭":'7380',"瑞芳":'7360',"侯硐":'7350',"三貂嶺":'7330',"牡丹":'7320',"雙溪":'7310',"貢寮":'7300',"福隆":'7290',"石城":'7280',"大里":'7270',"大溪":'7260',"龜山":'7250',"外澳":'7240',"頭城":'7230',"頂埔":'7220',"礁溪":'7210',"四城":'7200',"宜蘭":'7190',"二結":'7180',"中里":'7170',"羅東":'7160',"冬山":'7150',"新馬":'7140',"蘇澳新":'7130',"蘇澳":'7120',"永樂":'7110',"東澳":'7100',"南澳":'7090',"武塔":'7080',"漢本":'7070',"和平":'7060',"和仁":'7050',"崇德":'7040',"新城":'7030',"景美":'7020',"北埔":'7010',"花蓮":'7000',"吉安":'6250',"志學":'6240',"平和":'6230',"壽豐":'6220',"豐田":'6210',"林榮新光":'6200',"南平":'6190',"鳳林":'6180',"萬榮":'6170',"光復":'6160',"大富":'6150',"富源":'6140',"瑞穗":'6130',"三民":'6120',"玉里":'6110',"東里":'6100',"東竹":'6090',"富里":'6080',"池上":'6070',"海端":'6060',"關山":'6050',"瑞和":'6040',"瑞源":'6030',"鹿野":'6020',"山里":'6010',"臺東":'6000',"康樂":'5240',"知本":'5230',"太麻里":'5220',"金崙":'5210',"瀧溪":'5200',"大武":'5190',"古莊號":'5180',"枋野":'5170',"枋山":'5160',"內獅":'5140',"加祿":'5130',"枋寮":'5120',"東海":'5110',"佳冬":'5100',"林邊":'5090',"鎮安":'5080',"南州":'5070',"崁頂":'5060',"潮州":'5050',"竹田":'5040',"西勢":'5030',"麟洛":'5020',"歸來":'5010',"屏東":'5000',"六塊厝":'4470',"九曲堂":'4460',"後庄":'4450',"鳳山":'4440',"正義":'4430',"科工館":'4420',"民族":'4410'}
    
    nowclock=time.strftime("%R")
    now=nowclock.split(":")
    
    print("起程站")
    #st=input()#輸入
    st = start_st
    print("目標站")
    #et=input()
    et = target_st
    startS=dict[st]
    endS=dict[et]
    print("年月日例如 : 2019-06-12")
    #dayS=input() 
    dayS = train_date
    print("時間 例如 : 18:00")
    #checktime=input()
    checktime = train_time
    
    a = Auth(app_id, app_key)
    urT1= 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/DailyTrainTimetable/OD/'
    urT2='/to/'
    urT3='/'
    urT4='?$top=100&$format=JSON'
    ur1 = urT1+startS+urT2+endS+urT3+dayS+urT4
    response1 = request('get', ur1 , headers= a.get_auth_header())
    mis1=response1.text
    mist1 = json.loads(mis1)
    x=mis1.count("TrainInfo", 0, len(mis1))
    
    TrainNo=[]
    ArrivalTime=[]
    DepartureTime=[]
    checkR=0
    for i in range(0, x, +1):
        nT=mist1['TrainTimetables'][i]['StopTimes'][0]['DepartureTime']
        if(int(checktime[0]+checktime[1])<int(nT[0]+nT[1])):
            checkR+=1
            TrainNo.append(mist1['TrainTimetables'][i]['TrainInfo']['TrainNo'])
            DepartureTime.append(mist1['TrainTimetables'][i]['StopTimes'][0]['DepartureTime'])#出發時間
            ArrivalTime.append(mist1['TrainTimetables'][i]['StopTimes'][1]['ArrivalTime'])#到達時間
        elif(int(checktime[0]+checktime[1])==int(nT[0]+nT[1]) and int(checktime[3]+checktime[4])<int(nT[3]+nT[4])):
            checkR+=1
            TrainNo.append(mist1['TrainTimetables'][i]['TrainInfo']['TrainNo'])
            DepartureTime.append(mist1['TrainTimetables'][i]['StopTimes'][0]['DepartureTime'])#出發時間
            ArrivalTime.append(mist1['TrainTimetables'][i]['StopTimes'][1]['ArrivalTime'])#到達時間
    rT=0
    trainResultStr = '您所搜尋的車次有?'
    for j in range(0, 60, +1):
            for i in range(0, checkR, +1):
                if(int(DepartureTime[i][0]+DepartureTime[i][1])==(int(checktime[0]+checktime[1]))):
                    if(int(DepartureTime[i][3]+DepartureTime[i][4])==j):
                        rT+=1
                        trainResultStr = trainResultStr + DepartureTime[i] + '至' + ArrivalTime[i] + '?'
                        print("車次 : "+TrainNo[i]) 
                        print("出發時間 : "+DepartureTime[i])
                        print("抵達時間 : "+ArrivalTime[i])
                if(rT==3):
                    break
    if(rT<3):
        for j in range(0, 60, +1):
            for i in range(0, checkR, +1):
                if(int(DepartureTime[i][0]+DepartureTime[i][1])==(int(checktime[0]+checktime[1]))+1):
                    if(int(DepartureTime[i][3]+DepartureTime[i][4])==j):
                        rT+=1
                        trainResultStr = trainResultStr + DepartureTime[i] + '至' + ArrivalTime[i] + '?'
                        print("車次 : "+TrainNo[i]) 
                        print("出發時間 : "+DepartureTime[i])
                        print("抵達時間 : "+ArrivalTime[i])
                if(rT==3):
                    break;
    return trainResultStr
    
if __name__ == '__main__':
    print(trainData('嘉義','臺中','2019-09-24','21:00'))
    
    
