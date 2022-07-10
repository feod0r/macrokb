from machine import Pin
__version__ = '0.0.1'

class SR:
    def __init__(self, ser, srclk, rclk, srclr=None, oe=None):
        self.ser = ser
        self.srclk = srclk
        self.rclk = rclk
        self.srclr = srclr  # tie high if functionality not needed
        self.oe = oe        # tie low if functionality not needed

        self.ser.init(ser.OUT, value=0)
        self.srclk.init(srclk.OUT, value=0)
        self.rclk.init(rclk.OUT, value=0)

        if self.srclr is not None:
            self.srclr.init(srclr.OUT, value=1)
        if self.oe is not None:
            self.oe.init(oe.OUT, value=0)

    def _clock(self):
        self.srclk(1)
        self.srclk(0)

    def bit(self, value, latch=False):
        self.ser(value)
        self._clock()
        if latch:
            self.latch()

    def bits(self, value, num_bits, latch=False):
        for i in range(num_bits):
            self.bit((value >> i) & 1)
        if latch:
            self.latch()

    def latch(self):
        self.rclk(1)
        self.rclk(0)

    def clear(self, latch=True):
        if self.srclr is None:
            raise RuntimeError('srclr pin is required')
        self.srclr(0)
        self.srclr(1)
        if latch:
            self.latch()

    def enable(self, enabled=True):
        if self.oe is None:
            raise RuntimeError('oe pin is required')
        self.oe(not enabled)
        
ser = Pin(19, Pin.OUT) # ds / ser (14)
rclk = Pin(5, Pin.OUT)  # st_cp /  rclk (12)
srclk = Pin(18, Pin.OUT) # sh_cp / srclk (11)

# construct without optional pins
sr = SR(ser, srclk, rclk)


# reconstruct with all pins
oe = Pin(33, Pin.OUT, value=0)    # low enables output
srclr = Pin(32, Pin.OUT, value=1) # pulsing low clears data

sr = SR(ser, srclk, rclk, srclr, oe)

sr.bit(1)  # send high bit, do not latch yet
sr.bit(0)  # send low bit, do not latch yet
sr.latch() # latch outputs, outputs=0000_0010

sr.bit(1, 1) # send high bit and latch, outputs=0000_0101
sr.bit(0, 1) # send low bit and latch, outputs=0000_1010

sr.bits(0xff, 4) # send 4 lowest bits of 0xff (sends 0x0f), outputs=1010_1111

sr.clear(0) # clear the memory but don't latch yet
sr.latch()  # next latch shows the outputs have been reset

sr.bits(0b1010_1010, 8) # write some bits
sr.clear()  # clear the memory and latch, outputs have been reset

sr.enable()  # outputs enabled
sr.enable(0) # outputs disabled