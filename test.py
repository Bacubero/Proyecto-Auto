import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import PWM, Pin
import machine

ssid = 'MUGICA'
password = '20032006'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Conectando...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Conectado a {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./atras">
            <input type="submit" value="Atras" />
            </form>
            <form action="./motoron">
            <input type="submit" value="Motor on" />
            </form>
            <form action="./motoroff">
            <input type="submit" value="Motor off" />
            </form>
            <form action="./v25">
                <input type="submit" value="25%">
            </form>
            <form action="./v50">
                <input type="submit" value="50%">
            </form>
            <form action="./75">
                <input type="submit" value="75%">
            </form>
            <form action="./100">
                <input type="submit" value="100%">
            </form>
            <form action="./slider">
                0<input type="range" min="1" max="100" value="50">100
            </form>
            <p>El motor esta {state}</p>
            <p>La temperatura es {temperature}</p>
            </body>
            </html>
            """
    return str(html)

pwmPIN=16
cwPin=14 
acwPin=15

def motorMove(speed,direction,speedGP,cwGP,acwGP):
    if speed > 100: speed=100
    if speed < 0: speed=0
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    Speed.duty_u16(int(speed/100*65536))
    if direction < 0:
        cw.value(0)
        acw.value(1)
    if direction == 0:
        cw.value(0)
        acw.value(0)
    if direction > 0:
        cw.value(1)
        acw.value(0)

# main program
#motorMove(100,-1,pwmPIN,cwPin,acwPin)
#sleep(5)
#motorMove(100,0,pwmPIN,cwPin,acwPin)

def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/motoron?':
            pico_led.on()
            state = 'Prendido'
            motorMove(100,1,pwmPIN,cwPin,acwPin)
        elif request =='/atras?':
            pico_led.on()
            state = 'Atras'
            motorMove(100,-1,pwmPIN,cwPin,acwPin)
        elif request =='/motoroff?':
            pico_led.off()
            state = 'Apagado'
            motorMove(100,0,pwmPIN,cwPin,acwPin)
        elif request == '/v25?':
            pico_led.on()
            state= "Al 25%"
            motorMove(25,1,pwmPIN,cwPin,acwPin)
        html = webpage(temperature, state)
        temperature = pico_temp_sensor.temp
        client.send(html)
        client.close()



try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()