from email.encoders import encode_7or8bit
from flask import *
import mysql.connector
import requests
import time
import jwt
import configparser
config = configparser.ConfigParser()
config.read('config.ini')



orders_sys = Blueprint('orders',__name__,)
def get_token():
    JWT = request.cookies.get('JWT')
    if JWT==None :
        return (None)
    else:
        return(JWT)
def sql_get_data(username):
    mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='qweasdzxc',
    database='taipei_day_trip_website'
    )
    mycursor = mydb.cursor()
    sql="SELECT `id`,`username`,`email` FROM `MEMBER` WHERE `username` = %s "
    val=(username,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    mycursor.close()  
    mydb.close() 
    return(myresult)

def Number():
    mydb = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='qweasdzxc',
        database='taipei_day_trip_website'
        )
    mycursor = mydb.cursor()
    sql="SELECT `id` FROM `ORDER` order by `id` DESC limit 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()  
    mydb.close() 
    maxNumber=myresult[0][0]+1
    maxNumber_st=str(maxNumber)
    nowTime = int(time.time())
    struct_time = time.localtime(nowTime)
    number= time.strftime("%Y%m%d%H%M%S", struct_time)+maxNumber_st
    return(number)
def delet_book():
    response_js=jsonify({"ok":True})
    resp = make_response(response_js)
    resp.set_cookie(key='book', value='', expires=0)
    return resp
def PostOrder(data,user):
    mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='qweasdzxc',
    database='taipei_day_trip_website'
    )
    mycursor = mydb.cursor()
    
    order=data['order']
    contact=data['contact']
    OrderNumber=Number()
    name=contact['name']
    email=contact['email']
    phone=contact['phone']
    price=order['price']
    trip=order['trip']
    attraction=trip['attraction']
    id=attraction['id']
    attraName=attraction['name']
    address=attraction['address']
    image=attraction['image']
    date=trip['date']
    time=trip['time']
    userID=user['id']
    OrderAttracion=id+","+attraName+","+address+","+image

    Usercontact=name+","+email+","+phone
    sql="INSERT INTO `ORDER` (userID,OrderNumber,OrderData,status,date,time,price,contact) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(userID,OrderNumber,OrderAttracion,1,date,time,price,Usercontact)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()  
    mydb.close() 
    return(OrderNumber)
def pay(data,orderNumber):
    
    prime=data['prime']
    order=data['order']
    contact=data['contact']        
    name=contact['name']
    email=contact['email']
    phone=contact['phone']
    price=order['price']
    trip=order['trip']
    date=trip['date']
    time=trip['time']
    appkey=config['datakey']['appkey']
    Merchant=config['datakey']['Merchant']
    paydata={
        "prime":prime,
        "partner_key":appkey,
        "merchant_id":Merchant,
        "details":'test',
        "amount":price,
        "cardholder":{
            "phone_number":phone,
            "name":name,
            "email":email,
            "zip_code":"",
            "address":"",
            "national_id":""
        }    
    }
    paydata_js=json.dumps(paydata)
    headers= {'Content-Type':'application/json','x-api-key':appkey}
    done= requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime",data=paydata_js.encode('utf-8'),headers=headers)
    done_js=done.json()
    payStatus=done_js['status']
    print(done_js)

    if payStatus==0:
        mydb = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='qweasdzxc',
        database='taipei_day_trip_website'
        )
        mycursor = mydb.cursor()
        sql="UPDATE `ORDER` SET `status`= %s WHERE `OrderNumber` = %s "
        val=(0,orderNumber)
        mycursor.execute(sql,val,)
        mydb.commit()
        mycursor.close()  
        mydb.close()
        req={
            "data":{
                "number":orderNumber,
                "payment":{
                    "status":0,
                    "message":"付款成功"
                }
            }
        }
        return(req)
    else:
        req={
            "data":{
                "number":orderNumber,
                "payment":{
                    "status":1,
                    "message":done_js['msg']
                }
            }
        }
        return(req)
def getOrderStatus(ordernumber):
    mydb = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='qweasdzxc',
        database='taipei_day_trip_website'
        )
    mycursor = mydb.cursor()
    sql="SELECT `OrderData`,`status`,`date`,`time`,`price`,`contact` FROM `ORDER` WHERE `OrderNumber` = %s "
    val=(ordernumber,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    mycursor.close()  
    mydb.close() 
    if myresult==None:
        mycursor.close()  
        mydb.close() 
        req={"data":None}
        return(req)
    else:
        OrderData=myresult[0]
        status=myresult[1]
        date=myresult[2]
        time=myresult[3]
        price=myresult[4]
        contact=myresult[5]
        
        OrderData_list=OrderData.split(',')
        id=OrderData_list[0]
        name=OrderData_list[1]
        address=OrderData_list[2]
        image=OrderData_list[3]
        
        contact_list=contact.split(',')
        userName=contact_list[0]
        email=contact_list[1]
        phone=contact_list[2]
        
        req={
            "data":{
                "number":ordernumber,
                "price":price,
                "trip":{
                    "attraction":{
                        "id":id,
                        "name":name,
                        "address":address,
                        "image":image
                    },
                    "date":date,
                    "time":time
                },
                "contact":{
                    "name":userName,
                    'email':email,
                    "phone":phone
                },
                "status":status
            }
        }
        
        
        
        return(req)

    
        
        
        

    
@orders_sys.route('/orders',methods=["POST"])
def getOrder():
    token=get_token()
    if token==None:
        reqdata={"error":True,
              "message":"尚未登入系統"
        }
        return jsonify(reqdata)
    else:
        token_decode=jwt.decode(token, "secret", algorithms=["HS256"])   
        username=token_decode["username"]
        get_data=sql_get_data(username)
        Userdata={"id":get_data[0],"name":get_data[1],"email":get_data[2]}
        
    data=request.get_json()
    OrderNumber=PostOrder(data,Userdata)
    reqStatus=pay(data,OrderNumber)
    reqStatus_js=jsonify(reqStatus)
    resp = make_response(reqStatus_js)
    resp.set_cookie(key='book', value='', expires=0)
    
    
    print(resp)
    return (resp)
@orders_sys.route('/orders/<orderNumber>',methods=["GET"])
def getOrderNumber(orderNumber):
    token=get_token()
    if token==None:
        reqdata={"error":True,
              "message":"尚未登入系統"
        }
        return jsonify(reqdata)
    else:
        token_decode=jwt.decode(token, "secret", algorithms=["HS256"])   
        username=token_decode["username"]
        get_data=sql_get_data(username)
        Userdata={"id":get_data[0],"name":get_data[1],"email":get_data[2]}
        req=getOrderStatus(orderNumber)

        return jsonify(req)