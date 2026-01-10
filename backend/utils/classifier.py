from sklearn.ensemble import RandomForestClassifier
import numpy as np

model = RandomForestClassifier()

def classify(features):
    features = np.array(features).reshape(1, -1)
    return model.predict(features)
