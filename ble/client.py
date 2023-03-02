# Standard imports
from typing import Optional

# Local imports
from . driver import Driver, MockDriver, DISCOVERY_DEF_TIMEOUT
from . import linux

class Client:
	def __init__(self) -> None:
		self.__driver: Driver = MockDriver()

	def set_callback(self, event: Driver.Event, cb: 'function'):
		self.__driver.set_callback(event, cb)

	async def discovering(self, timeout: int = DISCOVERY_DEF_TIMEOUT, filter: Optional[str] = None) -> None:
		"""Scans around to find available devices

		Args:
			timeout (int, optional): Timeout before stop discovery. Defaults to 5.
			filter (Optional[str], optional): select only device with the UUID service indicated. Defaults to None.
		"""
		await self.__driver.discovering(timeout, filter)
	
	async def connect(self, mac_address: str, force: bool):
		"""Connects to a device

		Args:
			mac_address (str): MAC address of the device to connect
			force (bool): if set, we try to connect directly to the device, discovery is not necessary

		Raises:
		BluetoothConnectionError: connection failed
		"""
		await self.__driver.connect(mac_address, force)
