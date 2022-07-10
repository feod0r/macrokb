from machine import Pin
import time
#5,18,19
#5,19,18
#18,5,19
data = Pin(19, Pin.OUT, value=0) # ds / ser (14)
clock = Pin(5, Pin.OUT, value=0) # st_cp /  rclk (12)
latch = Pin(18, Pin.OUT, value=0) # sh_cp / srclk (11)

while True:
    for value in [0,1,3,7,15,31,63,127,255]:
        bits = [value >> i & 1 for i in range(7,-1,-1)]
        for i in range(7,-1,-1):
            print(bits[i])
            data.value(bits[i])
            clock.value(1)
            clock.value(0)
        latch.value(1)
        latch.value(0)

        time.sleep_ms(200)