import os
import pyvisa
import serial

from .utils import ReadUntil

class MCC1_controller:

    def __init__(self, adapter, **settings):
        self.inst = self.connect_MCC1_controller(adapter, **settings)

        self.ReadUntil = ReadUntil(self.inst)

        self.stx = '\x02'   # Start Of Text. chr(2)
        self.etx = '\x03'   # End Of Text. chr(3)
        self.ack = '\x06'   # Acknowledge. chr(6)

    def connect_MCC1_controller(self, device_name, **new_settings):
        settings = dict()
        settings['baudrate'] = 115200 #57600
        settings['bytesize'] = serial.EIGHTBITS
        settings['parity'] = serial.PARITY_NONE
        settings['stopbits'] = serial.STOPBITS_ONE
        settings['timeout'] = 5

        settings.update(new_settings)

        # Connect to device
        inst = serial.Serial(device_name, **settings)

        return inst

    # ========================      COMMAND      ===========================
    ############################# RUN PROGRAM  #############################
    # ======================================================================

    def run_program(self, program_name):
        """
        Runs a program that should be already loaded in the controller.

        Parameters
        ----------
        program_name : str
            Name of the program as it is loaded in the controller. It should be already loaded in the controller.
        """
        command = f"QP{program_name} N01A" # Starts {program_name} from line 01
        r = self.send_command(command)
        return r

    # ======================================================================

    def get_current_position(self):
        command = "XP20R"
        r = self.send_command(command)
        return r

    # ========================      COMMAND      ===========================
    ######################### CONFIGURE INSTRUMENT #########################
    # ======================================================================

    def relative_movement(self, movement):
        """
        Moves the motor {movement} rotations.

        Parameters
        ----------
        movement : float
            It can be negative or positive. If it is negative the motor will go {movement} rotations to the negative side, if it is positive it will move to the other side.
        """
        command = f"X{movement}"
        r = self.send_command(command)
        return r

    # ======================================================================

    # ========================      COMMAND      ===========================
    ######################### CONFIGURE INSTRUMENT #########################
    # ======================================================================

    def homing(self):
        """
        moves the motor to the 0 setpoint.
        """
        command = "X0-"
        r = self.send_command(command)
        return r
    
    # ======================================================================

    # ========================      COMMAND      ===========================
    ######################### CONFIGURE INSTRUMENT #########################
    # ======================================================================

    def stop_movement(self):
        """
        If the motor is moving, stops the movement. If a program is running, the program is not stopped.
        """
        command = "XS"
        r = self.send_command(command)
        return r

    # ======================================================================

    # ========================      COMMAND      ===========================
    ######################### CONFIGURE INSTRUMENT #########################
    # ======================================================================

    def stop_program(self):
        """
        If a program is running, stops the program. If the motor is running without a program, it does not stop the motor.
        """
        command = "QPE"
        r = self.send_command(command)
        return r

    # ======================================================================

    def system_status(self):
        command = "ST"
        r = self.send_command(command)
        return r

    def check_axis_standstill(self):
        command = "X=H"
        success, standstill = self.send_command(command)
        if success:
            if standstill == "E":
                return True
            elif standstill == "N":
                return False

    def decode_response(self, response):
        response_decoded = response.decode()
        success = response_decoded[1]
        message = response_decoded[2:-1]

        if success == self.ack:
            success = True
        else:
            success = False

        return success, message


    def send_command(self, command):

        telegram = f"{self.stx}0 {command}{self.etx}"

        w = self.inst.write(telegram.encode())    # Send message
        
        response = self.ReadUntil.read_until(expected = self.etx) # Read response
        success, message = self.decode_response(response)

        return success, message

    # ======================================================================

    # ========================     ATTRIBUTE    ============================
    ###########################  READ POSITION  ############################
    # ======================================================================

    def make_reading(self):
        """
        Returns a float with the current position of the motor.
        """
        return self.get_current_position()

    # ======================================================================