import os
import json
import time

label_path = 'datasets/train/lettuce_13932/annotations'
# label_path = 'datasets/val/annotations'
# images, tags, labels = [], [], []

# Define the classes
# disease_dict = {0:"normal", 9:"downymildew", 10:"sclerotiniarot"}
# disease_dict = {0: "normal"}
# downymildew:노균병 sclerotiniarot:균핵병

# 라벨 불러오기
# folder_num = 1
label_num = 1

# start = time.time()  # 라벨 불러오는 시간 측정


for label_file in os.listdir(label_path):
    # 진행도
    print("Find label now...    image %d / %d" %
          (label_num, len(os.listdir(label_path))))

    # json형태의 라벨링데이터 파일 열기
    with open(label_path + "/" + label_file, 'r') as f_json:
        json_data = json.load(f_json)
    # print("here is:\n" + json.dumps(json_data))

    # json 파일에서 disease class 가져오기
    # print(json_data["annotations"]["disease"])
    # disease_class = json_data["annotations"]["disease"]

    # 원본파일 경로 구하기
    file_path = "C:/FarmGuard/Image_Detection_YOLO/" + label_path.replace("labels", "images")\
                + "/" + str(label_file).replace(".json", "")
    file_path = file_path.replace("\\", "/")
    # print(file_path) # 원본파일경로
    # print("rounding box points")
    # print(json_data["annotations"]["points"][0]["xtl"], json_data["annotations"]["points"][0]["ytl"],
    #       json_data["annotations"]["points"][0]["xbr"], json_data["annotations"]["points"][0]["ybr"])


    # json 파일에서 rounding box 좌표를 가져와 중심좌표/가로/세로 길이 구하기
    width = json_data["description"]["width"]
    height = json_data["description"]["height"]

    x_center = ((json_data["annotations"]["points"][0]["xtl"] +
                 json_data["annotations"]["points"][0]["xbr"]) / 2) / width
    y_center = ((json_data["annotations"]["points"][0]["ytl"] +
                 json_data["annotations"]["points"][0]["ybr"]) / 2) / height

    width_norm  = (json_data["annotations"]["points"][0]["xbr"] -
                   json_data["annotations"]["points"][0]["xtl"]) / width
    height_norm = (json_data["annotations"]["points"][0]["ybr"] -
                   json_data["annotations"]["points"][0]["ytl"]) / height

    # annotation
    # annotation_line = "%s %s,%s,%s,%s,%d" % (file_path, xtl, ytl, xbr, ybr, disease_class)
    annotation_line = "0 %f %f %f %f" % (x_center, y_center, width_norm, height_norm)
    # print(annotation_line)

    # annotation 입력
    with open(label_path.replace("annotations", "labels") + "/" +
              label_file.replace("jpg.json", "txt"), 'w') as f_annotation:
        f_annotation.write(annotation_line)
    label_num += 1

# f_annotation.close()
# time_to_find_label = time.time() - start
# print("time to make label: %d min %d sec" % (time_to_find_label / 60, time_to_find_label % 60))
print("make label complete.")