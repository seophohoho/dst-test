HOST="192.168.0.8"
SERVER_PORT=43001
LOCAL_PORT = 54321
DEVICE_ID = '999001'

DB_HOST="192.168.0.8"
DB_PORT=3306
DB_USER="root"
DB_PW="root"
DB_NAME="joaelec"

INSERT_QUERY = '''
INSERT INTO sync_device (
    DEVICEID, 
    PROTOCOLTYPE, 
    DEVICENUMBER, 
    DEVICEMNGIPADDR, 
    DEVICEMNGPORT, 
    PINGYN, 
    PINGNUM, 
    TIMESYNCAUTO, 
    TIMESYNCNUM, 
    LEDAUTOYN, 
    LEDSTARTTIME, 
    LEDENDTIME, 
    TEMPAUTOYN, 
    TEMPMINNUM, 
    TEMPMAXNUM, 
    ADDID,
    ADDDATE, 
    ADDTIME, 
    CHANGEID, 
    CHANGEDATE, 
    CHANGETIME, 
    DEVICEUSE, 
    DEVICESTATUS
) 
VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

INSERT_DATA = (
    DEVICE_ID,          #DEVICEID,장비관리번호
    '002',              #PROTOCOLTYPE,통신타입
    '9999-001',         #DEVICENUMBER,장비모델번호
    HOST,               #DEVICEMNGIPADDR,장비관리IP
    str(LOCAL_PORT),    #DEVICEMNGPORT,장비관리포트
    'Y',                #PINGYN,카메라주소요청사용유무
    10,                 #PINGNUM,카메라 PING주기
    'Y',                #TIMESYNCAUTO,시간 정보 전송 사용유무
    10,                 #TIMESYNCNUM,시간동기화 주기 단위 초단위
    'N',                #LEDAUTOYN,LED 자동점등기능 사용유무
    '190000',           #LEDSTARTTIME,LED점등시간
    '070000',           #LEDENDTIME,LED소등시간
    'N',                #TEMPAUTOYN,FAN자동설정
    '25',               #TEMPMINNUM,FAN동작 최저온도(중지)
    '28',               #TEMPMAXNUM,FAN작동온도
    'admin',            #ADDID,등록자 아이디
    '20240529',         #ADDDATE,등록일 (YYYYMMDD)
    '202510',           #ADDTIME,등록시간 (24HHMISS)
    'admin',            #CHANGEID,수정자 아이디
    '20240701',         #CHANGEDATE,수정일 (YYYYMMDD)
    '160247',           #CHANGETIME,수정시간 (24HHMISS)
    'Y',                #DEVICEUSE,관리유무
    'WAIT'              #DEVICESTATUS,장비접속유무
    )

DELETE_QUERY = '''
DELETE FROM sync_device WHERE DEVICEID = %s;
'''
DELETE_DATA = (DEVICE_ID,)