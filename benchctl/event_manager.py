# Local imports
import asyncio
import concurrent.futures
import threading
from typing import Coroutine

class Singleton(type):
	__instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in Singleton.__instances:
			Singleton.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return Singleton.__instances[cls]

class EventManager(metaclass=Singleton):

	def __init__(self) -> None:
		self.__loop = asyncio.new_event_loop()
		self.__thread = threading.Thread(target=self.__event_loop, name="EventThread")
		self.__thread.start()
	
	def stop(self):
		self.__loop.call_soon_threadsafe(self.__loop.stop)
		self.__thread.join()
		

	def __event_loop(self) -> None:
		asyncio.set_event_loop(self.__loop)
		self.__loop.run_forever()
	
	def add_event(self, event: Coroutine) -> concurrent.futures.Future:
		"""Launchs a coroutine in the event thread

		Args:
			event (Coroutine): Couroutine to launch

		Returns:
			concurrent.futures.Future: Future concurent object
		"""
		return asyncio.run_coroutine_threadsafe(event, self.__loop)