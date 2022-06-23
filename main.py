try:
  import usocket as socket
except:
  import socket

from machine import Pin,ADC,PWM
import network

import esp
esp.osdebug(None)

import gc
gc.collect()
from time import sleep

# set pinout
po13 = Pin(13, Pin.OUT)
po12 = Pin(12, Pin.OUT)
po14 = Pin(14, Pin.OUT)
po27 = PWM(Pin(27), freq=50)
po26 = Pin(26, Pin.OUT)
po25 = Pin(25, Pin.OUT)
pi35 = ADC(Pin(35))
pi34 = ADC(Pin(34))

# set vari for pinout
AC_temp_write = po13
AC_temp_write.off()
Water_Humidity_write = po12
Water_Humidity_write.off()
Light = po14
Light.off()
servo = po27
Door_1 = po26
Door_1.off()
Door_2 = po25
Door_2.off()
Ac_temp_read = pi34
humidity_read = pi35

Ac_temp_read.atten(ADC.ATTN_11DB) #full range = 3.3V

# wifi setting
ssid = "GuyEyalCannbis"
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())




#test Pin
led = Pin(2, Pin.OUT)

#inital the state to OFF mode
ac_state = "OFF"
water_state = "OFF"
light_state = "OFF"
door_1_state = "OFF"
door_2_state="OFF"
led_state = "OFF"

#HTML WEB PAGE
def web_page():
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>Guy & Eyal CannaboTech Control Base</h2>
    <center>
    LED state: <strong>""" + led_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?led_2_on\"><button class="button">LED ON</button></a>
    </p>
    
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?led_2_off\"><button class="button button1">LED OFF</button></a>
    </p>
     AC state: <strong>""" + ac_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?AC=1\"><button class="button">AC ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?AC=0\"><button class="button button1">AC OFF</button></a>
    </p>
    WATER state: <strong>""" + water_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?WATER=1\"><button class="button">WATER ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?WATER=0\"><button class="button button1">WATER OFF</button></a>
    </p>
    light state: <strong>""" + light_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?LIGHT=1\"><button class="button">LIGHT ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?LIGHT=0\"><button class="button button1">LIGHT OFF</button></a>
    </p>
    door 1 state: <strong>""" + door_1_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?DOOR1=1\"><button class="button">DOOR 1 OPEN</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?DOOR1=0\"><button class="button button1">DOOR 1 CLOSE</button></a>
    </p>
    door 2 state: <strong>""" + door_2_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?DOOR2=1\"><button class="button">DOOR 2 OPEN</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?DOOR2=0\"><button class="button button1">DOOR2 CLOSE</button></a>
    </p>
    
    <h3><CannboTech DATA</h3>
    <h3>temp data 
    <span><strong>""" + ac_value + """"</strong></span>
    </h3>
    
    <h3>humidity data</h3>

    plu
</body>

</html>"""
    return html

#socket setting between WEBSERVER TO ESP32
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        #PIN ENABLE
        led_on = request.find('/?led_2_on')
        led_off = request.find('/?led_2_off')
        if led_on == 6:
            print('LED ON')
            led_state = "ON"
            led.on()
        if led_off == 6:
            print('LED OFF')
            led_state = "OFF"
            led.off()
        ac_on = request.find('/?AC=1')
        ac_off = request.find('/?AC=0')
        if ac_on == 6:
            print('AC ON')
            ac_state="ON"
            AC_temp_write.on()
        elif ac_off == 6:
            print('AC OFF')
            ac_state="OFF"
            AC_temp_write.off()
        water_on = request.find('/?WATER=1')
        water_off = request.find('/?WATER=0')
        if water_on == 6:
            print('WATER ON')
            water_state="ON"
            Water_Humidity_write.on()
            servo.duty(70)
        elif water_off == 6:
            print('Water OFF')
            water_state="OFF"
            Water_Humidity_write.off()
            servo.duty(20)
            sleep(0.1)
        light_on = request.find('/?LIGHT=1')
        light_off = request.find('/?LIGHT=0')
        if light_on == 6:
            print('light ON')
            light_state="ON"
            Light.on()
        elif light_off == 6:
            print('LIGHT OFF')
            light_state="OFF"
            Light.off()
        door1_on = request.find('/?DOOR1=1')
        door1_off = request.find('/?DOOR1=0')
        if door1_on == 6:
            print('DOOR 1 OPEN')
            door_1_state="OPEN"
            Door_1.on()
        elif door1_off == 6:
            print('DOOR 1 CLOSE')
            door_1_state="CLOSE"
            Door_1.off()
        door2_on = request.find('/?DOOR2=1')
        door2_off = request.find('/?DOOR2=0')
        if door2_on == 6:
            print('Door 2 open')
            door_2_state="OPEN"
            Door_2.on()
        elif door2_off == 6:
            print('Door 2 close')
            door_2_state="CLOSE"
            Door_2.off()
            ac_read = Ac_temp_read.read()
            ac_value = (ac_read * 0.1875)/1000
            ac_value = ac_value *100
            sleep(0.1)





        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        #close socket
    except OSError as e:
        conn.close()
        print('Connection closed')
