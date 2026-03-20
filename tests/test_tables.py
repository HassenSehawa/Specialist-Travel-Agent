"""
Unit tests for models/tables.py
Tester: Golda Masibo
Covers: Client, Airline, and Flight record validation,
        CRUD outcomes, search edge cases, and file persistence.
"""
import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.tables import ClientTable, AirlineTable, FlightTable


# ── Helper ──────────────────────────────────────────────────────────────────

def make_client(**overrides):
    defaults = dict(
        name="Jane Doe", address_line_1="123 Main St", address_line_2="",
        address_line_3="", city="Nairobi", state="", zip_code="00100",
        country="Kenya", phone_number="+254700000000"
    )
    defaults.update(overrides)
    return defaults


# ── Client Tests ─────────────────────────────────────────────────────────────

class TestClientTable(unittest.TestCase):

    def setUp(self):
        self.table = ClientTable()

    # Valid add
    def test_add_client_valid(self):
        record = self.table.add_record(**make_client())
        self.assertEqual(len(self.table.records), 1)
        self.assertEqual(record["name"], "Jane Doe")
        self.assertEqual(record["type"], "Client")

    # Empty name rejected
    def test_add_client_empty_name(self):
        with self.assertRaises(ValueError):
            self.table.add_record(**make_client(name=""))

    # Empty city rejected
    def test_add_client_empty_city(self):
        with self.assertRaises(ValueError):
            self.table.add_record(**make_client(city=""))

    # Empty country rejected
    def test_add_client_empty_country(self):
        with self.assertRaises(ValueError):
            self.table.add_record(**make_client(country=""))

    # Invalid phone rejected
    def test_add_client_invalid_phone(self):
        with self.assertRaises(ValueError):
            self.table.add_record(**make_client(phone_number="not-a-number"))

    # Update changes value
    def test_update_client(self):
        self.table.add_record(**make_client())
        self.table.update_record(1, **make_client(name="Updated Name"))
        self.assertEqual(self.table.get_record(1)["name"], "Updated Name")

    # Delete removes record
    def test_delete_client(self):
        self.table.add_record(**make_client())
        result = self.table.delete_record(1)
        self.assertTrue(result)
        self.assertIsNone(self.table.get_record(1))

    # Delete non-existent returns False
    def test_delete_nonexistent_client(self):
        result = self.table.delete_record(999)
        self.assertFalse(result)

    # Search returns correct record
    def test_search_client_by_name(self):
        self.table.add_record(**make_client(name="Alice"))
        results = self.table.find_records("name", "Ali")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice")

    # Search with no match returns empty list
    def test_search_client_no_match(self):
        self.table.add_record(**make_client())
        results = self.table.find_records("name", "ZZZZZ")
        self.assertEqual(results, [])


# ── Airline Tests ─────────────────────────────────────────────────────────────

class TestAirlineTable(unittest.TestCase):

    def setUp(self):
        self.table = AirlineTable()

    # Valid add
    def test_add_airline_valid(self):
        record = self.table.add_record(company_name="Kenya Airways")
        self.assertEqual(record["company_name"], "Kenya Airways")
        self.assertEqual(record["type"], "Airline")

    # Empty name rejected
    def test_add_airline_empty_name(self):
        with self.assertRaises(ValueError):
            self.table.add_record(company_name="")

    # Update changes value
    def test_update_airline(self):
        self.table.add_record(company_name="Old Name")
        self.table.update_record(1, company_name="New Name")
        self.assertEqual(self.table.get_record(1)["company_name"], "New Name")

    # Delete removes record
    def test_delete_airline(self):
        self.table.add_record(company_name="Kenya Airways")
        self.table.delete_record(1)
        self.assertIsNone(self.table.get_record(1))


# ── Flight Tests ──────────────────────────────────────────────────────────────

class TestFlightTable(unittest.TestCase):

    def setUp(self):
        self.table = FlightTable()

    # Valid add
    def test_add_flight_valid(self):
        record = self.table.add_record(
            airline_id=1, date="2025-06-01",
            start_city="Nairobi", end_city="London"
        )
        self.assertEqual(record["start_city"], "Nairobi")
        self.assertEqual(record["type"], "Flight")

    # Invalid date format rejected
    def test_add_flight_invalid_date(self):
        with self.assertRaises(ValueError):
            self.table.add_record(
                airline_id=1, date="01-06-2025",
                start_city="Nairobi", end_city="London"
            )

    # Non-integer airline_id rejected
    def test_add_flight_invalid_airline_id(self):
        with self.assertRaises(ValueError):
            self.table.add_record(
                airline_id="one", date="2025-06-01",
                start_city="Nairobi", end_city="London"
            )

    # Empty start city rejected
    def test_add_flight_empty_start_city(self):
        with self.assertRaises(ValueError):
            self.table.add_record(
                airline_id=1, date="2025-06-01",
                start_city="", end_city="London"
            )

    # Empty end city rejected
    def test_add_flight_empty_end_city(self):
        with self.assertRaises(ValueError):
            self.table.add_record(
                airline_id=1, date="2025-06-01",
                start_city="Nairobi", end_city=""
            )

    # Delete removes record
    def test_delete_flight(self):
        self.table.add_record(
            airline_id=1, date="2025-06-01",
            start_city="Nairobi", end_city="London"
        )
        self.table.delete_record(1)
        self.assertIsNone(self.table.get_record(1))


# ── File Persistence Tests ────────────────────────────────────────────────────

class TestFilePersistence(unittest.TestCase):

    def test_client_save_and_reload(self):
        table = ClientTable()
        table.add_record(**make_client(name="Persist Test"))

        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name

        try:
            table.save(path)
            new_table = ClientTable()
            new_table.load(path)
            self.assertEqual(len(new_table.records), 1)
            self.assertEqual(new_table.records[0]["name"], "Persist Test")
        finally:
            os.unlink(path)

    def test_load_missing_file_does_nothing(self):
        table = ClientTable()
        table.load("/tmp/this_file_does_not_exist.jsonl")
        self.assertEqual(table.records, [])


if __name__ == "__main__":
    unittest.main()
