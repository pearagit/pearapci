import re
import click
import typer
from typing import Annotated, Callable, Dict, List, Optional

from pearapci.utils import get_device


def parse_pid(pid: str):
    match = re.match(r"([0-9a-fA-F]{4}):([0-9a-fA-F]{4})", pid)
    if not match:
        raise typer.BadParameter("PID must be in the format vvvv:dddd")
    device = get_device(device=pid)
    if device is None:
        raise typer.BadParameter(f"No device with pid: {pid}")
    return device


def parse_slot(slot: str):
    match = re.match(r"\b([0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}.\d{1})", slot)
    if not match:
        raise typer.BadParameter("Slot must be in the format dddd:dd:d.d")
    device = get_device(slot=slot)
    if device is None:
        raise typer.BadParameter(f"No devices with slot: {slot}")
    return device


class DeviceParser(click.ParamType):
    name = "Device"
    parsers: Dict[str, Callable[[str], str]] = {"slots": parse_slot, "pids": parse_pid}

    def convert(self, value, param, _):
        return self.parsers[param.name](value)
