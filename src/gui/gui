"""
Script description here:
Something like, gui build to create initial gui.
"""
import tkinter as tk
from pprint import pprint
from tkinter import ttk, messagebox
from datetime import datetime

import sys
sys.path.append('../')

# Below to make it work on my system. 
import os
# os.chdir(r"C:\Users\jd000207\MyCode10\psnl\Group Project\src") src.

from data.dataclasses import ClientTable, AirlineTable, FlightTable


class DataManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Records Mangaer")
        self.root.geometry("1200x600")
        # Change path based on your system, need to resolve to make portable.
        self.path = r"C:\Users\jd000207\MyCode10\psnl\Group Project\src\record"
        try:
            # Read Data if there
            self.tables = {
                "Clients": ClientTable().from_pickle(os.path.join(self.path, "Clients")),
                "Airlines": AirlineTable().from_pickle(os.path.join(self.path, "Airlines")),
                "Flights": FlightTable().from_pickle(os.path.join(self.path, "Flights"))
            }

        except FileNotFoundError:
            # Intialise tables if not present
            self.tables = {
                "Clients": ClientTable(),
                "Airlines": AirlineTable(),
                "Flights": FlightTable()
            }

        self.setup_ui()

    def setup_ui(self):
        # Table Selection Header
        header = tk.Frame(self.root)
        header.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header, text="Select Table:").pack(side="left")
        self.table_selector = ttk.Combobox(header, values=list(self.tables.keys()), state="readonly")
        self.table_selector.pack(side="left", padx=5)
        self.table_selector.set("Clients")
        self.table_selector.bind("<<ComboboxSelected>>", self.refresh_view)

        # Tabs for different Operations
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.view_tab = ttk.Frame(self.tabs)
        self.search_tab = ttk.Frame(self.tabs)
        
        self.tabs.add(self.view_tab, text="View & Manage")
        self.tabs.add(self.search_tab, text="Search")

        self.setup_view_tab()
        self.setup_search_tab()
        self.refresh_view()

    def setup_view_tab(self):
        # View to display records
        self.tree_frame = tk.Frame(self.view_tab)
        self.tree_frame.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        btn_frame = tk.Frame(self.view_tab)
        btn_frame.pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="Add Record", command=self.open_add_window).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Selected", command=self.open_update_window).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected, fg="red").pack(side="left", padx=5)

    def setup_search_tab(self):
        search_controls = tk.Frame(self.search_tab)
        search_controls.pack(fill="x", pady=10)

        tk.Label(search_controls, text="Column:").grid(row=0, column=0, padx=5)
        self.search_col_combo = ttk.Combobox(search_controls, state="readonly")
        self.search_col_combo.grid(row=0, column=1, padx=5)

        tk.Label(search_controls, text="Value:").grid(row=0, column=2, padx=5)
        self.search_entry = tk.Entry(search_controls)
        self.search_entry.grid(row=0, column=3, padx=5)

        tk.Button(search_controls, text="Search", command=self.perform_search).grid(row=0, column=4, padx=5)

        self.search_results_text = tk.Text(self.search_tab, height=15)
        self.search_results_text.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_view(self, event=None):
        table_name = self.table_selector.get()
        table_obj = self.tables[table_name]
        cols = table_obj._get_column_names()

        # Update Search Columns
        self.search_col_combo['values'] = cols
        if cols: self.search_col_combo.current(0)

        # Update Treeview Columns
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)

        # Insert Data
        ids = getattr(table_obj, cols[0])
        for i in range(len(ids)):
            values = [getattr(table_obj, col)[i] for col in cols] # Error Here.
            self.tree.insert("", "end", values=values)

    def open_add_window(self):
        table_name = self.table_selector.get()
        table_obj = self.tables[table_name]
        cols = table_obj._get_column_names()[1:] # Skip ID (auto-gen)

        win = tk.Toplevel(self.root)
        win.title(f"Add to {table_name}")
        
        entries = {}
        for i, col in enumerate(cols):
            tk.Label(win, text=col).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[col] = entry

        def save():
            try:
                data = {k: v.get() for k, v in entries.items()}
                # Map inputs to specific append_row methods
                if table_name == "Clients":
                    table_obj.append_row(data['names'], data['address_line_1s'], data['address_line_2s'], 
                                       data['address_line_3s'], data['cities'], data['states'], 
                                       data['zip_codes'], data['countries'], data['phone_numbers'])
                elif table_name == "Airlines":
                    table_obj.append_row(0, data['record_types'], data['company_names'])
                elif table_name == "Flights":
                    # Simple date handling for the demo
                    # date_val = datetime.strptime(str(data['dates']), table_obj.date_format)
                    table_obj.append_row(0, int(data['airline_ids']), data['dates'], data['start_cities'], data['end_cities'])
                
                self.refresh_view()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add: {e}")

        tk.Button(win, text="Save", command=save).grid(row=len(cols), columnspan=2, pady=10)

    def open_update_window(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Select", "Please select a record to update")
        
        item_values = self.tree.item(selected[0])['values']
        target_id = int(item_values[0])
        table_name = self.table_selector.get()
        table_obj = self.tables[table_name]
        cols = table_obj._get_column_names()

        win = tk.Toplevel(self.root)
        win.title("Update Record")
        
        entries = {}
        for i, col in enumerate(cols[1:]): # Skip ID
            tk.Label(win, text=col).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(win)
            entry.insert(0, item_values[i+1])
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[col] = entry

        def update():
            update_data = {k: v.get() for k, v in entries.items()}
            table_obj.update_record(target_id, **update_data)
            self.refresh_view()
            win.destroy()

        tk.Button(win, text="Update", command=update).grid(row=len(cols), columnspan=2, pady=10)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected: return
        
        if messagebox.askyesno("Confirm", "Delete selected record(s)?"):
            table_obj = self.tables[self.table_selector.get()]
            for item in selected:
                target_id = int(self.tree.item(item)['values'][0])
                table_obj.delete_record(target_id)
            self.refresh_view()

    def perform_search(self):
        table_obj = self.tables[self.table_selector.get()]
        col = self.search_col_combo.get()
        val = self.search_entry.get()
        
        # Determine if search should be int or str
        try:
            search_val = int(val)
        except ValueError:
            search_val = val

        matching_ids = table_obj.find_records(col, search_val)
        results = table_obj.display_records(matching_ids)
        
        self.search_results_text.delete("1.0", tk.END)
        if not results:
            self.search_results_text.insert(tk.END, "No records found.")
        else:
            for res in results:
                self.search_results_text.insert(tk.END, str(res) + "\n\n")
