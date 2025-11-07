import pulseio
import board
import adafruit_irremote

ir_receiver = pulseio.PulseIn(board.GP0, maxlen = 300) #follow the board pin connected to IR receiver's Data pin
decoder = adafruit_irremote.GenericDecode()

while True:
    pulses = decoder.read_pulses(ir_receiver)
    print("length of pulses:", len(pulses), "\nPulses:", pulses)
        