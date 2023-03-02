import ble

class Client(ble.Client):

	def __init__(self):
		super().__init__()
		self.set_callback(ble.Driver.Event.DEVICE_DISCOVERED, lambda info: print(f"[{info.mac_address}] alias = {info.alias}"))
		self.set_callback(ble.Driver.Event.DEVICE_CONNECTED , lambda info: print(f"[{info.mac_address}] Connected"))
		self.set_callback(ble.Driver.Event.DEVICE_DISCONNECTED, lambda info: print(f"[{info.mac_address}] Disconnected"))