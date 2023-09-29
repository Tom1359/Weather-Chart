import network
import secrets
import urequests
import time
from machine import Pin, I2C
import neopixel
from pico_i2c_lcd import I2cLcd


i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))  
lcd_address = 0x27  
lcd = I2cLcd(i2c, lcd_address, 4, 20)

lcd.clear()

lcd.putstr("\n       Hello")
time.sleep(3)

lcd.clear()


lcd.putstr('\n Connecting to Wifi')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(secrets.SSID, secrets.PASSWORD)
while wlan.isconnected() == False:
    pass
print(f'Wifi Connected = {wlan.isconnected()}')
lcd.clear()
lcd.putstr('\n   Wifi Connected')





NUM_LEDS = 36  # Change this to the number of LEDs in your strip.
PIN = 0        # Change this to the GPIO pin where your data line is connected.

# Create a NeoPixel object.
leds = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)

# Color Codes for LED's
green = (255, 0, 0)
red = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (0, 255, 255)
off = (0, 0, 0)

# Function to set all LEDs to a specific color.
def set_color(color, airport):    
    leds[airport] = color
    leds.write()

# Function to cycle through colors.
def color_cycle():
    colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]  # Red, Green, Blue, Yellow, Purple
    for color in colors:
        set_color(color)
        time.sleep(1)

airports = {
'KSVH': 0,
'KIPJ': 1,
'KAKH': 2,
'KCLT': 3,
'KJQF': 4,
'KRUQ': 5,
'KEXX': 6,
'KGSO': 7,
'KHKY': 8,
'KMRN': 9,
'KEHO': 10,
'K35A': 11,
'KDCM': 12,
'KFDW': 13,
'KCDN': 14,
'KLKR': 15,
'KUDG': 16,
'KFLO': 17,
'KMAO': 18,
'KLBT': 19,
'KMEB': 20,
'KBBP': 21,
'KCQW': 22,
'KRCZ': 23,
'KAFP': 24,
'KVUJ': 25,
'KHBI': 26,
'KSCR': 27,
'KBUY': 28,
'KTTA': 29,
'KRDU': 30,
'KHRJ': 31,
'KPOB': 32,
'KFAY': 33,
'RELIABLE': 35}

while True:
    try:
        response = urequests.get(url="https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids=KBUY,KHKY,KGSO,K35A,KFLO,KAKH,KCLT,KJQF,KEXX,KEHO,KLKR,KUDG,KMAO,KCQW,KBBP,KAFP,KLBT,KFDW,KVUJ,KHBI,KDCM,KMRN,KTTA,KRUQ,KRDU,KIPJ,KCDN,KMEB,KSVH,KSCR,KHRJ,KPOB,KFAY,KRCZ&format=json")
        data = response.json()
        for item in data:
            apt = airports[str(item['icaoId'])]
            print(item['name'])
            VFR = True
            MVFR = False
            if item["visib"] == "10+":
                pass
            else:
                if int(item["visib"]) <= 2:
                    VFR = False
            for cloud in item['clouds']:
                try:
                    if int(cloud['base']) < 3000:
                        if cloud['cover'] == "BKN" or cloud['cover'] == "OVC":
                            VFR = False
                    if int(cloud['base']) >= 1000:
                        if item['visib'] == '10+' or int(item['visib']) >= 1:
                            MVFR = True
                except TypeError:
                    pass
            if VFR:
                print('VFR\n')
                set_color(green, apt)
            elif MVFR:
                print('MVFR\n')
                set_color(blue, apt)
            else:
                print('IFR\n')
                set_color(purple, apt)
            time.sleep(.05)
        
        lcd.clear()
        lcd.putstr(f'{data[28]["rawOb"]}')
        set_color(green, airports['RELIABLE'])
        data = []
        time.sleep(10)
        
    except:
        lcd.clear()
        lcd.putstr('\nNo Data Recieved')
        set_color(red, airports['RELIABLE'])
        time.sleep(5)
