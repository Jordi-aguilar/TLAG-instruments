
import pyvisa

import serial
import time

from instruments import GraphixTwo, find_device

#List available resources
rm = pyvisa.ResourceManager()
print(rm.list_resources())

mode = "read"
p_group = 5
p_number = 2

device = find_device("GraphixTwo")
inst = GraphixTwo(device)

success, message = inst.send_command(parameter_group = p_group, parameter_number = p_number, mode = mode)

print(success, message)



print(inst.inst.isOpen()) # Check if connection is open
print(inst.inst.name)


def read_pressure():
    pressure1 = inst.read_pressure(channel = 1)

    return pressure1


import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import numpy as np
import time
import csv

# style.use('fivethirtyeight')

fig, ax1 = plt.subplots(1, 1)
ax1.set_title('Channel 1')
# ax2.set_title('Channel 2')

ax1.set_ylabel('Pressure (mbar)')
# ax2.set_ylabel('Pressure (mbar)')

ax1.grid()
# ax2.grid()

# plt.setp(ax1.get_xticklabels(), visible=False)
ax1.set_xlabel('time (s)')
# ax2.set_xlabel('time (s)')

x = 0

xs = []
ts = []
y1s = []
y2s = []

file = "./tests/pressure2.txt"

def write_line(file, values):
    with open(file, "a", newline='') as f:

        csvwriter = csv.writer(f)

        csvwriter.writerow(values)

def animate(i):
    global x
    # y1, y2 = 
    y1 = read_pressure()
    ti = time.time()

    lapse = (ti-t0)
    print(y1)
    values = [lapse, y1]
    write_line(file, values)

    xs.append(float(x))
    ts.append(lapse)

    y1s.append(float(y1))
    # y2s.append(float(y2))

    # ax1.clear()
    print(values)
    ax1.plot(ts, y1s, c = 'b')
    # ax2.plot(ts, y2s, c = 'b')
    x += 1

offset = 0

def acquire_data():
    while True:
        y1 = read_pressure()
        ti = time.time()

        lapse = (ti-t0) + offset
        print(y1)
        values = [lapse, y1]
        write_line(file, values)

        time.sleep(10)


t0 = time.time()
# ani = animation.FuncAnimation(fig, animate, interval=2000)
acquire_data()
plt.show()
