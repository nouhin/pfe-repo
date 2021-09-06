from toolbox import *
from PIL import ImageTk, Image

FONT = ("Verdana", 12)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

image_afh = Image.open("assets/afh.png")
image_ensam = Image.open("assets/ensam.png")
image_pimm = Image.open("assets/pimm.png")

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        self.geometry("600x500")
        self.wm_title("Numerical Tool for Defect Caracterisation")
        self.configure(bg = "#333333")
        
        mainframe = ttk.Frame(self)
        mainframe.pack(side="top", fill="both", expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.afh = ImageTk.PhotoImage(image_afh)
        self.ensam = ImageTk.PhotoImage(image_ensam)
        self.pimm = ImageTk.PhotoImage(image_pimm)


        self.IMAGEJ_dir = ""
        self.src_dir = ""
        self.dest_dir = ""
        self.labels_dir = ""
        self.csv_file_dir = ""

        self.template_dir = ""
        self.img_dir = ""
        self.raw_tif_dir = ""


        self.frames = {}

        for F in (StartWindow, LabelingPage, AnalysePage, SegmentationPage, RegistrationPage):
            frame = F(mainframe, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="#333333")

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

    def getFile(self):
        self.template_dir = filedialog.askopenfilename(title="Choose a template")
        self.img_dir = filedialog.askopenfilename(title="Choose a file")
        self.raw_tif_dir = filedialog.askopenfilename(title="Choose a file")
        self.src_dir = filedialog.askdirectory( title = "Choose Raw Tomography images Directory ...")

    def getCsv(self):
        self.csv_file_dir = filedialog.askopenfilename(title="Choose a csv file")

class StartWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label_image_afh = Label(self, image=controller.afh)
        label_image_afh.grid(sticky='NE')
        label_image_ensam = Label(self, image=controller.ensam)
        label_image_ensam.grid(sticky='NE')
        label_image_pimm = Label(self, image=controller.pimm)
        label_image_pimm.grid(sticky='NE')


        label = Label(self, fg="#000000", text="Start Window", font=FONT)
        label.grid(sticky='N')

        label_button = ttk.Button(self, text="Extract Labels", command=lambda: controller.show_frame(LabelingPage))
        label_button.grid(row=2, column=0)

        analyse_button = ttk.Button(self, text="Quantify Pores", command=lambda: controller.show_frame(AnalysePage))
        analyse_button.grid(row=3, column=0)

        segmentation_button = ttk.Button(self, text="Segment 3D", command=lambda: controller.show_frame(SegmentationPage))
        segmentation_button.grid(row=4, column=0)

        registration_button = ttk.Button(self, text="Visualize", command=lambda: controller.show_frame(RegistrationPage))
        registration_button.grid(row=5, column=0)

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

        def resizeFrame(self, y, x):
            self.parent.geometry('{}x{}'.format(y, x))    

class AnalysePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, fg="#000000", text="Analyse Page", font=FONT)
        label.grid(sticky=N)    

        self.vol_layer = 8691600.00

        self.df =  pd.DataFrame()
        self.table = pt = Table(self, dataframe=self.df, showtoolbar=True, showstatusbar=True)
        pt.show()
        
        label_button_21 = ttk.Button(self, text="Browse", command=lambda: controller.getCsv())
        label_button_21.grid(sticky=SW)   
        label_button_22 = ttk.Button(self, text="Clean", command=lambda: controller.show_frame(StartWindow))
        label_button_22.grid(sticky=S) 
        label_button_23 = ttk.Button(self, text="Compute", command=lambda: controller.show_frame(StartWindow))
        label_button_23.grid(sticky=SE) 

        save_button_2 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartWindow))
        save_button_2.grid(row=3, column=2) 

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
        label_41 = Label(self, fg="#000000", text="Registration Page", font=FONT)
        label_41.pack(pady=10, padx=10)

        label_42 = Label(self, text="Output message")
        label_42.pack()

        self.angle = 0

        f = Figure()
    
        label_button_41 = ttk.Button(self, text="Browse", command=lambda: controller.getFile())
        label_button_41.pack()
        label_button_42 = ttk.Button(self, text="Find Angle",  command=lambda: find_angle(controller.template_dir, controller.img_dir, f, self, label_42))
        label_button_42.pack()
        label_button_42 = ttk.Button(self, text="Rotate stack", command=lambda: rotate_stack(controller.raw_tif_dir, controller.src_dir, self.angle, label_42))
        label_button_42.pack()          
        label_button_43 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartWindow))
        label_button_43.pack
        

        f = Figure()

app = App()
app.mainloop()