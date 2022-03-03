from urllib import response
from flask import *
import json,math
import mysql.connector
attractions_sys = Blueprint('attractions_sys',__name__,)
def search_key(page):
    if page=="0":
        sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT 12"
        print(sql)
        return(sql)
    elif page=="1":
        sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT 12 OFFSET 12"
        print(sql)
        return(sql)
    elif page=="2":
        sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT 12 OFFSET 24"
        print(sql)
    elif page=="3":
        sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT 12 OFFSET 36"
        print(sql)
    elif page=="4":
        sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT 12 OFFSET 48"
        print(sql)
    else:
        sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT 12 OFFSET 48"
        print(sql)
@attractions_sys.route('/attractions',methods=["GET"])
def attractions_search():
    page=request.args.get("page","0")
    keyword=request.args.get("keyword","*")
    print(page)
    mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='qweasdzxc',
    database='taipei_day_trip_website'
    )
    mycursor = mydb.cursor()
    if keyword=="*":
        # sql="SELECT count(*)FROM `TAIPEI_VIEW`"
        # mycursor.execute(sql)
        print(keyword)
        if page=="0":
            view_page=[]
            sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`LIMIT 12" 
            mycursor.execute(sql)
            myresult_page = mycursor.fetchall()
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_page)):
                data_resoponse=dict(zip(datas_field,myresult_page[i]))
                view_page.append(data_resoponse)
                print(data_resoponse)
            view_page_js=jsonify({"nextPage":int(page)+1,"data":view_page})
            print(myresult_page)
            print(datas_field)
            print(view_page_js)
            mycursor.close()
            mydb.close()
            return(view_page_js)
        elif page=="1":
            view_page=[]
            sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`LIMIT 12 OFFSET 12"
            mycursor.execute(sql)
            myresult_page= mycursor.fetchall()
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_page)):
                data_resoponse=dict(zip(datas_field,myresult_page[i]))
                view_page.append(data_resoponse)
                print(data_resoponse)
            view_page_js=jsonify({"nextPage":int(page)+1,"data":view_page})
            print(myresult_page)
            print(datas_field)
            print(view_page_js)
            mycursor.close()
            mydb.close()
            return(view_page_js)
        elif page=="2":
            view_page=[]
            sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`LIMIT 12 OFFSET 24"
            mycursor.execute(sql)
            myresult_page= mycursor.fetchall()
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_page)):
                data_resoponse=dict(zip(datas_field,myresult_page[i]))
                view_page.append(data_resoponse)
                print(data_resoponse)
            view_page_js=jsonify({"nextPage":int(page)+1,"data":view_page})
            print(myresult_page)
            print(datas_field)
            print(view_page_js)
            mycursor.close()
            mydb.close()
            return(view_page_js)
        elif page=="3":
            view_page=[]
            sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`LIMIT 12 OFFSET 36"
            mycursor.execute(sql)
            myresult_page= mycursor.fetchall()
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_page)):
                data_resoponse=dict(zip(datas_field,myresult_page[i]))
                view_page.append(data_resoponse)
                print(data_resoponse)
            view_page_js=jsonify({"nextPage":int(page)+1,"data":view_page})
            print(myresult_page)
            print(datas_field)
            print(view_page_js)
            mycursor.close()
            mydb.close()
            return(view_page_js)
        elif page=="4":
            view_page=[]
            sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`LIMIT 12 OFFSET 48"
            mycursor.execute(sql)
            myresult_page= mycursor.fetchall()
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_page)):
                data_resoponse=dict(zip(datas_field,myresult_page[i]))
                view_page.append(data_resoponse)
                print(data_resoponse)
            if len(myresult_page)<12:
                nextpage="此頁為最終頁"
            else:
                nextpage=int(page)+1
            view_page_js=jsonify({"nextPage":nextpage,"data":view_page})
            # print(myresult_page)
            # print(datas_field)
            # print(view_page_js)
            mycursor.close()
            mydb.close()
            return(view_page_js)
    else :
        sql_count="SELECT count(*) FROM `TAIPEI_VIEW` WHERE `name` like %s  "
        keyword_sql=["%"+keyword+"%"]
        mycursor.execute(sql_count,keyword_sql)
        myresult_page_count=mycursor.fetchall()
        page_max=myresult_page_count[0][0]/12
        page_max=math.ceil(page_max)-1
        if page_max==int(page):
        # sql="SELECT `id` FROM `TAIPEI_VIEW` WHERE `name` like %s LIMIT 12 OFFSET 2 "
            sql=search_key(page)
            keyword_sql=["%"+keyword+"%"]
            print(keyword_sql)
            mycursor.execute(sql,keyword_sql)
            myresult_key=mycursor.fetchall()
            view_key_data=[]
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_key)):
                data_resoponse=dict(zip(datas_field,myresult_key[i]))
                view_key_data.append(data_resoponse)
                print(data_resoponse)
            view_page_js=jsonify({"nextPage":"此頁為最終頁","data":view_key_data})
            print(myresult_key)
            mycursor.close()
            mydb.close()
            return(view_page_js)
        elif int(page) > page_max:
        # print(view_key_data)
        # print(datas_field)
        # print(view_page_js)
        # if myresult_key==[]:
        # sql_count="SELECT count(*) FROM `TAIPEI_VIEW` WHERE `name` like %s  "
        # mycursor.execute(sql_count,keyword_sql)
        # myresult_page_count=mycursor.fetchall()
        # page_max=myresult_page_count[0][0]/12
        # page_max=math.ceil(page_max)-1
            response_body={
                "error":"true",
                "message":"最後一頁為第"+str(page_max)+"頁"
            }
            response_body=jsonify(response_body)
            mycursor.close()
            mydb.close()
            return(response_body)  
    response_body={
        "error":"true",
        "message":"最後一頁為第4頁"
    }
    response_body=jsonify(response_body)
    mycursor.close()
    mydb.close()
    return(response_body)
@attractions_sys.route('/attraction/<attractionID>')
def attraction_id_search(attractionID):
    mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='qweasdzxc',
    database='taipei_day_trip_website'
    )
    mycursor = mydb.cursor()
    attractionID_sql=(attractionID,)
    sql=sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW` WHERE `view_id`=%s"
    mycursor.execute(sql,attractionID_sql)
    myresult=mycursor.fetchone()
    datas_field=list(zip(*mycursor.description))[0]
    if myresult!=None:
        data_resoponse=dict(zip(datas_field,myresult))
        data_resoponse_data={'data':data_resoponse}
        print(data_resoponse_data)
        data_resoponse_js=jsonify(data_resoponse_data)
        mycursor.close()
        mydb.close()
        return(data_resoponse_js)
    else:
        response_body={
        "error":"true",
        "message":"景點id錯誤，請輸入1~58"
        }
        response_body=jsonify(response_body)
        return(response_body)
@attractions_sys.route('/attraction/')
def attraction_id_error():
    response_body={
        "error":"true",
        "message":"請輸入attraction id"
    }
    response_body=jsonify(response_body)
         
    return(response_body)  