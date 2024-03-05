#!/usr/bin/python3

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from rx_tx_conf import *

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


lora = LoRa(verbose=True)
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
lora.set_freq(FREQ)

try:
    while True:
        lora.write_payload(list(TX_DEFAULT_MSG.encode('utf-8')))
        print(f'Status: {lora.get_modem_status()} RSSI: {lora.get_rssi_value()}')
        lora.set_mode(MODE.TX)

        sleep(TX_INTERVAL_MS/1000)

except KeyboardInterrupt:
    pass
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
    print("Bye!")
