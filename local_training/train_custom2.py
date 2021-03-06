# -*- coding: utf-8 -*-
"""train_custom2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u_cPbXAJULhctDybjY-LiJrlAqKmnXrj

# Train simple vision model for phishing detection

## Mount and extract
"""
##
##from google.colab import drive
##drive.mount('./gdrive')
##
##!unzip -q ./gdrive/MyDrive/phi_dataset.zip -d /content

"""## Imports"""

import numpy as np
import os
import pathlib
##import PIL
##import PIL.Image
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.models import Sequential

dataset_dir = pathlib.Path("phi_dataset/")
model_dir = pathlib.Path('phi_models/')
checkpoint_dir = pathlib.Path('phi_checkpoints/')

os.listdir(dataset_dir)

import datetime
date = datetime.datetime.now()
date = '_'.join(str(date).split()).replace(':', ';')
print(date)

"""## Params"""

model_name = "custom2"
batch_size = 10
img_height = 512
img_width = 720

"""## Load dataset"""

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  dataset_dir,
  validation_split=0.2,
  subset="training",
  label_mode = 'binary',
  seed=132,
  image_size=(img_height, img_width),
  batch_size=batch_size)

rest_ds = tf.keras.preprocessing.image_dataset_from_directory(
  dataset_dir,
  validation_split=0.2,
  subset="validation",
  label_mode='binary',
  seed=132,
  image_size=(img_height, img_width),
  batch_size=batch_size)

rest_batches = rest_ds.cardinality()
print(rest_batches)

val_ds = rest_ds.skip(int(2108 * 0.2 // batch_size))
test_ds = rest_ds.take(int(2108 * 0.2 // batch_size))

class_names = train_ds.class_names

print(class_names)

"""## Visualize data"""

import matplotlib.pyplot as plt
##plt.figure(figsize=(20, 50))
##for images, labels in train_ds.take(1):
##  for i in range(16):
##    ax = plt.subplot(8, 2, i + 1)
##    plt.imshow(images[i].numpy().astype("uint8"))
##    plt.title(class_names[int(labels[i])])
##    plt.axis("off")

"""## Tune dataset"""

AUTOTUNE = tf.data.AUTOTUNE

# train_ds = train_ds.cache().shuffle(20).prefetch(buffer_size=AUTOTUNE)
train_ds = train_ds.shuffle(200).prefetch(buffer_size=AUTOTUNE)
# val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
# test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

"""## Model"""

num_classes = 2
reg_rate1 = 0.005
reg_rate2 = 0.001
dropout_prob1 = 0.2
dropout_prob2 = 0.3
model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(32, 3, padding='same', activation='relu', activity_regularizer=regularizers.l2(reg_rate1)),
  # layers.MaxPool2D(pool_size=(1,2)),
  layers.MaxPool2D(),
  layers.Dropout(dropout_prob1),
  layers.Conv2D(64, 3, padding='same', activation='relu', activity_regularizer=regularizers.l2(reg_rate1)),
  layers.MaxPool2D(),
  layers.Dropout(dropout_prob1),
  layers.Conv2D(64, 2, padding='same', activation='relu', activity_regularizer=regularizers.l2(reg_rate2)),
  layers.MaxPool2D(),
  layers.Dropout(dropout_prob2),
  layers.Conv2D(128, 2, padding='same', activation='relu', activity_regularizer=regularizers.l2(reg_rate2)),
  layers.MaxPool2D(),
  layers.Dropout(dropout_prob2),
  layers.Conv2D(128, 2, padding='same', activation='relu', activity_regularizer=regularizers.l2(reg_rate2)),
  layers.MaxPool2D(),
  layers.Dropout(dropout_prob2),
  layers.Flatten(),
  layers.Dense(512, activation='relu', activity_regularizer=regularizers.l1(reg_rate2)),
  layers.Dense(num_classes-1, activity_regularizer=regularizers.l1(reg_rate2))
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

"""## Training"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        # Path where to save the model
        # The two parameters below mean that we will overwrite
        # the current checkpoint if and only if
        # the `val_loss` score has improved.
        # The saved model name will include the current epoch.
        filepath=checkpoints_dir / f"{date}_{model_name}_valacc{{val_accuracy:.4f}}_e{{epoch}}",
        save_best_only=True,  # Only save a model if `val_loss` has improved.
##        save_freq=2,
        monitor="val_loss",
        verbose=1,
    ),
    keras.callbacks.EarlyStopping(
        # Stop training when `val_loss` is no longer improving
        monitor="val_loss",
        # "no longer improving" being defined as "no better than 1e-2 less"
        min_delta=1e-3,
        # "no longer improving" being further defined as "for at least 2 epochs"
        patience=4,
        verbose=1,
    )
]

resume_epoch=0
##resume_epoch=5
##resume_chkp_path = checkpoint_dir / "2021-07-24_02:22:00.400711_custom2_valacc0.8936_e4"

os.listdir(checkpoint_dir)

# resume_chkp_path = tf.train.latest_checkpoint(checkpoint_dir / "2021-07-24_02:22:00.400711_custom2_valacc0.8948_e7")
##print(resume_chkp_path)

epochs=3
if resume_epoch:
  # resume_chkp_path = tf.train.latest_checkpoint(checkpoint_dir)
  model.load_weights(resume_chkp_path)
  print(f"Resuming from {resume_chkp_path}")
  # model = keras.models.load_model(resume_chkp_path)

history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs,
  initial_epoch=resume_epoch,
  callbacks=callbacks
)

resume_epoch = history.epoch[-1]

"""## Save model"""

val_acc = history.history['val_accuracy']
model.save(str(model_dir / f"{date}_{model_name}_valacc{val_acc[-1]:0.4f}_e{len(val_acc)}_b{batch_size}_w{img_width}_h{img_height}.tf"),
           include_optimizer=True)

"""## Load model"""

### change filename to the model you want to load
##model_filename = "2021-07-23_10:41:26.182203_custom1_valacc0.9185_e4_b16.tf"
##model2 = keras.models.load_model(
##    str(model_dir / model_filename),
##    compile=True)

"""## Visulaize loss and acc"""

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

# epochs_range = range(epochs)
epochs_range = history.epoch

plt.figure(figsize=(20, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

"""## Evaluate (test)"""

val_results = model.evaluate(test_ds, batch_size=256)
print("val loss, val acc:", val_results)

results = model.evaluate(test_ds, batch_size=256)
print("test loss, test acc:", results)
