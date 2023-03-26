# import tensorflow as tf
import numpy as np
import os
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import time

# Define the data path
# 학습데이터: 정상 10,765장 / 질병 3,167장
# data_path = 'data'
data_path = 'G:/내 드라이브/TUKorea/캡스톤디자인/data/1.Training/원천데이터/05.상추'
images, tags = [], []


# Load the images
folder_num = 1
start = time.time() # 이미지 불러오는 시간 측정
for class_folder in os.listdir(data_path):
    class_path = os.path.join(data_path, class_folder)
    image_num = 1
    for image_file in os.listdir(class_path):
        print("Find image now...    folder %d / %d  image %d / %d" %
              (folder_num, len(os.listdir(data_path)), image_num, len(os.listdir(class_path))))
        img = image.load_img(os.path.join(class_path, image_file), target_size=(224, 224))
        images.append(np.array(img))
        tags.append(int(class_folder))
        image_num += 1
    folder_num += 1
time_to_find_image = time.time() - start


# print("time to find image: %d sec" % (time.time() - start))

# 학습자료 시각화

# plt.figure(figsize=(10, 10))
# for i in range(16):
#     ax = plt.subplot(4, 4, i + 1)
#     plt.imshow(x[i].astype("uint8"))
#     plt.title(y[i])
#     plt.axis("off")
# plt.show()

# Convert the data to numpy arrays
images = np.array(images)
tags = np.array(tags)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(images, tags, test_size = 0.2, random_state = 42)

# Preprocess the data
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Convert class vectors to binary class matrices
# One-Hot Encoding ex) 5 = [0, 0, 0, 0, 0, 1]
y_train = keras.utils.to_categorical(y_train, 2)
y_test = keras.utils.to_categorical(y_test, 2)

start = time.time() # 모델 훈련하는 시간 측정
# Build the model
model = keras.Sequential()
# 필터 구성
# 컨볼루션 2D 레이어: 필터로 특징을 뽑아냄

# 필터의 개수 = 32, 필터의 크기 = (3, 3), padding(입출력 개수) = same (or valid)
# activation(활성화 함수) = relu(rectifier 함수, 은닉층에 주로 쓰입니다.)
model.add(keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(224, 224, 3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(keras.layers.Flatten())
# 출력 뉴런의 수 = 64
model.add(keras.layers.Dense(64, activation = 'relu'))
# 출력 뉴런의 일부만 사용 - 과적합 방지를 위함
model.add(keras.layers.Dropout(0.2))
# 출력 뉴런의 수 = 2, 'softmax': 소프트맥스 함수, 다중 클래스 분류 문제에서 출력층에 주로 쓰입니다.
model.add(keras.layers.Dense(2, activation = 'softmax'))
# model.add(keras.layers.Dense(2, activation = 'sigmoid'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(x_train, y_train, batch_size = 32, epochs = 10, validation_data = (x_test, y_test))
time_to_train_model = time.time() - start
# print("time to train model: %d sec" % (time.time() - start))

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)

# Save the model to a file
model.save('model.h5')


# Convert lite file - 필요한지 아직 모름
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()
# with open("model.tflite", "wb") as f:
#     f.write(tflite_model)

# Check the time
print("time to find image: %d min %d sec" % (time_to_find_image / 60, time_to_find_image % 60))
print("time to train model: %d min %d sec" % (time_to_train_model / 60, time_to_train_model % 60))

# Plot the training and validation accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot the training and validation loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
