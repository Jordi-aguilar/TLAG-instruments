import os
import pyvisa
import serial
import minimalmodbus

from .utils import ReadUntil

class FujiTemperatureController:

    def __init__(self, adapter, **settings):
        self.inst = self.connect_FujiTemperatureController(adapter, **settings)

    def connect_FujiTemperatureController(self, device_name, **new_settings):
        # Connect to device
        inst = minimalmodbus.Instrument(mode = 'rtu', port = device_name, slaveaddress = 1, # Slaveaddress is hardcoded as 1
                                close_port_after_each_call = False, debug = False)

        # Setting up specific configuration parameters
        inst.serial.baudrate = 9600 # Baudrate must be the same as the instrument, otherwise it won't read anything (=9600 for the Fuji PXR4)
        inst.serial.bytesize = 8
        inst.serial.parity = serial.PARITY_NONE
        inst.serial.stopbits = 1
        inst.serial.timeout = 1 # seconds
        inst.clear_buffers_before_each_transaction = True

        return inst

    def read_temperature(self):
        temperature = self.inst.read_register(0, 1, 4) # Registeraddress, number of decimals, function code (4 = holding registers)
        return temperature


    # ========================     ATTRIBUTE    ============================
    #########################  READ TEMPERATURE  ###########################
    # ======================================================================

    def make_reading(self):
        """
        Returns a float. Measures the temperature.
        """
        return self.read_temperature()

    # ======================================================================


