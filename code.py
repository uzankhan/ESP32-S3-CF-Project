import time
import board
import busio
import wifi
import socketpool
import ssl
import adafruit_requests
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import adafruit_dht
import analogio
import digitalio
import json

# ========== SETTINGS ==========
try:
    from settings import WIFI_SSID, WIFI_PASSWORD
except:
    WIFI_SSID = "RK"
    WIFI_PASSWORD = "gabbar125"

# ========== PIN DEFINITIONS - GPIO ==========
DHT_PIN = board.GPIO15
LDR_PIN = board.GPIO16
MQ2_PIN = board.GPIO2
TRIG_PIN = board.GPIO17
ECHO_PIN = board.GPIO18
PIR_PIN = board.GPIO19

RELAY_PIN = board.GPIO7
LED_PIN = board.GPIO14
BUZZER_PIN = board.GPIO6

LCD_SCL = board.GPIO9
LCD_SDA = board.GPIO8

print("ESP32-S3 Starting...")

# ========== LCD INIT ==========
try:
    i2c = busio.I2C(LCD_SCL, LCD_SDA)
    lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)
    lcd.clear()
    lcd.message = "ESP32-S3 READY"
    print("LCD Initialized!")
    time.sleep(2)
except Exception as e:
    print("LCD Error:", e)
    lcd = None

# ========== SENSORS INIT ==========
try:
    dht = adafruit_dht.DHT11(DHT_PIN)
    print("DHT11 Initialized!")
except Exception as e:
    print("DHT Error:", e)
    dht = None

try:
    ldr = analogio.AnalogIn(LDR_PIN)
    print("LDR Initialized!")
except Exception as e:
    print("LDR Error:", e)
    ldr = None

try:
    mq2 = digitalio.DigitalInOut(MQ2_PIN)
    mq2.direction = digitalio.Direction.INPUT
    mq2.pull = digitalio.Pull.DOWN
    print("MQ-2 Initialized!")
except Exception as e:
    print("MQ-2 Error:", e)
    mq2 = None

try:
    pir = digitalio.DigitalInOut(PIR_PIN)
    pir.direction = digitalio.Direction.INPUT
    pir.pull = digitalio.Pull.DOWN
    print("PIR Initialized!")
except Exception as e:
    print("PIR Error:", e)
    pir = None

# ========== OUTPUTS INIT ==========
try:
    led = digitalio.DigitalInOut(LED_PIN)
    led.direction = digitalio.Direction.OUTPUT
    led.value = False
    print("LED Initialized!")
except Exception as e:
    print("LED Error:", e)
    led = None

try:
    relay = digitalio.DigitalInOut(RELAY_PIN)
    relay.direction = digitalio.Direction.OUTPUT
    relay.value = False
    print("Relay Initialized!")
except Exception as e:
    print("Relay Error:", e)
    relay = None

try:
    buzzer = digitalio.DigitalInOut(BUZZER_PIN)
    buzzer.direction = digitalio.Direction.OUTPUT
    buzzer.value = False
    print("Buzzer Initialized!")
except Exception as e:
    print("Buzzer Error:", e)
    buzzer = None

# ========== ULTRASONIC ==========
def get_distance():
    try:
        trig = digitalio.DigitalInOut(TRIG_PIN)
        trig.direction = digitalio.Direction.OUTPUT
        echo = digitalio.DigitalInOut(ECHO_PIN)
        echo.direction = digitalio.Direction.INPUT

        trig.value = False
        time.sleep(0.000002)
        trig.value = True
        time.sleep(0.000010)
        trig.value = False

        pulse_start = time.monotonic()
        pulse_end = time.monotonic()
        timeout = 0.1
        start = time.monotonic()

        while echo.value == 0 and (time.monotonic() - start) < timeout:
            pulse_start = time.monotonic()

        start = time.monotonic()
        while echo.value == 1 and (time.monotonic() - start) < timeout:
            pulse_end = time.monotonic()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300 / 2

        trig.deinit()
        echo.deinit()

        if distance > 400 or distance < 2:
            return 0
        return round(distance, 1)
    except:
        return 0

# ========== WIFI CONNECT ==========
print("WiFi Connecting...")
if lcd:
    lcd.clear()
    lcd.message = "WiFi\nConnecting..."

try:
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print("WiFi Connected!")
    print("IP:", wifi.radio.ipv4_address)
    if lcd:
        lcd.clear()
        lcd.message = "WiFi OK\n" + str(wifi.radio.ipv4_address)
    time.sleep(2)
except Exception as e:
    print("WiFi Failed:", e)
    if lcd:
        lcd.clear()
        lcd.message = "WiFi FAILED"

# ========== WEB SERVER ==========
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()
requests = adafruit_requests.Session(pool, ssl_context)

if lcd:
    lcd.clear()
    lcd.message = "Server\nREADY"
time.sleep(2)

# ========== SENSOR READ ==========
def read_sensors():
    data = {
        "temperature": 0,
        "humidity": 0,
        "light": 0,
        "gas": 0,
        "distance": 0,
        "motion": False,
        "led": "OFF",
        "relay": "OFF",
        "buzzer": "OFF"
    }
    if dht:
        try:
            data["temperature"] = round(dht.temperature, 1)
            data["humidity"] = round(dht.humidity, 1)
        except:
            pass
    if ldr:
        try:
            data["light"] = ldr.value
        except:
            pass
    if mq2:
        try:
            data["gas"] = mq2.value
        except:
            pass
    if pir:
        try:
            data["motion"] = pir.value
        except:
            pass
    data["distance"] = get_distance()
    if led:
        data["led"] = "ON" if led.value else "OFF"
    if relay:
        data["relay"] = "ON" if relay.value else "OFF"
    if buzzer:
        data["buzzer"] = "ON" if buzzer.value else "OFF"
    return data

# ========== LCD UPDATE ==========
def update_lcd(data):
    if not lcd:
        return
    try:
        lcd.clear()
        temp = data.get("temperature", 0)
        hum = data.get("humidity", 0)
        lcd.set_cursor_pos(0, 0)
        lcd.message = str(temp) + "C " + str(hum) + "%"
        dist = data.get("distance", 0)
        gas = data.get("gas", 0)
        lcd.set_cursor_pos(1, 0)
        lcd.message = str(dist) + "cm Gas:" + str(gas)
    except:
        pass

# ========== WEB HANDLER ==========
def handle_request(client):
    try:
        request = client.recv(1024).decode()
        if not request:
            return
        lines = request.split('\r\n')
        if not lines:
            return
        path = lines[0].split(' ')[1] if len(lines[0].split(' ')) > 1 else '/'

        if path == '/data':
            data = read_sensors()
            response = json.dumps(data)
            client.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + response)
        elif path == '/led/on':
            if led:
                led.value = True
            client.send(b"HTTP/1.1 200 OK\r\n\r\nLED ON")
        elif path == '/led/off':
            if led:
                led.value = False
            client.send(b"HTTP/1.1 200 OK\r\n\r\nLED OFF")
        elif path == '/relay/on':
            if relay:
                relay.value = True
            client.send(b"HTTP/1.1 200 OK\r\n\r\nRELAY ON")
        elif path == '/relay/off':
            if relay:
                relay.value = False
            client.send(b"HTTP/1.1 200 OK\r\n\r\nRELAY OFF")
        elif path == '/buzzer/on':
            if buzzer:
                buzzer.value = True
            client.send(b"HTTP/1.1 200 OK\r\n\r\nBUZZER ON")
        elif path == '/buzzer/off':
            if buzzer:
                buzzer.value = False
            client.send(b"HTTP/1.1 200 OK\r\n\r\nBUZZER OFF")
        elif path == '/':
            html = """
<!DOCTYPE html>
<html>
<head>
<title>ESP32-S3 Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#0f0c29;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);min-height:100vh;color:white;padding:20px}
h1{text-align:center;font-size:2.5em;margin:20px 0;color:#e94560}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:20px;max-width:900px;margin:0 auto}
.card{background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-radius:15px;padding:20px;text-align:center;border:1px solid rgba(255,255,255,0.1)}
.card h3{color:#aaa;font-size:14px}
.card .value{font-size:28px;font-weight:bold;margin:10px 0;color:#e94560}
.card .value.green{color:#00b894}
.controls{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:30px auto}
.btn{padding:10px 20px;border:none;border-radius:5px;cursor:pointer;font-weight:bold}
.btn-on{background:#00b894;color:white}
.btn-off{background:#e94560;color:white}
.status{text-align:center;margin-top:20px;color:#888}
.footer{text-align:center;margin-top:30px;color:#555;font-size:12px}
</style>
</head>
<body>
<h1>ESP32-S3 Dashboard</h1>
<div class="grid" id="sensors">
<div class="card"><h3>Temp</h3><div class="value" id="temp">--C</div></div>
<div class="card"><h3>Humidity</h3><div class="value green" id="hum">--%</div></div>
<div class="card"><h3>Distance</h3><div class="value" id="dist">--cm</div></div>
<div class="card"><h3>Light</h3><div class="value" id="light">--</div></div>
<div class="card"><h3>Gas</h3><div class="value" id="gas">Safe</div></div>
<div class="card"><h3>Motion</h3><div class="value" id="motion">No</div></div>
</div>
<div class="controls">
<button class="btn btn-on" onclick="control('led/on')">LED ON</button>
<button class="btn btn-off" onclick="control('led/off')">LED OFF</button>
<button class="btn btn-on" onclick="control('relay/on')">RELAY ON</button>
<button class="btn btn-off" onclick="control('relay/off')">RELAY OFF</button>
</div>
<div class="status" id="status">Loading...</div>
<div class="footer">ESP32-S3 | CircuitPython</div>
<script>
function fetchData(){fetch('/data').then(r=>r.json()).then(data=>{document.getElementById('temp').textContent=data.temperature+'C';document.getElementById('hum').textContent=data.humidity+'%';document.getElementById('dist').textContent=data.distance+'cm';document.getElementById('light').textContent=data.light;document.getElementById('gas').textContent=data.gas?'GAS':'Safe';document.getElementById('gas').style.color=data.gas?'#e94560':'#00b894';document.getElementById('motion').textContent=data.motion?'Motion':'No Motion';document.getElementById('status').textContent='Last update: '+new Date().toLocaleTimeString();}).catch(()=>{document.getElementById('status').textContent='Error!';});}
function control(cmd){fetch('/'+cmd).then(()=>setTimeout(fetchData,500)).catch(()=>{});}
fetchData();setInterval(fetchData,10000);
</script>
</body>
</html>
"""
            client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
        else:
            client.send(b"HTTP/1.1 404 Not Found\r\n\r\nNot Found")
    except Exception as e:
        print("Request error:", e)
    finally:
        client.close()

# ========== MAIN LOOP ==========
print("Starting main loop...")
while True:
    try:
        data = read_sensors()
        update_lcd(data)
        try:
            server = socketpool.SocketPool(wifi.radio)
            server_socket = server.socket(server.AF_INET, server.SOCK_STREAM)
            server_socket.bind(('0.0.0.0', 80))
            server_socket.listen(1)
            server_socket.settimeout(0.1)
            try:
                client, addr = server_socket.accept()
                handle_request(client)
            except TimeoutError:
                pass
            except Exception as e:
                print("Server error:", e)
            finally:
                server_socket.close()
        except:
            pass
    except Exception as e:
        print("Main loop error:", e)
    time.sleep(10)