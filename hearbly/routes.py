import re
from flask import render_template ,request,session
from flask.globals import current_app, g
from hearbly import app ,db
from hearbly.models import User ,Register
from hearbly import send_email
from hearbly.send_email import send_email
from hearbly.pandas import request_data_base , make_plot
from hearbly.pyplot import make_pie

#route for the home page
@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("home.html" , title = 'Herbaly Wellness Collection')

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

#route for sign up
@app.route("/Sign Up" , methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        send_email(request.form.get("make_email"),request.form.get("make_email"),'send')
        return render_template('sign_in.html' ,title = 'Create Account', messages = 'Your Email Has Been Sent successfully')
    return render_template("sign_up.html" , title = 'Create Account')

#route for forget password
@app.route("/Forget password", methods = ['GET','POST'])
def forget_password():
    global change_number
    if request.method == 'POST':
        session['change_email'] = request.form.get('change_email')
        user = User.query.filter_by(email=session['change_email']).first()
        if user:
            change_number = send_email('pass','pass','change')
            return render_template("change_password.html" , title = "Change Password")
        else:
            message = 'This User Dont Have An Account , please chaque your information'
            return render_template("forget_password.html" ,message = message, title = "Forget Password")
    return render_template("forget_password.html" , title = "Forget Password")

#route for change password
@app.route("/Change password" , methods = ['GET','POST'])
def change_password():
    if request.method == 'POST':
        session['change_password'] = request.form.get("change_password")
        session['change_email_chque'] = request.form.get("change_email_chque")
        session['password_change'] = request.form.get("password_change")
        session['conf_password_change'] = request.form.get("conf_password_change")
        if int(session['change_password']) != change_number:
            message = 'Error !,wrong Number please chaque and try Again'
            return render_template("change_password.html" ,message = message, title = "Change Password")
        elif session['password_change'] != session['conf_password_change']:
            error = 'Error!, Password and Confirm password are not the same'
            return render_template("change_password.html" ,message = error, title = "Change Password")
        else:
            user = User.query.filter_by(email=session['change_email']).first()
            user_re = Register.query.filter_by(email=session['change_email']).first()
            user.password = session['password_change']
            user_re.password = session['password_change']
            user_re.confirm_password = session['password_change']
            db.session.commit()
            message = 'Your password has been change Successfully'
            return render_template("sign_in.html" ,messages = message, title = "Account")
    return render_template("change_password.html" , title = "Change Password")

#route for the application
@app.route("/app" , methods = ['GET','POST']) 
def main():
    if request.method == 'POST':
        return render_template("app.html", title = 'Hearbly Data Base')
    return render_template("sign_in.html")

#route for log out
@app.route("/Log Out" , methods = ['GET','POST'])
def log_out():
    session.clear()
    return render_template("sign_in.html" ,title='Sign In')

#route for manage account
@app.route("/Manage Account" , methods = ['GET','POST'])
def account_manage():
    if not info_all.name == 'admin':
        message = 'You cant access to this Part, Its only for admin account'
        return render_template("app.html" , title = 'Data Base Query', data = info_all , message = message)
    if request.method == 'POST':
        session.clear()
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
        return render_template("manage_account.html" , alert = alert )
    return render_template("manage_account.html" , title = 'Manage Accounts', data = info_all)

#route for modifier account
@app.route("/Active account" , methods = ['GET','POST'])
def active_account():
    if request.method == 'POST':
        session.clear()
        change = User.query.filter_by(email=info_all.email).first()
        info_all.name = request.form.get("ch_name")
        info_all.l_name =request.form.get("ch_l_name")
        info_all.email = request.form.get("ch_email")
        info_all.password = request.form.get("ch_password")
        info_all.con_password = request.form.get("ch_con_password")
        info_all.phone = request.form.get("ch_phone")
        change.email = info_all.email
        change.password = info_all.password
        db.session.commit()
        message = 'Setting has been adding Successfully'
        session.clear()
        return render_template("active_account.html" , title = 'Active Account' , data = info_all , message = message)
    return render_template("active_account.html" , title = 'Active Account' , data = info_all)

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

#route for data base result
@app.route("/Data base result" , methods = ['GET','POST'])
def data_base_result():
    return render_template("data_base.html" , title = 'Data Base Result' , data = info_all)