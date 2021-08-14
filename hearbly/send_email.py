from flask import request , redirect ,url_for ,render_template,session
from hearbly import app
import smtplib
from hearbly import routes
#generale function for sending email
def send_email(email,password,type):
    EMAIL_ADDRESS = 'test.send53@gmail.com'
    EMAIL_PASSWORD = 'badBOY@2002'
    with smtplib.SMTP('smtp.gmail.com' , 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        if type == 'send':
            subject = 'Request To Access To Hearbly Data Base'
            body = 'This Person is trying to access to Hearbly Data Base System .if it able to : please inser it into the Data Base Query System with the fallowing email : '+str(email)
            msg = f'Subject : {subject} \n\n {body}'
            smtp.sendmail(EMAIL_ADDRESS , EMAIL_ADDRESS ,msg)
        elif type == 'request':
            subject = 'You Have Been Add To Hearbly Data Base'
            body = 'You Are New Able To Acess To Hearbly Data Base System ,Use The Folowing Information To Acces : \nEmail : '+email+'\nPassword : '+password 
            msg = f'Subject : {subject} \n\n {body}'
            smtp.sendmail(EMAIL_ADDRESS , EMAIL_ADDRESS ,msg)
