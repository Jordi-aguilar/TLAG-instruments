import pyvisa

from .utils import ReadUntil

class LEYSPECView100S:
    def __init__(self, adapter, **settings):
        self.inst = self.connect_LEYSPECView100S(adapter, **settings)

        self.ReadUntil = ReadUntil(self.inst)

        self.cr = '\r'   # Carriage Return. chr(13)
        self.lf = '\n'   # Line Feed. chr(10)

    # ======================================================================
    ##################### CONNECT TO THE DEVICE ############################
    # ======================================================================

    def connect_LEYSPECView100S(self, device_name, **new_settings):
        settings = dict()
        settings['write_termination'] = ""
        settings['read_termination'] = ""

        settings.update(new_settings)

        # Connect to device
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(device_name, **settings)

        return inst

    # ======================================================================

    # ======================================================================
    ###################### INTERNAL FUNCTIONS ##############################
    # ======================================================================

    def decode_string(self, encoded_string):
        new_str = ""

        for c in encoded_string:
            new_str += chr(c)

        return new_str

    def decode_response(self, response):
        response_decoded = self.decode_string(response)
        response_decoded_no_cs = response_decoded[:-4]
        response_fields = response_decoded_no_cs.split(',')
        response_data = response_fields[1:]

        try:
            data_matrix = response_data.reshape((-1, 3))

            data = {r[0] : tuple(r[1:]) for r in data_matrix}

            return data

        except:
            return response_data

    def send_command(self):

        # Unique command. This is the only command accepted.
        command = "DA1B6" + self.cr + self.lf

        w = self.inst.write(command)    # Send message

        response = self.ReadUntil.read_until(expected = self.lf) # Read response
        print("Response = ", response)
        data = self.decode_response(response)

        return data

    # ======================================================================

    # ========================   ATTRIBUTE    ==============================
    # #################### READ PARTIAL PRESSURES ##########################
    # ======================================================================

    def make_reading(self):
        """
        Returns a dictionary.
        The key is the mass number. (For example 16 is oxygen)
        The value is a tuple with two elements.
            First element is the partial pressue
            Second element is the setpoint Alarm
        """
        return self.send_command()

    # ======================================================================
