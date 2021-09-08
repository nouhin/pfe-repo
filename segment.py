from skimage import io
import numpy as np
import tensorflow as tf
import keras_applications
from keras.models import load_model
import segmentation_models_3D as sm
from patchify import patchify, unpatchify
from tifffile import imsave

BACKBONE = 'vgg16'  #Try vgg16, efficientnetb7, inceptionv3, resnet50
my_model = load_model('model/3D_model_vgg16_100epochs_1.h5', compile=False)

large_image = io.imread('demo/265x265x265_image.tif')
patches = patchify(large_image, (64, 64, 64), step=64)  #Step=256 for 256 patches means no overlap

preprocess_input = sm.get_preprocessing(BACKBONE)

predicted_patches = []
for i in range(patches.shape[0]):
  for j in range(patches.shape[1]):
    for k in range(patches.shape[2]):
      single_patch = patches[i,j,k, :,:,:]
      single_patch_3ch = np.stack((single_patch,)*3, axis=-1)
      single_patch_3ch_input = preprocess_input(np.expand_dims(single_patch_3ch, axis=0))
      single_patch_prediction = my_model.predict(single_patch_3ch_input)
      single_patch_prediction_argmax = np.argmax(single_patch_prediction, axis=4)[0,:,:,:]
      predicted_patches.append(single_patch_prediction_argmax)

predicted_patches = np.array(predicted_patches)

predicted_patches_reshaped = np.reshape(predicted_patches, 
                                        (patches.shape[0], patches.shape[1], patches.shape[2],
                                         patches.shape[3], patches.shape[4], patches.shape[5]) )

reconstructed_image = unpatchify(predicted_patches_reshaped, large_image.shape)

reconstructed_image=reconstructed_image.astype(np.uint8)

imsave('demo/segmented.tif', reconstructed_image)

from apeer_ometiff_library import io

num_segments=3
segm0 = (reconstructed_image == 0)
segm1 = (reconstructed_image == 1)
segm2 = (reconstructed_image == 2)

final = np.empty((reconstructed_image.shape[0], reconstructed_image.shape[1], reconstructed_image.shape[2], num_segments))
final[:,:,:,0] = segm0
final[:,:,:,1] = segm1
final[:,:,:,2] = segm2

final = np.expand_dims(final, axis=0)
final=np.swapaxes(final, 2, 4)

final = final.astype(np.int8)

io.write_ometiff("demo/segmented_multi_channel.ome.tiff", final)