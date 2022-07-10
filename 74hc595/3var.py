from machine import Pin
import utime
import random
#dataPIN = 18
#latchPIN = 19
#clockPIN = 5

dataPIN = 19 # ds / ser (14)
latchPIN = 18 # sh_cp / srclk (11)
clockPIN = 5 # st_cp /  rclk (12)
dataPIN=Pin(dataPIN, Pin.OUT)
latchPIN=Pin(latchPIN, Pin.OUT)
clockPIN=Pin(clockPIN, Pin.OUT)
def shift_update(input,data,clock,latch):
  #put latch down to start data sending
  clock.value(0)
  latch.value(0)
  clock.value(1)
  
  #load data in reverse order
  for i in range(7, -1, -1):
    clock.value(0)
    data.value(int(input[i]))
    clock.value(1)

  #put latch up to store data on register
  clock.value(0)
  latch.value(1)
  clock.value(1)
  
bit_string="00000000"

while True:
    shift_update(bit_string,dataPIN,clockPIN,latchPIN)
    bit_string = str(random.randint(0, 1))+bit_string[:-1]
    #print(bit_string)
    utime.sleep(0.2)
