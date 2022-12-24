# Standard imports
from typing import List

# Local imports
from . driver import *


class Client:
	def __init__(self) -> None:
		self.__driver: Driver = LinuxDriver()

	async def discovering(self, timeout: int = DISCOVERY_DEF_TIMEOUT, filter: Optional[str] = None) -> None:
		"""Scans around to find available devices

		Args:
			timeout (int, optional): Timeout before stop discovery. Defaults to 5.
			filter (Optional[str], optional): select only device with the UUID service indicated. Defaults to None.
		"""
		await self.__driver.discovering(timeout, filter)
	
	async def connect(self, mac_address: str, force: bool):
		await self.__driver.connect(mac_address, force)
