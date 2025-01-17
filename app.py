from flask import *
from api.attractions_sys.view import attractions_sys
from api.member_sys.view import member_sys
from api.book_sys.view import book_sys
from api.orders_sys.view import orders_sys
import mysql.connector


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.register_blueprint(attractions_sys, url_prefix='/api')
app.register_blueprint(member_sys, url_prefix='/api')
app.register_blueprint(book_sys, url_prefix='/api')
app.register_blueprint(orders_sys, url_prefix='/api')
dbconfig = {
    "host":"localhost",
    "port":"3306",
    "user":"root",
    "password":"qweasdzxc",
    "database":"taipei_day_trip_website"
}
cnx = mysql.connector.connect(pool_name = "mypool",
                              pool_size = 25,
                              pool_reset_session=True,
                              **dbconfig)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
@app.route("/member/orders")
def ordersearch():
    return render_template("orders.html")
@app.route("/member/information")
def memberinformation():    
    return render_template("information.html")


app.run(host='0.0.0.0', port=3000)