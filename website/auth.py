from asyncio import run_coroutine_threadsafe
from flask import Blueprint, redirect, render_template , request,flash, url_for
from importlib_metadata import method_cache

from website.models import Student, Teacher, Admin

auth=Blueprint('auth',__name__)

@auth.route('/login/<user>',methods=['GET','POST'])
def login(user):
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        if(user=='student'):
            user="STUDENT"
            std_row=Student.query.filter_by(semail=email).first()
            if std_row:
                if std_row.spass==password:
                    return redirect("/student-home")
                else:
                    flash('Wrong Password!!!','error')
            else:
                flash("The User Doesn't Exist!!!","error" )
        elif(user=='teacher'):
            user="TEACHER"
            tch_row=Teacher.query.filter_by(temail=email).first()
            if tch_row:
                if tch_row.tpass==password:
                    return redirect("/teacher-home")
                else:
                    flash('Wrong Password!!!','error')
            else:
                flash("The User Doesn't Exist!!!","error" )
        elif(user=='admin'):
            user="ADMIN"
            adm_row=Admin.query.filter_by(aemail=email).first()
            if adm_row:
                if adm_row.apass==password:
                    return redirect("/admin-home")
                else:
                    flash('Wrong Password!!!','error')
            else:
                flash("The User Doesn't Exist!!!","error" )
    return render_template('popup.html',user=user)

@auth.route('/student-register',methods=['GET','POST'])
def studentreg():
    if request.method=='POST':
        sfname=request.form['sfname']
        slname=request.form['slname']
        sbranch=request.form['sbranch']
        syear=request.form['syear'] 
        sdob=request.form['sdob'].split('-')                               # YYYY-MM-DD



        print(f'{sfname}<-->{slname}<-->{sbranch}<-->{syear}<-->{sdob}')
    return render_template('student-register.html')