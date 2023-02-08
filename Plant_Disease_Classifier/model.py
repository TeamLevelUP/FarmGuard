import tensorflow as tf
import numpy as np
import os
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Define the data path
# os.chdir(os.path.dirname(__file__))
data_path = 'data'

# Load the images and labels
x, y = [], []
for class_folder in os.listdir(data_path):
    class_path = os.path.join(data_path, class_folder)
    for image_file in os.listdir(class_path):
        img = image.load_img(os.path.join(class_path, image_file), target_size=(224, 224))
        x.append(np.array(img))
        y.append(int(class_folder))

# plt.figure(figsize=(10, 10))
# for i in range(16):
#     ax = plt.subplot(4, 4, i + 1)
#     plt.imshow(x[i].astype("uint8"))
#     plt.title(y[i])
#     plt.axis("off")
# plt.show()

# Convert the data to numpy arrays
x = np.array(x)
y = np.array(y)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

# Preprocess the data
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Convert class vectors to binary class matrices
# One-Hot Encoding ex) 5 = [0, 0, 0, 0, 0, 1]
y_train = keras.utils.to_categorical(y_train, 3)
y_test = keras.utils.to_categorical(y_test, 3)

# Build the model
model = keras.Sequential()
# 필터 구성
# 컨볼루션 2D 레이어: 필터로 특징을 뽑아냄
#
# 필터의 개수 = 32, 필터의 크기 = (3, 3), padding(입출력 개수) = same (or valid)
# activation(활성화 함수) = relu(rectifier 함수, 은닉층에 주로 쓰입니다.), input_shape(입출력형태, 첫 레이어에서만 정의) = (224, 224, 3)
model.add(keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(224, 224, 3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(keras.layers.Flatten())
# 출력 뉴런의 수 = 64
model.add(keras.layers.Dense(64, activation = 'relu'))
# 출력 뉴런의 수 = 10, 'softmax': 소프트맥스 함수, 다중 클래스 분류 문제에서 출력층에 주로 쓰입니다.
model.add(keras.layers.Dense(3, activation = 'softmax'))
# model.add(keras.layers.Dense(1, activation = 'sigmoid'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test))

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)

# Save the model to a file
model.save('model.h5')
