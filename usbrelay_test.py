import os
import time

from instruments import Dollatek2USBRelay, find_device

# device = find_device("Dollatek2USBRelay") ALWAYS "BITFT"

usb_rele = Dollatek2USBRelay()

time.sleep(1)

print(usb_rele.status)
usb_rele.single_open(2)
print(usb_rele.status)

time.sleep(2)

print(usb_rele.status)
usb_rele.single_open(1)
usb_rele.single_close(2)
print(usb_rele.status)

time.sleep(2)

print(usb_rele.status)
usb_rele.open_all()
print(usb_rele.status)