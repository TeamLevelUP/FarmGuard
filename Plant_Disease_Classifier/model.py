import tensorflow as tf
import numpy as np
import os
from tensorflow import keras
from keras.preprocessing import image
from sklearn.model_selection import train_test_split

# Define the data path
disease_data_path = '/data/05.상추_1.질병'

# Load the images and labels
x, y = [], []
for class_folder in os.listdir(disease_data_path):
    class_path = os.path.join(disease_data_path, class_folder)
    for image_file in os.listdir(class_path):
        img = image.load_img(os.path.join(class_path, image_file), target_size=(224, 224))
        x.append(np.array(img))
        y.append(int(class_folder))

# Convert the data to numpy arrays
x = np.array(x)
y = np.array(y)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Preprocess the data
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

# Build the model
model = keras.Sequential()
model.add(keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(224, 224, 3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(10, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test))

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)