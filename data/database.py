from optparse import Values
import mysql.connector
import json

from sqlalchemy import false, null

file=open('taipei-attractions.json',"r",encoding="utf-8")
data=json.load(file)
file.close()
# print(type(data))
data_list=data["result"]["results"]

mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='qweasdzxc',
    database='taipei_day_trip_website'
    )
cursor=mydb.cursor()
view_id=0
for view in data_list:
    view_id+=1
    if  view_id is None:
        view_id="no data"
    # print (view["_id"])
    view_stitle=view['stitle']
    if view_stitle is None:
        view_id="no data"
    # print(view_stitle)
    view_info=view['info']
    if view_info is None:
        view_info="no data"
    # print(view_info)
    view_address=view['address']
    if view_info is None:
        view_info="no data"
    # print(view_address)
    view_introd=view['xbody']
    print(view_introd)
    if view_introd is None:
        view_introd=view="no data"
    view_MRT=view['MRT']
    if view_MRT is None:
        view_MRT="no data"
    view_MEMO_TIME=view['MEMO_TIME']
    if view_MEMO_TIME is None:
        view_MEMO_TIME="no data"
    view_CAT1=view['CAT1']
    if view_CAT1 is None:
        view_CAT1="no data"
    view_CAT2=view['CAT2']
    if view_CAT2 is None:
        view_CAT2="no data"
    view_longitude=view['longitude']
    if view_longitude is None:
        view_longitude="no data"
    view_latitude=view['latitude']
    if view_latitude is None:
        view_latitude="no data"
    # print(view_introd)
    view_img=view['file'].split('https://')
    del view_img[0]
    # print(len(view_img))
    for i in  range(len(view_img)):
        # print(i)
        # print(view_img[i])
        # if "jpg"  in view_img[i]:
        #     view_img[i]="https://"+view_img[i]
        #     print("ok")
        # elif "JPG" in view_img[i]:
        #     view_img[i]="https://"+view_img[i]
        #     print("ok")
        # else:
        #     print(view_img[i])
        # if view_img[i].endswith('jpg')==True:
        #     print("0")
        if view_img[i].endswith("jpg"):
            view_img[i]="https://"+view_img[i]
            # print("ok")
        elif view_img[i].endswith("JPG"):
            view_img[i]="https://"+view_img[i]
            # print("ok")
        elif  view_img[i].endswith("png"):
            view_img[i]="https://"+view_img[i]
            # print("ok")
        elif view_img[i].endswith("PNG"):
            view_img[i]="https://"+view_img[i]
            # print("ok")
        else:
            view_img[i]=" "
            # print(view_img[i]+"Data already blank")
    vlaueisspace=" "
    view_img=[value for value in view_img if value !=vlaueisspace]
    view_img=",".join(view_img)
    # print(view_img)
    # print(type(view_img))
    sql="INSERT INTO TAIPEI_VIEW(`name`,`description`,`address`,`transport`,`MRT`,`MEMO_TIME`,`VIEW_CAT1`,`category`,`images`,`view_id`,`longitude`,`latitude`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(view_stitle,view_introd,view_address,view_info,view_MRT,view_MEMO_TIME,view_CAT1,view_CAT2,view_img,view_id,view_longitude,view_latitude)
    cursor.execute(sql,val)
    mydb.commit()
    # print(view_id)
    # print(type(view_stitle))
    # print(type(view_info))
    # print(type(view_address))
    # print(type(view_introd))
    # print((view_MRT))
    # print(type(view_MEMO_TIME))
    # print(type(view_CAT1))
    # print(type(view_CAT2))
    # print(type(view_img))
    print("---------------------------"+str(view_id))
cursor.close()
mydb.close()