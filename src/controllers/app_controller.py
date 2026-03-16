"""
Controller
Handles all user interactions and coordinates between the models and the view.
"""
import os
from models.tables import ClientTable, AirlineTable, FlightTable
from views.app_view import AppView


class AppController:
    """Connects the models and view. Handles all CRUD and search events."""

    RECORD_DIR = "record"

    TABLE_CLASSES = {
        "Clients": ClientTable,
        "Airlines": AirlineTable,
        "Flights": FlightTable,
    }

    def __init__(self, view: AppView):
        self.view = view
        self.tables = {name: cls() for name, cls in self.TABLE_CLASSES.items()}
        self._load_all()

        # Wire view callbacks to controller methods
        view.on_table_change = self.refresh
        view.on_add = self.add_record
        view.on_update = self.update_record
        view.on_delete = self.delete_record
        view.on_search = self.search_records

        self.refresh()

    def _table_path(self, name: str) -> str:
        """Returns the JSONL file path for a given table name."""
        return os.path.join(self.RECORD_DIR, f"{name.lower()}.jsonl")

    def _load_all(self):
        """Loads all tables from the file system on startup."""
        for name, table in self.tables.items():
            table.load(self._table_path(name))

    def save_all(self):
        """Saves all tables to the file system. Called on application close."""
        for name, table in self.tables.items():
            table.save(self._table_path(name))

    def _current_table_name(self) -> str:
        return self.view.get_selected_table()

    def _current_table(self):
        return self.tables[self._current_table_name()]

    def refresh(self):
        """Refreshes the view with the current table's data."""
        table = self._current_table()
        self.view.display_records(table.records, table.fields)
        self.view.update_search_columns(table.fields)

    def _airline_options(self) -> list[str]:
        """Returns a list of airline display strings for the flight dropdown."""
        return [f"{a['id']} - {a['company_name']}" for a in self.tables["Airlines"].records]

    def add_record(self):
        name = self._current_table_name()
        table = self._current_table()

        def on_save(data: dict, win):
            try:
                table.add_record(**data)
                self.refresh()
                win.destroy()
            except Exception as e:
                self.view.show_error(f"Failed to add record: {e}")

        if name == "Flights":
            self.view.open_flight_window("Add Flight Record", self._airline_options(),
                                         table.fields, {}, on_save)
        else:
            self.view.open_add_window(name, table.fields, on_save)

    def update_record(self):
        record_id = self.view.get_selected_id()
        if record_id is None:
            return self.view.show_warning("Please select a record to update.")

        name = self._current_table_name()
        table = self._current_table()
        record = table.get_record(record_id)

        def on_update(data: dict, win):
            try:
                table.update_record(record_id, **data)
                self.refresh()
                win.destroy()
            except Exception as e:
                self.view.show_error(f"Failed to update record: {e}")

        if name == "Flights":
            self.view.open_flight_window("Update Flight Record", self._airline_options(),
                                         table.fields, record, on_update)
        else:
            self.view.open_update_window(name, table.fields, record, on_update)

    def delete_record(self):
        selected = self.view.tree.selection()
        if not selected:
            return

        if self.view.confirm("Delete selected record(s)?"):
            table = self._current_table()
            for item in selected:
                record_id = int(self.view.tree.item(item)["values"][0])
                table.delete_record(record_id)
            self.refresh()

    def search_records(self):
        """Searches the current table and displays matching records."""
        table = self._current_table()
        field = self.view.get_search_field()
        value = self.view.get_search_value()

        try:
            search_val = int(value)
        except ValueError:
            search_val = value

        results = table.find_records(field, search_val)
        self.view.show_search_results(results)
