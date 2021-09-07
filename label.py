from toolbox import *
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()
IMAGEJ_PATH = filedialog.askdirectory( title = "Local ImageJ Directory ...")
IN_DIR = filedialog.askdirectory( title = "Choose Raw Tomography images Directory ...")
OUT_DIR = filedialog.askdirectory( title = "Choose Destination Directory for processed images...")
TOMO_LABELS_DIR = filedialog.askdirectory( title = "Choose Destination Directory for Labels...")
root.destroy()

label(IMAGEJ_PATH, IN_DIR, OUT_DIR, TOMO_LABELS_DIR)
