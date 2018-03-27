""" fauxmo_minimal.py - Fabricate.IO

	This is a demo python file showing what can be done with the debounce_handler.
	The handler prints True when you say "Alexa, device on" and False when you say
	"Alexa, device off".

	If you have two or more Echos, it only handles the one that hears you more clearly.
	You can have an Echo per room and not worry about your handlers triggering for
	those other rooms.

	The IP of the triggering Echo is also passed into the act() function, so you can
	do different things based on which Echo triggered the handler.
"""

import fauxmo
import logging
import time
import requests

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

class device_handler(debounce_handler):
	"""Publishes the on/off state requested,
	   and the IP address of the Echo making the request.
 
   """
	TRIGGERS = {
		 "light"			: 52001,
		 "light 2"			: 52002,
		 "corridor light"	: 52004,
		 "toilet led"		: 52005,
		 "security"			: 52006,
		 "bedroom light"	: 52003,
		 'bedroom light 2'	: 52007,
		 "kitchen light"	: 52008,
		 "toilet light"		: 52009,
		 "bathroom light"		: 52010,
	 }

def act(self, client_address, state, name):
	global r
	print("State", state, "on ", name, "from client @", client_address)
	if name == "light":
		if state:
			r = requests.get('http://192.168.1.100/control/bedroom-1/light/on')
		else:
			r = requests.get('http://192.168.1.100/control/bedroom-1/light/off')
	else:
		if name == "light 2":
			if state:
				r = requests.get('http://192.168.1.100/control/bedroom-2/light/on')
			else:
				r = requests.get('http://192.168.1.100/control/bedroom-2/light/off')
		else:
			if name == 'corridor light':
				if state:
					r = requests.get('http://192.168.1.100/control/corridor/light/on')
				else:
					r = requests.get('http://192.168.1.100/control/corridor/light/off')
			else:
				if name == 'toilet led':
					if state:
						r = requests.get('http://192.168.1.100/control/toilet/led/animate')
					else:
						r = requests.get('http://192.168.1.100/control/toilet/led/off')
				else:
					if name == 'security':
						if state:
							r = requests.get('http://192.168.1.100/control/security/on')
						else:
							r = requests.get('http://192.168.1.100/control/security/off')
					else:
						if name == 'bedroom light':
							if state:
								r = requests.get('http://192.168.1.100/control/room/light/on')
							else:
								r = requests.get('http://192.168.1.100/control/room/light/off')
						else:
							if name == 'bedroom light 2':
								if state:
									r = requests.get('http://192.168.1.100/control/room/light-2/on')
								else:
									r = requests.get('http://192.168.1.100/control/room/light-2/off')
							else:
								if name == 'kitchen light':
									if state:
										r = requests.get('http://192.168.1.100/control/kitchen/light/on')
									else:
										r = requests.get('http://192.168.1.100/control/kitchen/light/off')
								else:
									if name == 'toilet light':
										if state:
											r = requests.get('http://192.168.1.100/control/toilet/light/on')
										else:
											r = requests.get('http://192.168.1.100/control/toilet/light/off')
									else:
										if name == 'bathroom light':
											if state:
												r = requests.get('http://192.168.1.100/control/bathroom/light/on')
											else:
												r = requests.get('http://192.168.1.100/control/bathroom/light/off')
	print(r.status_code)
	return True

if __name__ == "__main__":
	# Startup the fauxmo server
	fauxmo.DEBUG = True
	p = fauxmo.poller()
	u = fauxmo.upnp_broadcast_responder()
	u.init_socket()
	p.add(u)

	# Register the device callback as a fauxmo handler
	d = device_handler()
	for trig, port in d.TRIGGERS.items():
		fauxmo.fauxmo(trig, u, p, None, port, d)

	# Loop and poll for incoming Echo requests
	logging.debug("Entering fauxmo polling loop")
	while True:
		try:
			# Allow time for a ctrl-c to stop the process
			p.poll(100)
			time.sleep(0.1)
		except Exception, e:
			logging.critical("Critical exception: " + str(e))
			break
