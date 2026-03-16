"""
Entry point.
Initialises the tkinter window, wires up the MVC components,
and saves data to disk when the application is closed.
"""
import tkinter as tk
import os
import sys

# Ensure src/ is on the path when running from any directory
sys.path.insert(0, os.path.dirname(__file__))

from views.app_view import AppView
from controllers.app_controller import AppController


if __name__ == "__main__":
    root = tk.Tk()
    view = AppView(root, ["Clients", "Airlines", "Flights"])
    controller = AppController(view)
    root.protocol("WM_DELETE_WINDOW", lambda: (controller.save_all(), root.destroy()))
    root.mainloop()
