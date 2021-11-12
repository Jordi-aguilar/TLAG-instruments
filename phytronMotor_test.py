
import pyvisa

import serial
import time

from instruments import MCC1_controller, find_device

#List available resources
rm = pyvisa.ResourceManager()
print(rm.list_resources())


device = "COM5"
inst = MCC1_controller(device)

print(inst.inst.isOpen()) # Check if connection is open
print(inst.inst.name)
print(inst.inst.baudrate)

stx = chr(2)
etx = chr(3)

# w = inst.inst.write(f"{stx}0 X+2{etx}".encode())
# r = inst.ReadUntil.read_until(etx)
# r = inst.get_current_position()

# r = inst.homing()
# print(r)

"""
r = inst.homing()
print(r)

r = inst.get_current_position()
print(r)

r = inst.relative_movement("+5")
print(r)

time.sleep(2)

r = inst.stop_movement()
print(r)

r = inst.get_current_position()
print(r)

r = inst.run_program("Growth_5")
print(r)

r = inst.stop_movement()
print(r)

r = inst.get_current_position()
print(r)

r = inst.relative_movement("-10 H")
print(r)

r = inst.get_current_position()
print(r)

r = inst.check_axis_standstill()
print(r)

r = inst.relative_movement("-10")
print(r)

r = inst.run_program("Growth_5")
print(r)

r = inst.stop_program()
print(r)
"""
# r = inst.homing()
# print(r)

r = inst.get_current_position()
print(r)

r = inst.check_axis_standstill()
print(r)