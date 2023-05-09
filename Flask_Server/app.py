# WEB
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os, logging
from dao import selectUsers, appendUsers
import xml.etree.ElementTree as elemTree

# AI
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import sys
# sys.path.append("/yolov5-master")
from yolov5 import detect

app = Flask(__name__)
#Parse XML
tree = elemTree.parse('keys.xml')
app.secret_key = tree.find('string[@name="secret_key"]').text

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
        
        # print("uid: %s" % uid)
        # print("upw: %s" % upw)
        
        if row: # 회원이면
            # 세션 설정
            session['userid'] = uid
            
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

@app.route('/myfarm')
def myfarm():
    return render_template('myfarm.html', userid = session['userid'])

@app.route('/myfarm/temp')
def checkTemp():
    temps = [{'time': '1', 'data': 28.5},
             {'time': '2', 'data': 29.5},
             {'time': '3', 'data': 22.5},
             {'time': '4', 'data': 23.5},
             {'time': '5', 'data': 25.5},
             {'time': '6', 'data': 27.5},
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
    hums = [{'time': '1', 'data': 40},
            {'time': '2', 'data': 41},
            {'time': '3', 'data': 40},
            {'time': '4', 'data': 41},
            {'time': '5', 'data': 43},
            {'time': '6', 'data': 43},
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
    ilums = [{'time': '1', 'data': 4783},
             {'time': '2', 'data': 4889},
             {'time': '3', 'data': 4932},
             {'time': '4', 'data': 4959},
             {'time': '5', 'data': 4999},
             {'time': '6', 'data': 5003},
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
    return render_template("gallery.html", userid = session['userid'], **locals())

@app.route('/upload', methods=['POST'])
def upload_file():
    # gallery num is posted
    # file의 이름을 파악함
    if 'gallery' in request.form:
        filename = request.form['gallery']
        # print(filename)
        # print(os.getcwd() + "/static/images/" + filename)
        image_path = os.getcwd() + "/static/images/" + filename
        image_path.replace('\\', '/')

    # image is posted
    # file을 저장하고 file의 이름을 파악함
    elif 'image' in request.form:
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
        file.save(os.path.join("static/images", "input_image.jpg"))
        # file.save(os.path.join("static/images", filename))
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

    # yolo학습을 위해 이미지파일 복사
    os.system("cp static/images/" + filename + " yolov5/data/images/input_image.jpg")

    # 기존에 사용한 폴더 지우기
    # print(os.getcwd()) # C:\FarmGuard\Flask_Server
    # os.system("cd yolov5/runs/detect")
    if os.path.isdir('yolov5/runs/detect/exp'):
        for file in os.listdir("yolov5/runs/detect/exp"):
            os.remove('yolov5/runs/detect/exp/' + file)
        os.rmdir('yolov5/runs/detect/exp')

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

    # Load an image file to classify
    # img = image.load_img('input_image/common2.jpg', target_size=(224, 224)) # 정상
    # img = image.load_img('input_image/disease2.jpeg', target_size=(224, 224)) # 질병

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
    disease_list = {0:'normal', 1:'sclerotiniarot', 2:'downymildew'}
    # print("Prediction: ", prediction)
    # print("Predicted class:", predicted_class)
    disease_class = disease_list[int(predicted_class)]
    # return redirect(url_for('upload_success', filename = filename, disease_class = disease_class))
    # print(len(session)) # 0
        
    # 화면에 Bounding Box를 포함한 이미지 출력을 위해 복사
    os.system("cp yolov5/runs/detect/exp/input_image.jpg static/images/input_image.jpg")

    if 'userid' in session:
        return render_template('success.html',
                               filename = filename, disease_class = disease_class, userid = session['userid'])
    else:
        return render_template('success.html',
                               filename=filename, disease_class=disease_class)


# @app.route('/success/<filename>')
# def upload_success(filename, disease_class):
#     return render_template('success.html', filename = filename, disease_class = disease_class)
#

if __name__ == '__main__':
    app.run(debug = True)
