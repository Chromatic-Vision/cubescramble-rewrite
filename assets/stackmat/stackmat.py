import sounddevice as sd
from math import sqrt

# https://github.com/coder13/stackmat-python

DEVICE_NUM = 8

THRESHOLD_EDGE = 0.7
AGC_FACTOR = 0.0001

class BitStream:
    def __init__(self):
        self.buffer = []
        self.idleValue = 0
        self.lastBit = 0
        self.lastBitLength = 0

    def append(self, bit):
        self.buffer.insert(len(self.buffer), bit)
        self.lastBitLength = self.lastBitLength + 1 if bit == self.lastBit else 1
        self.lastBit = bit

        if self.lastBitLength > 10:
            self.idleValue = bit
            self.reset()

    def reset(self):
        self.buffer = []

    def isEmpty(self):
        return len(self.buffer) == 0

    def isFull(self):
        if len(self.buffer) >= 10:
            if self.buffer[0] == self.idleValue or self.buffer[9] != self.idleValue:
                self.buffer.pop(0)
                return False
            else:
                return True
        return False

    def toByte(self):
        byte = 0
        for i in range(8, 0, -1):
            byte = (byte << 1) | (self.buffer[i] == self.idleValue)
        return chr(byte)

    def dump(self):
        byte = self.toByte()
        self.reset()
        return byte

class Stackmat:

    def __init__(self, deviceNum):
        print(sd.query_devices()[deviceNum])
        sampleRate = 44100
        self.bitSampleRate = sampleRate / 1200
        self.agcFactor = 0.001 / self.bitSampleRate
        self.stream = sd.InputStream(
            device=deviceNum,
            samplerate=sampleRate,
            channels=1,
            callback=self.callback
        )
        self.sign = 1
        self.signalDuration = 0
        self.signalBuffer = [0] * round(self.bitSampleRate / 6)
        self.byteBuffer = []
        self.bits = BitStream()

        self.state = None
        self.last = 0
        self.taken = False

        self.stream.start()

    def callback(self, indata, frames, time, status):

        if status:
            print(status)
        self.process(indata)

    def close(self):
        self.stream.close()

    def process(self, inputs):
        power = 0
        lastPower = 1

        for i in inputs:
            v = i[0]
            power = v * v
            lastPower = max(self.agcFactor, lastPower + (power - lastPower) * self.agcFactor)
            gain = 1 / sqrt(lastPower)
            self.processSignal(v * gain)

    def processSignal(self, signal):
        self.signalBuffer.insert(0, signal)
        lastSignal = self.signalBuffer.pop()
        self.signalDuration += 1

        if self.signalIsEdge(signal, lastSignal):
            for i in range(0, round(self.signalDuration / self.bitSampleRate)):
                self.bits.append(self.sign)

                if self.bits.isEmpty():
                    self.byteBuffer = []

                if self.bits.isFull():
                    byte = self.bits.dump()
                    self.byteBuffer.insert(len(self.byteBuffer), byte)

                    if len(self.byteBuffer) >= 10:
                        self.processByteBlock()

            self.sign ^= 1
            self.signalDuration = 0

    def signalIsEdge(self, signal, lastSignal):
        return abs(lastSignal - signal) > THRESHOLD_EDGE and self.signalDuration > self.bitSampleRate * 0.6

    def processByteBlock(self):

        if self.state is not None:
            last_time = self.state.time
        else:
            last_time = 0

        state = decodeByteblock(self.byteBuffer)

        if state is not None:

            state.frozen = state.time == last_time and state.time != 0 and last_time != 0

            self.state = state

        # if state != None:
        #     print(state.state, state.time, state.resting, state.running)
        self.byteBuffer = []

class StackmatState:
    def __init__(self, state, time):
        self.state = state
        self.time = time
        self.resting = state == 'I'
        self.running = state == ' '
        self.frozen = False

def decodeByteblock(byteBuffer):
    try:
        state = byteBuffer[0]
        digits = list(map(lambda x: int(x), byteBuffer[1:7]))

        checkSum = ord(byteBuffer[7])
        sumDigits = 64 + sum(digits)

        if sumDigits != checkSum:
            return None

        milli = (digits[5] +
                 digits[4] * 10 +
                 digits[3] * 100 +
                 digits[2] * 1000 +
                 digits[1] * 10000 +
                 digits[0] * 60000)

        return StackmatState(state, milli)
    except ValueError:
        return None


if __name__ == '__main__':
    Stackmat(DEVICE_NUM)
