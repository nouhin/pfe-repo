from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Frame, Label

FONT = ("Verdana", 12)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class app(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        self.title("Numerical Tool for Defect Caracterisation")
        self.configure(bg = "#333333")
        
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartWindow(container, self)
        self.frames[StartWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        canvas = Canvas(self, bg = "#333333", height = 750, width = 1100, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        self.show_frame(StartWindow)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, fg="#000000", text="Start Page", font=FONT)
        label.pack(pady=10, padx=10)


app = app()
app.mainloop()