import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def model_predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    model = load_model('./model.py')

    x = image.img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    if preds < 0.24:
        return True
    else:
        return False
    return preds
