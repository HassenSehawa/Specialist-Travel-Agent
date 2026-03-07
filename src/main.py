from gui.gui import DataManagerApp
import tkinter as tk
import os

# os.chdir(r"C:\Users\jd000207\MyCode10\psnl\Group Project\src") #src.

if __name__ == "__main__":
    root = tk.Tk()
    app = DataManagerApp(root)
    root.mainloop()
    for name, table in app.tables.items():
        # Need to change to relative path to make more portable.  
        path = r"C:\Users\jd000207\MyCode10\psnl\Group Project\src\record"
        table.to_pickle(os.path.join(path, name))
