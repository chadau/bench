#!/usr/bin/env python3

# Standard imports
from multiprocessing import Event

# Third-party imports
import typer
import ble
from bench.gatt import BENCH_GATT_SERVICE_UUID
from rich.progress import Progress, SpinnerColumn, TextColumn

# Local imports
from . event_manager import EventManager

app = typer.Typer()

@app.command()
def list():
	with Progress(
		SpinnerColumn(),
		TextColumn("[progress.description]{task.description}"),
		transient=True,
	) as progress:
		progress.add_task(description="Discovering...", total=None)
		EventManager().add_event(ble.Client().discovering(filter=BENCH_GATT_SERVICE_UUID)).result()
		EventManager().stop()


@app.command()
def connect(mac_address: str):
	pass

def main():
	app()

if __name__ == '__main__':
	main()