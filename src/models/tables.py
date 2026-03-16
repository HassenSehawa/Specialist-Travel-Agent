"""
Data models.
Each table stores records internally as a list of dictionaries and
persists data to the file system as JSONL (JSON Lines).
"""
import json
import os
from datetime import datetime
from typing import Union


class BaseTable:
    """Shared CRUD and persistence logic for all record tables."""

    record_type: str = ""
    fields: list[str] = []  # editable fields, excludes auto-generated id and type

    def __init__(self):
        self.records: list[dict] = []

    def _next_id(self) -> int:
        """Returns the next available ID (max existing ID + 1)."""
        if not self.records:
            return 1
        return max(r["id"] for r in self.records) + 1

    def add_record(self, **kwargs) -> dict:
        record = {"id": self._next_id(), "type": self.record_type, **kwargs}
        self.records.append(record)
        return record

    def get_record(self, record_id: int) -> dict | None:
        for record in self.records:
            if record["id"] == record_id:
                return record
        return None

    def update_record(self, record_id: int, **kwargs) -> bool:
        record = self.get_record(record_id)
        if record is None:
            return False
        for key, value in kwargs.items():
            if key in record:
                record[key] = value
        return True

    def delete_record(self, record_id: int) -> bool:
        for i, record in enumerate(self.records):
            if record["id"] == record_id:
                self.records.pop(i)
                return True
        return False

    def find_records(self, field: str, value: Union[int, str]) -> list[dict]:
        """
        Searches records by field value.
        - int: exact match
        - str: case-insensitive starts-with match
        """
        results = []
        for record in self.records:
            if field not in record:
                continue
            if isinstance(value, int):
                if record[field] == value:
                    results.append(record)
            elif isinstance(value, str):
                if str(record[field]).lower().startswith(value.lower()):
                    results.append(record)
        return results

    def save(self, path: str):
        """Saves all records to a JSONL file."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            for record in self.records:
                f.write(json.dumps(record) + "\n")

    def load(self, path: str):
        """Loads records from a JSONL file. Does nothing if file doesn't exist."""
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            self.records = [json.loads(line) for line in f if line.strip()]


class ClientTable(BaseTable):
    record_type = "Client"
    fields = ["name", "address_line_1", "address_line_2", "address_line_3",
              "city", "state", "zip_code", "country", "phone_number"]

    def add_record(self, name: str, address_line_1: str, address_line_2: str,
                   address_line_3: str, city: str, state: str, zip_code: str,
                   country: str, phone_number: str) -> dict:
        return super().add_record(
            name=name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            address_line_3=address_line_3,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            phone_number=phone_number,
        )


class AirlineTable(BaseTable):
    record_type = "Airline"
    fields = ["company_name"]

    def add_record(self, company_name: str) -> dict:
        return super().add_record(company_name=company_name)


class FlightTable(BaseTable):
    record_type = "Flight"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    fields = ["airline_id", "date", "start_city", "end_city"]

    def add_record(self, airline_id: int, date: str, start_city: str, end_city: str) -> dict:
        datetime.strptime(date, self.DATE_FORMAT)  # validate date format
        return super().add_record(
            airline_id=airline_id,
            date=date,
            start_city=start_city,
            end_city=end_city,
        )
