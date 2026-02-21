import os
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(processed_image):
    prediction = model.predict(processed_image)[0][0]

    if prediction >= 0.5:
        return float(prediction), "REAL"
    else:
        return float(prediction), "FORGED"