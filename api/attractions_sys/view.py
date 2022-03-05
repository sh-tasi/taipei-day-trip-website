from urllib import response
from flask import *
import json,math
import mysql.connector
attractions_sys = Blueprint('attractions_sys',__name__,)
def search_key(page):
    sql_select_key="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW`WHERE `name` like %s LIMIT "   
    sql_page=12*int(page)
    print(sql_page)
    sql=sql_select_key+" "+str(sql_page)+","+"12"
    return(sql)
def view_select(page):
    sql_select="SELECT  `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM  `TAIPEI_VIEW` LIMIT "
    sql_page=12*page
    sql=sql_select+" "+str(sql_page)+","+"12"
    print(sql)
    return(sql)
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
        view_page=[]
        sql_conut="SELECT count(*)FROM `TAIPEI_VIEW`"
        mycursor.execute(sql_conut)
        view_count=mycursor.fetchall()
        view_count=view_count[0][0]           #所有資料總數
        view_maxpage=view_count/12            #12筆為一頁資料量
        view_maxpage=math.ceil(view_maxpage)  #最大頁數
        page_int=int(page)                    #PAGE轉換成數字做判斷使用
        sql=view_select(page_int)             #取出第N頁資料
        mycursor.execute(sql)              
        datas_field=list(zip(*mycursor.description))[0]
        myresult_page=mycursor.fetchall()
        for i in range(len(myresult_page)):   #SQL資料整理
            data_resoponse=dict(zip(datas_field,myresult_page[i]))
            # print(data_resoponse["images"])
            images=data_resoponse["images"]
            images_list=images.split(',')
            data_resoponse["images"]=images_list
            # for a in range(len(images_list)):
            #     images_list[a]=
            view_page.append(data_resoponse)
        view_maxpage=view_maxpage-1 #第0頁開始計算
        if page_int<view_maxpage:    
            view_page_js=jsonify({"nextPage":int(page)+1,"data":view_page})
            mycursor.close()
            mydb.close()
            return(view_page_js)
        else :
            view_page_js=jsonify({"nextPage":None,"data":view_page})
            mycursor.close()
            mydb.close()
            return(view_page_js)
        '''    
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
        '''
    else :
        sql_count="SELECT count(*) FROM `TAIPEI_VIEW` WHERE `name` like %s  "
        keyword_sql=["%"+keyword+"%"]
        mycursor.execute(sql_count,keyword_sql)
        myresult_page_count=mycursor.fetchall()
        print(myresult_page_count)
        page_max=myresult_page_count[0][0]/12   
        page_max=math.ceil(page_max)-1
        page_int=int(page)
        if page_int<page_max:
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
                images=data_resoponse["images"]
                images_list=images.split(',')
                data_resoponse["images"]=images_list
                view_key_data.append(data_resoponse)
            view_page_js=jsonify({"nextPage":page_int+1,"data":view_key_data})
            # print(myresult_key)
            mycursor.close()
            mydb.close()
            return(view_page_js)
        else :
            sql=search_key(page)
            print(sql)
            print("H")
            keyword_sql=["%"+keyword+"%"]
            print(keyword_sql)
            mycursor.execute(sql,keyword_sql)
            myresult_key=mycursor.fetchall()
            view_key_data=[]
            datas_field=list(zip(*mycursor.description))[0]
            for i in range(len(myresult_key)):
                data_resoponse=dict(zip(datas_field,myresult_key[i]))
                images=data_resoponse["images"]
                images_list=images.split(',')
                data_resoponse["images"]=images_list
                view_key_data.append(data_resoponse)
            view_page_js=jsonify({"nextPage":None,"data":view_key_data})
            mycursor.close()
            mydb.close()
            return(view_page_js) 
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
    sql="SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`images` FROM `TAIPEI_VIEW` WHERE `view_id`=%s"
    mycursor.execute(sql,attractionID_sql)
    myresult=mycursor.fetchone()
    datas_field=list(zip(*mycursor.description))[0]
    if myresult!=None:
        data_resoponse=dict(zip(datas_field,myresult))
        images=data_resoponse["images"]
        images_list=images.split(',')
        data_resoponse["images"]=images_list
        data_resoponse_data={'data':data_resoponse}
        print(data_resoponse_data)
        data_resoponse_js=jsonify(data_resoponse_data)
        mycursor.close()
        mydb.close()
        return(data_resoponse_js)
    else:
        sql_count="SELECT count(*) FROM `TAIPEI_VIEW`"
        mycursor.execute(sql_count)
        myresult=mycursor.fetchone()
        print(myresult)
        view_count=myresult[0]
        print(view_count)
        response_body={
        "error":"true",
        "message":"景點id超出範圍,目前共有"+str(view_count)+"個資料"
        }
        response_body=jsonify(response_body)
        mycursor.close()
        mydb.close()
        return(response_body)
@attractions_sys.route('/attraction/')
def attraction_id_error():
    response_body={
        "error":"true",
        "message":"請輸入attraction id"
    }
    response_body=jsonify(response_body)
         
    return(response_body)  