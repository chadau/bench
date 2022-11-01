# Standard imports
from abc import ABC, abstractmethod
from typing import Final, Optional
import asyncio

# Local imports
from . import linux

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

class MockDriver(Driver):
	"""Mocks the BLE features for test purpose
	"""

	async def discovering(self, timeout: int = 5, filter: Optional[str] = None) -> None:

		async def discovery():
				await asyncio.sleep(0.2) # 0.1s to be close of the realtiming
				print("[5d:28:8a:4a:3f:73] Discovered, alias = 5D-28-8A-4A-3F-73")

		try:
			await asyncio.wait_for(discovery(), timeout)
		except asyncio.TimeoutError:
			pass


class LinuxDriver(Driver):
	"""Implements the BLE features for Linux operating system
	"""

	def __init__(self) -> None:
		self._manager = linux.DeviceManager()

	async def discovering(self, timeout: int = DISCOVERY_DEF_TIMEOUT, filter: Optional[str] = None) -> None:
		async def _timeout():
			await asyncio.sleep(timeout)
			self._manager.stop()

		self._manager.start_discovery([filter])
		asyncio.create_task(_timeout())
		await asyncio.get_event_loop().run_in_executor(None, self._manager.run)
