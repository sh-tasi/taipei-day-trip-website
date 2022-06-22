
from flask import *
import jwt
import time
import mysql.connector



member_sys = Blueprint('member_sys',__name__,)
def check_data(username,password,email):
    for ch in password:
        if '\u4e00' <= ch <= '\u9fa5':
            resp={"error":True,"message":"請勿輸入中文"}
            resp_js=jsonify(resp)
            return(resp_js)
    for ch in email:
        if '\u4e00' <= ch <= '\u9fa5':
            resp={"error":True,"message":"請勿輸入中文"}
            resp_js=jsonify(resp)
            return(resp_js)
    if username==None or password==None or email==None:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    elif len(username)==0 or len(password)==0 or len(email)==0 or username.isspace()==True or password.isspace()==True or email.isspace() or "@"  not in email :
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    elif len(username)>25 or len(password)>25 or len(email)>60:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    else:
        return("ok")
def check_data_login(email,password):
    for ch in password:
        if '\u4e00' <= ch <= '\u9fa5':
            resp={"error":True,"message":"請勿輸入中文"}
            resp_js=jsonify(resp)
            return(resp_js)
    for ch in email:
        if '\u4e00' <= ch <= '\u9fa5':
            resp={"error":True,"message":"請勿輸入中文"}
            resp_js=jsonify(resp)
            return(resp_js)
    if email==None or password==None:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    elif len(password)==0 or len(email)==0 or password.isspace()==True or email.isspace()==True or "@" not in email:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    elif len(password)>25 or len(email)>60:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    else:
        return("ok")
def check_data_change_password(newpassword,oldpassword):
    for ch in newpassword:
        if '\u4e00' <= ch <= '\u9fa5':
            resp={"error":True,"message":"請勿輸入中文"}
            resp_js=jsonify(resp)
            return(resp_js)
    for ch in oldpassword:
        if '\u4e00' <= ch <= '\u9fa5':
            resp={"error":True,"message":"請勿輸入中文"}
            resp_js=jsonify(resp)
            return(resp_js)
    if newpassword==None or oldpassword==None:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    elif len(newpassword)==0 or len(oldpassword)==0 or newpassword.isspace()==True or oldpassword.isspace()==True:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
        return(resp_js)
    elif len(oldpassword)>25 or len(newpassword)>25:
        resp={"error":True,"message":"資料格式不符合"}
        resp_js=jsonify(resp)
            
        return(resp_js)
    else:
        return("ok")
def set_token(username):
    encoded_jwt = jwt.encode({"username": username}, "secret", algorithm="HS256")
    response_js=jsonify({"ok":True})
    resp = make_response (response_js)
    resp.set_cookie(key='JWT', value=encoded_jwt, expires=time.time()+60*60*24,httponly=True)
    return resp
def get_token():
    JWT = request.cookies.get('JWT')
    print(JWT)
    if JWT==None :
        return (None)
    else:
        return(JWT)
def delet_token():
    response_js=jsonify({"ok":True})
    resp = make_response(response_js)
    resp.set_cookie(key='JWT', value='', expires=0)
    return resp
def sql_check_email(email):
    mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='qweasdzxc',
    database='taipei_day_trip_website'
    )
    mycursor = mydb.cursor()
    sql = "SELECT `email` FROM `MEMBER` WHERE `email` = %s"
    email_sql = (email, )
    mycursor.execute(sql, email_sql)
    myresult = mycursor.fetchall()
    if email_sql in myresult:
        mycursor.close()    
        mydb.close()
        resp={"error":True,"message":"信箱已被註冊"}
        resp_js=jsonify(resp)
        return (resp_js)
    else :
        mycursor.close()    
        mydb.close()
        return("ok")
def sql_register(email,username,password):
    # mydb = mysql.connector.connect(
    # host='localhost',
    # port='3306',
    # user='root',
    # password='qweasdzxc',
    # database='taipei_day_trip_website'
    # )
    cnx = mysql.connector.connect(pool_name = "mypool")
    mycursor = cnx.cursor()
    sql="INSERT INTO `MEMBER` (username,email,password) VALUES(%s,%s,%s)"
    val=(username,email,password)
    mycursor.execute(sql, val)
    cnx.commit()
    mycursor.close()  
    cnx.close() 
    resp={"ok":True}
    resp_js=jsonify(resp)
    return (resp_js)
def sql_longin(email,password):
    # mydb = mysql.connector.connect(
    # host='localhost',
    # port='3306',
    # user='root',
    # password='qweasdzxc',
    # database='taipei_day_trip_website'
    # )
    cnx = mysql.connector.connect(pool_name = "mypool")
    mycursor = cnx.cursor()
    sql="SELECT `email`,`password`,`username` FROM `MEMBER` WHERE `email` = %s "
    val=(email,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    mycursor.close()  
    cnx.close() 
    if myresult==None:
        return("error")
    else:
        print(myresult)
        check_email=myresult[0]
        check_passwrod=myresult[1]
        username=myresult[2]
        if password==check_passwrod and email==check_email:
            return (username)
        else:
            return("error")
def sql_get_data(username):
    # mydb = mysql.connector.connect(
    # host='localhost',
    # port='3306',
    # user='root',
    # password='qweasdzxc',
    # database='taipei_day_trip_website'
    # )
    cnx = mysql.connector.connect(pool_name = "mypool")
    mycursor = cnx.cursor()
    sql="SELECT `id`,`username`,`email` FROM `MEMBER` WHERE `username` = %s "
    val=(username,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    mycursor.close()  
    cnx.close() 
    return(myresult)
     
def decodeUser(token):
    token_decode=jwt.decode(token, "secret", algorithms=["HS256"])   
    username=token_decode["username"]
    get_data=sql_get_data(username)
    data={"id":get_data[0],"name":get_data[1],"email":get_data[2]}
    return (data)  

def changeUserPassword(userID,newPassword):
    cnx = mysql.connector.connect(pool_name = "mypool")
    mycursor = cnx.cursor()
    sql = "UPDATE `MEMBER` SET `password` = %s WHERE `id` = %s"
    val = (newPassword,userID)
    mycursor.execute(sql,val)
    cnx.commit()
    mycursor.close()
    cnx.close()
    rep={"ok":True}
    return(rep)
def checkPassword(userID,oldPassword):
    cnx = mysql.connector.connect(pool_name = "mypool")
    mycursor = cnx.cursor()
    sql ="SELECT `password` FROM `MEMBER` WHERE `id` = %s "
    val=(userID,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    password=myresult[0]
    mycursor.close()
    cnx.close()
    if password==oldPassword:
        req="ok"
    else:
        req="error"
        
    return(req)
    
    
    
    

@member_sys.route('/user',methods=["GET"])
def getuser():
    token=get_token()
    if token==None:
        data={"data":None}
        return jsonify(data)
    else:
        token_decode=jwt.decode(token, "secret", algorithms=["HS256"])   
        username=token_decode["username"]
        get_data=sql_get_data(username)
        data={"id":get_data[0],"name":get_data[1],"email":get_data[2]}
        response={"data":data}  
        return jsonify(response), 200

@member_sys.route('/user',methods=["POST"])
def registeruser():
    data=request.get_json()
    username=data['username']
    email=data['email']
    password=data['password']
    check=check_data(username,password,email)
    if check !="ok":
        return(check),500
    check_email=sql_check_email(email)
    if check_email=="ok":
        resp=sql_register(email,username,password)
        return(resp),200
    else:
        return(check_email),400
@member_sys.route('/user',methods=["PATCH"])
def loginuser():
    data=request.get_json()
    email=data['email']
    password=data['password']
    check=check_data_login(email,password)
    if check!="ok":
        return(check),500
    login=sql_longin(email,password)
    if login=="error":
        resp={"error":True,"message":"帳號或密碼輸入錯誤"}
        resp_js=jsonify(resp)
        return(resp_js)
    else:
        return(set_token(login))
      
@member_sys.route('/user',methods=["DELETE"])
def logoutuser():
    resp=delet_token()
    return (resp)

@member_sys.route('/user/changePassword',methods=["POST"])
def changePassword():
    token=get_token()
    if token==None:
        data={"error":True,"message":"尚未登入系統"}
        return jsonify(data)
    else:
        userData=decodeUser(token)
        userID=userData['id']
        data=request.get_json()
        newPassword=data['newPassword']
        oldPassword=data['oldPassword']
        reqDataCheck=check_data_change_password(newPassword,oldPassword)
        if reqDataCheck=="ok":
            check=checkPassword(userID,oldPassword)
            if check=="ok":
                rep=changeUserPassword(userID,newPassword)
                return jsonify(rep),200
            else:
                rep={"error":True,"message":"舊密碼錯誤"}
                return jsonify(rep),400
        else:
            return (reqDataCheck),400
    
    





