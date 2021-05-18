import requests 
import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def publish_message():
    symbol = 'dogeusdt'
    # symbol = 'filusdt'
    Headers = {"Content-Type": "application/json",
                       "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'https://api.huobi.pro/market/history/kline?symbol=' + symbol + '&period=1day&size=1'
    # print(url)
    resp = requests.get(url=url,headers=Headers)
    # print (resp.json()['data'])
    now_price = resp.json()['data'][0]['close']
    open_price = resp.json()['data'][0]['open']
    precent = (now_price - open_price )/open_price * 100
    precent = ('%.2f' % precent)
    now_price = ('%.5f' % now_price)
    message = str(now_price) + "&" + precent
    # print(precent)
    client.publish('jiucai', payload=message, qos=0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 1883, 600) # 600为keepalive的时间间隔
while True:
    publish_message()
    # print("ok")
    time.sleep(2)
