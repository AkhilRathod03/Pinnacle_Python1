
import tkinter as tk
from calendar_ui import CalendarApp
import ttkbootstrap as tb

def main():
    root = tb.Window(themename="superhero")
    app = CalendarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
