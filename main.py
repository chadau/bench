import asyncio
from threading import Thread
import time
import ble
from ble.linux.device import Device
from ble.linux.manager import DeviceManager

def event_loop(loop) -> None:
	asyncio.set_event_loop(loop)
	loop.run_forever()

async def main():
	manager = DeviceManager()
	loop = asyncio.new_event_loop()
	thread = Thread(target=manager.run, name="BluetoothThread")
	thread.start()

	device = Device("fc:0f:e7:69:43:62", manager)
	device.connect()
	time.sleep(2)
	device.disconnect()
	manager.start_discovery()
	time.sleep(2)
	manager.stop_discovery()

if __name__ == "__main__":
	asyncio.run(main())