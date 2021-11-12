import serial

from .utils import ReadUntil

class GraphixTwo:

    def __init__(self, adapter, **settings):
        self.inst = self.connect_GraphixTwo(adapter, **settings)

        self.ReadUntil = ReadUntil(self.inst)

        self.eot = '\x04'   # End Of Transmission. chr(4)
        self.ack = '\x06'   # Acknowledge. chr(6)
        self.so = '\x0e'    # Shift Out. chr(14)
        self.si = '\x0f'    # Shift In. chr(15)

    # ======================================================================
    ##################### CONNECT TO THE DEVICE ############################
    # ======================================================================

    def connect_GraphixTwo(self, device_name, **new_settings):
        settings = dict()
        settings['baudrate'] = 9600
        settings['bytesize'] = serial.EIGHTBITS
        settings['parity'] = serial.PARITY_NONE
        settings['stopbits'] = serial.STOPBITS_ONE
        settings['timeout'] = 10

        settings.update(new_settings)

        # Connect to device
        inst = serial.Serial(device_name, **settings)

        return inst

    # ======================================================================

    # ======================================================================
    ###################### INTERNAL FUNCTIONS ##############################
    # ======================================================================

    def calculate_CRC(self, command):
        byte_sum = 0

        for c in command:
            byte_sum += ord(c)

        crc_char = 255 - (byte_sum % 256)

        if crc_char < 32:
            crc_char += 32

        return chr(crc_char)

    def create_command_GraphixTwo(self, parameter_group, parameter_number, mode, value = ''):
        parameter_group = str(parameter_group)
        parameter_number = str(parameter_number)

        if mode == "write":
            command = self.so + parameter_group + ';' + parameter_number + ';' + value + ' '

        elif mode == "read":
            command = self.si + parameter_group + ';' + parameter_number

        crc = self.calculate_CRC(command)

        command = command + crc + self.eot

        return command

    def decode_string(self, encoded_string):
        new_str = ""

        for c in encoded_string:
            new_str += chr(c)

        return new_str


    def decode_response(self, response):
        response_decoded = self.decode_string(response)
        success = response_decoded[0]
        message = response_decoded[1:-2]

        if success == self.ack:
            success = True
        else:
            success = False

        return success, message


    def send_command(self, parameter_group, parameter_number, mode, value = ''):

        command = self.create_command_GraphixTwo(parameter_group, parameter_number, mode)

        w = self.inst.write(command.encode())    # Send message
        
        response = self.ReadUntil.read_until(expected = self.eot) # Read response
        success, message = self.decode_response(response)

        return success, message

    def read_pressure(self, channel = "all"):
        mode = "read"
        p_number = 29         # Read pressure

        if channel == "all":
            p_group_1 = 1
            success1, pressure1 = self.send_command(p_group_1, p_number, mode)
            p_group_2 = 2
            success2, pressure2 = self.send_command(p_group_2, p_number, mode)

            return pressure1, pressure2

        else:
            success1, pressure = self.send_command(channel, p_number, mode)

            return pressure

    # ======================================================================


    # ========================     ATTRIBUTE    ============================
    ###########################  READ PRESSURE  ############################
    # ======================================================================

    def make_reading(self):
        """
        Returns a tuple of two elements.
        First element is the pressure of channel 1.
        Second element is the pressure of channel 2.
        The unit is the same that is configured in the device. Default: mbar
        """
        return self.read_pressure()

    # ======================================================================



