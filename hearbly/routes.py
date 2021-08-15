from flask import render_template ,url_for , redirect ,request,session , flash
from flask.globals import current_app, g
from hearbly import app ,db
from hearbly.models import User ,Register
from hearbly import send_email
from hearbly.send_email import send_email
from hearbly.pandas import request_data_base , make_plot
from hearbly.pyplot import make_pie
##########################################################################################
#route for the home page
@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("home.html" , title = 'Herbaly Wellness Collection')
##########################################################################################
#route for the Sign In page
@app.route("/Sign In" , methods = ['GET','POST'])
def sign_in():
    if request.method == 'POST':
        global info_all    
        session['email'] = request.form.get('email')
        session['password'] = request.form.get('password')
        info = User.query.filter_by(email=session['email']).first()
        if info :
            if not info.email == session['email']:
                message = 'Invalid !! Please Check Your Information and Try again'
                return render_template("sign_in.html" , message = message)
            if not info.password == session['password']:
                message = 'Invalid !! Please Check Your Information and Try again'
                return render_template("sign_in.html" , message = message)
            info_all = Register.query.filter_by(email = session['email']).first()
            return render_template("app.html" ,title = 'Hearbly Data Base' , data = info_all)
    return render_template("sign_in.html" , title = "Account")
##########################################################################################
#route for sign up
@app.route("/Sign Up" , methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        send_email(request.form.get("make_email"),request.form.get("make_email"),'send')
        return render_template('sign_in.html' ,title = 'Create Account', messages = 'Your Email Has Been Sent successfully')
    return render_template("sign_up.html" , title = 'Create Account')
##########################################################################################
#route for the application
@app.route("/app" , methods = ['GET','POST'])
def main():
    if request.method == 'POST':
        return render_template("app.html", title = 'Hearbly Data Base')
    return render_template("sign_in.html")
##########################################################################################
#route for log out
@app.route("/Log Out" , methods = ['GET','POST'])
def log_out():
    session.clear()
    return render_template("sign_in.html" ,title='Sign In')
##########################################################################################
#route for manage account
@app.route("/Manage Account" , methods = ['GET','POST'])
def account_manage():
    if request.method == 'POST':
        session['name'] = request.form.get("name")
        session['l_name'] = request.form.get("l_name")
        session['email'] = request.form.get("email")
        session['password'] = request.form.get("password")
        session['con_password'] = request.form.get("con_password")
        session['phone'] = request.form.get("phone")
        if session['password'] != session['con_password']:
            alert = 'Password and Confirm Password are not the Same'
            return render_template("manage_account.html" , alert = alert)
        new = Register(name = session['name'] ,l_name = session['l_name'] ,email = session['email'] ,password = session['password'] ,confirm_password = session['con_password'] ,phone = session['phone'])
        new_user = User(email = session['email'] , password = session['password'])
        db.session.add(new)
        db.session.add(new_user)
        db.session.commit()
        alert = 'Your Request Has Been added Secssefuly'
        send_email(session['email'],session['password'],'request')
        session.clear()
        return render_template("manage_account.html" , alert = alert )
    return render_template("manage_account.html" , title = 'Manage Accounts', data = info_all)
##########################################################################################
#route for database in first time
@app.route("/Data Base" , methods = ['GET','POST'])
def data_base():
    if request.method == 'POST':
        session['make'] = request.form.get("test")
        base = 'hearbly/static/EXCEL/'+session['make']
        data_base = request_data_base(base)
        make_plot(base)
        make_pie(base)
        return render_template("data_base.html" , data = info_all, data_base = data_base ,title = 'Data Base Result')
    return render_template("app.html" , title = 'Data Base Query', data = info_all)
###########################################################################################
@app.route("/Data base result" , methods = ['GET','POST'])
def data_base_result():
    return render_template("data_base.html" , title = 'Data Base Result' , data = info_all)