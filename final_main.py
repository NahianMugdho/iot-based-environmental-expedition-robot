from machine import PWM,Pin,ADC,Timer
from mq2 import MQ2
import time
import dht
from dcmotor import DCMotor        
from time import sleep
import hcsr04
import network
import time
from umqtt.robust import MQTTClient
import sys
import random #del after colour sensor
import urequests
import _thread
import usocket as socket

ultrasonic = hcsr04.HCSR04(trigger_pin=13, echo_pin=22, echo_timeout_us=1000000)
#Motor Part
frequency = 15000  #5000#15000
led=Pin(2,Pin.OUT)  
pin1 = Pin(12, Pin.OUT) #D12   
pin2 = Pin(14, Pin.OUT)  #D14   
enable = PWM(Pin(27), frequency)  #27
dc_motor = DCMotor(pin1, pin2, enable)      
dc_motor = DCMotor(pin1, pin2, enable, 350, 1023)
pin3 = Pin(26, Pin.OUT)  #D26  
pin4 = Pin(25, Pin.OUT)  #D25  
enable2 = PWM(Pin(33), frequency)  #D33
dc_motor2 = DCMotor(pin3, pin4, enable2,350, 1023)
#MQ-2 Part
pin=36
mq = MQ2(pinData = pin, baseVoltage = 3.3)
#COLOURS SENSOR S1,S2,S3,S4,OUT###########
s0 = Pin(16,Pin.OUT)
s1 = Pin(17,Pin.OUT)
s2 = Pin(18,Pin.OUT)
s3 = Pin(19,Pin.OUT)
out = Pin(21,Pin.IN,Pin.PULL_UP)
s0.on()
s1.off()       #s1.on()
def wait_for_edge(pin):
    global edge
    edge =True
out.irq(trigger=Pin.IRQ_FALLING,handler=wait_for_edge)
    
def measure():
    global edge
    delta = 0
    time.sleep(0.1)
    start= time.ticks_us()
    for compute in range(10):
        edge = False
        while edge == False:
            pass
    delta =time.ticks_diff(time.ticks_us(),start)
    return delta
def red():
    s2.off()
    s3.off()
    red=measure()
    return red
def green():
    s2.on()
    s3.on()
    green=measure()
    return green
def blue():
    s2.off()
    s3.on()
    blue=measure()
    return blue
#############
#####SERVO############
# Defining  Trigger and Echo pins
trigger = Pin(13, Pin.OUT)
echo = Pin(22, Pin.IN)
# Defining  Servo pin and PWM object
servoPin = Pin(23)
servo = PWM(servoPin)
duty_cycle = 0 # Defining and initializing duty cycle PWM
# Defining frequency for servo and enable pins
servo.freq(50)
def get_distance():
   distance = ultrasonic.distance_cm()
   return distance


#Defining function to set servo angle
def setservo(angle):
    duty_cycle = int(angle*(7803-1950)/180) + 1950
    servo.duty_u16(duty_cycle)

setservo(90)


######################

#DHT 11
dh = dht.DHT11(Pin(15))
# MQTT
WIFI_SSID     = ''            
WIFI_PASSWORD = ' '          #
#####
mqtt_client_id      = bytes('client_'+'12321', 'utf-8') # Just a random client ID
ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = ''
ADAFRUIT_IO_KEY     = ''
TOGGLE_FEED_ID      = 'mot'
TOGGLE_FEED_ID2      = 'gas'
TOGGLE_FEED_ID3     = 'me'
TOGGLE_FEED_ID4     = 'temp'
TOGGLE_FEED_ID5     = 'hum'
TOGGLE_FEED_ID6     = 'stream'
TOGGLE_FEED_ID7     = 'control'

flag = 1

########
api_key = '' #IFTTT
mail_api = ''#email
####Creating Functions
def forward():
    dc_motor.forward(80) #60
    dc_motor2.forward(80)
   
def backward():
    dc_motor.backwards(80)
    dc_motor2.backwards(80)
    
def right():
    dc_motor.forward(60)
    dc_motor2.backwards(60)
    
def left():
    dc_motor2.forward(60)
    dc_motor.backwards(60)
def stop():
    
    
    dc_motor.stop()
    dc_motor2.stop()
    




#Wifi####
def connect_wifi():
    print("Calibrating")
    mq.calibrate()
    print("Calibration completed")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 10):
            print(5 - timeout)
            timeout = timeout + 1
            led.value(1)
            time.sleep(1)
            led.value(0)
    if(wifi.isconnected()):
        print('Connected...')
        print('network config:', wifi.ifconfig())
        led.on()
    else:
        print('not connected')
        sys.exit()
        led.off()
        

connect_wifi() # Connecting to WiFi Router


# HTML Document

html='''<!DOCTYPE html>
<html>
<title>Army Ants</title>
<head>
<center><h1 style="color: white"> ANTBOT </h1></center>
<form>
</head>
<body>
    <style>
        html body {
          background-color: rgb(206, 206, 228);
          background-image:url(https://img.freepik.com/free-vector/digital-global-connection-network-technology-background_1017-23324.jpg?w=900&t=st=1672858471~exp=1672859071~hmac=23839581e669bd9d59f386dc6161b6758c0a30536f98b8fa92885c9b221490e4);
          background-repeat: no-repeat;
           
          background-size: 100% 700px;
        }
        
      </style> 

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;margin:0px auto;}
.tg td{border-color:white;border-style:dot;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-jxkc{background-color:#96fgfb;border-color:#ffffff;text-align:center;vertical-align:top}
.tg .tg-ib22{background-color:#fe996b;border-color:#ffffff;text-align:center;vertical-align:top}
.tg .tg-kf7a{background-color:#9698ed;border-color:#ffffff;text-align:center;vertical-align:middle}
</style>
<table class="tg">
<tbody>
  <tr>
    <td class="tg-jxkc" colspan="6">
<button name="LED3" value='ON' type='submit'> <h3> FORWARD </h3> </button>

    
    
    </td>
  </tr>
  <tr>
    <td class="tg-ib22" colspan="2" rowspan="2">
<button name="LED2" value='ON' type='submit'> <h3> LEFT </h3> </button>


    <td class="tg-kf7a" colspan="2" rowspan="2"><button name="LED3" value='OFF' type='submit'> <h3> STOP </h3> </button></td>
    
    <td class="tg-ib22" colspan="2" rowspan="2">
<button name="LED1" value='ON' type='submit'>  <h3> RIGHT </h3></button>

  </tr>
  <tr>
  </tr>
  <tr>
    <td class="tg-jxkc" colspan="6">
<button name="LED4" value='ON' type='submit'>  <h3> BACKWARD </h3> </button>

</td>
  </tr>
</tbody>
</table>
<center>
<h3 style="color: white"> AUTO PILOT </h3>
<button name="LED5" value='ON' type='submit'>  ON </button>

</center>
</body>
</html>






'''
# Initialising Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

Host = '' # Empty means, it will allow all IP address to connect
Port = 80 # HTTP port
s.bind(('',80)) # Host,Port

s.listen(5) # It will handle maximum 5 clients at a time
#####MQTTT Connection
client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
    
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    led.off()
    sys.exit()
    
###Feed IDs
motor_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8') #motor

hydro_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID2), 'utf-8')#hydro
met_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID3), 'utf-8')#CH4
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID4), 'utf-8')#temparature
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID5), 'utf-8')#Humidity
stream_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID6), 'utf-8')#Stream
control_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID7), 'utf-8')#Control
#######################
#hydrogen Calculation
def hydro_data():
#     hydro = mq.readHydrogen()
#     
#     meth = mq.readMethane()
#     lpg = mq.readLPG()
    smoke_val = ADC(Pin(36))
    
    hydro =int(smoke_val.read()/10)+random.uniform(0.5, 1) #mq.readHydrogen() #random.uniform(0.3, 1)
    
    meth = int(smoke_val.read()/20)+random.uniform(0.5, 1)#mq.readMethane() #random.uniform(0.3, 1)
    lpg = int(smoke_val.read()/30)+random.uniform(0.5, 1) #mq.readLPG()#random.uniform(0.3, 1)
    #global meth
    #client.publish(hydro_feed,    
                 # bytes(str(hydro), 'utf-8'),   # Publishing Hydro feed to adafruit.io
                  #qos=0)
   # client.publish(met_feed,    
                #  bytes(str(meth), 'utf-8'),   # Publishing Meth feed to adafruit.io
                 # qos=0)
   
    sensor_readings2 = {'value1':hydro,'value2':meth,'value3':lpg}
    request_headers2 = {'Content-Type': 'application/json'}
    #IFTTT Google sheet
    request2 = urequests.post(
        'http://maker.ifttt.com/trigger/LPG/with/key/' + api_key,
        json=sensor_readings2,
        headers=request_headers2)
    print(request2.text)#IFTTT command
    request2.close()
    
#CH4 Calculation#####

    
    
    

#####DHT11###########
def dh_data():
    dh.measure()
    global temp_data
    global hum_data
    temp_data = dh.temperature()
    hum_data = dh.humidity()
#     smk = mq.readSmoke()
    smoke_val = ADC(Pin(36))
    smk = int((smoke_val.read())/100) #mq.readSmoke()     #int((smoke_val.read())/100)   #random.uniform(0, 10)
    #client.publish(temp_feed,    
              #    bytes(str(temp_data), 'utf-8'),   # Publishing Meth feed to adafruit.io
             #     qos=0)
    if smk >=38:
        smail = urequests.post(
                'http://maker.ifttt.com/trigger/SmokeAlert/with/key/' + mail_api
                )
        print(smail.text)#IFTTT command
        smail.close()
        sleep(10)
        
        
    client.publish(hum_feed,    
                  bytes(str(hum_data), 'utf-8'),   # Publishing Meth feed to adafruit.io
                  qos=0)
    
    sensor_readings3 = {'value1':temp_data,'value2':hum_data,'value3':smk}
    request_headers3 = {'Content-Type': 'application/json'}
    #IFTTT Google sheet
    request3 = urequests.post(
        'http://maker.ifttt.com/trigger/THS/with/key/' + api_key,
        json=sensor_readings3,
        headers=request_headers3)
    print(request3.text)#IFTTT command
    request3.close()


######Colour Sensor############
def colour():
    n = blue()  #int(((blue())/(blue()+red()+green())))                  #blue()  #(blue())/(blue()+red()+green())
    p = green() #int(((green())/(blue()+red()+green()))) #green() #(green())/(blue()+red()+green())
    k = red() #int(((red())/(blue()+red()+green())))  #red() #(red())/(blue()+red()+green())
    client.publish(stream_feed,    
                  bytes(str(n), 'utf-8'),   # Publishing Meth feed to adafruit.io
                  qos=0)
    sensor_readings = {'value1':n,'value2':p,'value3':k}
    request_headers = {'Content-Type': 'application/json'}
    #IFTTT Google sheet
    request1 = urequests.post(
        'http://maker.ifttt.com/trigger/NPK/with/key/' + api_key,
        json=sensor_readings,
        headers=request_headers)
    print(request1.text)#IFTTT command
    request1.close()


    
def sens_data():
    #NPK
    while True:
        try:
            #dh_data()
            #sleep(5)
            led.on()
            dh_data()
            
            colour()
            #sleep(5)
            
            hydro_data()
           
            sleep(5)
            
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
            led.off()
            #IFTTT mail
            mail = urequests.post(
                'http://maker.ifttt.com/trigger/goodbye/with/key/' + mail_api
                
                )
            print(mail.text)#IFTTT command
            mail.close()
            sleep(10)
            pass
        
        
        #LPG,Methane,Hydrogen
        
        
    #temp,humidity,smoke
        
        
def auto():
    if flag == 0:
        while True:
            
            distance=get_distance() #Getting distance in cm
            print("disance",distance)
    #Defining direction based on conditions
            if distance < 30:
                stop()
                #backward()
                right()
                time.sleep(1)
                stop()
                time.sleep(0.5)
                setservo(30) #Servo angle to 30 degree
                time.sleep(1)
                right_distance=get_distance()
        #print(right_distance)
                time.sleep(0.5)
                setservo(150) #Servo angle to 150 degree
                time.sleep(1)
                left_distance=get_distance()
        #print(left_distance)
                time.sleep(0.5)
                setservo(90)
        
                if right_distance > left_distance:
                    #right()
                    forward()
                    time.sleep(2)
                    stop()
                else:
                    backward()
                    time.sleep(2)
                    stop()
            else:
                left()

            time.sleep(0.5)
    
        
#  no need     
def cb(topic, msg):                             # Callback function
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="f":
        dc_motor.forward(50)
        dc_motor2.forward(50)
        
        
    elif recieved_data=="b":
        dc_motor.backwards(50)
        dc_motor2.backwards(50)
        
    elif recieved_data=="r":#LEFT
        
        dc_motor2.forward(100)
        dc_motor.backwards(100)
        
    elif recieved_data=="l":#RIGHT
        dc_motor.forward(100)
        dc_motor2.backwards(100)
        
    elif recieved_data=="0":
        dc_motor.stop()
        dc_motor2.stop()
    elif recieved_data=="a":
        
         auto()
    else:
        
        dc_motor.stop()
        dc_motor2.stop()
        


client.set_callback(cb)
client.subscribe(motor_feed)
_thread.start_new_thread(sens_data,())

# main loop
while True:
  connection_socket,address=s.accept() # Storing Conn_socket & address of new client connected
  print("Got a connection from ", address)
  request=connection_socket.recv(1024) # Storing Response coming from client
  print("Content ", request) # Printing Response 
  request=str(request) # Coverting Bytes to String
  # Comparing & Finding Postion of word in String 
  FOR_ON =request.find('/?LED1=ON')
  FOR_OFF =request.find('/?LED1=OFF')
  
  BACK_ON =request.find('/?LED2=ON')
  BACK_OFF =request.find('/?LED2=OFF')
  
  LEFT_ON =request.find('/?LED3=ON')
  LEFT_OFF =request.find('/?LED3=OFF')
  
  RIGHT_ON =request.find('/?LED4=ON')
  RIGHT_OFF =request.find('/?LED4=OFF')
  
  AUTO_ON =request.find('/?LED5=ON')
  AUTO_OFF =request.find('/?LED5=OFF')
  
  if(FOR_ON==6):
    forward()
    
  if(FOR_OFF==6):
    stop()
    
  if(BACK_ON==6):
    backward()
    
  if(BACK_OFF==6):
    stop()
    
  if(LEFT_ON==6):
    left()
    
  if(LEFT_OFF==6):
    stop()
    
    
  if(RIGHT_ON==6):
    right()
    
  if(RIGHT_OFF==6):
    stop()
    
  if(AUTO_ON==6):
    flag=0
    auto()
  if(AUTO_OFF==6):
    flag=1  
    sys.exit()
    stop()
    
    
    
    
    
  # Sending HTML document in response everytime to all connected clients  
  response=html 
  connection_socket.send(response)
  
  #Closing the socket
  connection_socket.close()

    




















