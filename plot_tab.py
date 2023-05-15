import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# my own custom classes/objects
from custom_colours import *

class PlottingTab:
    def __init__(self, parent_tab, runSim, width):
        self.tab = parent_tab
        self.runSim = runSim
        self.width = width

        self.variables_frame = tk.Frame(self.tab, bg=blue, width=100)
        self.variables_frame.pack(side=tk.LEFT)

        self.plot_button = tk.Button(self.variables_frame, bg=blue, text="Plot", command=self.plotData)
        self.plot_button.pack(side=tk.LEFT)

        self.plot_frame = tk.Frame(self.tab, width=self.width-100, height=self.width-100)
        self.plot_frame.pack()

        canvas = FigureCanvasTkAgg(master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

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