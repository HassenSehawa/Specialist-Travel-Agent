"""
Responsible for building and managing all UI widgets.
Does not contain any business logic — all actions are delegated to the controller.
"""
import tkinter as tk
from tkinter import ttk, messagebox


class AppView:
    """Main application window. Builds the UI and exposes callbacks for the controller."""

    def __init__(self, root: tk.Tk, table_names: list[str]):
        self.root = root
        self.root.title("Specialist Travel Agent")
        self.root.geometry("1200x600")

        # Callbacks wired up by the controller
        self.on_table_change = None
        self.on_add = None
        self.on_update = None
        self.on_delete = None
        self.on_search = None

        self._build_ui(table_names)

    def _build_ui(self, table_names: list[str]):
        """Builds the full UI layout."""
        # Header — table selector
        header = tk.Frame(self.root)
        header.pack(fill="x", padx=10, pady=10)

        tk.Label(header, text="Select Table:").pack(side="left")
        self.table_selector = ttk.Combobox(header, values=table_names, state="readonly")
        self.table_selector.pack(side="left", padx=5)
        self.table_selector.set(table_names[0])
        self.table_selector.bind("<<ComboboxSelected>>", self._table_changed)

        # Tabs
        tabs = ttk.Notebook(self.root)
        tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.view_tab = ttk.Frame(tabs)
        self.search_tab = ttk.Frame(tabs)
        tabs.add(self.view_tab, text="View & Manage")
        tabs.add(self.search_tab, text="Search")

        self._build_view_tab()
        self._build_search_tab()

    def _build_view_tab(self):
        """Builds the records table and action buttons."""
        tree_frame = tk.Frame(self.view_tab)
        tree_frame.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(tree_frame, show="headings")
        self.tree.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.view_tab)
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="Add Record", command=self._on_add).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Selected", command=self._on_update).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self._on_delete, fg="red").pack(side="left", padx=5)

    def _build_search_tab(self):
        """Builds the search controls and results area."""
        controls = tk.Frame(self.search_tab)
        controls.pack(fill="x", pady=10)

        tk.Label(controls, text="Field:").grid(row=0, column=0, padx=5)
        self.search_col_combo = ttk.Combobox(controls, state="readonly")
        self.search_col_combo.grid(row=0, column=1, padx=5)

        tk.Label(controls, text="Value:").grid(row=0, column=2, padx=5)
        self.search_entry = tk.Entry(controls)
        self.search_entry.grid(row=0, column=3, padx=5)

        tk.Button(controls, text="Search", command=self._on_search).grid(row=0, column=4, padx=5)

        self.search_results = tk.Text(self.search_tab, height=15)
        self.search_results.pack(fill="both", expand=True, padx=5, pady=5)

    # --- Public methods called by the controller ---

    def get_selected_table(self) -> str:
        return self.table_selector.get()

    def get_selected_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            return None
        return int(self.tree.item(selected[0])["values"][0])

    def get_selected_record_values(self) -> list | None:
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"]

    def get_search_field(self) -> str:
        return self.search_col_combo.get()

    def get_search_value(self) -> str:
        return self.search_entry.get()

    def display_records(self, records: list[dict], fields: list[str]):
        all_cols = ["id", "type"] + fields
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = all_cols
        for col in all_cols:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)
        for record in records:
            values = [record.get(col, "") for col in all_cols]
            self.tree.insert("", "end", values=values)

    def update_search_columns(self, fields: list[str]):
        all_cols = ["id"] + fields
        self.search_col_combo["values"] = all_cols
        if all_cols:
            self.search_col_combo.current(0)

    def show_search_results(self, results: list[dict]):
        self.search_results.delete("1.0", tk.END)
        if not results:
            self.search_results.insert(tk.END, "No records found.")
        else:
            for record in results:
                self.search_results.insert(tk.END, str(record) + "\n\n")

    def open_add_window(self, table_name: str, fields: list[str], on_save, required_fields: list[str] = []):
        """Opens a dialog window for adding a new record."""
        win = tk.Toplevel(self.root)
        win.title(f"Add {table_name} Record")

        entries = {}
        for i, field in enumerate(fields):
            label = field.replace("_", " ").title() + (" *" if field in required_fields else "")
            tk.Label(win, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(win, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        tk.Button(win, text="Save", command=lambda: on_save({k: v.get() for k, v in entries.items()}, win)).grid(
            row=len(fields), columnspan=2, pady=10
        )

    def open_update_window(self, table_name: str, fields: list[str], current_values: dict, on_update, required_fields: list[str] = []):
        """Opens a dialog window pre-filled with the current record values."""
        win = tk.Toplevel(self.root)
        win.title(f"Update {table_name} Record")

        entries = {}
        for i, field in enumerate(fields):
            label = field.replace("_", " ").title() + (" *" if field in required_fields else "")
            tk.Label(win, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(win, width=30)
            entry.insert(0, current_values.get(field, ""))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        tk.Button(win, text="Update", command=lambda: on_update({k: v.get() for k, v in entries.items()}, win)).grid(
            row=len(fields), columnspan=2, pady=10
        )

    def open_flight_window(self, title: str, airline_options: list[str], fields: list[str],
                           current_values: dict, on_save, required_fields: list[str] = []):
        win = tk.Toplevel(self.root)
        win.title(title)

        entries = {}
        for i, field in enumerate(fields):
            label = field.replace("_", " ").title() + (" *" if field in required_fields else "")
            tk.Label(win, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            if field == "airline_id":
                widget = ttk.Combobox(win, values=airline_options, state="readonly", width=28)
                current = str(current_values.get("airline_id", ""))
                matched = next((o for o in airline_options if o.startswith(current + " -")), "")
                widget.set(matched)
            elif field == "date":
                widget = tk.Entry(win, width=30)
                widget.insert(0, current_values.get("date", "YYYY-MM-DD"))
            else:
                widget = tk.Entry(win, width=30)
                widget.insert(0, current_values.get(field, ""))
            widget.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = widget

        def collect():
            data = {}
            for k, v in entries.items():
                if k == "airline_id":
                    selected = v.get()
                    if not selected:
                        raise ValueError("Please select an airline.")
                    data[k] = int(selected.split(" - ")[0])
                elif k == "date":
                    data[k] = v.get()
                else:
                    data[k] = v.get()
            return data

        def on_click():
            try:
                on_save(collect(), win)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Save", command=on_click).grid(
            row=len(fields), columnspan=2, pady=10
        )

    def show_error(self, message: str):
        messagebox.showerror("Error", message)

    def show_warning(self, message: str):
        messagebox.showwarning("Warning", message)

    def confirm(self, message: str) -> bool:
        return messagebox.askyesno("Confirm", message)

    # --- Internal event dispatchers ---

    def _table_changed(self, event=None):
        if self.on_table_change:
            self.on_table_change()

    def _on_add(self):
        if self.on_add:
            self.on_add()

    def _on_update(self):
        if self.on_update:
            self.on_update()

    def _on_delete(self):
        if self.on_delete:
            self.on_delete()

    def _on_search(self):
        if self.on_search:
            self.on_search()
