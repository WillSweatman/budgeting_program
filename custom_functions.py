import tkinter as tk
from random import choice

def randomColour():
    return "#" + "".join(choice("0123456789abcdef") for _ in range(6))
    
def validColour(colour):
    # is there an input
    if not colour:
        return randomColour()
    # is the input a valid colour for tkinter
    try:
        root = tk.Tk()
        dummy = tk.Label(root, bg=colour)
        dummy.destroy()
        return colour
    except Exception:
        tk.messagebox.showerror("Error", "Not a valid colour!\n" +
                                "Try a hex code (#123456) or colour name (red).")
        return None
    finally:
        root.destroy()

def validFloat(raw_value):
    try:
        value = float(raw_value)
        return value
    except ValueError:
        tk.messagebox.showerror("Error", "Input must be a number.")
        return None