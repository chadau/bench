#Standard imports
from typing import Optional
import asyncio

# Local imports
from .. driver  import Driver, DISCOVERY_DEF_TIMEOUT
from .  manager import DeviceManager
from .  device  import Device

class LinuxDriver(Driver):
	"""Implements the BLE features for Linux operating system
	"""

	def __init__(self) -> None:
		self.__manager = DeviceManager()

	def __del__(self) -> None:
		self.__manager.stop()

	async def discovering(self, timeout: int = DISCOVERY_DEF_TIMEOUT, filter: Optional[str] = None) -> None:
		self.__manager.start_discovery([filter])
		await asyncio.sleep(timeout)
		self.__manager.stop_discovery()

	async def connect(self, mac_address, force: bool) -> None:
		self.__manager.connect(mac_address, force)
	
	async def disconnect(self) -> None:
		self.__manager.disconnect()