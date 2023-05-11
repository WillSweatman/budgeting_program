import tkinter as tk
from tkinter import ttk
import numpy as np
import os

# my own classes/objects
from treeview_class import CustomTreeview
#from style_file import set_custom_style

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budgeting App")
        width=500
        self.geometry(str(width)+"x"+str(width))

        # Set the custom style
        #custom_style = set_custom_style()

        # in the mean time
        red = "#e76f51"
        amber = "#f4a261"
        green = "#2a9d8f"
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill='both', expand=True)
        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Salary and Ratios')
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Expenses')
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Help')

        """tab1"""

        core = tk.Frame(self.tab1)
        core.pack()

        self.label_title = tk.Label(core, text="Enter Salary Below")
        self.label_title.pack()

        self.init_salary = 0
        self.salary_entry = tk.Entry(core)
        self.salary_entry.insert(0, "33000")
        self.salary_entry.pack()

        self.loan_check_var = tk.BooleanVar(value=True)
        self.loan_check = tk.Checkbutton(core, text="Student Loan", variable=self.loan_check_var)
        self.loan_check.pack()
        
        self.button = tk.Button(core, text="Calculate", command=self.onClick)
        self.button.pack()

        self.label_monthly = tk.Label(core, text="")
        self.label_monthly.pack()

        ratios = tk.Frame(self.tab1)
        ratios.pack()

        self.label_scrolls = tk.Label(ratios, text="Need : Want : Use (Roughly 50:30:20)" + 
                                      "\nNeed shouldnt breach 50, and dictate the others")
        self.label_scrolls.grid(row=0, column=1)

        self.label_need = tk.Label(ratios, text="\nNeed", bg=red, fg="white")
        self.label_want = tk.Label(ratios, text="\nWant", bg=amber, fg="white")
        self.label_use = tk.Label(ratios, text="\nUse", bg=green, fg="white")

        self.scroll_need = tk.Scale(ratios, from_=0, to=100, orient=tk.HORIZONTAL, bg=red,
                                    command=lambda *args: self.updateScrollbars("need", *args))
        self.scroll_want = tk.Scale(ratios, from_=0, to=100, orient=tk.HORIZONTAL, bg=amber,
                                    command=lambda *args: self.updateScrollbars("want", *args))
        self.scroll_use = tk.Scale(ratios, from_=0, to=100, orient=tk.HORIZONTAL, bg=green,
                                    command=lambda *args: self.updateScrollbars("use", *args))
        
        self.label_need_val = tk.Label(ratios, text="\u2007"*7, bg=red, fg="white")
        self.label_want_val = tk.Label(ratios, text="\u2007"*7, bg=amber, fg="white")
        self.label_use_val = tk.Label(ratios, text="\u2007"*7, bg=green, fg="white")

        self.label_need.grid(row=1, column=0)
        self.label_want.grid(row=2, column=0)
        self.label_use.grid(row=3, column=0)
        self.scroll_need.grid(row=1, column=1)
        self.scroll_want.grid(row=2, column=1)
        self.scroll_use.grid(row=3, column=1)
        self.label_need_val.grid(row=1, column=2)
        self.label_want_val.grid(row=2, column=2)
        self.label_use_val.grid(row=3, column=2)

        """tab2"""

        self.expenses_tree = CustomTreeview(self.tab2, width)
        self.expenses_tree.pack()

        self.expense_input = tk.Frame(self.tab2)
        self.expense_input.pack()

        self.name_label = tk.Label(self.expense_input, text="Name:")
        self.value_label = tk.Label(self.expense_input, text="Value (Monthly):")
        self.colour_label = tk.Label(self.expense_input, text="Color:")
        self.name_entry = tk.Entry(self.expense_input)
        self.value_entry = tk.Entry(self.expense_input)
        self.colour_entry = tk.Entry(self.expense_input)

        # just for now!!!, saves me entering it in every time
        self.name_entry.insert("0", "train")
        self.value_entry.insert("0", "130")
        self.colour_entry.insert("0", "red")

        self.name_label.grid(row=0, column=0)
        self.value_label.grid(row=0, column=1)
        self.colour_label.grid(row=0, column=2)
        self.name_entry.grid(row=1, column=0)
        self.value_entry.grid(row=1, column=1)
        self.colour_entry.grid(row=1, column=2)

        self.input_button = tk.Button(self.expense_input, text="Input", command=self.newExpense)
        self.input_button.grid(row=2, column=0, columnspan=3)

        """tab3"""
        self.help_label = tk.Label(self.tab3)
        self.help_label.pack(side="left", anchor="nw")

        # ive opted to have it as a .txt file and open it so that
        # its easier to edit and it can be accessed without running
        # the program every time
        path = os.path.dirname(__file__) + "\help.txt"
        with open(path, "r") as f:
            text = f.read()

        self.help_label.config(text=text, justify="left")
        
    def onClick(self):
        self.init_salary = float(self.salary_entry.get())

        self.monthly_salary = self.allTaxes()
        
        self.label_monthly.config(text="Monthly income = "+str(self.monthly_salary))

        self.updateScrollbars("calc_button_pressed")

    def allTaxes(self):
        salary = self.init_salary

        # basic income bands
        salary -= self.singleTax(12571, 0.20)
        salary -= self.singleTax(50271, 0.20) # rolling calc, so 20+20=40% tax
        salary -= self.singleTax(125140, 0.05) # dito, 20+20+5=45% tax

        # national insurance
        salary -= self.singleTax(1048*12, 0.12)

        # student loan
        if self.loan_check_var.get():
            salary -= self.singleTax(27295, 0.09)

        return np.round(salary/12, 2)

    def singleTax(self, band, rate):
        if self.init_salary < band:
            return 0
        
        return (self.init_salary - band) * rate

    def updateScrollbars(self, *args):
        #print(args) # (scrollbar name, scrollbar attempted value)
        # scrollbar.get() is quick enough to not worry about frequent calling

        need = float(self.scroll_need.get())
        want_use_string = ["want", "use"]
        want_use_widget = [self.scroll_want, self.scroll_use]
        if args[0] == "need":
            #can cap at 50 if wanted
            # if need > 50:
            #     self.scroll_need.set(50)
            #     return
            self.scroll_want.set(0)
            self.scroll_use.set(100 - float(self.scroll_need.get()))

        elif args[0] in want_use_string:
            idx = want_use_string.index(args[0])
            if float(want_use_widget[idx].get()) > 100 - need:
                want_use_widget[idx].set(100-need)
            want_use_widget[idx-1].set(100 - need - float(want_use_widget[idx].get()))

        if self.label_monthly.cget("text") == "":
            return
        # attempt at stopping the wobbling by adding spaces (full-width \u2007) to text
        need_text = "{:.2f}".format(np.round(self.monthly_salary*(self.scroll_need.get()/100), 2))
        want_text = "{:.2f}".format(np.round(self.monthly_salary*(self.scroll_want.get()/100), 2))
        use_text = "{:.2f}".format(np.round(self.monthly_salary*(self.scroll_use.get()/100), 2))
        self.label_need_val.config(text=(7 - len(need_text))*"\u2007" + need_text)
        self.label_want_val.config(text=(7 - len(want_text))*"\u2007" + want_text)
        self.label_use_val.config(text=(7 - len(use_text))*"\u2007" + use_text)

    def newExpense(self):
        new_expense = [self.name_entry.get(), self.value_entry.get(), self.colour_entry.get()]
        self.expenses_tree.addItem(new_expense)

if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()