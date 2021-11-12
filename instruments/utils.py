import instruments

import os
import pyvisa
import serial

class ReadUntil:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def read_until(self, expected = '\n'):
        i = self.buf.find(expected.encode())
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            if data == b'':     # Handle timeout
                return self.buf
            i = data.find(expected.encode())
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)


def find_device(name):
    rm = pyvisa.ResourceManager()
    
    if name == "Keithley2450":
        resources = rm.list_resources()
        print(resources)
        for resource in resources:
            try:
                keithley = instruments.Keithley2450(resource)
                id_keithley = keithley.id

                brand, model, sn, version = id_keithley.split(',')

                if brand == "KEITHLEY INSTRUMENTS" and model == "MODEL 2450":
                    return resource

            except:
                pass

        return None
        
    elif name == "GraphixTwo":
        resources = rm.list_resources()

        for resource in resources:
            if resource[:4] == "ASRL":
                com_number = resource[4]
            else:
                continue

            COM_port = "COM" + com_number
            try:
                inst = instruments.GraphixTwo(COM_port)

                # Command to read the serial number of the instrument:
                # Parameter group = 5, Parameter number = 2
                mode = "read"
                p_group = 5
                p_number = 2

                success, message = inst.send_command(parameter_group = p_group, parameter_number = p_number, mode = mode)

                if success:
                    return COM_port

            except:
                pass

        return None

    elif name == "FujiTemperatureController":
        resources = rm.list_resources()

        for resource in resources:
            if resource[:4] == "ASRL":
                com_number = resource[4]
            else:
                continue

            COM_port = "COM" + com_number
            try:
                inst = instruments.FujiTemperatureController(COM_port)

                # Try to read the temperature
                temp = inst.read_temperature()

                if type(temp) == float:
                    return COM_port

            except:
                pass

        return None

    elif name == "Dollatek2USBRelay":

        return "BITFT"