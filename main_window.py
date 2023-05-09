import tkinter as tk
import numpy as np

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budgeting App")
        self.geometry("400x400")
        
        self.label_title = tk.Label(self, text="Enter Salary Below")
        self.label_title.pack()

        self.init_salary = 0
        self.salary_entry = tk.Entry(self)
        self.salary_entry.pack()

        self.loan_check_var = tk.BooleanVar()
        self.loan_check = tk.Checkbutton(self, text="Student Loan", variable=self.loan_check_var)
        self.loan_check.pack()
        
        self.button = tk.Button(self, text="Calculate", command=self.on_click)
        self.button.pack()

        self.label = tk.Label(self, text="")
        self.label.pack()
        
        
    def on_click(self):
        self.init_salary = float(self.salary_entry.get())
        
        self.label.config(text="Monthly salary = "+str(self.allTaxes()))

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
            print("loan")
            salary -= self.singleTax(27295, 0.09)

        return np.round(salary/12, 2)

    def singleTax(self, band, rate):
        if self.init_salary < band:
            return 0
        
        return (self.init_salary - band) * rate

        

if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()