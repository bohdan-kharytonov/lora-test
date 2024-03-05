#!/usr/bin/python3

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

from rx_tx_conf import FREQ

# Original values was...
# DIO0 = 4
# DIO1 = 17
# DIO2 = 18
# DIO3 = 27
# RST  = 22
# LED  = 13 
# IO4 - ?
# IO5 - ?

BOARD.DIO0 = 18
BOARD.DIO1 = 27
BOARD.DIO2 = 22
BOARD.DIO3 = 23
BOARD.RST  = 17
BOARD.LED  = 13

BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(1)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            self.on_rx_done()
            
    def on_rx_done(self):
        print("\nReceived: ")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8",'ignore'))
#        self.set_mode(MODE.SLEEP)
#        self.reset_ptr_rx()
#        self.set_mode(MODE.RXCONT)

lora = LoRaRcvCont(verbose=True)
lora.set_mode(MODE.STDBY)

lora.set_freq(FREQ)

print(f'LoRa chip version {lora.get_version()}. Frequency {lora.get_freq()}')

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
