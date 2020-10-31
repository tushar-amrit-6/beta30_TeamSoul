import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH ='xray/model.h5'

# Load your trained model
model = load_model(MODEL_PATH)

def model_predict(img_path, model=model):
    img = image.load_img(img_path, target_size=(224, 224))

    x = image.img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    if preds < 0.24:
        return True
    else:
        return False
    return preds    

if __name__ == "__main__":
    print(model_predict('aa.jpeg', model=model))