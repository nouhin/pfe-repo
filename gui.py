from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog
from toolbox import *

FONT = ("Verdana", 12)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        # self.geometry("500x500")
        self.wm_title("Numerical Tool for Defect Caracterisation")
        self.configure(bg = "#333333")
        
        mainframe = ttk.Frame(self)
        mainframe.pack(side="top", fill="both", expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.IMAGEJ_dir = ""
        self.src_dir = ""
        self.dest_dir = ""
        self.labels_dir = ""

        self.frames = {}

        for F in (StartWindow, LabelingPage, AnalysePage, SegmentationPage, RegistrationPage):
            frame = F(mainframe, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # canvas = Canvas(self, bg = "#333333", height = 750, width = 1100, bd = 0, highlightthickness = 0, relief = "ridge")
        # canvas.place(x = 0, y = 0)

        # pimm_logo = PhotoImage(file=relative_to_assets("pimm.png"))
        # image_1 = canvas.create_image( 1051.0, 47.0, image=pimm_logo)

        # ensam_logo = PhotoImage(file=relative_to_assets("ensam.png"))
        # image_2 = canvas.create_image(942.0, 47.0, image=ensam_logo)

        # afh_logo = PhotoImage(file=relative_to_assets("afh.png"))
        # image_3 = canvas.create_image(997.0, 46.0, image=afh_logo)

        self.show_frame(StartWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def getFolders(self):
        self.src_dir = filedialog.askdirectory( title = "Local ImageJ Directory ...")
        self.src_dir = filedialog.askdirectory( title = "Choose Raw Tomography images Directory ...")
        self.dest_dir = filedialog.askdirectory( title = "Choose Destination Directory for processed images...")
        self.labels_dir = filedialog.askdirectory( title = "Choose Destination Directory for Labeled images...")

class StartWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, fg="#000000", text="Start Window", font=FONT)
        label.pack(pady=10, padx=10)

        label_button = ttk.Button(self, text="Extract Labels", command=lambda: controller.show_frame(LabelingPage))
        label_button.pack()

        analyse_button = ttk.Button(self, text="Quantify Pores", command=lambda: controller.show_frame(AnalysePage))
        analyse_button.pack()

        segmentation_button = ttk.Button(self, text="Segment 3D", command=lambda: controller.show_frame(SegmentationPage))
        segmentation_button.pack()

        registration_button = ttk.Button(self, text="Visualize", command=lambda: controller.show_frame(RegistrationPage))
        registration_button.pack()

class LabelingPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg = "#333333")
        self.place(height =500, width = 600)

        label = Label(self, fg="#000000", text="Labeling Page", font=FONT)
        label.pack(pady=10, padx=10)  

        label_button = ttk.Button(self, text="Browse", command=lambda: controller.getFolders())
        label_button.pack()

        clean_button = ttk.Button(self, text="Label", command=lambda: extact_labels(controller.IMAGEJ_dir, controller.src_dir, controller.dest_dir, controller.labels_dir))
        clean_button.pack()

        save_button_1 = ttk.Button(self, text="save", command=lambda: controller.show_frame(StartWindow))
        save_button_1.pack()

        label_button = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartWindow))
        label_button.pack()

class AnalysePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, fg="#000000", text="Analyse Page", font=FONT)
        label.pack(pady=10, padx=10)       
        label_button = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartWindow))
        label_button.pack()

        save_button_2 = ttk.Button(self, text="save", command=lambda: controller.show_frame(StartWindow))
        save_button_2.pack()

class SegmentationPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, fg="#000000", text="Segmentation Page", font=FONT)
        label.pack(pady=10, padx=10)       
        label_button = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartWindow))
        label_button.pack()

class RegistrationPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, fg="#000000", text="Registration Page", font=FONT)
        label.pack(pady=10, padx=10)       
        label_button = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartWindow))
        label_button.pack()

app = App()
app.mainloop()