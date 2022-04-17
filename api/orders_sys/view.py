from email.encoders import encode_7or8bit
from itertools import count
from flask import *
# import mysql.connector.pooling
import mysql.connector
import requests
import time

import jwt
import configparser
import math
# from pool import cnxpool

config = configparser.ConfigParser()
config.read('config.ini')
# dbconfig = {
#     "host":"localhost",
#     "port":"3306",
#     "user":"root",
#     "password":"qweasdzxc",
#     "database":"taipei_day_trip_website"
# }

# start = time.perf_counter()
# cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
#                                                       pool_size = 10,
#                                                       pool_reset_session=True,
#                                                       **dbconfig)

# end = time.perf_counter()


# print("order pool 連線建立完成"+str(end - start))




# cnx = cnxpool.get_connection()
orders_sys = Blueprint('orders',__name__,)
def get_token():
    JWT = request.cookies.get('JWT')
    if JWT==None :
        return (None)
    else:
        return(JWT)
def sql_get_data(username):
    # mydb = mysql.connector.connect(
    # host='localhost',
    # port='3306',
    # user='root',
    # password='qweasdzxc',
    # database='taipei_day_trip_website'
    # )
    # start = time.perf_counter()
    # cnx = cnxpool.get_connection()    
    cnx = mysql.connector.connect(pool_name = "mypool")
    cursor = cnx.cursor()
    # mycursor=mydb.cursor()
    sql="SELECT `id`,`username`,`email` FROM `MEMBER` WHERE `username` = %s "
    val=(username,)
    cursor.execute(sql,val)
    myresult=cursor.fetchone()
    cursor.close()  
    cnx.close()
    # end = time.perf_counter()
    # print("資料庫取得帳號時間:"+str(end - start))
    # mydb.close()
    return(myresult)

def addOrderNumber():
    # mydb = mysql.connector.connect(
    #     host='localhost',
    #     port='3306',
    #     user='root',
    #     password='qweasdzxc',
    #     database='taipei_day_trip_website'
    # #     )
    # start = time.perf_counter()
    # cnx = cnxpool.get_connection()    
    cnx = mysql.connector.connect(pool_name = "mypool")
    cursor = cnx.cursor()
    sql="SELECT `id` FROM `ORDER` order by `id` DESC limit 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    cursor.close()  
    cnx.close() 
    maxNumber=myresult[0][0]+1
    maxNumber_st=str(maxNumber)
    nowTime = int(time.time())
    struct_time = time.localtime(nowTime)
    number = time.strftime("%Y%m%d%H%M%S", struct_time)+maxNumber_st
    # print("資料庫新增訂單號碼時間:"+str(end - start))
    return(number)
def clearShoppingCart(req):
    resp = make_response(req)
    resp.set_cookie(key='book', value='', expires=0)
    return resp
def postOrder(data,user):
    # mydb = mysql.connector.connect(
    # host='localhost',
    # port='3306',
    # user='root',
    # password='qweasdzxc',
    # database='taipei_day_trip_website'
    # )
    # start = time.perf_counter()
    # cnx = cnxpool.get_connection()  
    cnx = mysql.connector.connect(pool_name = "mypool")  
    cursor = cnx.cursor()
    order=data['order']
    contact=data['contact']
    orderNumber=addOrderNumber()
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
    times=trip['time']
    userID=user['id']
    orderAttracion=id+","+attraName+","+address+","+image

    userContact=name+","+email+","+phone
    sql="INSERT INTO `ORDER` (userID,OrderNumber,OrderData,status,date,time,price,contact) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(userID,orderNumber,orderAttracion,1,date,times,price,userContact)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()  
    cnx.close()
    # end = time.perf_counter()
    # print("資料庫新增訂單時間:"+str(end - start)) 
    return(orderNumber)
def payOrder(data,orderNumber):
    
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
    # print(done_js)

    if payStatus==0:
        # mydb = mysql.connector.connect(
        # host='localhost',
        # port='3306',
        # user='root',
        # password='qweasdzxc',
        # database='taipei_day_trip_website'
        # )
        # cnx = cnxpool.get_connection() 
        cnx = mysql.connector.connect(pool_name = "mypool")   
        cursor = cnx.cursor()
        sql="UPDATE `ORDER` SET `status`= %s WHERE `OrderNumber` = %s "
        val=(0,orderNumber)
        cursor.execute(sql,val,)
        cnx.commit()
        cursor.close()  
        cnx.close()
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
    # mydb = mysql.connector.connect(
    #     host='localhost',
    #     port='3306',
    #     user='root',
    #     password='qweasdzxc',
    #     database='taipei_day_trip_website'
    #     )
    # cnx = cnxpool.get_connection()
    cnx = mysql.connector.connect(pool_name = "mypool")    
    cursor = cnx.cursor()
    sql="SELECT `OrderData`,`status`,`date`,`time`,`price`,`contact` FROM `ORDER` WHERE `OrderNumber` = %s "
    val=(ordernumber,)
    cursor.execute(sql,val)
    myresult=cursor.fetchone()
    cursor.close()  
    cnx.close() 
    if myresult==None:
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
def decodeUser(token):
    token_decode=jwt.decode(token, "secret", algorithms=["HS256"])   
    username=token_decode["username"]
    get_data=sql_get_data(username)
    data={"id":get_data[0],"name":get_data[1],"email":get_data[2]}
    return (data)  
    
def sql_get_user_order(userId,page,maxPage):
    cnx = mysql.connector.connect(pool_name = "mypool")
    cursor = cnx.cursor()
    sql="SELECT `OrderNumber`,`OrderData`,`status`,`date`,`time`,`price`,`contact` FROM `ORDER` WHERE `userID` = %s ORDER BY `DATA_CREATE_TIME`DESC LIMIT "
    val=(userId,)
    sql_page=10*page
    sql_add_page=sql+" "+str(sql_page)+","+"10"
    cursor.execute(sql_add_page,val)
    myresult=cursor.fetchall()
    cursor.close()  
    cnx.close()
    thisPageOrderDataList=[]
    for i in range(len(myresult)):
        thisOrder=myresult[i]
        orderNumber=thisOrder[0]
        orderData=thisOrder[1]
        
        orderData_list=orderData.split(',')
        id=orderData_list[0]
        name=orderData_list[1]
        address=orderData_list[2]
        image=orderData_list[3]
        
        orderStatus=thisOrder[2]
        orderDate=thisOrder[3]
        orderTime=thisOrder[4]
        orderPrice=thisOrder[5]
        orderContact=thisOrder[6]
        
        orderContact_list=orderContact.split(',')
        ordererUserName=orderContact_list[0]
        orderUserEmail=orderContact_list[1]
        orderUserPhone=orderContact_list[2]
        thisOrderData={
            "number":orderNumber,
            "price":orderPrice,
            "trip":{
                "attraction":{
                    "id":id,
                    "name":name,
                    "address":address,
                    "image":image
                },
            "date":orderDate,
            "time":orderTime,
            },
            "contact":{
                "name":ordererUserName,
                "email":orderUserEmail,
                "phone":orderUserPhone
            },
            "status":orderStatus
        }        
        thisPageOrderDataList.append(thisOrderData)
    if page<maxPage:
        nextPage=page+1
    elif page==maxPage:
        nextPage=None
    else :
        nextPage=None
        thisPageOrderDataList=None
    reponse={"nextPage":nextPage,"data":thisPageOrderDataList}
    return(reponse) 
def sql_get_user_all_order_count(userId):
    cnx = mysql.connector.connect(pool_name = "mypool")
    cursor = cnx.cursor()
    sql="SELECT count(*)FROM  `ORDER` WHERE `userID` = %s "
    val=(userId,)  
    cursor.execute(sql,val)
    order_count=cursor.fetchall()
    order_count=order_count[0][0]           #所有資料總數
    order_maxpage=order_count/10            #10筆為一頁資料量
    order_maxpage=math.ceil(order_maxpage)-1  #最大頁數(僅從第0頁開始，最大頁數-1) 
    cursor.close()
    cnx.close()   
    return(order_maxpage)
    
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
        userData={"id":get_data[0],"name":get_data[1],"email":get_data[2]}
        
    data=request.get_json()
    orderNumber=postOrder(data,userData)
    orderPaymentStatus=payOrder(data,orderNumber)
    orderPaymentStatus_js=jsonify(orderPaymentStatus)
    resp = clearShoppingCart(orderPaymentStatus_js)
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
@orders_sys.route('/orders/allOrder',methods=["GET"])
def getUserOrder():
    token=get_token()
    if token==None:
        data={"error":True,"message":"尚未登入系統"}
        return jsonify(data)
    else:
        userData=decodeUser(token)
        page=request.args.get("page","0")
        page_int=int(page)
        userId=userData['id']
        orderMaxPage=sql_get_user_all_order_count(userId)
        rep=sql_get_user_order(userId,page_int,orderMaxPage)
     
    return jsonify(rep)