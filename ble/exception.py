class BluetoothError(Exception):
	pass

class BluetoothConnectionError(BluetoothError):

	def __init__(self, mac_address: str) -> None:
		self.__mac_address = mac_address
	
	@property
	def mac_address(self):
		return self.__mac_address