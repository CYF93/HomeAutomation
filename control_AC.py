import adafruit_dht as dht
import board
import array
import pulseio
from time import sleep, localtime, monotonic
import wifi, socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT

WIFI_SSID = "" #your wifi SSID
WIFI_PASSWORD = "" #your wifi PW
print(f"Connecting to WiFi: {WIFI_SSID}")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)

aio_username = "" #your adafruit io username
aio_key = "" #your adafruit io key
ADAFRUIT_IO_URL = "io.adafruit.com"
pool = socketpool.SocketPool(wifi.radio)

mqtt_client = MQTT.MQTT(
    broker = ADAFRUIT_IO_URL,
    username=aio_username,
    password=aio_key,
    socket_pool=pool
)

print("Connecting to Adafruit IO...")
mqtt_client.connect()
print(f"Connected: {mqtt_client.is_connected()}")

on_command = array.array("H",[]) #enter the on signal into the list

off_command = array.array("H", []) #enter the off signal into the list

ir_send = pulseio.PulseOut(board.GP3, frequency=38000, duty_cycle=2**15) #follow the board pin connected to IR transmitter's Data pin
def control_AC(command,ir_send):
    ir_send.send(command)
    
feed = aio_username + "/feeds/temperature" #follow the name of your temperature feed in adafruit io
feed2 = aio_username + "/feeds/humidity" #follow the name of your humidity feed in adafruit io

sensor = dht.DHT11(board.GP4) #follow the board pin connected to DHT11's Data pin

feed3 = aio_username + "/feeds/AC_On" #follow the name of your on control feed in adafruit io
feed4 = aio_username + "/feeds/AC_Off" #follow the name of your off control feed in adafruit io

def on_message(client, topic, message):
    print(f"Feed {topic} received new value: {message}")
    if message == "1": #value of on control feed when on button is pressed in adafruit IO dashboard
        control_AC(on_command,ir_send)
        print("on command sent!")
    if message == "2": #value of off control feed when off button is pressed in adafruit IO dashboard
        control_AC(off_command,ir_send)
        print("off command sent!")
    
mqtt_client.on_message = on_message

mqtt_client.subscribe(feed3)
mqtt_client.subscribe(feed4)

last_publish_time = 0
publish_interval = 5 #temperature & humidity publishing interval in number of seconds
while True:
    
    try:
        current_time = monotonic()
        if current_time - last_publish_time >= publish_interval:
            try:
                sensor.measure()
                temp = sensor.temperature
                hum = sensor.humidity
                mqtt_client.publish(feed,temp)
                mqtt_client.publish(feed2,hum)
                time = str(localtime()[3])+":"+str(localtime()[4])+":"+str(localtime()[5])
                print(f"Temperature: {temp}C, Humidity: {hum}" + "  " + time)
                print("Waiting in loop...")
                last_publish_time = current_time
            except:
                mqtt_client.loop()
        mqtt_client.loop()
    except:
        print(f"Connecting to WiFi: {WIFI_SSID}")
        wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
        pool = socketpool.SocketPool(wifi.radio)
        mqtt_client.reconnect()
    


