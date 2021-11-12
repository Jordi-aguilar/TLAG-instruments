from instruments import FujiTemperatureController


instr = FujiTemperatureController("COM4")
print(instr.make_reading())
