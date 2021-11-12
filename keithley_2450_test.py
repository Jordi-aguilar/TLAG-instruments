from instruments import Keithley2450

import pyvisa
import serial

import time

rm = pyvisa.ResourceManager()
print(rm.list_resources())

"""
# Connect to device
inst = rm.open_resource("TCPIP0::169.254.71.51::inst0::INSTR")

print(inst.write_termination.encode())
print(inst.read_termination)
print(inst.write('*IDN?'))
print(inst.read())
"""
# adapter = SerialAdapter("COM3")
keithley = Keithley2450("TCPIP0::169.254.71.51::inst0::INSTR") # USB0::0x05E6::0x2450::04322477::INSTR

print(keithley.id)

print("Hello")

keithley.apply_current()                # Sets up to source current
keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
keithley.compliance_voltage = 10        # Sets the compliance voltage to 10 V
keithley.source_current = 0             # Sets the source current to 0 mA
keithley.enable_source()                # Enables the source output

keithley.measure_voltage()              # Sets up to measure voltage
keithley.write("SENS:VOLT:UNIT OHM;")   # Change unit of measurement to OHM

keithley.ramp_to_current(1e-5)          # Ramps the current to 5 mA

print(keithley.voltage)                 # Prints the voltage in the selected unit
# print(keithley.measure_resistance(nplc=1, resistance=210000.0, auto_range=True))

time.sleep(2)
keithley.shutdown()                     # Ramps the current to 0 mA and disables output
