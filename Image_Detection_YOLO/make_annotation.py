import os
import json
import time

label_path = 'data/2.Validation/라벨링데이터/05.상추'
# images, tags, labels = [], [], []

# Define the classes
desease_dict = {0:"normal", 9:"downymildew", 10:"sclerotiniarot"}
# downymildew:노균병 sclerotiniarot:균핵병

# 라벨 불러오기
folder_num = 1
another_disease_num = 0
start = time.time()  # 라벨 불러오는 시간 측정
# print(os.listdir(label_path)) ['1', '0']

# 파일경로 xtl,ytl,xbr,ybr,class_id 로 구성된 annotation 파일
f_annotation = open("keras_yolo3/train.txt", "w")

for class_folder in os.listdir(label_path):
    class_path = os.path.join(label_path, class_folder)
    # print(class_path) # G:/내 드라이브/TUKorea/캡스톤디자인/data/1.Training/라벨링데이터/05.상추\0
    label_num = 1
    for label_file in os.listdir(class_path):
        # 진행도
        print("Find label now...    folder %d / %d  image %d / %d" %
              (folder_num, len(os.listdir(label_path)), label_num, len(os.listdir(class_path))))

        # json형태의 라벨링데이터 파일 열기
        with open(class_path + "/" + label_file, 'r') as f_json:
            json_data = json.load(f_json)
        # print("here is:\n" + json.dumps(json_data))

        # json 파일에서 disease class 가져오기
        # print(json_data["annotations"]["disease"])
        disease_class = json_data["annotations"]["disease"]

        # 다른 작물의 질병이 나오는거 같아서 체크
        if disease_class != 0 and disease_class != 9 and disease_class != 10:
            another_disease_num += 1
            print("count another disease")
        elif disease_class == 9 or disease_class == 10:
            disease_class -= 8

        # 원본파일 경로 구하기
        file_path = "C:/FarmGuard/Image_Detection_YOLO/" + class_path.replace("라벨링데이터", "원천데이터") + "/" + str(label_file).replace(".json", "")
        file_path = file_path.replace("\\", "/")
        # print(file_path) # 원본파일경로
        # print("rounding box points")
        # print(json_data["annotations"]["points"][0]["xtl"], json_data["annotations"]["points"][0]["ytl"],
        #       json_data["annotations"]["points"][0]["xbr"], json_data["annotations"]["points"][0]["ybr"])

        # json 파일에서 rounding box 좌표 가져오기
        xtl = str(json_data["annotations"]["points"][0]["xtl"]); ytl = str(json_data["annotations"]["points"][0]["ytl"])
        xbr = str(json_data["annotations"]["points"][0]["xbr"]); ybr = str(json_data["annotations"]["points"][0]["ybr"])

        # annotation
        annotation_line = "%s %s,%s,%s,%s,%d" % (file_path, xtl, ytl, xbr, ybr, disease_class)
        # print(annotation_line)

        # annotation 입력
        f_annotation.write(annotation_line + "\n")
        label_num += 1
    folder_num += 1

f_annotation.close()
time_to_find_label = time.time() - start
print("num of another disease: %d" % another_disease_num)
print("time to train label: %d min %d sec" % (time_to_find_label / 60, time_to_find_label % 60))