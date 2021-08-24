import os
import re
import imutils
import fnmatch
import numpy as np
import pandas as pd
import cv2 as cv
import tifffile as tifio
import imagej
from scipy.spatial.distance import pdist


def extact_labels(IMAGEJ_dir, src_dir, dest_dir, labels_dir):
    ij = imagej.init(IMAGEJ_dir)
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

def load_labels_file(part_number, labels_dir):
    filename = re.match(part_number)
    csv_path = os.path.join(labels_dir, filename)
    df = pd.read_csv(csv_path, delimiter=" ")
    filename = os.path.splitext(filename)[0]
    return df, filename

def clean_labels_file(df):
  df = df[['xg', 'yg', 'zg', 'volpix','volmarch', 'sphericity']]
  df = df.sort_values('zg', ascending=False)
  df = df[ df["volpix"] != df["volpix"].max()]
  return df

def dist(df):
    return sum(pdist(df.values, 'euclid'))
  
def compute_indicators_porosity_level(df, vol_layer):
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
  return new_df 

# df, filename  = load_labels_file(part_number, labels_dir)
# df =  clean_labels_file(df)
# df.to_csv(labels_dir +"/"+filename)

extact_labels('/home/spi-2019-34/Téléchargements/Fiji.app', '/home/spi-2019-34/testing/TTT', '/home/spi-2019-34/testing/TTT/out', '/home/spi-2019-34/testing/TTT/labels')