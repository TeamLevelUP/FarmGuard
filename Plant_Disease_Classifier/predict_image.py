import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image

# Load the saved model
# model = keras.models.load_model('model.h5')
model = keras.models.load_model('G:/내 드라이브/TUKorea/캡스톤디자인/model/model.h5')

# Load an image file to classify
img = image.load_img('input_image/common2.jpg', target_size=(224, 224)) # 정상
# img = image.load_img('input_image/disease2.jpeg', target_size=(224, 224)) # 질병

img_array = np.array(img)
img_array = img_array.astype('float32') / 255.0
img_array = np.expand_dims(img_array, axis = 0)

# Use the model to make a prediction
prediction = model.predict(img_array)
predicted_class = np.argmax(prediction[0])

print("Prediction: ", prediction)
print("Predicted class:", predicted_class)