from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

ConnectionDetails = Dict[str, Optional[str]]
ConnectionOptions = Dict[str, str]


@dataclass(frozen=True)
class Connection:
    name: str
    uuid: str
    conn_type: str
    timestamp: int
    timestamp_real: str
    autoconnect: bool
    autoconnect_priority: int
    readonly: bool
    dbus_path: str
    active: bool
    device: str
    state: str
    active_path: str
    slave: str
    filename: str

    def to_json(self):
        return self.__dict__

    @classmethod
    def fromList(cls, fields: List[str]) -> Connection:
        to_none = lambda s: s if s != '--' else None
        to_bool = lambda s: (s == 'yes') if s is not None else None 
        to_int  = lambda s: int(s)       if s is not None else None

        fields = [to_none(f) for f in fields]
        name, uuid, conn_type, timestamp, timestamp_real, autoconnect, autoconnect_priority, readonly, dbus_path, active, device, state, active_path, slave, filename = fields

        timestamp = to_int(timestamp)
        autoconnect_priority = to_int(autoconnect_priority)

        autoconnect = to_bool(autoconnect)
        readonly = to_bool(readonly)
        active = to_bool(active)

        return Connection(name, uuid, conn_type, timestamp, timestamp_real, autoconnect, autoconnect_priority, readonly, dbus_path, active, device, state, active_path, slave, filename)

    @classmethod
    def parse(cls, text: str) -> Connection:
        return parseAll(text)[0]

    @classmethod
    def parseAll(cls, text: str) -> List[Connection]:
        reader = csv.reader(io.StringIO(text), delimiter=':', escapechar='\\')
        return [Connection.fromList(row) for row in reader]

