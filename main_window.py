import tkinter as tk
import numpy as np

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budgeting App")
        self.geometry("400x400")
        
        core = tk.Frame(self)
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

        self.label_scrolls = tk.Label(core, text="Need : Want : Use (Roughly 50:30:20)\nNeed capped at 50, and determines the others")
        self.label_scrolls.pack()

        self.scroll_need = tk.Scale(core, from_=0, to=100, orient=tk.HORIZONTAL,
                                    command=lambda *args: self.updateScrollbars("need", *args))
        self.scroll_want = tk.Scale(core, from_=0, to=100, orient=tk.HORIZONTAL,
                                    command=lambda *args: self.updateScrollbars("want", *args))
        self.scroll_use = tk.Scale(core, from_=0, to=100, orient=tk.HORIZONTAL,
                                    command=lambda *args: self.updateScrollbars("use", *args))

        self.scroll_need.pack()
        self.scroll_want.pack()
        self.scroll_use.pack()

        
    def onClick(self):
        self.init_salary = float(self.salary_entry.get())
        
        self.label.config(text="Monthly income = "+str(self.allTaxes()))

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
        if args[0] == "need":
            if need > 50:
                self.scroll_need.set(50)
            return
        
        want_use_string = ["want", "use"]
        want_use_widget = [self.scroll_want, self.scroll_use]
        if args[0] in want_use_string:
            idx = want_use_string.index(args[0])
            if float(want_use_widget[idx].get()) > 100 - need:
                want_use_widget[idx].set(100-need)
            want_use_widget[idx-1].set(100 - need - float(want_use_widget[idx].get()))


        

if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()