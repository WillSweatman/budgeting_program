from tkinter import ttk

def set_custom_style():
    custom_style = ttk.Style()

    # Set the theme to your custom style
    custom_style.theme_create("CustomStyle", parent="alt", settings={
        "TLabel": {"configure": {"foreground": "#e76f51", "background": "white"}},
        "Custom_Red": {"foreground": "#e76f51"},
        "Custom_Amber": {"foreground": "#f4a261"},
        "Custom_Green": {"foreground": "#2a9d8f"},
    })
    custom_style.theme_use("CustomStyle")

    return custom_style