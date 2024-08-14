![](https://img.shields.io/github/repo-size/Sachinuhemo/LCD-displays-distance-measured-by-ultrasonic-sensor)

[Japanese readme](https://github.com/Sachinuhemo/LCD-displays-distance-measured-by-ultrasonic-sensor/blob/main/README-jp.md)

This program connects an ultrasonic distance sensor to a Raspberry pi and displays the measured distance on the display.
## Preparations and operating environment
・Raspberry pi 3<br>
・[OLEDdisplay](https://amzn.asia/d/0ixCi5Gz)<br>
・Ultrasonic distance sensor HC-SR04<br>
・breadboard

Enable I2C communication.

## Install
```

pip install Pillow

```

## Connection
Connect GPIO2 to SDA on the LCD and GPIO3 to SCL.
Use the `i2cdetect` command to check if they are connected.
```
pi@raspberrypi:~ $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
It is connected because it shows 3c.
Connect GPIO15 to the trig_pin of the ultrasonic sensor and GPIO14 to the echo_pin.

## Run
```python
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306
import time
import sys

trig_pin = 15
echo_pin = 14
speed_of_sound = 34370 # speed of sound(cm/s)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_address=0x3C)
disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

font_path = "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf"
font = ImageFont.truetype(font_path, 30)

def get_distance():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    while not GPIO.input(echo_pin):
        pass
    t1 = time.time()

    while GPIO.input(echo_pin):
        pass
    t2 = time.time()

    return (t2 - t1) * speed_of_sound / 2

while True:
    try:
        distance = int(get_distance())
        text = f"{distance} cm"

        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), text, font=font, fill=1)

        disp.image(image)
        disp.display()

        time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
```
```

sudo pyhon3 dc.py

```
## Websites we referred to
・[ラズベリーパイで超音波距離センサーの使い方](https://raspi-school.com/ultrasonic-sensor/)
・[ラズパイを使って、OLED表示デバイスに文字列や画像を表示するよ](https://zenn.dev/kotaproj/articles/6f08ea43cd4dda8e0d2f)
