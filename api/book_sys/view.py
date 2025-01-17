
from flask import *
import time
import json
import mysql.connector.pooling
import mysql.connector

# dbconfig = {
#     "host":"localhost",
#     "port":"3306",
#     "user":"root",
#     "password":"qweasdzxc",
#     "database":"taipei_day_trip_website"
# }
# start = time.perf_counter()
# cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "order_sys_pool",
#                                                       pool_size = 15,
#                                                       pool_reset_session=True,
#                                                       **dbconfig)
# cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "order_sys_pool")
# end = time.perf_counter()


# print("book pool 連線建立完成"+str(end - start))

book_sys = Blueprint('book_sys',__name__,)
def get_token():
    JWT = request.cookies.get('JWT')
    if JWT==None :
        return (None)
    else:
        return(JWT)
def post_book(data):
    response_js=jsonify({"ok":True})
    data_str = json.dumps(data)
    resp = make_response (response_js)
    resp.set_cookie(key='book', value=data_str,expires=time.time()+60*60,httponly=True)
    return resp
def get_book():  
    book = request.cookies.get('book')
    if book == None :
        return(None)
    else:
        book_dict = json.loads(book) 
        return(book_dict)
def delet_book():
    response_js=jsonify({"ok":True})
    resp = make_response(response_js)
    resp.set_cookie(key='book', value='', expires=0)
    return resp
    
def sql_get_data(book):
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

    # cnx = mysql.connector.connect(pool_name = "order1111_sys_pool",
    #                               pool_size = 10,
    #                               **dbconfig)
    cursor = cnx.cursor()
    sql="SELECT `name`,`address`,`images` FROM `TAIPEI_VIEW` WHERE `id` = %s "
    
    id=book['attractionId']
    date=book['date']
    times=book['time']
    price=book['price']
    
    val=(id,)
    cursor.execute(sql,val)
    myresult=cursor.fetchone()
    cursor.close()  
    cnx.close()
    # end = time.perf_counter()
    # print("資料庫取得景點時間:"+str(end - start))
    
    name=myresult[0]
    address=myresult[1]
    images=myresult[2]
    images_list=images.split(',')
    image=images_list[0]
    
    resp={
        "data":{
            "id":id,
            "name":name,
            "address":address,
            "image":image
        },
        "date":date,
        "time":times,
        "price":price
    } 
    return (resp)

@book_sys.route('/booking',methods=["GET"])
def getbooking():
    user=get_token()
    book=get_book()
    if user==None:
        resp={"error":"未登入系統，拒絕存取"}
        return jsonify(resp),403
    else:
        if book == None :
            resp={"data":None}
            return jsonify(resp)
        else :
            resp=sql_get_data(book)
            return jsonify(resp)
    
@book_sys.route('/booking',methods=["POST"])
def postbooking():
    data=request.get_json()
    user=get_token()
    if user==None:
        resp={"error":"未登入系統，拒絕存取"}
        return jsonify(resp),403
    else:
        if 'attractionId'  in data and 'date' in data  and 'time' in data and 'price' in data:    

            return (post_book(data))
        else:
            resp={"error":"資料格式不符合"}
            return jsonify(resp),400

@book_sys.route('/booking',methods=["DELETE"])
def deletbooking():
    user=get_token()
    if user==None:
        resp={"error":"未登入系統，拒絕存取"}
        return jsonify(resp),403
    else:
        resp=delet_book()
        return(resp)