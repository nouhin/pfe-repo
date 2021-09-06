from toolbox import *

# code that will load files / paths)

label(IMAGEJ_PATH, IN_DIR, OUT_DIR, TOMO_LABELS_PATH, file_number)

df, filename  = load_tomo_data(file_number, TOMO_LABELS_PATH)
df = clean_tomo_data(df)
df.to_csv(TOMO_LABELS_PATH +"/"+filename)

new_df = compute_indicators_porosity_level(df, vol_layer)

