import tkinter as tk

class CustomSlider(tk.Canvas):
    def __init__(self, master, min_value, max_value, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.handle1 = self.create_rectangle(0, 0, 10, 20, fill='blue')
        self.handle2 = self.create_rectangle(90, 0, 100, 20, fill='red')
        self.bind('<B1-Motion>', self._on_drag)
    
    def _on_drag(self, event):
        x = self.canvasx(event.x)
        if x < 0:
            x = 0
        elif x > self.winfo_width():
            x = self.winfo_width()
        handle = self.handle1 if abs(x - self.coords(self.handle1)[0]) < abs(x - self.coords(self.handle2)[0]) else self.handle2
        self.coords(handle, x-5, 0, x+5, 20)
    
    def get_values(self):
        x1, _, x2, _ = self.coords(self.handle1)
        y1, _, y2, _ = self.coords(self.handle2)
        return (self.min_value + int((x1/self.winfo_width()) * (self.max_value - self.min_value)),
                self.min_value + int((y1/self.winfo_width()) * (self.max_value - self.min_value)),
                self.min_value + int((y2/self.winfo_width()) * (self.max_value - self.min_value)))

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Custom Slider Demo")
        self.geometry("400x400")
        
        self.slider = CustomSlider(self, 0, 100)
        self.slider.pack(fill=tk.X, padx=20, pady=20)
        
        self.button = tk.Button(self, text="Get Values", command=self.on_click)
        self.button.pack(pady=10)
        
        self.label = tk.Label(self, text="")
        self.label.pack()
        
    def on_click(self):
        values = self.slider.get_values()
        self.label.config(text=f"Values: {values}")
        
if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()
