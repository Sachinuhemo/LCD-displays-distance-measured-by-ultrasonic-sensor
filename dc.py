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
