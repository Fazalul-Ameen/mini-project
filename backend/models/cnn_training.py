import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# ==============================
# CONFIG
# ==============================

DATASET_PATH = "datasets"
IMG_SIZE = 128
BATCH_SIZE = 16
EPOCHS = 30
MODEL_PATH = "model.h5"

# ==============================
# DATA PREPROCESSING
# ==============================

train_gen = ImageDataGenerator(rescale=1./255)
val_gen = ImageDataGenerator(rescale=1./255)
test_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    "datasets/train",
    target_size=(128,128),
    batch_size=32,
    class_mode="binary"
)

val_data = val_gen.flow_from_directory(
    "datasets/val",
    target_size=(128,128),
    batch_size=32,
    class_mode="binary"
)

test_data = test_gen.flow_from_directory(
    "datasets/test",
    target_size=(128,128),
    batch_size=32,
    class_mode="binary",
    shuffle=False
)
# ==============================
# CNN MODEL
# ==============================

model = Sequential([

    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),

    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ==============================
# SAVE BEST MODEL
# ==============================

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

# ==============================
# TRAIN MODEL
# ==============================

early = EarlyStopping(patience=5, restore_best_weights=True)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=[early]
)

print("\n✅ Training Completed.")
print("Model saved as model.h5")

# ==============================
# PLOT GRAPHS
# ==============================

# Accuracy Plot
plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Validation"])
plt.savefig("accuracy_graph.png")
plt.show()

# Loss Plot
plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["Train", "Validation"])
plt.savefig("loss_graph.png")
plt.show()

print("📊 Graphs saved as accuracy_graph.png and loss_graph.png")

#-------------------------------
#metrics
#-------------------------------


# Predict
preds = model.predict(test_data)
pred_classes = (preds > 0.5).astype("int32")

true_classes = test_data.classes

# Confusion matrix
cm = confusion_matrix(true_classes, pred_classes)
print("Confusion Matrix:\n", cm)

# Classification report
report = classification_report(true_classes, pred_classes, target_names=["REAL","FORGED"])
print(report)




# Accuracy graph
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.legend(["Train", "Validation"])
plt.savefig("accuracy.png")
plt.clf()

# Loss graph
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.legend(["Train", "Validation"])
plt.savefig("loss.png")
plt.clf()

# Confusion matrix heatmap
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig("confusion_matrix.png")

print(model.summary())