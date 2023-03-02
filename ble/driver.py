# Standard imports
from abc import ABC, abstractmethod
from typing import Final, Optional
import asyncio
import enum

# Local imports
from . import exception
from . info import DeviceInfo

DISCOVERY_DEF_TIMEOUT: Final[int] = 5

class Driver(ABC):
	"""Implements the BLE core features
	"""

	@enum.unique
	class Event(enum.IntEnum):
		"""Driver event
		"""
		DEVICE_DISCOVERED   = 0
		DEVICE_CONNECTED    = enum.auto()
		DEVICE_DISCONNECTED = enum.auto()

	class Callback():
		"""Subclass to manage callback for driver event
		"""
		__callbacks: 'dict[Driver.Event, function]' = {}

		@classmethod
		def set(cls, id: 'Driver.Event', cb: 'function') -> None:
			"""Sets a callback

			Args:
				id (Driver.Event): Driver event id
				cb (function): function to call for the event
			"""
			cls.__callbacks[id] = cb
		
		@classmethod
		def unset(cls, id: 'Driver.Event') -> None:
			"""Unsets a callback attached to an id

			Args:
				id (Driver.Event): Driver event id
			"""
			del cls.__callbacks[id]
		
		@classmethod
		def is_set(cls, id: 'Driver.Event') -> bool:
			"""Checks if a callback is set for an id

			Args:
				id (Driver.Event): Driver event id

			Returns:
				bool: True if a callback is attached to an event, false otherwise
			"""
			return id in cls.__callbacks
		
		@classmethod
		def _call(cls, id: 'Driver.Event', info: DeviceInfo) -> None:
			"""Call the callback attached to an event, only used internally in SDK

			Args:
				id (Driver.Event): Driver event id
				info (DeviceInfo): Infomation about a device
			"""
			if id in cls.__callbacks:
				cls.__callbacks[id](info)

	def set_callback(self, event: Event, cb: "function"):
		"""Sets a callback on an event

		Args:
			event (Event): Event id
			cb (function): function to call when event occur
		"""
		Driver.Callback.set(event, cb)

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

	@abstractmethod
	async def disconnect(self) -> None:
		"""Disconnects the peripheral
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
				if "fc:0f:e7:69:43:62" not in self.__discovered:
					self.__discovered.append("fc:0f:e7:69:43:62")
					self.Callback._call(Driver.Event.DEVICE_DISCOVERED, DeviceInfo("fc:0f:e7:69:43:62", "Bench"))

		try:
			await asyncio.wait_for(discovery(), timeout)
		except asyncio.TimeoutError:
			pass
	
	async def connect(self, mac_address: str, force: bool) -> None:
		if force:
			self.__discovered = mac_address
			self.Callback._call(Driver.Event.DEVICE_CONNECTED, DeviceInfo(mac_address, "Bench"))

		if mac_address not in self.__discovered:
			raise exception.BluetoothConnectionError(mac_address)
	
	async def disconnect(self) -> None:
		self.Callback._call(Driver.Event.DEVICE_DISCONNECTED, DeviceInfo(self.__connected, "Bench"))
		self.__connected = None
