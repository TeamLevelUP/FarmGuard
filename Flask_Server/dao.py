import pymysql as my
import xml.etree.ElementTree as elemTree

# Parse XML
tree = elemTree.parse('keys.xml')
conn = None

try:
    conn = my.connect(host='localhost',  # 로컬 주소
                      user='root',
                      password=tree.find('string[@name="SQL_PASS"]').text,
                      database='user',  # DB 스키마 이름
                      cursorclass=my.cursors.DictCursor  # 명령어 입력을 위한 커서
                      )
except Exception as e:
    print('접속오류', e)

cursor = conn.cursor()


def closeConnection():
    if conn:
        conn.close()
    # print('종료')


def selectUsers(uid, upw):
    row = None  # 쿼리 결과
    # sql 실행문
    if upw is None:
        sql = '''
        SELECT * FROM user WHERE userID = %s;
        '''
        # 쿼리 실행
        cursor.execute(sql, uid)
    else:
        sql = '''
        SELECT * FROM user WHERE userID = %s AND userPassword = %s;
        '''
        # 쿼리 실행
        cursor.execute(sql, (uid, upw))
    row = cursor.fetchone()
    # print( row )
    # 결과 리턴
    return row


def appendUsers(uid, upw, uname):
    sql = '''
    INSERT INTO user VALUES
        (%s, %s, %s);
    '''
    # 쿼리 실행 후 커밋
    cursor.execute(sql, (uid, upw, uname))
    conn.commit()


def appendSensorVal(temp, hum, ilum):
    MAX_SENSOR_VAL = 6
    sql = '''
            SELECT * FROM sensorval;
            '''
    cursor.execute(sql)
    row = cursor.fetchall()
    # print(len(row))
    id = len(row) + 1

    # 최대값보다 적으면 그냥 삽입
    if id < MAX_SENSOR_VAL + 1:
        sql = '''
        INSERT INTO sensorval VALUES
        (%s, %s, %s, %s);    
        '''
        # 쿼리 실행
        cursor.execute(sql, (id, temp, hum, ilum))
    # 최대값이면 한칸씩 밀기
    else:
        for i in range(1, MAX_SENSOR_VAL):
            sql = '''
            SELECT * FROM sensorval WHERE id = %s;
            '''
            cursor.execute(sql, i + 1)
            # _, temp_back, hum_back, ilum_back = cursor.fetchone()
            # print(temp_back, hum_back, ilum_back)
            row_back = cursor.fetchone()
            # print(row_back)
            print(row_back)

            sql = '''
            UPDATE sensorval SET temp = %s, hum = %s, ilum = %s WHERE id = %s;
            '''
            # cursor.execute(sql, (temp_back, hum_back, ilum_back, i))
            cursor.execute(sql, (row_back['temp'], row_back['hum'], row_back['ilum'], i))
        sql = '''
        UPDATE sensorval SET temp = %s, hum = %s, ilum = %s WHERE id = %s;
             '''
        cursor.execute(sql, (temp, hum, ilum, id - 1))

    # 커밋
    conn.commit()


def getSensorVal(id):
    sql = '''
            SELECT temp, hum, ilum FROM sensorval WHERE id = %s;
            '''
    cursor.execute(sql, id)
    row = cursor.fetchone()
    return row


def appendTempVal(temp):
    MAX_SENSOR_VAL = 6
    sql = '''
            SELECT * FROM tempVal;
            '''
    cursor.execute(sql)
    row = cursor.fetchall()
    # print(len(row))
    id = len(row) + 1

    # 최대값보다 적으면 그냥 삽입
    if id < MAX_SENSOR_VAL + 1:
        sql = '''
        INSERT INTO tempVal VALUES
        (%s, %s);
        '''
        # 쿼리 실행
        cursor.execute(sql, (id, temp))
    # 최대값이면 한칸씩 밀기
    else:
        for i in range(1, MAX_SENSOR_VAL):
            sql = '''
            SELECT * FROM tempVal WHERE id = %s;
            '''
            cursor.execute(sql, i + 1)
            # _, temp_back, hum_back, ilum_back = cursor.fetchone()
            # print(temp_back, hum_back, ilum_back)
            row_back = cursor.fetchone()
            # print(row_back)
            print(row_back)

            sql = '''
            UPDATE tempVal SET temp = %s WHERE id = %s;
            '''
            # cursor.execute(sql, (temp_back, hum_back, ilum_back, i))
            # print("row_back['temp']")
            # print(row_back['temp'])
            # print("i")
            # print(i)
            cursor.execute(sql, (row_back['temp'], i))
        sql = '''
            UPDATE tempVal SET temp = %s WHERE id = %s;
             '''
        cursor.execute(sql, (temp, id - 1))

    # 커밋
    conn.commit()


def appendHumVal(hum):
    MAX_SENSOR_VAL = 6
    sql = '''
            SELECT * FROM humVal;
            '''
    cursor.execute(sql)
    row = cursor.fetchall()
    # print(len(row))
    id = len(row) + 1

    # 최대값보다 적으면 그냥 삽입
    if id < MAX_SENSOR_VAL + 1:
        sql = '''
        INSERT INTO humVal VALUES
        (%s, %s);
        '''
        # 쿼리 실행
        cursor.execute(sql, (id, hum))
    # 최대값이면 한칸씩 밀기
    else:
        for i in range(1, MAX_SENSOR_VAL):
            sql = '''
            SELECT * FROM humVal WHERE id = %s;
            '''
            cursor.execute(sql, i + 1)
            # _, temp_back, hum_back, ilum_back = cursor.fetchone()
            # print(temp_back, hum_back, ilum_back)
            row_back = cursor.fetchone()
            # print(row_back)
            print(row_back)

            sql = '''
            UPDATE humVal SET hum = %s WHERE id = %s;
            '''
            # cursor.execute(sql, (temp_back, hum_back, ilum_back, i))
            cursor.execute(sql, (row_back['hum'], i))
        sql = '''
            UPDATE humVal SET hum = %s WHERE id = %s;
             '''
        cursor.execute(sql, (hum, id - 1))

    # 커밋
    conn.commit()


def appendIlumVal(ilum):
    MAX_SENSOR_VAL = 6
    sql = '''
            SELECT * FROM ilumVal;
            '''
    cursor.execute(sql)
    row = cursor.fetchall()
    # print(len(row))
    id = len(row) + 1

    # 최대값보다 적으면 그냥 삽입
    if id < MAX_SENSOR_VAL + 1:
        sql = '''
        INSERT INTO ilumVal VALUES
        (%s, %s);
        '''
        # 쿼리 실행
        cursor.execute(sql, (id, ilum))
    # 최대값이면 한칸씩 밀기
    else:
        for i in range(1, MAX_SENSOR_VAL):
            sql = '''
            SELECT * FROM ilumVal WHERE id = %s;
            '''
            cursor.execute(sql, i + 1)
            # _, temp_back, hum_back, ilum_back = cursor.fetchone()
            # print(temp_back, hum_back, ilum_back)
            row_back = cursor.fetchone()
            # print(row_back)

            sql = '''
            UPDATE ilumVal SET ilum = %s WHERE id = %s;
            '''
            # cursor.execute(sql, (temp_back, hum_back, ilum_back, i))
            cursor.execute(sql, (row_back['ilum'], i))
        sql = '''
            UPDATE ilumVal SET ilum = %s WHERE id = %s;
             '''
        cursor.execute(sql, (ilum, id - 1))

    # 커밋
    conn.commit()


def getTempVal(id):
    sql = '''
            SELECT temp FROM tempVal WHERE id = %s;
            '''
    cursor.execute(sql, id)
    row = cursor.fetchone()
    return row


def getHumVal(id):
    sql = '''
            SELECT hum FROM humVal WHERE id = %s;
            '''
    cursor.execute(sql, id)
    row = cursor.fetchone()
    return row


def getIlumVal(id):
    sql = '''
            SELECT ilum FROM ilumVal WHERE id = %s;
            '''
    cursor.execute(sql, id)
    row = cursor.fetchone()
    return row


if __name__ == '__main__':
    # 테스트
    # row = selectUsers('rlaalstn1969@naver.com', '1234')
    # print('회원 조회 결과 : ', row)
    # 비회원 테스트(회원이 아님, 비번이 틀림, 아이디 틀림)
    # row = selectUsers('minsoo', 'wrong_password')
    # print('회원 조회 결과 : ', row)
    pass