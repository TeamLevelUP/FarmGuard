import cv2
import matplotlib.pyplot as plt
from glob import glob

img_paths = glob("C:/FarmGuard/Image_Detection_YOLO/data/myface.jpg")

img = cv2.imread(img_paths[0])
plt.figure(figsize=(10,6))
plt.imshow(img)
# plt.show()

import yaml

with open("/content/dataset/data.yaml", 'r') as f:
  data = yaml.load(f, Loader=yaml.FullLoader)

data['train'] = "/content/dataset/"
data['test'] = "/content/dataset/"
data['val'] = "/content/dataset/"

with open("/content/dataset/data.yaml", 'w') as f:
  yaml.dump(data, f)