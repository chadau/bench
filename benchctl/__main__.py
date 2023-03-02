#!/usr/bin/env python3

# Standard imports

# Third-party imports
import typer
from bench.gatt import BENCH_GATT_SERVICE_UUID
from rich.progress import Progress, SpinnerColumn, TextColumn

# Local imports
from . event_manager import EventManager
from . client        import Client

app = typer.Typer()

@app.command()
def list():
	with Progress(
		SpinnerColumn(),
		TextColumn("[progress.description]{task.description}"),
		transient=True,
	) as progress:
		progress.add_task(description="Discovering...", total=None)
		EventManager().add_event(Client().discovering(filter=BENCH_GATT_SERVICE_UUID)).result()
		EventManager().stop()


@app.command()
def connect(mac_address: str):
	with Progress(
		SpinnerColumn(),
		TextColumn("[progress.description]{task.description}"),
		transient=True,
	) as progress:
		progress.add_task(description="Connecting...", total=None)
		EventManager().add_event(Client().connect(mac_address, force=True)).result()
		EventManager().stop()

def main():
	app()

if __name__ == '__main__':
	main()