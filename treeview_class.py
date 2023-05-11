import tkinter as tk
from tkinter import ttk


class CustomTreeview(ttk.Frame):
    def __init__(self, root, width=400, items=[["tube fair", 5, "red"]]*5):
        super().__init__(root)

        # Create Treeview with 3 columns
        self.tree = ttk.Treeview(self, columns=("Name", "Value (Monthly)", "Color"),
                                 selectmode="extended")
        self.tree.pack(fill="both", expand=True)

        # Set column headings
        self.tree.column("#0", width=int(width/4)-5)
        self.tree.column("#1", width=int(width/4)-5)
        self.tree.column("#2", width=int(width/4)-5)
        self.tree.column("#3", width=int(width/4)-5)
        self.tree.heading("#0", text="iid", anchor="w")
        self.tree.heading("#1", text="Name", anchor="w")
        self.tree.heading("#2", text="Value (Monthly)", anchor="w")
        self.tree.heading("#3", text="Color", anchor="w")
        
        # Create the Scrollbar widget and associate it with the Treeview
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Add the items to the Treeview
        for i, item in enumerate(items):
            self.tree.insert("", "end", text=i, values=(item))

        
        # Pack the widgets into the frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events to enable drag-and-drop reordering of items
        self.tree.bind("<Button-1>", self.on_select)
        self.tree.bind("<B1-Motion>", self.on_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_release)
        self.dragged_iid = None
    
    def on_select(self, event):
        # Remember the ID of the item that was clicked
        item_id = self.tree.identify_row(event.y)
        if item_id != "":
            self.dragged_iid = item_id
    
    def on_drag(self, event):
        # Reorder the items as the mouse is dragged
        if self.dragged_iid is not None:
            new_index = self.tree.index(self.tree.identify_row(event.y))
            if new_index != "":
                self.tree.move(self.dragged_iid, "", new_index)
    
    def on_release(self, event):
        # Save the new order of the items
        self.dragged_iid = None
        new_order = [self.tree.item(iid)['text'] for iid in self.tree.get_children()]
        #print(new_order)  # replace with your own code to save the new order

    def addItem(self, new_item):
        self.tree.insert("", "end", text=len(self.tree.get_children()), values=new_item)
    


if __name__ == "__main__":

    root = tk.Tk()
    root.geometry('400x300')

    tree = CustomTreeview(root)
    tree.pack(fill='both', expand=True)

    root.mainloop()