import os
import time

class Dollatek2USBRelay:
    def __init__(self, serial_number = "BITFT"):
        self.relative_path = '\\usb_relay\\dollatek_usb_relay_hid\\TestApp\\'
        self.cwd = os.getcwd()

        self.path = self.cwd+self.relative_path

        self.serial_number = "BITFT"

        self.num_switches = 2

        # Close all swithces at initialization
        self.close_all()
        self.status = [False for _ in range(self.num_switches)]

    
    # ========================      COMMAND      ===========================
    # ########################   OPEN ONE CHANNEL     ######################
    # ======================================================================

    def single_open(self, channel):
        """
        Opens the specified channel

        Parameters:
        channel : int
            the switch that we are going to open
        """
        cmd = f'{self.path}CommandApp_USBRelay {self.serial_number} open {channel}'
        print(cmd)
        os.system(cmd)
        self.status[channel-1] = True

    # ======================================================================

    # ========================      COMMAND      ===========================
    # ########################   CLOSE ONE CHANNEL     #####################
    # ======================================================================

    def single_close(self, channel):
        """
        Closes the specified channel

        Parameters:
        channel : int
            the switch that we are going to close
        """
        cmd = f'{self.path}CommandApp_USBRelay {self.serial_number} close {channel}'
        os.system(cmd)
        self.status[channel-1] = False

    # ======================================================================

    # ========================      COMMAND      ===========================
    # ########################   OPEN ALL CHANNELS     #####################
    # ======================================================================

    def open_all(self):
        cmd = f'{self.path}CommandApp_USBRelay {self.serial_number} open 255'
        os.system(cmd)
        self.status = [True for _ in range(self.num_switches)]

    # ======================================================================

    # ========================      COMMAND      ===========================
    # ########################   CLOSE ALL CHANNELS     ####################
    # ======================================================================

    def close_all(self):
        cmd = f'{self.path}CommandApp_USBRelay {self.serial_number} close 255'
        os.system(cmd)
        self.status = [False for _ in range(self.num_switches)]

    # ======================================================================

    # ========================     ATTRIBUTE    ============================
    # ########################    READ STATUS   ############################
    # ======================================================================

    def make_reading(self):
        """
        Returns a vector with the same number of elements as channels the relay has.
            Each element 'i' is True if the switch in channel 'i+1' is open
            Each element 'i' is False if the switch in channel 'i+1' is closed
            
        Example: If channel 1 is closed and channel 2 i open this function will return [False, True]
        """
        return self.status

    # ======================================================================
