import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import uniform
from random import choice


# my own classes/objects
from treeview_class import CustomTreeview
from plot_tab import PlottingTab
from custom_functions import *
from custom_colours import *
#from style_file import set_custom_style

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budgeting App")
        self.width = 800
        self.height = 600
        self.geometry(str(self.width)+"x"+str(self.height)+"+200+25")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set the custom style (not implemented)
        #custom_style = set_custom_style()
        
        # creating notebook format
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill='both', expand=True)
        self.tab1 = tk.Frame(self.notebook, bg=dark)
        self.notebook.add(self.tab1, text='Salary and Ratios')
        self.tab2 = tk.Frame(self.notebook, bg=dark)
        self.notebook.add(self.tab2, text='Expenses')
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Plot')
        self.tab4 = tk.Frame(self.notebook, bg=blue)
        self.notebook.add(self.tab4, text='Hints')
        self.tab5 = tk.Frame(self.notebook, bg=blue)
        self.notebook.add(self.tab5, text='Help')

        # filling tabs with content
        self.tab1Content()
        self.tab2Content()
        self.tab1Content = PlottingTab(self.tab3, self.runSim, self.width)
        self.tab4Content()
        #self.tab5Content()


    def tab1Content(self):
        self.core = tk.Frame(self.tab1, bg=dark2)
        self.core.pack()

        self.label_title = tk.Label(self.core, bg=blue, text="Enter Salary Below")
        self.label_title.pack()

        self.init_salary = 0
        self.monthly_salary = 0
        self.salary_entry = tk.Entry(self.core, bg=blue, fg="white")
        self.salary_entry.insert(0, "33000")
        self.salary_entry.pack()

        self.loan_check_var = tk.BooleanVar(value=True)
        self.loan_check = tk.Checkbutton(self.core, bg=blue, text="Student Loan", variable=self.loan_check_var)
        self.loan_check.pack()
        
        self.button = tk.Button(self.core, bg=blue, text="Tax me", command=self.onClickTax)
        self.button.pack()

        self.label_monthly = tk.Label(self.core, text="", bg=dark2, fg="white")
        self.label_monthly.pack()

        ratios = tk.Frame(self.tab1, bg=dark2)
        ratios.pack()

        self.label_scrolls = tk.Label(ratios, bg=dark2, fg="white", text="Need : Want : Use (Roughly 50:30:20)" + 
                                      "\nNeed shouldnt breach 50, and dictate the others")
        self.label_scrolls.grid(row=0)

        ratios_1 = tk.Frame(ratios, width=self.width/1.5, bg=red2)
        ratios_1.grid(row=1, sticky="nsew")
        ratios_2 = tk.Frame(ratios, width=self.width/1.5, bg=amber2)
        ratios_2.grid(row=2, sticky="nsew")
        ratios_3 = tk.Frame(ratios, width=self.width/1.5, bg=green2)
        ratios_3.grid(row=3, sticky="nsew")

        self.label_need = tk.Label(ratios_1, text="\nNeed", bg=red, fg="white")
        self.label_want = tk.Label(ratios_2, text="\nWant", bg=amber, fg="white")
        self.label_use = tk.Label(ratios_3, text="\nUse \u2007", bg=green, fg="white")

        self.scroll_need = tk.Scale(ratios_1, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, bg=red,
                                    command=lambda *args: self.updateScrollbars("need", *args))
        self.scroll_want = tk.Scale(ratios_2, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, bg=amber,
                                    command=lambda *args: self.updateScrollbars("want", *args))
        self.scroll_use = tk.Scale(ratios_3, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, bg=green,
                                    command=lambda *args: self.updateScrollbars("use", *args))
        
        self.label_need_val = tk.Label(ratios_1, text="\u2007"*7, bg=red, fg="white")
        self.label_want_val = tk.Label(ratios_2, text="\u2007"*7, bg=amber, fg="white")
        self.label_use_val = tk.Label(ratios_3, text="\u2007"*7, bg=green, fg="white")

        self.label_need.grid(row=0, column=0)
        self.label_want.grid(row=0, column=0)
        self.label_use.grid(row=0, column=0)
        self.scroll_need.grid(row=0, column=1)
        self.scroll_want.grid(row=0, column=1)
        self.scroll_use.grid(row=0, column=1)
        self.label_need_val.grid(row=0, column=2)
        self.label_want_val.grid(row=0, column=2)
        self.label_use_val.grid(row=0, column=2)

        for r in [ratios_1, ratios_2, ratios_3]:
            r.grid_rowconfigure(1, weight=1)
            r.grid_columnconfigure(1, weight=1)

    def tab2Content(self):
        # treeview
        self.expenses_tree = CustomTreeview(self.tab2, self.width)
        self.expenses_tree.pack()

        # treeview stats
        self.tree_stats = tk.Frame(self.tab2, width=self.width, bg=dark)
        self.tree_stats.pack()

        self.iid_stat = tk.Label(self.tree_stats, text="Population = ", justify="left", bg=blue)
        self.name_stat = tk.Label(self.tree_stats, text="Mode(Name) = ", justify="left", bg=amber)
        self.value_stat = tk.Label(self.tree_stats, text="Sum(Value) = ", justify="left", bg=red)
        self.colour_stat = tk.Label(self.tree_stats, text="Mode(Colour) = ", justify="left", bg=green)

        self.iid_stat.grid(row=0, column=0, sticky="nsew")
        self.name_stat.grid(row=0, column=1, sticky="nsew")
        self.value_stat.grid(row=0, column=2, sticky="nsew")
        self.colour_stat.grid(row=0, column=3, sticky="nsew")

        # treeview empty
        self.expense_input = tk.Frame(self.tab2, bg=dark)
        self.expense_input.pack()

        self.name_label = tk.Label(self.expense_input, text="Name", bg=dark2, fg="white")
        self.value_label = tk.Label(self.expense_input, text="Value (Monthly)", bg=dark2, fg="white")

        self.colour_frame = tk.Frame(self.expense_input, bg=dark)
        self.colour_frame.grid(row=0, column=2)
        self.colour_label = tk.Label(self.colour_frame, text="Colour", bg=dark2, fg="white")
        self.colour_button = tk.Button(self.colour_frame, text="Random", bg=dark2, fg="white", command=self.applyColour)
        self.colour_label.grid(row=0, column=0)
        self.colour_button.grid(row=0, column=1)

        self.name_entry = tk.Entry(self.expense_input, bg=blue, fg = "white")
        self.value_entry = tk.Entry(self.expense_input, bg=blue, fg = "white")
        self.colour_entry = tk.Entry(self.expense_input, bg=blue, fg = "white")

        self.name_label.grid(row=0, column=0)
        self.value_label.grid(row=0, column=1)
        self.name_entry.grid(row=1, column=0)
        self.value_entry.grid(row=1, column=1)
        self.colour_entry.grid(row=1, column=2)

        self.input_button = tk.Button(self.expense_input, text="Input", bg=dark2, fg="white", command=self.newExpense)
        self.input_button.grid(row=2, column=0, columnspan=3)

        # button to send over the expenses total to "need" on tab1
        self.send_need_button = tk.Button(self.tab2, text="Set 'Need' in Salary and Ratios to Sum(Values)", bg=dark2, fg="white",
                                          command=lambda: self.usingExpenses(float(self.value_stat.cget("text")[13:])))
        self.send_need_button.pack()

        # just for now!!!, saves me entering it in every time
        self.name_entry.insert("0", "example")
        self.value_entry.insert("0", "0.00")
        self.colour_entry.insert("0", "#ce2252")
        self.applyColour("#ce2252")

    def tab4Content(self):
        self.scroll_hints = tk.Scrollbar(self.tab4)
        self.scroll_hints.pack(side=tk.RIGHT, fill=tk.Y)

        self.hints = tk.Text(self.tab4, yscrollcommand=self.scroll_hints.set, bg=dark, fg="white", font="TkDefaultFont")
        self.hints.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ive opted to have it as a .txt file and open it so that
        # its easier to edit and it can be accessed without running
        # the program every time
        path = os.path.dirname(__file__) + "\hints.txt"
        with open(path, "r") as f:
            text = f.read()

        self.hints.insert(tk.END, text)
        self.hints.configure(state="disabled")
        self.scroll_hints.config(command=self.hints.yview)

    def tab5Content(self):
        print("Not implemented")

    def onClickTax(self):

        value = validFloat(self.salary_entry.get())
        if  value == None:
            return

        self.init_salary = value

        self.monthly_salary = self.allTaxes()
        
        self.label_monthly.config(text="Monthly income = "+str(self.monthly_salary))

        self.updateScrollbars("calc_button_pressed")

        self.label_monthly.config(bg=blue)

    def allTaxes(self, *args):
        pre_salary = 0
        if len(args) == 0:
            pre_salary = self.init_salary
        else:
            pre_salary = args[0]

        salary = pre_salary

        # basic income bands
        salary -= self.singleTax(pre_salary, 12571, 0.20)
        salary -= self.singleTax(pre_salary, 50271, 0.20) # rolling calc, so 20+20=40% tax
        salary -= self.singleTax(pre_salary, 125140, 0.05) # dito, 20+20+5=45% tax

        # national insurance
        salary -= self.singleTax(pre_salary, 1048*12, 0.12)

        # student loan
        if self.loan_check_var.get():
            salary -= self.singleTax(pre_salary, 27295, 0.09)

        return np.round(salary/12, 2)

    def singleTax(self, total, band, rate):
        if total < band:
            return 0
        
        return (total - band) * rate

    def updateScrollbars(self, *args):
        #print(args) # (scrollbar name, scrollbar attempted value)
        # scrollbar.get() is quick enough to not worry about frequent calling

        # for passing in an outside value
        need = 0
        if len(args) > 2 and args[2] == "outside":
            need = args[1]
            self.scroll_need.set(need)
            self.scroll_want.set(0)
            self.scroll_use.set(100 - float(self.scroll_need.get()))
        else:
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
        self.colour_entry.configure(bg=blue, fg = "white")
        value = validFloat(self.value_entry.get())
        colour = validColour(self.colour_entry.get())
        if None in [value, colour]:
            return
        
        new_expense = [self.name_entry.get(), value, colour]
        self.expenses_tree.addItem(new_expense)

        # clear entry boxes ready for new entry
        self.name_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.colour_entry.delete(0, tk.END)

        # calculate stats
        self.iid_stat.configure(text="Population = "+str(len(self.expenses_tree.tree.get_children())))
        self.name_stat.configure(text="Mode(Name) = "+str(self.expenses_tree.modeColumn(-3)))
        self.value_stat.configure(text="Sum(Value) = "+str(self.expenses_tree.sumColumn(-2)))
        self.colour_stat.configure(text="Mode(Colour) = "+str(self.expenses_tree.modeColumn(-1)))

    def runSim(self, years):

        x = [0]
        y_pre_tax = [self.init_salary]
        y = [self.allTaxes(y_pre_tax[-1])*12]

        for i in range(1, years+1):
            x.append(i)
            y_pre_tax.append(y_pre_tax[-1]*uniform(1.03, 1.09))
            y.append(self.allTaxes(y_pre_tax[-1])*12)
            
        return x, y_pre_tax, y

    def applyColour(self, colour=None):
        if colour == None:
            colour = randomColour()

        self.colour_entry.configure(bg=colour)
        self.colour_entry.delete(0, tk.END)
        self.colour_entry.insert("0", colour)

    def usingExpenses(self, expense_total):
        if self.monthly_salary == 0:
            tk.messagebox.showerror("Error", "No Monthly Salary entered.")
            return

        if expense_total > self.monthly_salary:
            tk.messagebox.showerror("Error", "Expenses larger than Monthly Salary.")
            return
        
        self.updateScrollbars("need", 100*expense_total/self.monthly_salary, "outside")

    def on_closing(self):
        
        # Get a list of all the figure numbers
        fig_total = plt.get_fignums()
        #print("Graphs created:",len(fig_total))

        # Loop over the figure numbers and close each figure
        for fig_num in fig_total:
            fig = plt.figure(fig_num)
            plt.close(fig)

        # Close main window
        self.destroy()






if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()