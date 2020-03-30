import requests
import json
import time
from boltiot import Bolt
import config
mybolt=Bolt(config.Api_Key,config.device_id)
print(mybolt.isonline())
def get_sensor_value(pin):
    try:
        response=mybolt.analogRead(pin)
        data=json.loads(response)
        if(data['success'])!=1:
            print("request not succesfull")
            print("this is the response",data)
            return -999
        sesnor_value=int(data['value'])
        return sesnor_value
    except Exception as e:
        print("something wenr wrong!!!!")
        print(e)
        return -999
def send_telegram_message(message):
    URL="https://api.telegram.org/"+config.Telegram_bot_id+"/sendMessage"
    data={
        "chat_id":config.Telegram_chat_id,
        "text":message
    }
    try:
        response=requests.request("POST",URL,params=data)
        print("This is the telegram response")
        print(response.txt)
        telegram_data=json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error ocuured in sending message")
        print(e)
        return false
i=1
while i<3:
    sensor_value=get_sensor_value('A0')
    print("The current sensor value is " + str(sensor_value))
    if sensor_value==-999:
        print("request was unsuccesfull")
        time.sleep(10)
        continue
    if int(sensor_value)>=int(config.Threshold):
        print("sensor value exceeded threshold!!")
        message="Alert!! temperature value ecxeded" +" "+ str((int(config.Threshold))/10.24) + "degree celcius" + "the current temperature value is" + str((int(sensor_value))/10.24)+"degree celcius"
        telegran_status=send_telegram_message(message)
        print("this is the response",telegram_status)

