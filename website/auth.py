from flask import Blueprint, redirect, render_template , request,flash, url_for

auth=Blueprint('auth',__name__)

@auth.route('/login/<user>',methods=['GET','POST'])
def login(user):
    print("\n\n\n\n\n",user,"\n\n\n\n\n")
    return render_template('popup.html')

@auth.route('/student-register',methods=['GET','POST'])
def studentreg():
    return render_template('student-register.html')