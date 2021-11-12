from pymeasure.instruments.keithley import Keithley2450 as Keithley2450_pymeasure

class Keithley2450(Keithley2450_pymeasure):
    def __init__(self, device, **kwargs):
        super().__init__(device, **kwargs)

    # ========================      COMMAND      ===========================
    ######################### CONFIGURE INSTRUMENT #########################
    # ======================================================================

    def prepare_resistance_measurement(self, current):
        """
        (Adaptation of the example found in https://pymeasure.readthedocs.io/en/latest/api/instruments/keithley/keithley2450.html)

        Configures desired current in Amperes and enables the current trough the wires.
        Changes the unit of measurement to Ohms.

        Parameters
        -----------
        current : float
            The desired current in Amperes that is going to be sourced.
        """
        self.apply_current()                # Sets up to source current
        self.source_current_range = 10e-3   # Sets the source current range to 10 mA
        self.compliance_voltage = 10        # Sets the compliance voltage to 10 V
        self.source_current = 0             # Sets the source current to 0 mA
        self.enable_source()                # Enables the source output

        self.measure_voltage()              # Sets up to measure voltage
        self.write("SENS:VOLT:UNIT OHM;")   # Change unit of measurement to OHM (resistance)

        self.source_current = current       # Ramps the current to {current} A

    # ======================================================================


    # ========================     ATTRIBUTE    ============================
    ######################### READ RESISTANCE ##############################
    # ======================================================================

    def make_reading(self):
        """
        Returns a float. Measurement of resitance in Ohms.
        """
        return self.voltage                 # Returns de voltage in the selected unit

    # ======================================================================
