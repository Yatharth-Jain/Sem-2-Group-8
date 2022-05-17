from flask import Blueprint, redirect, render_template , request,flash, url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from website.models import Student, Teacher, Admin
from flask_login import login_required, login_user, logout_user

auth=Blueprint('auth',__name__)

@auth.route('/')
def homepage():
    return render_template('home.html')

@auth.route('/login/<user>',methods=['GET','POST'])
def login(user):
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if(user=='student'):
            std_row=Student.query.filter_by(semail=email).first()
            if std_row:
                if check_password_hash(std_row.spass,password):
                    login_user(std_row, remember=True)
                    session["name"] = "student"
                    print("\n\n\n\nStd Login\n\n\n\n\n")
                    return redirect("/student-home")
                else:
                    flash('Wrong Password!!!','error')
            else:
                flash("The User Doesn't Exist!!!","error" )
        elif(user=='teacher'):
            tch_row=Teacher.query.filter_by(temail=email).first()
            if tch_row:
                if check_password_hash(tch_row.tpass,password):
                    login_user(tch_row, remember=True)
                    session["name"] = "teacher"
                    
                    print("\n\n\n\ntch Login\n\n\n\n\n")
                    return redirect("/teacher-home")
                else:
                    flash('Wrong Password!!!','error')
            else:
                flash("The User Doesn't Exist!!!","error" )
        elif(user=='admin'):
            adm_row=Admin.query.filter_by(aemail=email).first()
            if adm_row:
                if check_password_hash(adm_row.apass,password):
                    login_user(adm_row, remember=True)
                    session["name"] = "admin"
                    print("\n\n\n\nadm Login\n\n\n\n\n")
                    return redirect("/admin-home")
                else:
                    flash('Wrong Password!!!','error')
            else:
                flash("The User Doesn't Exist!!!","error" )
        else:
            return redirect("/")
    return render_template('popup.html',user=user)

@auth.route('/student-register',methods=['GET','POST'])
def studentreg():
    if request.method=='POST':
        sfname=request.form['sfname']
        slname=request.form['slname']
        sbranch=request.form['sbranch']
        syear=request.form['syear'] 
        sdob=request.form['sdob'].split('-')
        print(f'{sfname}<-->{slname}<-->{sbranch}<-->{syear}<-->{sdob}')
    return render_template('student-register.html')


@auth.route("/logout")
@login_required
def logout():
    session["name"] = None
    logout_user()
    return redirect(url_for('auth.homepage'))