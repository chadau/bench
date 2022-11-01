import asyncio
import ble

async def main():
	client = ble.Client()
	await client._driver.discovering()

if __name__ == "__main__":
	asyncio.run(main())