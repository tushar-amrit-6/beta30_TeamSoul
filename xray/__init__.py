import os
import cv2
import numpy as np
import keras
import tensorflow as tf
from keras.layers import *
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.utils import np_utils
from keras.models import model_from_json


def xray_predict(image):
    model = tf.lite.TFLiteConverter.from_keras_model('.')
    # model = load_model('model_covid.h5')
    model._make_predict_function()
    frame = cv2.imread(image)
    test_data = cv2.resize(frame, (224, 224))

    test_data = np.array(test_data)
    test_data.shape = (1, 224, 224, 3)

    zz = model.predict(test_data)

    if zz[0][0] < 0.24:
        return True
    else:
        return False
    cv2.destroyAllWindows()
    return True


if __name__ == '__main__':
    print(xray_predict('aa.jpeg'))
