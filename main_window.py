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
#from style_file import set_custom_style

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budgeting App")
        self.width = 800
        self.height = 600
        self.geometry(str(self.width)+"x"+str(self.height)+"+200+25")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set the custom style (not implemented)
        #custom_style = set_custom_style()

        # in the mean time
        self.dark = "#23404b"
        self.dark2 = "#264653"
        self.blue = "#488299"
        self.red = "#e76f51"
        self.red2 = "#e97c61"
        self.amber = "#f4a261"
        self.amber2 = "#efb366"
        self.green = "#2a9d8f"
        self.green2 = "#5aa786"
        
        # creating notebook format
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill='both', expand=True)
        self.tab1 = tk.Frame(self.notebook, bg=self.dark)
        self.notebook.add(self.tab1, text='Salary and Ratios')
        self.tab2 = tk.Frame(self.notebook, bg=self.dark)
        self.notebook.add(self.tab2, text='Expenses')
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Plot')
        self.tab4 = tk.Frame(self.notebook, bg=self.blue)
        self.notebook.add(self.tab4, text='Hints')
        self.tab5 = tk.Frame(self.notebook, bg=self.blue)
        self.notebook.add(self.tab5, text='Help')

        # filling tabs with content
        self.tab1Content()
        self.tab2Content()
        self.tab3Content()
        self.tab4Content()
        #self.tab5Content()


    def tab1Content(self):
        self.core = tk.Frame(self.tab1, bg=self.dark2)
        self.core.pack()

        self.label_title = tk.Label(self.core, bg=self.blue, text="Enter Salary Below")
        self.label_title.pack()

        self.init_salary = 0
        self.salary_entry = tk.Entry(self.core, bg=self.blue, fg="white")
        self.salary_entry.insert(0, "33000")
        self.salary_entry.pack()

        self.loan_check_var = tk.BooleanVar(value=True)
        self.loan_check = tk.Checkbutton(self.core, bg=self.blue, text="Student Loan", variable=self.loan_check_var)
        self.loan_check.pack()
        
        self.button = tk.Button(self.core, bg=self.blue, text="Tax me", command=self.onClickTax)
        self.button.pack()

        self.label_monthly = tk.Label(self.core, text="", bg=self.dark2, fg="white")
        self.label_monthly.pack()

        ratios = tk.Frame(self.tab1, bg=self.dark2)
        ratios.pack()

        self.label_scrolls = tk.Label(ratios, bg=self.dark2, fg="white", text="Need : Want : Use (Roughly 50:30:20)" + 
                                      "\nNeed shouldnt breach 50, and dictate the others")
        self.label_scrolls.grid(row=0)

        ratios_1 = tk.Frame(ratios, width=self.width/1.5, bg=self.red2)
        ratios_1.grid(row=1, sticky="nsew")
        ratios_2 = tk.Frame(ratios, width=self.width/1.5, bg=self.amber2)
        ratios_2.grid(row=2, sticky="nsew")
        ratios_3 = tk.Frame(ratios, width=self.width/1.5, bg=self.green2)
        ratios_3.grid(row=3, sticky="nsew")

        self.label_need = tk.Label(ratios_1, text="\nNeed", bg=self.red, fg="white")
        self.label_want = tk.Label(ratios_2, text="\nWant", bg=self.amber, fg="white")
        self.label_use = tk.Label(ratios_3, text="\nUse \u2007", bg=self.green, fg="white")

        self.scroll_need = tk.Scale(ratios_1, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, bg=self.red,
                                    command=lambda *args: self.updateScrollbars("need", *args))
        self.scroll_want = tk.Scale(ratios_2, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, bg=self.amber,
                                    command=lambda *args: self.updateScrollbars("want", *args))
        self.scroll_use = tk.Scale(ratios_3, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, bg=self.green,
                                    command=lambda *args: self.updateScrollbars("use", *args))
        
        self.label_need_val = tk.Label(ratios_1, text="\u2007"*7, bg=self.red, fg="white")
        self.label_want_val = tk.Label(ratios_2, text="\u2007"*7, bg=self.amber, fg="white")
        self.label_use_val = tk.Label(ratios_3, text="\u2007"*7, bg=self.green, fg="white")

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
        self.tree_stats = tk.Frame(self.tab2, width=self.width, bg=self.dark)
        self.tree_stats.pack()

        self.iid_stat = tk.Label(self.tree_stats, text="Population = ", justify="left", bg=self.blue)
        self.name_stat = tk.Label(self.tree_stats, text="Mode(Name) = ", justify="left", bg=self.amber)
        self.value_stat = tk.Label(self.tree_stats, text="Sum(Value) = ", justify="left", bg=self.red)
        self.colour_stat = tk.Label(self.tree_stats, text="Mode(Colour) = ", justify="left", bg=self.green)

        self.iid_stat.grid(row=0, column=0, sticky="nsew")
        self.name_stat.grid(row=0, column=1, sticky="nsew")
        self.value_stat.grid(row=0, column=2, sticky="nsew")
        self.colour_stat.grid(row=0, column=3, sticky="nsew")

        # treeview empty
        self.expense_input = tk.Frame(self.tab2, bg=self.dark)
        self.expense_input.pack()

        self.name_label = tk.Label(self.expense_input, text="Name", bg=self.dark2, fg="white")
        self.value_label = tk.Label(self.expense_input, text="Value (Monthly)", bg=self.dark2, fg="white")

        self.colour_frame = tk.Frame(self.expense_input, bg=self.dark)
        self.colour_frame.grid(row=0, column=2)
        self.colour_label = tk.Label(self.colour_frame, text="Colour", bg=self.dark2, fg="white")
        self.colour_button = tk.Button(self.colour_frame, text="Random", bg=self.dark2, fg="white", command=self.randomColour)
        self.colour_label.grid(row=0, column=0)
        self.colour_button.grid(row=0, column=1)

        self.name_entry = tk.Entry(self.expense_input, bg="white")
        self.value_entry = tk.Entry(self.expense_input, bg="white")
        self.colour_entry = tk.Entry(self.expense_input, bg="white")

        self.name_label.grid(row=0, column=0)
        self.value_label.grid(row=0, column=1)
        self.name_entry.grid(row=1, column=0)
        self.value_entry.grid(row=1, column=1)
        self.colour_entry.grid(row=1, column=2)

        self.input_button = tk.Button(self.expense_input, text="Input", bg=self.dark2, fg="white", command=self.newExpense)
        self.input_button.grid(row=2, column=0, columnspan=3)

        # button to send over the expenses total to "need" on tab1
        self.send_need_button = tk.Button(self.tab2, text="Set 'Need' in Salary and Ratios to Sum(Values)", bg=self.dark2, fg="white",
                                          command=lambda: self.updateScrollbars("need", 100*float(self.value_stat.cget("text")[13:])/self.monthly_salary, "outside"))
        self.send_need_button.pack()

        # just for now!!!, saves me entering it in every time
        self.name_entry.insert("0", "train")
        self.value_entry.insert("0", "130")
        self.colour_entry.insert("0", "#e9c46a")

    def tab3Content(self):

        self.variables_frame = tk.Frame(self.tab3, bg=self.blue, width=100)
        self.variables_frame.pack(side=tk.LEFT)

        self.plot_button = tk.Button(self.variables_frame, bg=self.blue, text="Plot", command=self.plotData)
        self.plot_button.pack(side=tk.LEFT)

        self.plot_frame = tk.Frame(self.tab3, width=self.width-100, height=self.width-100)
        self.plot_frame.pack()

        canvas = FigureCanvasTkAgg(master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def tab4Content(self):
        self.scroll_hints = tk.Scrollbar(self.tab4)
        self.scroll_hints.pack(side=tk.RIGHT, fill=tk.Y)

        self.hints = tk.Text(self.tab4, yscrollcommand=self.scroll_hints.set, bg=self.dark, fg="white", font="TkDefaultFont")
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

        value = self.validFloat(self.salary_entry.get())
        if  value == None:
            return

        self.init_salary = value

        self.monthly_salary = self.allTaxes()
        
        self.label_monthly.config(text="Monthly income = "+str(self.monthly_salary))

        self.updateScrollbars("calc_button_pressed")

        self.label_monthly.config(bg=self.blue)

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
        self.colour_entry.configure(bg="white")
        value = self.validFloat(self.value_entry.get())
        colour = self.validColour(self.colour_entry.get())
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

    def plotData(self):

        plt.close()

        x, y_pre_tax, y = self.runSim(20)

        fig, ax = plt.subplots()
        ax.plot(x, y_pre_tax)
        ax.plot(x, y)
        ax.set_title("Plot")
        ax.set_xlabel("Years")
        ax.set_ylabel("Salary (K)")
        ax.set_xlim(0, max(x))
        ax.set_ylim(0)
        plt.tight_layout()

        # Clear the plot frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Display the plot in the plot frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def runSim(self, years):

        x = [0]
        y_pre_tax = [self.init_salary]
        y = [self.allTaxes(y_pre_tax[-1])*12]

        for i in range(1, years+1):
            x.append(i)
            y_pre_tax.append(y_pre_tax[-1]*uniform(1.03, 1.09))
            y.append(self.allTaxes(y_pre_tax[-1])*12)
            
        return x, y_pre_tax, y

    def randomColour(self):
        colour = "#" + "".join(choice("0123456789abcdef") for _ in range(6))
        self.colour_entry.configure(bg=colour)
        self.colour_entry.delete(0, tk.END)
        self.colour_entry.insert("0", colour)

    def validColour(self, colour):
        # is there an input
        if not colour:
            return "#" + "".join(choice("0123456789abcdef") for _ in range(6))
        # is the input a valid colour for tkinter
        try:
            dummy = tk.Label(self, bg=colour)
            dummy.destroy()
            return colour
        except Exception:
            tk.messagebox.showerror("Error", "Not a valid colour!\n" +
                                    "Try a hex code (#123456) or colour name (red).")
            return None

    def validFloat(self, raw_value):
        try:
            value = float(raw_value)
            return value
        except ValueError:
            tk.messagebox.showerror("Error", "Input must be a number.")
            return None

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
    app = MyWindow()
    app.mainloop()