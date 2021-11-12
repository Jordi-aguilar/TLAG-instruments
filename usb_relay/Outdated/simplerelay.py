import simpleusbrelay # requires pyusb

import time


for i in range(5):

	# turn on relay 2
	relaycontroller= simpleusbrelay.simpleusbrelay(Vendor = int("16c0", 16) , Product = int("05df", 16) )
	relaycontroller.array_on(2)
	time.sleep(.1)

	# turn off relay 2
	relaycontroller= simpleusbrelay.simpleusbrelay(Vendor = int("16c0", 16) , Product = int("05df", 16) )
	relaycontroller.array_off(2)
	time.sleep(.1)

	# turn on all
	relaycontroller= simpleusbrelay.simpleusbrelay(Vendor = int("16c0", 16) , Product = int("05df", 16) )
	relaycontroller.array_on("all")
	time.sleep(.1)

	# turn off all
	relaycontroller= simpleusbrelay.simpleusbrelay(Vendor = int("16c0", 16) , Product = int("05df", 16) )
	relaycontroller.array_off("all")
	time.sleep(.1)