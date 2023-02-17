import pymysql as my

conn = None
try:
    conn = my.connect(      host        ='localhost',       # 로컬 주소
                            user        ='root',    
                            password    ='password',
                            database    ='user',        # DB 스키마 이름
                            cursorclass = my.cursors.DictCursor # 명령어 입력을 위한 커서
                            )
except Exception as e:
    print('접속오류', e)

cursor = conn.cursor()

def closeConnection():
    if conn:      
        conn.close()
    # print('종료')

def selectUsers(uid, upw):
    row        = None # 쿼리 결과
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

if __name__ == '__main__':
    # 테스트
    # row = selectUsers('rlaalstn1969@naver.com', '1234')
    # print('회원 조회 결과 : ', row)
    # 비회원 테스트(회원이 아님, 비번이 틀림, 아이디 틀림)
    # row = selectUsers('minsoo', 'wrong_password')
    # print('회원 조회 결과 : ', row)
    pass