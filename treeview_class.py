import tkinter as tk
from tkinter import ttk
import numpy as np


class CustomTreeview(ttk.Frame):
    def __init__(self, root, width=400, items=[["tube fair", 5, "#ee8959"]]*5):
        super().__init__(root)

        # Create Treeview with 3 columns
        self.tree = ttk.Treeview(self, columns=("Name", "Value (Monthly)", "Colour"),
                                 selectmode="extended")
        self.tree.pack(fill="both", expand=True)

        # lets me stop selected items from turning blue everytime
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.map("Treeview",
        )

        # stops the annoying dashed box around the selected notebook tab
        self.style.configure("Tab", focuscolor=self.style.configure(".")["background"])

        # Set column headings
        self.tree.column("#0", width=int(width/4)-5)
        self.tree.column("#1", width=int(width/4)-5)
        self.tree.column("#2", width=int(width/4)-5)
        self.tree.column("#3", width=int(width/4)-5)
        self.tree.heading("#0", text="iid", anchor="w")
        self.tree.heading("#1", text="Name", anchor="w")
        self.tree.heading("#2", text="Value (Monthly)", anchor="w")
        self.tree.heading("#3", text="Colour", anchor="w")
        
        # Create the Scrollbar widget and associate it with the Treeview
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Add the items to the Treeview
        for i, item in enumerate(items):
            self.tree.insert("", "end", text=i, values=(item), tags=item[-1])
            self.tree.tag_configure(item[-1], background=item[-1])

        # Pack the widgets into the frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events to enable drag-and-drop reordering of items
        self.tree.bind("<Button-1>", self.on_select)
        self.tree.bind("<B1-Motion>", self.on_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_release)
        self.dragged_iid = None
    
    def on_select(self, event):
        iid = self.tree.identify_row(event.y)

        if len(self.tree.item(iid)["values"]) != 0:
            colour = self.tree.item(iid)["values"][-1]
            self.style.map("Treeview",
                background=[("selected", "focus", colour)],
                foreground=[("selected", "focus", "white")]
            )

        if iid != "":
            self.dragged_iid = iid
       
    def on_drag(self, event):
        if self.dragged_iid is not None:
            new_index = self.tree.index(self.tree.identify_row(event.y))
            if new_index != "":
                self.tree.move(self.dragged_iid, "", new_index)

    def on_release(self, event):
        iid = self.tree.identify_row(event.y)
        if len(self.tree.item(iid)["values"]) != 0:
            colour = self.tree.item(iid)["values"][-1]
            self.style.map("Treeview",
                background=[("selected", "focus", colour)],
                foreground=[("selected", "focus", "black")]
            )
        self.dragged_iid = None

    def addItem(self, new_item):
        new_item[-2] = "{:.2f}".format(new_item[-2])
        self.tree.insert("", "end", text=len(self.tree.get_children()), values=new_item, tags=new_item[-1])
        self.tree.tag_configure(new_item[-1], background=new_item[-1])
        
        #scroll down to see newly added item
        self.tree.see(self.tree.get_children()[-1])

    def sumColumn(self, column_idx):
        total = 0
        for item in self.tree.get_children():
            value = float(self.tree.item(item, "values")[column_idx])
            total += value

        return "{:.2f}".format(total)
    
    def modeColumn(self, column_idx):
        # find frequency of each value
        freq_dict = {}
        for item in self.tree.get_children():
            value = self.tree.item(item, "values")[column_idx]
            freq_dict[value] = freq_dict.get(value, 0) + 1

        # Find the mode of column 2
        mode_value = None
        mode_count = 0
        for value, count in freq_dict.items():
            if count > mode_count:
                mode_value = value
                mode_count = count

        return mode_value
        


if __name__ == "__main__":

    root = tk.Tk()
    root.geometry('400x300')

    tree = CustomTreeview(root)
    tree.pack(fill='both', expand=True)

    root.mainloop()