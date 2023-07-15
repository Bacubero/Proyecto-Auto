MIME-Version: 1.0
Date: Tue, 20 Jun 2023 21:54:39 -0400
Message-ID: <CALrSOm2dsoWgheZxSh1a1LgsQdPB2-zojPmZtEjUPBOUXAhKXQ@mail.gmail.com>
Subject: Codigo controlador de motores v2
From: Bautista Olivera <bautista@3mundos.com>
To: Bautista Olivera <bautista@3mundos.com>
Content-Type: multipart/alternative; boundary="000000000000b146ac05fe9a0cfd"

--000000000000b146ac05fe9a0cfd
Content-Type: text/plain; charset="UTF-8"

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

--000000000000b146ac05fe9a0cfd
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div dir=3D"ltr">import network<br>import socket<br>from time import sleep<=
br>from picozero import pico_temp_sensor, pico_led<br>from machine import P=
WM, Pin<br>import machine<br><br>ssid =3D &#39;MUGICA&#39;<br>password =3D =
&#39;20032006&#39;<br><br>def connect():<br>=C2=A0 =C2=A0 wlan =3D network.=
WLAN(network.STA_IF)<br>=C2=A0 =C2=A0 wlan.active(True)<br>=C2=A0 =C2=A0 wl=
an.connect(ssid, password)<br>=C2=A0 =C2=A0 while wlan.isconnected() =3D=3D=
 False:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 print(&#39;Conectando...&#39;)<br>=
=C2=A0 =C2=A0 =C2=A0 =C2=A0 sleep(1)<br>=C2=A0 =C2=A0 ip =3D wlan.ifconfig(=
)[0]<br>=C2=A0 =C2=A0 print(f&#39;Conectado a {ip}&#39;)<br>=C2=A0 =C2=A0 r=
eturn ip<br><br>def open_socket(ip):<br>=C2=A0 =C2=A0 address =3D (ip, 80)<=
br>=C2=A0 =C2=A0 connection =3D socket.socket()<br>=C2=A0 =C2=A0 connection=
.bind(address)<br>=C2=A0 =C2=A0 connection.listen(1)<br>=C2=A0 =C2=A0 retur=
n connection<br><br>def webpage(temperature, state):<br>=C2=A0 =C2=A0 html =
=3D f&quot;&quot;&quot;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;!D=
OCTYPE html&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;html&gt;<b=
r>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;form action=3D&quot;./atras=
&quot;&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;input type=3D&q=
uot;submit&quot; value=3D&quot;Atras&quot; /&gt;<br>=C2=A0 =C2=A0 =C2=A0 =
=C2=A0 =C2=A0 =C2=A0 &lt;/form&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =
=C2=A0 &lt;form action=3D&quot;./motoron&quot;&gt;<br>=C2=A0 =C2=A0 =C2=A0 =
=C2=A0 =C2=A0 =C2=A0 &lt;input type=3D&quot;submit&quot; value=3D&quot;Moto=
r on&quot; /&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;/form&gt;=
<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;form action=3D&quot;./mot=
oroff&quot;&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;input type=
=3D&quot;submit&quot; value=3D&quot;Motor off&quot; /&gt;<br>=C2=A0 =C2=A0 =
=C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;/form&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =
=C2=A0 =C2=A0 &lt;p&gt;El motor esta {state}&lt;/p&gt;<br>=C2=A0 =C2=A0 =C2=
=A0 =C2=A0 =C2=A0 =C2=A0 &lt;p&gt;La temperatura es {temperature}&lt;/p&gt;=
<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;/body&gt;<br>=C2=A0 =C2=
=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 &lt;/html&gt;<br>=C2=A0 =C2=A0 =C2=A0 =C2=
=A0 =C2=A0 =C2=A0 &quot;&quot;&quot;<br>=C2=A0 =C2=A0 return str(html)<br><=
br>pwmPIN=3D16<br>cwPin=3D14 <br>acwPin=3D15<br><br>def motorMove(speed,dir=
ection,speedGP,cwGP,acwGP):<br>=C2=A0 =C2=A0 if speed &gt; 100: speed=3D100=
<br>=C2=A0 =C2=A0 if speed &lt; 0: speed=3D0<br>=C2=A0 =C2=A0 Speed =3D PWM=
(Pin(speedGP))<br>=C2=A0 =C2=A0 Speed.freq(50)<br>=C2=A0 =C2=A0 cw =3D Pin(=
cwGP, Pin.OUT)<br>=C2=A0 =C2=A0 acw =3D Pin(acwGP, Pin.OUT)<br>=C2=A0 =C2=
=A0 Speed.duty_u16(int(speed/100*65536))<br>=C2=A0 =C2=A0 if direction &lt;=
 0:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 cw.value(0)<br>=C2=A0 =C2=A0 =C2=A0 =C2=
=A0 acw.value(1)<br>=C2=A0 =C2=A0 if direction =3D=3D 0:<br>=C2=A0 =C2=A0 =
=C2=A0 =C2=A0 cw.value(0)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 acw.value(0)<br>=
=C2=A0 =C2=A0 if direction &gt; 0:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 cw.value(=
1)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 acw.value(0)<br><br># main program<br>#mo=
torMove(100,-1,pwmPIN,cwPin,acwPin)<br>#sleep(5)<br>#motorMove(100,0,pwmPIN=
,cwPin,acwPin)<br><br>def serve(connection):<br>=C2=A0 =C2=A0 state =3D &#3=
9;OFF&#39;<br>=C2=A0 =C2=A0 pico_led.off()<br>=C2=A0 =C2=A0 temperature =3D=
 0<br>=C2=A0 =C2=A0 while True:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 client =3D c=
onnection.accept()[0]<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 request =3D client.rec=
v(1024)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 request =3D str(request)<br>=C2=A0 =
=C2=A0 =C2=A0 =C2=A0 try:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 requ=
est =3D request.split()[1]<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 except IndexError=
:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 pass<br>=C2=A0 =C2=A0 =C2=A0=
 =C2=A0 if request =3D=3D &#39;/motoron?&#39;:<br>=C2=A0 =C2=A0 =C2=A0 =C2=
=A0 =C2=A0 =C2=A0 pico_led.on()<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=
=A0 state =3D &#39;Prendido&#39;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=
=A0 motorMove(100,1,pwmPIN,cwPin,acwPin)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 eli=
f request =3D=3D&#39;/atras?&#39;:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =
=C2=A0 pico_led.on()<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 state =3D=
 &#39;Atras&#39;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 motorMove(100=
,-1,pwmPIN,cwPin,acwPin)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 elif request =3D=3D=
&#39;/motoroff?&#39;:<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 pico_led=
.off()<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 state =3D &#39;Apagado&=
#39;<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 =C2=A0 motorMove(100,0,pwmPIN,cw=
Pin,acwPin)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 html =3D webpage(temperature, st=
ate)<br>=C2=A0 =C2=A0 =C2=A0 =C2=A0 temperature =3D pico_temp_sensor.temp<b=
r>=C2=A0 =C2=A0 =C2=A0 =C2=A0 client.send(html)<br>=C2=A0 =C2=A0 =C2=A0 =C2=
=A0 client.close()<br><br><br><br>try:<br>=C2=A0 =C2=A0 ip =3D connect()<br=
>=C2=A0 =C2=A0 connection =3D open_socket(ip)<br>=C2=A0 =C2=A0 serve(connec=
tion)<br>except KeyboardInterrupt:<br>=C2=A0 =C2=A0 machine.reset()</div>

--000000000000b146ac05fe9a0cfd--