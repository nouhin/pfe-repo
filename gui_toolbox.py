import os
import re
import imutils
import fnmatch
import numpy as np
import pandas as pd
import cv2 as cv
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tifffile as tifio
import imagej
from scipy.spatial.distance import pdist
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog
from pandastable import Table, TableModel


def test(f, self):
    a = f.add_subplot(111)
    a.plot([1,2,6,7,9,5], [7,8,9,6,4,8])
    canvas = FigureCanvasTkAgg(f, self)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

def find_angle(template_dir, img_dir, f, self, label_42):
    template = cv.imread(template_dir)
    template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    _, template = cv.threshold(template, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    (tH, tW) = template.shape[:2]

    image = cv.imread(img_dir)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, gray_th = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    for angle in np.arange(0, 360, 1):
        rotated = imutils.rotate(gray_th, angle)
        result = cv.matchTemplate(template, rotated, cv.TM_CCOEFF_NORMED)
        threshold = 0.70
        loc = np.where(result >= threshold)
        i = len(list(zip(*loc[::-1])))
        if i > 0:
            label_42.config(text="match found \n found correct angle : "+ str(angle))
            clone = np.dstack([rotated, rotated, rotated])
            a = f.add_subplot(111)
            a.imshow(clone)
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
            self.angle = angle
            break
        if i == 0:
            label_42.config(text="testing diffrent angle : "+ str(angle))

def rotate_stack(src_tif_dir, dest_tif_dir, angle, label_42):
    tif = tifio.imread(src_tif_dir)
    tif_file = os.path.basename(src_tif_dir)
    assert len(tif) != 0, "No images were loaded"
    tif_th = []
    tif_processed = os.path.join(dest_tif_dir, tif_file [:len(tif_file) - 4] + "_rotated.tif")
    for idx, slice in enumerate(tif):
        slice = imutils.rotate(slice, angle)
        tif_th.append(slice)
    cv.imwritemulti(tif_processed, tif_th) 
    label_42.config(text="Stack rotated and saved click browse to process other stacks")    

def extact_labels(IMAGEJ_dir, src_dir, dest_dir, labels_dir):
    ij = imagej.init(IMAGEJ_dir, headless=False)
    tif_paths = []
    listOfFiles = os.listdir(src_dir)
    pattern = "*.tif"

    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern) and not fnmatch.fnmatch(entry, ".*"):
            print(entry)
            # selects tif files and appends them to a list
            tif_paths.append(entry)

    for index, tif in enumerate(tif_paths):
        # iterate over tif files
        # etval, mats = cv.imreadmulti(tif, flags=cv.IMREAD_GRAYSCALE)
        mats = tifio.imread(tif)
        assert len(mats) != 0, "No images were loaded"
        mats_th = []
        tif_processed = os.path.join(dest_dir, tif[:len(tif) - 4] + "_binary_" + str(index+1) + ".tif")
        for idx, mat in enumerate(mats):
            # iterates over all slices in each tif files
            mat = cv.fastNlMeansDenoising(mat, h=10, templateWindowSize=7, searchWindowSize=21)  # denoise
            _, gray_th = cv.threshold(mat, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # threshold
            # gray_th = imutils.rotate(gray_th, angles[index])  # rotate
            mats_th.append(gray_th)
        cv.imwritemulti(tif_processed, mats_th)

    for index, tif in enumerate(os.listdir(dest_dir)):
    
        ij_img = ij.io().open(dest_dir+'/'+ tif)
        ij.ui().show('image', ij_img)

        plugin = 'Labeling'

        args = {
            'color' :0,
            'minimum' :0,
            '3d' :6
            }
        ij.py.run_plugin(plugin,args)

        tif = os.path.splitext(tif)[0]
        plugin = 'Parameters'
        args =  {
            'save' : '/'+ labels_dir + "Labels_" +tif+ ".dat"
        }
        ij.py.run_plugin(plugin,args)

        ij.dispose()

def clean_labels_file(self, csv_file_dir):
    df = pd.read_csv(csv_file_dir, delimiter=" ")
    df = df[['xg', 'yg', 'zg', 'volpix','volmarch', 'sphericity']]
    df = df.sort_values('zg', ascending=False)
    df = df[ df["volpix"] != df["volpix"].max()]
    self.df = df

def dist(df):
    return sum(pdist(df.values, 'euclid'))
  
def compute_indicators_porosity_level(df, vol_layer, self):
    # occurrence frequency
    mu1 = pd.DataFrame(df.pivot_table(index=['numLayer'], aggfunc='size')).rename(columns = {0:'mu1'})
    mu1_norm = (mu1-mu1.mean())/mu1.std()

    # propotion of affected zone 
    mu2 = pd.DataFrame(df.groupby('numLayer')['volmarch'].sum().div(vol_layer)).rename(columns = {'volmarch':'mu2'})
    mu2_norm = (mu2-mu2.mean())/mu2.std()

    # average distance between pores
    mu1_serie = df.pivot_table(index=['numLayer'], aggfunc='size')
    mu3 = pd.DataFrame(df.groupby('numLayer')[['xg','yg']].apply(lambda x: dist(x)).div(mu1_serie)).rename(columns = {0:'mu3'})
    mu3_norm = (mu3-mu3.mean())/mu3.std()

    # porosity level
    mu = pd.DataFrame(mu2_norm['mu2'].mul(mu1_norm['mu1']).div(mu3_norm['mu3'])).rename(columns = {0:'mu'})
  
    # normalised porosity level
    normalised_mu = (mu-mu.min())/(mu.max()-mu.min())
    normalised_mu_V2 = (mu-mu.mean())/mu.std()
    new_df = pd.concat([mu1, mu2, mu3,normalised_mu], axis=1)
    self.df = df


# df, filename  = load_labels_file(part_number, labels_dir)
# df =  clean_labels_file(df)
# df.to_csv(labels_dir +"/"+filename)

#extact_labels('/home/spi-2019-34/Téléchargements/Fiji.app', '/home/spi-2019-34/pfe-repo', '/home/spi-2019-34/pfe-repo/dest_data', '/home/spi-2019-34/pfe-repo/labels_data')


# df = pd.read_csv("/home/spi-2019-34/pfe-repo/sample1_label.dat", delimiter=" ")
# df = clean_labels_file(df)

# df.to_csv("cleaned_labels.csv")