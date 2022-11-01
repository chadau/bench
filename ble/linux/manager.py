# Standard imports
from typing import Final

# Third-party imports
import gatt

# Local imports
from . device import Device

DEFAULT_ADAPTATER: Final[str] = "hci0"

class DeviceManager(gatt.DeviceManager):

	def __init__(self) -> None:
		super().__init__(adapter_name=DEFAULT_ADAPTATER)
		self.__devices: dict[str, Device] = {}

	def device_discovered(self, device: Device):
		if device.mac_address not in self.__devices:
			self.__devices[device.mac_address] = device
			print("[%s] Discovered, alias = %s" % (device.mac_address, device.alias()))

