import pyvisa

import serial
import time

from instruments import ElFlowSelect, find_device

#List available resources
# rm = pyvisa.ResourceManager()
# print(rm.list_resources())

massflow = ElFlowSelect("COM3")
print(massflow.gas2flow)

# massflow.total_flow = 800
# print(massflow.total_flow)

# massflow.set_gas_percentage(100, total_flow = 10) # 10% of oxygen with total_flow fixed

massflow.set_gas_partial_pressure(partial_pressure = 0.1, total_pressure = 0.5, total_flow = 10, air = True) # 10% of oxygen with total_flow fixed
print(massflow.oxygen_partial_pressure)

massflow.set_gas_percentage_maximize(100) # 0.01% of oxygen

massflow.set_gas_percentage_minimize(90) # 0.01% of oxygen

print("--------------------------")

print(massflow.total_flow)
print(massflow.proportions)

# time.sleep(5)

# print(massflow.request_measure("03"))
# print(massflow.request_measure("04"))
"""
massflow.set_total_flow(800) # 800 ml/min of total_flow with percentages fixed

massflow.set_gas_percentage_maximize(50) # 50% of oxygen

massflow.set_gas_percentage_maximize(0.01) # 0.01% of oxygen
"""

"""
serialNum2flow = {
    "M21211517B" : 10,
    "M21211517A" : 800
}

settings = dict()
settings['baudrate'] = 38400
settings['bytesize'] = serial.EIGHTBITS
settings['parity'] = serial.PARITY_NONE
settings['stopbits'] = serial.STOPBITS_ONE
settings['timeout'] = 2

device_name = "COM3"
# Connect to device
inst = serial.Serial(device_name, **settings)

# Request setpoint and measure (chained)
w = inst.write(":0703047163716300\r\n".encode())
r = inst.read_until()
print(r)


# Change setpoint
w = inst.write(":06040101217D00\r\n".encode())
r = inst.read_until()
print(r)

time.sleep(1)

# Request setpoint and measure (chained)
w = inst.write(":0A04048121012101210120\r\n".encode())
r = inst.read_until()
print(r)


# Request setpoint
w = inst.write(":06030401210121\r\n".encode())
r = inst.read_until()
print(r) # :06800201217D00\r\n
# Request measure
w = inst.write(":06030401210120\r\n".encode())
r = inst.read_until()
print(r) # :06800201217D00



# Request serial number :108002716300__4D31353231303633344100\r\n
"""

