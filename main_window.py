import tkinter as tk

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budgeting App")
        self.geometry("400x400")
        
        self.label = tk.Label(self, text="Hello, world!")
        self.label.pack()
        
        self.button = tk.Button(self, text="Click me!", command=self.on_click)
        self.button.pack()
        
    def on_click(self):
        self.label.config(text=self.allTaxes())

    def allTaxes(self):
        salary = init_salary = 33000

        # basic income
        salary -= self.singleTax(init_salary, 12571, 0.20)

        # national insurance
        salary -= self.singleTax(init_salary, 1048*12, 0.12)

        # student loan
        salary -= self.singleTax(init_salary, 27295, 0.09)

        return salary

    def singleTax(self, init_salary, band, rate):
        return (init_salary - band) * rate

        

if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()