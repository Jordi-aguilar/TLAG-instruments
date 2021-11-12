from instruments import Keithley2450

import pyvisa
import serial

import time

rm = pyvisa.ResourceManager()
print(rm.list_resources())

keithley = Keithley2450("TCPIP0::169.254.71.51::inst0::INSTR") # USB0::0x05E6::0x2450::04322477::INSTR

print(keithley.id)

current = 10e-6
keithley.prepare_resistance_measurement(current)

print(keithley.voltage)

keithley.shutdown()                     # Ramps the current to 0 mA and disables output
