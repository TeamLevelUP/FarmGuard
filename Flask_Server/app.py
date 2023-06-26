# WEB
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os, logging
from dao import selectUsers, appendUsers, getTempVal, getHumVal, getIlumVal
import xml.etree.ElementTree as elemTree
import paho.mqtt.client as mqtt

# AI
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
# from yolov5 import detect
import sys
sys.path.append("C:/FarmGuard/Image_Detection_YOLO")
from yolov5 import detect

app = Flask(__name__)
#Parse XML
tree = elemTree.parse('keys.xml')
app.secret_key = tree.find('string[@name="secret_key"]').text
broker_address = "58.225.135.14"
broker_port = 3456

mqtt = mqtt.Client("PC")
mqtt.connect(broker_address, broker_port)
# mqtt.

# @app.route('/')
# def before_

@app.route('/')
def index():
    # session.pop('userid', None)
    # if len(session) == 0:
    if 'userid' in session:
        # return render_template('index.html', userid = None)
        return render_template('index.html', userid = session['userid'])
    else:
        return render_template('index.html')
        # print(session['userid'])
        # if session['userid']:
        #     return render_template('index.html', userid = session['userid'])
        # else:
        #     return render_template('index.html', userid = None)
# if 'userid' not in session:
#     return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        id_1 = request.form.get('userid1')
        id_2 = request.form.get('userid2')
        id = id_1 + '@' + id_2
        password = request.form.get('userpassword')
        name = request.form.get('username')
        # 확인용
        # print("ID: %s\nPassword: %s\nName: %s" % (id, password, name))
        if not (id_1 and id_2 and password and name):
            return '''
                    <script>
                        // 경고창
                        alert("입력하지 않은 항목이 있습니다.")
                        // 이전페이지로 이동
                        history.back()
                    </script>
                                '''
        elif request.form['userpassword'] != request.form['userpasswordconfirm']:
            return  '''
                    <script>
                        // 경고창
                        alert("비밀번호가 일치하지 않습니다.")
                        // 이전페이지로 이동
                        history.back()
                    </script>
                    '''

        # 회원가입 성공시
        if not selectUsers(id, None):
            appendUsers(id, password, name)
            # 세션 설정
            session['userid'] = id
            session['username'] = name
            return redirect('/')
        # 회원가입 실패시
        else:
            return '''
                <script>
                    // 경고창 
                    alert("중복된 ID가 있습니다.")
                    // 이전페이지로 이동
                    history.back()
                </script>
            '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        uid = request.form.get('userid')
        upw = request.form.get('userpassword')

        row = selectUsers(uid, upw)
        #print(row)
        # print("uid: %s" % uid)
        # print("upw: %s" % upw)

        if row: # 회원이면
            # 세션 설정
            session['userid'] = uid
            session['username'] = row['userName']

            # 페이지 이동
            return redirect('/')
            # return render_template('index.html', userid = uid)
        else:
            # 회원이 아니면 다시 로그인 화면
            return '''
                <script>
                    // 경고창 
                    alert("로그인 실패, 다시 시도하세요")
                    // 이전페이지로 이동
                    history.back()
                </script>
            '''

@app.route('/logout')
def logout():
    session.pop('userid', None)
    # return render_template('index.html', userid = None)
    # print(len(session)) # 0
    return redirect('/')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/myPage')
def myPage():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''
    return render_template('myPage.html', userid = session['userid'], username = session['username'])


@app.route('/myfarm')
def myfarm():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''
    return render_template('myfarm.html', userid = session['userid'])


@app.route('/farmcontrol')
def farmcontrol():
    return render_template('farmcontrol.html', userid=session['userid'])


@app.route('/farmcontrol/ilum', methods=['GET', 'POST'])
def ilumControl():
    # 페이지에서 입력한 조도값 자료형:int
    ilum_data = int(request.form.get('ilumdata'))
    if ilum_data is None:
        return '''
                            <script>
                                // 오류창 
                                alert("데이터를 입력하세요!")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''
    if ilum_data < 0:
        ilum_data = 0
    elif ilum_data > 1023:
        ilum_data = 1023

    # print(ilum_data)

    # MQTT 메시지 전송부분
    mqtt.publish("ilumPoint", ilum_data)
    return '''
                    <script>
                        // 완료창 
                        alert("전송 완료!")
                            // 이전페이지로 이동
                        history.back()
                    </script>
        '''

@app.route('/diseaseIdentification')
def disease():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''
    return render_template('diseaseIdentification.html', userid = session['userid'])

@app.route('/myfarm/temp')
def checkTemp():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''

    sensorVal1 = getTempVal(1)
    sensorVal2 = getTempVal(2)
    sensorVal3 = getTempVal(3)
    sensorVal4 = getTempVal(4)
    sensorVal5 = getTempVal(5)
    sensorVal6 = getTempVal(6)



    temps = [{'time': '1', 'data': sensorVal1['temp'] if sensorVal1 is not None else 0},
             {'time': '2', 'data': sensorVal2['temp'] if sensorVal2 is not None else 0},
             {'time': '3', 'data': sensorVal3['temp'] if sensorVal3 is not None else 0},
             {'time': '4', 'data': sensorVal4['temp'] if sensorVal4 is not None else 0},
             {'time': '5', 'data': sensorVal5['temp'] if sensorVal5 is not None else 0},
             {'time': '6', 'data': sensorVal6['temp'] if sensorVal6 is not None else 0},
             ]

    label = '온도'
    xlabels = []
    dataset = []
    i = 0
    for temp in temps:
        xlabels.append('')
        dataset.append(temp['data'])
        i += 1

    return render_template('temp.html', userid = session['userid'], **locals())



@app.route('/myfarm/hum')
def checkHum():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''

    sensorVal1 = getHumVal(1)
    sensorVal2 = getHumVal(2)
    sensorVal3 = getHumVal(3)
    sensorVal4 = getHumVal(4)
    sensorVal5 = getHumVal(5)
    sensorVal6 = getHumVal(6)


    hums =  [{'time': '1', 'data': sensorVal1['hum'] if sensorVal1 is not None else 0},
             {'time': '2', 'data': sensorVal2['hum'] if sensorVal2 is not None else 0},
             {'time': '3', 'data': sensorVal3['hum'] if sensorVal3 is not None else 0},
             {'time': '4', 'data': sensorVal4['hum'] if sensorVal4 is not None else 0},
             {'time': '5', 'data': sensorVal5['hum'] if sensorVal5 is not None else 0},
             {'time': '6', 'data': sensorVal6['hum'] if sensorVal6 is not None else 0},
             ]

    label = '습도'
    xlabels = []
    dataset = []
    i = 0
    for hum in hums:
        xlabels.append('')
        dataset.append(hum['data'])
        i += 1

    return render_template('hum.html', userid = session['userid'], **locals())


@app.route('/myfarm/ilum')
def checkIlum():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''

    sensorVal1 = getIlumVal(1)
    sensorVal2 = getIlumVal(2)
    sensorVal3 = getIlumVal(3)
    sensorVal4 = getIlumVal(4)
    sensorVal5 = getIlumVal(5)
    sensorVal6 = getIlumVal(6)

    # print(sensorVal1)
    # print(sensorVal2)
    # print(sensorVal3)
    # print(sensorVal4)
    # print(sensorVal5)
    # print(sensorVal6)


    ilums = [{'time': '1', 'data': sensorVal1['ilum'] if sensorVal1 is not None else 0},
           {'time': '2', 'data': sensorVal2['ilum'] if sensorVal2 is not None else 0},
           {'time': '3', 'data': sensorVal3['ilum'] if sensorVal3 is not None else 0},
           {'time': '4', 'data': sensorVal4['ilum'] if sensorVal4 is not None else 0},
           {'time': '5', 'data': sensorVal5['ilum'] if sensorVal5 is not None else 0},
           {'time': '6', 'data': sensorVal6['ilum'] if sensorVal6 is not None else 0},
           ]

    label = '조도'
    xlabels = []
    dataset = []
    i = 0
    for ilum in ilums:
        xlabels.append('')
        dataset.append(ilum['data'])
        i += 1

    return render_template('ilum.html', userid = session['userid'], **locals())

@app.route('/gallery')
def gallery():
    if 'userid' not in session:
        return '''
                            <script>
                                // 경고창 
                                alert("로그인이 필요한 서비스입니다.")
                                    // 이전페이지로 이동
                                history.back()
                            </script>
                '''
    return render_template("gallery.html", userid = session['userid'], **locals())

@app.route('/take_photo')
def take_photo():
    # mqtt를 통한 사진촬영 메시지 전송
    mqtt.publish("camera", "go")
    return '''
                    <script>
                        alert("사진 촬영 완료!")
                            // 이전페이지로 이동
                        history.back()
                    </script>
        '''
    # return render_template()

@app.route('/apiTest')
def apiTest():
    return render_template('apiTest.html', userid = session['userid'])

@app.route('/show')
def show():
    return render_template('show.html', userid = session['userid'])



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'userid' not in session:
        return '''
                    <script>
                        // 경고창 
                        alert("로그인이 필요한 서비스입니다.")
                            // 이전페이지로 이동
                        history.back()
                    </script>
        '''
    # print(request.form)
    # gallery num is posted
    # file의 이름을 파악함
    if 'gallery' in request.form:
        filename = request.form['gallery']
        # print(filename)
        image_path = os.getcwd() + "/static/images/" + filename
        image_path.replace('\\', '/')
        # print(image_path)

    # image is posted
    # file을 저장하고 file의 이름을 파악함
    # elif 'image' in request.form: # 알 수 없는 오류로 request.form을 받아오지 못함
    elif 'image' in request.files:
    # else:
        file = request.files['image']
        # 사진이 업로드되있지 않으면
        if not file:
            return '''
                            <script>
                                // 경고창 
                                alert("이미지 업로드 실패")
                                // 이전페이지로 이동
                                history.back()
                            </script>
                        '''
        # print(secure_filename(file.filename))
        # Save the img file
        filename = secure_filename(file.filename)
        # print(type(filename)) # str
        # print(filename)       # xx.jpg
        # file.save(os.path.join("static/images", "input_image.jpg"))
        file.save(os.path.join("static/images", filename))
    # wrong post
    # return
    else:
        return '''
                            <script>
                                // 경고창
                                alert("ERROR")
                                // 이전페이지로 이동
                                history.back()
                            </script>
                        '''

    yolo_path = "C:/FarmGuard/Image_Detection_YOLO/"
    # yolo학습을 위해 이미지파일 복사

    # print("cp static/images/" + filename + " " + yolo_path + "yolov5/data/images/input_image.jpg")
    # print("mkdir " + yolo_path + "yolov5/data/images") # mkdir C:/FarmGuard/Image_Detection_YOLO/yolov5/data/images
    if not os.path.isdir(yolo_path + "yolov5/data/images"):
        os.mkdir(yolo_path + "yolov5/data/images")
    print("cp static/images/" + filename + " " + yolo_path + "yolov5/data/images/input_image.jpg")

    os.system("cp static/images/" + filename + " " + yolo_path + "yolov5/data/images/input_image.jpg")

    # 기존에 사용한 폴더 지우기
    # print(os.getcwd()) # C:\FarmGuard\Flask_Server
    # os.system("cd yolov5/runs/detect")
    if os.path.isdir(yolo_path + 'yolov5/runs/detect/exp'):
        for file in os.listdir(yolo_path + "yolov5/runs/detect/exp"):
            os.remove(yolo_path + 'yolov5/runs/detect/exp/' + file)
        os.rmdir(yolo_path + 'yolov5/runs/detect/exp')

    # 감지 여부 확인 - 감지 했으면 True 못했으면 False
    opt = detect.parse_opt()
    # detect.main: image detection and save file, return 검출 여부
    is_detected = detect.main(opt)
    # print(is_detected)

    # 이미지에서 상추 검출 안됐을시 리턴
    if not is_detected:
        return '''
                    <script>
                        // 경고창 
                        alert("상추 검출 실패, 다른 이미지로 다시 시도하세요")
                            // 이전페이지로 이동
                        history.back()
                    </script>
        '''

    # keras-이미지에서 상추 검출시 질병 예측 시작

    # Load the saved model
    # model = keras.models.load_model('model/model_class2_epoch7_dropout0.2.h5')
    model = keras.models.load_model('model/model_class3_epoch10_dropout0.2.h5')

    # print(link) # .jpg까지 저장됨
    # img = image.load_img(f'static/images/{filename}', target_size=(224, 224))
    img = image.load_img('static/images/input_image.jpg', target_size=(224, 224))

    img_array = np.array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis = 0)

    # Use the model to make a prediction
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])

    # predict result
    # sclerotiniarot(균핵병) downymildew(노균병)
    disease_list = {0:'정상', 1:'균핵병', 2:'노균병'}
    # print("Prediction: ", prediction)
    # print("Predicted class:", predicted_class)
    predicted_class = int(predicted_class)
    disease_class = disease_list[predicted_class]
    # return redirect(url_for('upload_success', filename = filename, disease_class = disease_class))
    # print(len(session)) # 0

    # 화면에 Bounding Box를 포함한 이미지 출력을 위해 복사
    # os.system("cp yolov5/runs/detect/exp/input_image.jpg static/images/input_image.jpg")
    os.system("cp C:/FarmGuard/Image_Detection_YOLO/yolov5/runs/detect/exp/input_image.jpg static/images/input_image.jpg")

    if 'userid' in session:
        return render_template('success.html',
                               filename = filename, disease_class = disease_class, predicted_class=predicted_class, userid = session['userid'])
    else:
        return render_template('success.html',
                               filename=filename, disease_class=disease_class, predicted_class = predicted_class)


# @app.route('/success/<filename>')
# def upload_success(filename, disease_class):
#     return render_template('success.html', filename = filename, disease_class = disease_class)
#

if __name__ == '__main__':
    app.run(debug = True)
