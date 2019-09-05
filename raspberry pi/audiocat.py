#coding:utf-8
import wave
import time
import requests
import base64
import os
import json
from aip import AipSpeech
import os
import sqlite3


def cat_audiohint(result,doAudio):
    conn1 = sqlite3.connect('trashdb.db')
    cursor1 = conn1.cursor()
    conn2 = sqlite3.connect('trashdb.db')
    cursor2 = conn2.cursor()
    conn3 = sqlite3.connect('trashdb.db')
    cursor3 = conn3.cursor()
    conn4 = sqlite3.connect('trashdb.db')
    cursor4 = conn4.cursor()
    conn5 = sqlite3.connect('trashdb.db')
    cursor5 = conn5.cursor()

    cursor1.execute("select * from cycletrash where NAME='" + result + "'")
    cursor2.execute("select * from harmtrash where NAME='" + result + "'")
    cursor3.execute("select * from drytrash where NAME='" + result + "'")
    cursor4.execute("select * from wettrash where NAME='" + result + "'")
    cursor5.execute("select * from drywettrash where NAME='"+result+"'")
    if cursor1.fetchall():
        values = "请将内容物压扁，尖锐物包裹后投放"
        cat="cycletrash"
    elif cursor2.fetchall():
        values = "请连同包装投放"
        cat="harmtrash"
    elif cursor3.fetchall():
        values = "尽量沥干水份后投入垃圾桶内"
        cat="drytrash"
    elif cursor4.fetchall():
        values = "将流体放入湿垃圾桶内，将包裹等固体放入可回收物容器"
        cat="wettrash"
    elif cursor5.fetchall():
        values = "将内容物放入湿垃圾桶内，将包装外壳放入干垃圾桶内"
        cat="drywettrash"
    else:
        values = "无法识别，请将物体投入侧方垃圾桶"
        cat=None

    cursor1.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    conn1.close()
    conn2.close()
    conn3.close()
    conn4.close()
    conn5.close()
    if doAudio:
        APP_ID = '16695449'
        API_KEY = 'bpaBivKg9oTW07UcBhBIt973'
        SECRET_KEY = ' xBfN3F8gDc7OB6F5gUdPrk044Q649Mhf'
        client = AipSpeech('16695449', 'bpaBivKg9oTW07UcBhBIt973', 'xBfN3F8gDc7OB6F5gUdPrk044Q649Mhf')
        result1 = client.synthesis(text=values, options={'vol': 5})
        
        if not isinstance(result1, dict):
            with open('audio.mp3', 'wb') as f:
                f.write(result1)
        else:
            print(result1)

        os.system('omxplayer -o local audio.mp3')
    return cat


def audioinput():
    my_buf = []  # 存放录音数据
    framerate = 16000  # 采样率
    num_samples = 2000  # 采样点
    channels = 1  # 声道
    sampwidth = 2  # 采样宽度2bytes
    filepath = 'speech.wav'

    # 录音
    print("recording")
    os.system("arecord -D \"plughw:1,0\" -d 4 -r 16000 -c 1 -t wav -f S16_LE speech.wav")
    print("ending")

    baidu_server = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"
    # API Key
    client_id = "bpaBivKg9oTW07UcBhBIt973"
    # Secret Key
    client_secret = "xBfN3F8gDc7OB6F5gUdPrk044Q649Mhf"
    # 拼url
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=bpaBivKg9oTW07UcBhBIt973&client_secret=xBfN3F8gDc7OB6F5gUdPrk044Q649Mhf"
    # print(url)
    # 获取token
    res = requests.post(url)

    print(res.text)
    token = json.loads(res.text)["access_token"]

    RATE = "16000"  # 采样率16KHz
    FORMAT = "wav"  # wav格式
    CUID = "ff03224b463a40dc92746a5d2c5a6a25"
    DEV_PID = "1536"  # 无标点普通话

    # 以字节格式读取文件之后进行编码
    with open("./speech.wav", "rb") as f:
        speech = base64.b64encode(f.read()).decode('utf8')
    size = os.path.getsize("./speech.wav")
    print(size)
    headers = {'Content-Type': 'application/json'}
    url = "https://vop.baidu.com/server_api"
    data = {
        "format": FORMAT,
        "rate": RATE,
        "dev_pid": DEV_PID,
        "speech": speech,
        "cuid": CUID,
        "len": size,
        "channel": 1,
        "token": token,
    }
    print("正在识别")
    req = requests.post(url, json.dumps(data), headers)
    result = json.loads(req.text)
    print("识别成功")
    speechresult = result["result"][0]
    print(result["result"][0])

    speechresult = speechresult[:-1]
    cat_audiohint(speechresult,1)
