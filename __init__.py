import time
import datetime
import math
import colorsys
from random import randint

from blinkstick import blinkstick

LED_COUNT = 10

WAKE_UP_MINTUES = 30
ALARM_HOUR = 7
ALARM_MINUTE = 0
ALARM_SECOND = 0

MAX_BRIGHTNESS = 255
R_RATIO = 1.0
G_RATIO = 0.5
B_RATIO = 0.5


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def get_led_color(progress, ratio):
    return clamp((progress * MAX_BRIGHTNESS) * ratio, 0, 255)

class Main(blinkstick.BlinkStickPro):
    def run(self):
        try:
            self.bstick.set_mode(2)
            self.off()
            self.send_data_all()

            brightness = 0
            status_blink = False
            light_message_start_shown = False
            light_message_end_shown = False

            now = datetime.datetime.now()
            alarm = now.replace(hour = ALARM_HOUR, minute = ALARM_MINUTE, second = ALARM_SECOND, microsecond = 0)
            if alarm < now:
                alarm += datetime.timedelta(days = 1)
            print 'Current time:\t' + now.strftime('%Y-%m-%d %H:%M:%S')
            print 'Alarm time:\t' + alarm.strftime('%Y-%m-%d %H:%M:%S')

            while True: 
                if brightness >= MAX_BRIGHTNESS:
                    continue

                start_time = alarm - datetime.timedelta(minutes=WAKE_UP_MINTUES)
                elapsed = datetime.datetime.now() - start_time
                progress = elapsed.total_seconds() / (WAKE_UP_MINTUES * 60.0) - 1
                
                if progress > 0:
                    if not light_message_start_shown:
                        print 'Turning lights on over ' + str(WAKE_UP_MINTUES) + ' minutes...'
                        light_message_start_shown = True;

                    r = get_led_color(progress, R_RATIO)
                    g = get_led_color(progress, G_RATIO)
                    b = get_led_color(progress, B_RATIO)
                    for led_index in range(1, self.r_led_count):
                        self.bstick.set_color(0, led_index, r, g, b)

                if progress > 1:
                    if not light_message_end_shown:
                        print 'Lights fully lit.'
                        light_message_end_shown = True

                self.bstick.set_color(0, 0, 1 * int(status_blink), 0, 0)
                status_blink = not status_blink

                time.sleep(1)

        except KeyboardInterrupt:
            self.off()
            return

main = Main(r_led_count = LED_COUNT)
if main.connect():
    main.run()
else:
    print 'No BlinkSticks found'