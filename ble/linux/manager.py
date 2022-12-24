# Standard imports
import asyncio
from typing import Final, Optional
import weakref

# Third-party imports
import gatt

# Local imports
from . device import Device
from .. exception import BluetoothConnectionError

DEFAULT_ADAPTATER: Final[str] = "hci0"

class DeviceManager(gatt.DeviceManager):

	def __init__(self) -> None:
		super().__init__(adapter_name=DEFAULT_ADAPTATER)
		self.__devices: dict[str, Device]  = {}
		self.__connected: Optional[Device] = None

		asyncio.get_event_loop().run_in_executor(None, self.run)
	
	def __del__(self) -> None:
		self.stop() # Stop the run loop, the executor will be stop

	def device_discovered(self, device: Device) -> None:
		"""Method call when a device is discovered

		Args:
			device (Device): Discovered device
		"""
		if device.mac_address not in self.__devices:
			self.__devices[device.mac_address] = device
			print("[%s] Discovered, alias = %s" % (device.mac_address, device.alias()))

	def connect(self, mac_address: str, force: bool) -> None:
		"""Connects to a peripheral

		Args:
			mac_address (str): MAC address of the peripheral to connect
			force (bool): if set, we try to connect directly to the peripheral, discovery is not necessary

		Raises:
			BluetoothConnectionError: A connection failed
		"""
		if force:
			self.__devices[mac_address] = Device(mac_address, self)

		if mac_address in self.__devices:
			self.__devices[mac_address].connect()

			# We want to disconnect as quick as the object is destroy, then we use the weakref callback
			self.__connected = weakref.ref(self.__devices[mac_address], self.__devices[mac_address].disconnect())
		else:
			raise BluetoothConnectionError(mac_address)
	
	def disconnect(self) -> None:
		self.__connected.disconnect()
		self.__connected = None
