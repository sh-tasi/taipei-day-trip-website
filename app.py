from flask import *
from api.attractions_sys.view import attractions_sys
from api.member_sys.view import member_sys


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.register_blueprint(attractions_sys, url_prefix='/api')
app.register_blueprint(member_sys, url_prefix='/api')


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

app.run(host='0.0.0.0', port=3000)