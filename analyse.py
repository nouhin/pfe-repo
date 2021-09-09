from toolbox import *
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()
TOMO_LABELS_DIR = filedialog.askdirectory( title = "Choose Destination Directory for Modified Labels...")
file = filedialog.askopenfilename(title="Choose a .dat file")

root.destroy()

df = load_tomo_data(file)
df = clean_tomo_data(df)
df.to_csv(TOMO_LABELS_DIR +"/output.xlsx")

new_df = compute_indicators_porosity_level(df, 8691600.00)
new_df.to_csv(TOMO_LABELS_DIR +"/output2.xlsx")


