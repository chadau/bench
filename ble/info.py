
class Info(type):
	pass

class DeviceInfo(metaclass=Info):

	def __init__(self, mac_address: str, alias: str) -> None:
		self.__mac_address = mac_address
		self.__alias = alias
	
	@property
	def mac_address(self):
		return self.__mac_address
	
	@property
	def alias(self):
		return self.__alias