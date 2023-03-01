import os
import json
from keras_yolo3.yolo import YOLO

# Define paths and parameters
train_data_path = 'path/to/train/data'
val_data_path = 'path/to/validation/data'
annotation_file = 'path/to/annotations.json'
classes_path = os.getcwd() + 'keras_yolo3/model_data/desease_classes.txt'
anchors_path = os.getcwd() + 'keras_yolo3/model_data/yolo_anchors.txt'
log_dir = 'path/to/logs'
pretrained_weights = 'path/to/pretrained/weights.h5'
epochs = 100
batch_size = 32

# Load annotations from JSON file
with open(annotation_file, 'r') as f:
    # json 파일을 읽어서 " 파일경로 xmin,ymin,xmax,ymax,class_id " << 이거를 여러줄 반복하는 형식으로 바꿔주기
    annotations = json.load(f)

# Load list of classes
# 0:정상 1:노균병 2:균핵병
with open(classes_path, 'r') as f:
    class_names = f.read().splitlines()

# Load list of anchors
with open(anchors_path, 'r') as f:
    anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    anchors = [(anchors[i], anchors[i+1]) for i in range(0, len(anchors), 2)]

# Define YOLO model
yolo = YOLO(model_path=None, anchors=anchors, classes=class_names)

# Train on custom data using train.py script
os.system('python train.py --model_path {} --anchors_path {} --classes_path {} '
          '--annotation_file {} --log_dir {} --epochs {} --batch_size {} '
          '--input_shape 416'.format(pretrained_weights, anchors_path, classes_path,
                                      annotation_file, log_dir, epochs, batch_size))
