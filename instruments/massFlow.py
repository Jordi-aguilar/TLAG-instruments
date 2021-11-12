import serial
import numpy as np

from .utils import ReadUntil

class ElFlowSelect:

    def __init__(self, adapter, **settings):
        self.inst = self.connect_ElFlowSelect(adapter, **settings)

        self.ReadUntil = ReadUntil(self.inst)

        self.cmd_serialNumber = f":07{{node}}047163716300\r\n"
        self.cmd_changeSetpoint = f":06{{node}}010121{{setpoint}}\r\n"
        self.cmd_requestSetpoint = f":06{{node}}0401210121\r\n"
        self.cmd_requestMeasure = f":06{{node}}0401210120\r\n"

        self.oxygenair = 4.762

        self.total_flow = 10 # ml/min
        
        self.proportions = {
            "oxygen" : 1,
            "nitrogen" : 99
        }
        self.oxygen_partial_pressure = self.proportions["oxygen"] / 100

        self.serialNum2flow = {
            "M21211517B" : 10,
            "M21211517A" : 800,
            "M16202264B" : 600,
            "M15208965A" : 3000
        }
        self.flow2serialNum = {value : key for key, value in self.serialNum2flow.items()}

        # The node should be passed in hexadecimal format. Luckily, this nodes numbers are the same in decimal than in hexadecimal.
        self.nodes = ["03", "04", "05", "06"]

        # self.serialNum2node = self.get_serialNum2node()

        self.gas2othergas = {"oxygen" : "nitrogen",
                            "nirogen" : "oxigen"}
 
        self.main_gas = "oxygen"
        self.other_gas = self.gas2othergas[self.main_gas]

        self.set_gas2serialNum()

    # ======================================================================
    ##################### CONNECT TO THE DEVICE ############################
    # ======================================================================

    def connect_ElFlowSelect(self, device_name, **new_settings):
        settings = dict()
        settings['baudrate'] = 38400
        settings['bytesize'] = serial.EIGHTBITS
        settings['parity'] = serial.PARITY_NONE
        settings['stopbits'] = serial.STOPBITS_ONE
        settings['timeout'] = 2

        settings.update(new_settings)

        # Connect to device
        inst = serial.Serial(device_name, **settings)

        return inst

    # ======================================================================

    # ======================================================================
    ###################### INTERNAL FUNCTIONS ##############################
    # ======================================================================

    def get_serialNum2node(self):
        serial_numbers = []
        for node in self.nodes:
            try:
                serial_numbers.append(self.request_serial_number(node))
            except:
                serial_numbers.append(None)
        
        serialNum2node = {serial_number : node for serial_number, node in zip(serial_numbers, self.nodes) if serial_number is not None}

        return serialNum2node

    def set_gas2serialNum(self, main_gas_SN = None, other_gas_SN = None):
        if main_gas_SN is None or other_gas_SN is None:
            self.gas2serialNum = {
                self.main_gas : "M21211517B",
                self.other_gas : "M21211517A",
            }

        else:
            self.gas2serialNum = {
                self.main_gas : main_gas_SN,
                self.other_gas : other_gas_SN,
            }

        self.gas2flow = {key : self.serialNum2flow[value] for key, value in self.gas2serialNum.items()}
        # self.gas2node = {key : self.serialNum2node[value] for key, value in self.gas2serialNum.items()}

    def set_gas2flow(self, oxygen, nitrogen):
        main_gas_SN = self.flow2serialNum[oxygen]
        other_gas_SN = self.flow2serialNum[nitrogen]
        self.set_gas2serialNum(main_gas_SN, other_gas_SN)

    def send_command(self, cmd, r_type):

        w = self.inst.write(cmd.encode())
        r = self.ReadUntil.read_until()
        decoded_r = self.decode_response(r, r_type)

        return decoded_r

    def decode_response(self, r, r_type = "reading"):
        if r_type == "reading":
            value_hex = r[-6:-2]
            value_dec = int(value_hex, 16) / 32000

            return value_dec

        elif r_type == "serial_number":
            value_hex = r[-24:-4] # [-14:-4]
            value_string = bytes.fromhex(value_hex.decode()).decode('utf-8')

            return value_string

    def request_setpoint(self, node):
        cmd = self.cmd_requestSetpoint.format(node = node)

        r = self.send_command(cmd, "reading")

        return r

    # ======================================================================

    # ========================== ATTRIBUTE =================================
    ########################## Measure flow ################################
    # ======================================================================

    def request_measure(self, node):
        """
        Returns the measurement of the flow that is going trough a massflow

        Parameters
        ----------
        node : int
            the node of the massflow that we want to measure. Nodes usually are 3, 4, 5 or 6

        Returns
        -------
        r : float
            the measurement of the flow. A value between 0 and 100.

        """
        cmd = self.cmd_requestMeasure.format(node = node)

        r = self.send_command(cmd, "reading")

        return r

    # ======================================================================

    # ======================================================================
    ###################### INTERNAL FUNCTIONS ##############################
    # ======================================================================

    def request_serial_number(self, node):
        cmd = self.cmd_serialNumber.format(node = node)

        r = self.send_command(cmd, "serial_number")

        return r

    def change_setpoint(self, node, percentage):
        setpoint_hex = hex(int((percentage/100)*32000))[2:].upper().zfill(4)

        cmd = self.cmd_changeSetpoint.format(node = node, setpoint = setpoint_hex)

        r = self.send_command(cmd, None)

        return r

    def close_all_massflows(self):
        for _, node in self.serialNum2node.items():
            self.change_setpoint(node, 0)

    def calculate_setpoints(self, p, total_flow, gas):
        # Given the total flow and the percentage of the gases, calculate the setpoint (openings) of each massflow
        if gas == self.main_gas:
            p = p
        elif gas == self.other_gas:
            p = 100-p

        setpoint1 = (p*total_flow)/(self.gas2flow[self.main_gas])
        setpoint2 = 100*(total_flow - (setpoint1/100)*self.gas2flow[self.main_gas])/self.gas2flow[self.other_gas]

        return setpoint1, setpoint2

    def calculate_setpoints_maximize(self, p, gas):
        # Given the percentage of the gases, calculate the setpoint (openings) of each massflow at which the total_flow is maximized
        if gas == self.main_gas:
            p = p
        elif gas == self.other_gas:
            p = 100-p

        if p == 0:
            setpoint1 = 0
            setpoint2 = 100
            return setpoint1, setpoint2

        # try with setpoint1 full open
        setpoint1 = 100
        setpoint2 = 100*(self.gas2flow[self.main_gas]*(1-p/100))/(p/100*self.gas2flow[self.other_gas])
        if setpoint2 <= 100:
            return setpoint1, setpoint2

        # try with setpoint2 full open
        setpoint2 = 100
        setpoint1 = 100*(self.gas2flow[self.other_gas]*p/100)/(self.gas2flow[self.main_gas]*(1-p/100))
        return setpoint1, setpoint2

    def calculate_setpoints_minimize(self, p, gas):
        # Given the percentage of the gases, calculate the setpoint (openings) of each massflow at which the total_flow is minimized
        if gas == self.main_gas:
            p = p
        elif gas == self.other_gas:
            p = 100-p


        if p == 0:
            setpoint1 = 0
            setpoint2 = 4
            return setpoint1, setpoint2

        if p == 100:
            setpoint1 = 4
            setpoint2 = 0
            return setpoint1, setpoint2

        # try with setpoint1 almost closed
        setpoint1 = 4
        setpoint2 = 100*(0.04*self.gas2flow[self.main_gas]*(1-p/100))/(p/100*self.gas2flow[self.other_gas])
        # print("intermediate......", setpoint1, setpoint2)
        if setpoint2 >= 4:
            return setpoint1, setpoint2

        # try with setpoint2 full open
        setpoint2 = 4
        setpoint1 = 100*(0.04*self.gas2flow[self.other_gas]*p/100)/(self.gas2flow[self.main_gas]*(1-p/100))
        return setpoint1, setpoint2

    def set_gas_percentage(self, percentage, total_flow = None, gas = "oxygen"):
        if total_flow is not None:
            self.total_flow = total_flow
        
        other_gas = self.gas2othergas[gas]
        if percentage < 0 or percentage > 100:
            print("Incorrect percentage")
        else:
            setpoint1, setpoint2 = self.calculate_setpoints(percentage, self.total_flow, gas)
            print(setpoint1, setpoint2)
            
            if setpoint1 >= 4 and setpoint1 <= 100 and setpoint2 >= 4 and setpoint2 <= 100:
                self.change_setpoint(self.gas2node[self.main_gas], setpoint1)
                self.change_setpoint(self.gas2node[self.other_gas], setpoint2)

                self.proportions[gas] = percentage
                self.proportions[other_gas] = 100 - percentage
                self.oxygen_partial_pressure = self.proportions["oxygen"] / 100
                return setpoint1, setpoint2
            else:
                print("Invalid percentage with current flow...")
                return None, None

    # ======================================================================

    # ========================      COMMAND      ===========================
    ##################### SET GAS PARTIAL PRESSURE #########################
    # ======================================================================

    def set_gas_partial_pressure(self, partial_pressure, total_flow = None, total_pressure= 1, gas = "oxygen", air = True):
        """
        Adjust the massflow setpoints (openings) to meet the partial pressure desired at the given conditions.

        Parameters
        --------------
        partial_pressure : float
            The partial pressure in bars that we want to reach
        total_flow : float (optional)
            The new total flow that we want to reach. If it is not given, it will remain the default one in {self.total_flow}.
        total_pressure : float (optional)
            The total pressure in bars at which we are working. It is important for calculating the partial pressure of a gas. If not is not given, default is 1 bar.
        gas : str (optional)
            Either "oxygen" or "nitrogen". The specific gas that we want to change the partial pressure.
        air : bool (optional)
            True or False. If True, we will consider that we are working with air (20% of oxygen) instead of pure oxygen (100% of oxygen).
        """
        if air:
            self.set_gas_percentage(self.oxygenair*100*partial_pressure/total_pressure, total_flow, gas)
            self.oxygen_partial_pressure = total_pressure*((self.proportions["oxygen"]/self.oxygenair) / 100)
        else:
            self.set_gas_percentage(100*partial_pressure/total_pressure, total_flow, gas)
            self.oxygen_partial_pressure = total_pressure*(self.proportions["oxygen"] / 100)

    # ======================================================================

    # ======================================================================
    ###################### INTERNAL FUNCTIONS ##############################
    # ======================================================================
        
    def set_total_flow(self, total_flow):
        setpoint1, setpoint2 = self.calculate_setpoints(self.proportions[self.main_gas], total_flow, "oxygen")
        print(setpoint1, setpoint2)
        
        if setpoint1 >= 0 and setpoint1 <= 100 and setpoint2 >= 0 and setpoint2 <= 100:
            self.change_setpoint(self.gas2node[self.main_gas], setpoint1)
            self.change_setpoint(self.gas2node[self.other_gas], setpoint2)

            self.total_flow = total_flow
        else:
            print("Invalid total flow with current percentages...")
            return -1, -1


    def set_gas_percentage_maximize(self, percentage, gas = "oxygen", air = False):
        other_gas = self.gas2othergas[gas]
        if percentage < 0 or percentage > 100:
            print("Incorrect percentage")
        else:
            if air:
                constant = 4.762
            else:
                constant = 1
            setpoint1, setpoint2 = self.calculate_setpoints_maximize(percentage*constant, gas)
            print("Maximized setpoints: ", setpoint1, setpoint2)
            
            if setpoint1 >= 0 and setpoint1 <= 100 and setpoint2 >= 0 and setpoint2 <= 100:
                # self.change_setpoint(self.gas2node[self.main_gas], setpoint1)
                # self.change_setpoint(self.gas2node[self.other_gas], setpoint2)

                self.proportions[gas] = percentage
                self.proportions[other_gas] = 100 - percentage

                self.total_flow = setpoint1/100*self.gas2flow[self.main_gas] + setpoint2/100*self.gas2flow[self.other_gas]
            else:
                print("Invalid percentage with current flow...")

    def set_gas_partial_pressure_maximize(self, partial_pressure, total_pressure= 1, gas = "oxygen", air = False):
        self.set_gas_percentage_maximize(100*partial_pressure/total_pressure, gas, air)
        self.oxygen_partial_pressure = total_pressure*((self.proportions["oxygen"]/self.oxygenair) / 100)

    def set_gas_percentage_minimize(self, percentage, gas = "oxygen", air = False):
        other_gas = self.gas2othergas[gas]
        if percentage < 0 or percentage > 100:
            print("Incorrect percentage")
        else:
            if air:
                constant = 4.762
            else:
                constant = 1
            setpoint1, setpoint2 = self.calculate_setpoints_minimize(percentage*constant, gas)
            print("Minimized setpoints: ", setpoint1, setpoint2)
            
            if setpoint1 >= 0 and setpoint1 <= 100 and setpoint2 >= 0 and setpoint2 <= 100:
                # self.change_setpoint(self.gas2node[self.main_gas], setpoint1)
                # self.change_setpoint(self.gas2node[self.other_gas], setpoint2)

                self.proportions[gas] = percentage
                self.proportions[other_gas] = 100 - percentage

                self.total_flow = setpoint1/100*self.gas2flow[self.main_gas] + setpoint2/100*self.gas2flow[self.other_gas]
            else:
                print("Invalid percentage with current flow...")


    def set_gas_partial_pressure_minimize(self, partial_pressure, total_pressure= 1, gas = "oxygen", air = False):
        self.set_gas_percentage_minimize(100*partial_pressure/total_pressure, gas, air)
        self.oxygen_partial_pressure = total_pressure*((self.proportions["oxygen"]/self.oxygenair) / 100)


    def find_total_pressure_limits(self, partial_pressure, total_flow, gas, air):
        other_gas = self.gas2othergas[gas]
        p1x = 0.04
        p1y = (total_flow - p1x*self.gas2flow[self.main_gas]) / self.gas2flow[self.other_gas]

        p2x = 1
        p2y = (total_flow - p2x*self.gas2flow[self.main_gas]) / self.gas2flow[self.other_gas]

        p3y = 0.04
        p3x = (total_flow - p3y*self.gas2flow[self.other_gas]) / self.gas2flow[self.main_gas]

        p4y = 1
        p4x = (total_flow - p4y*self.gas2flow[self.other_gas]) / self.gas2flow[self.main_gas]

        p1_valid = p1y <= 1 and p1y >= 0.04
        p2_valid = p2y <= 1 and p2y >= 0.04
        p3_valid = p3x <= 1 and p3x >= 0.04
        p4_valid = p4x <= 1 and p4x >= 0.04

        candidates = [(p1x, p1y), (p2x, p2y), (p3x, p3y), (p4x, p4y)]
        evaluations = [p1_valid, p2_valid, p3_valid, p4_valid]
        
        valid_points = np.where(evaluations)[0]

        print(candidates)
        print(len(valid_points))
        print(valid_points)

        if len(valid_points) >= 2:
            p1_s0 = candidates[valid_points[0]][0]
            p2_s0 = candidates[valid_points[1]][0]

            min_s0 = min(p1_s0, p2_s0)
            max_s0 = max(p1_s0, p2_s0)
            print(min_s0, max_s0)
            max_pt = partial_pressure*total_flow/(0.21*min_s0*self.gas2flow[self.main_gas])
            min_pt = partial_pressure*total_flow/(0.21*max_s0*self.gas2flow[self.main_gas])

            return min_pt, max_pt

        return None, None

    # ======================================================================
            