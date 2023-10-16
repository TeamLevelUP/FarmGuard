import paho.mqtt.client as mqtt
import base64
import os
# print(os.path.abspath('.')) # C:\FarmGuard\IoT_Controller\RPI
import time
import sys
import shutil
sys.path.append("C:/FarmGuard/Flask_Server")
from dao import appendTempVal, appendHumVal, appendIlumVal
# from ...Flask_Server.dao import appendTempVal, appendHumVal, appendIlumVal # 상대경로 불가

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    # temp = 0; hum = 0; ilum = 0
    # global temp; global hum; global ilum;
    #수신 받은 mqtt 메시지 내용을 str로 변환

    # message의 topic을 비교하여 저장기능 수행
    if msg.topic == "temp":
        temp = str(msg.payload.decode("utf-8"))
        print(msg.topic, temp)
        temp = int(temp)
        appendTempVal(temp)
    elif msg.topic == "hum":
        hum = str(msg.payload.decode("utf-8"))
        print(msg.topic, hum)
        hum = int(hum)
        appendHumVal(hum)
    elif msg.topic == "ilum":
        ilum = str(msg.payload.decode("utf-8"))
        print(msg.topic, ilum)
        ilum = int(ilum)
        appendIlumVal(ilum)
    elif msg.topic == "test":
        with open("output.bin", "wb") as file:
            print(type(msg.payload))
            file.write(msg.payload)
        file = open('output.bin', 'rb')
        byte = file.read()
        file.close()
        print("recv complete.")

        decodeit = open("output.png","wb")
        decodeit.write(base64.b64decode((byte)))
        decodeit.close()
        
        gallery_image_num = 5
        gallery_path = "C:/FarmGuard/Flask_Server/static/images/"
        # print(os.path.isfile("output.png"))
        if(os.path.isfile("output.png")):
            # os.system("ls")
            for i in range(1, gallery_image_num):
                # print("cp %sgallery%d.jpg %sgallery%d.jpg" % (gallery_path, i+1, gallery_path, i))
                # os.system("cp %sgallery%d.jpg %sgallery%d.jpg" % (gallery_path, i+1, gallery_path, i))
                gallery_image_name_back = "%sgallery%d.jpg" % (gallery_path, i+1)
                gallery_image_name_front = "%sgallery%d.jpg" % (gallery_path, i)
                shutil.copy(gallery_image_name_back, gallery_image_name_front)
            # os.system("cd C:/FarmGuard/IoT_Controller/RPI")
            # os.system("cp output.png C:/FarmGuard/Flask_Server/static/images/gallery5.jpg")
            shutil.copy("output.png", "C:/FarmGuard/Flask_Server/static/images/gallery5.jpg")
        # db에 추가
        # appendSensorVal(temp, hum, ilum)
    # time.sleep(5)
    else :
        print(msg.payload)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("localhost", 1883, 60)
# client.connect("58.225.135.14", 3456, 60)
client.connect("192.168.23.143", 1883, 60)


client.loop_forever()
