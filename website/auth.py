from flask import Blueprint, redirect, render_template , request,flash, url_for

auth=Blueprint('auth',__name__)

@auth.route('/login/<user>',methods=['GET','POST'])
def login(user):
    print("\n\n\n\n\n",user,"\n\n\n\n\n")
    return render_template('popup.html')

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