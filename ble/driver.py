# Standard imports
from abc import ABC, abstractmethod
from typing import Final, Optional
import asyncio

# Local imports
from . import linux
from . import exception

DISCOVERY_DEF_TIMEOUT: Final[int] = 5

class Driver(ABC):
	"""Implements the BLE core features
	"""

	@abstractmethod
	async def discovering(self, timeout: int, filter: Optional[str]) -> None:
		"""Scans around to find available devices

		Args:
			timeout (int, optional): Timeout before stop discovery. Defaults to 5.
			filter (Optional[str], optional): select only device with the UUID service indicated. Defaults to None.
		"""
		pass

	@abstractmethod
	async def connect(self, mac_address: str, force: bool) -> None:
		"""Connects to a peripheral

		Args:
			mac_address (str): MAC address of the peripheral to connect
			force (bool): if set, we try to connect directly to the peripheral, discovery is not necessary

		Raises:
		BluetoothConnectionError: connection failed
		"""
		pass

class MockDriver(Driver):
	"""Mocks the BLE features for test purpose
	"""
	def __init__(self) -> None:
		self.__discovered: list[str] = []
		self.__connected: Optional[str] = None

	async def discovering(self, timeout: int = DISCOVERY_DEF_TIMEOUT, filter: Optional[str] = None) -> None:

		async def discovery():
				await asyncio.sleep(0.2) # 0.1s to be close of the realtiming
				print("[fc:0f:e7:69:43:62] Discovered, alias = Bench")
				if "fc:0f:e7:69:43:62" not in self.__discovered:
					self.__discovered.append("fc:0f:e7:69:43:62")

		try:
			await asyncio.wait_for(discovery(), timeout)
		except asyncio.TimeoutError:
			pass
	
	async def connect(self, mac_address: str, force: bool) -> None:
		if force:
			self.__discovered = mac_address

		if mac_address not in self.__discovered:
			raise exception.BluetoothConnectionError(mac_address)

class LinuxDriver(Driver):
	"""Implements the BLE features for Linux operating system
	"""

	def __init__(self) -> None:
		self.__manager = linux.DeviceManager()
	
	def __del__(self) -> None:
		self.__manager.stop()

	async def discovering(self, timeout: int = DISCOVERY_DEF_TIMEOUT, filter: Optional[str] = None) -> None:
		self.__manager.start_discovery([filter])
		await asyncio.sleep(timeout)
		self.__manager.stop_discovery()
	
	async def connect(self, mac_address, force: bool) -> None:
		self.__manager.connect(mac_address, force)
