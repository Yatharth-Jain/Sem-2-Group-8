from flask import Blueprint, redirect, render_template, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from website import view
from website.models import Courses, Marks, Sems, Student, Subjects, Teacher, Admin, Years,Courses,Subjects,Sems,Assignments,ClassForm
from flask_login import login_required, login_user, logout_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/')
def homepage():
    return render_template('home.html')


@auth.route('/login/<user>', methods=['GET', 'POST'])
def login(user):
    if user not in ['student','teacher','admin']:
        return redirect(url_for("auth.homepage"))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if(user == 'student'):
            std_row = Student.query.filter_by(semail=email).first()
            if std_row:
                if check_password_hash(std_row.spass, password):
                    login_user(std_row, remember=True)
                    session["name"] = "student"
                    print("\n\n\n\nStd Login\n\n\n\n\n")
                    return redirect("/student-home")
                else:
                    flash('Wrong Password!!!', 'error')
            else:
                flash("The User Doesn't Exist!!!", "error")
        elif(user == 'teacher'):
            tch_row = Teacher.query.filter_by(temail=email).first()
            if tch_row:
                if check_password_hash(tch_row.tpass, password):
                    login_user(tch_row, remember=True)
                    session["name"] = "teacher"

                    print("\n\n\n\ntch Login\n\n\n\n\n")
                    return redirect("/teacher-home")
                else:
                    flash('Wrong Password!!!', 'error')
            else:
                flash("The User Doesn't Exist!!!", "error")
        elif(user == 'admin'):
            adm_row = Admin.query.filter_by(aemail=email).first()
            if adm_row:
                if check_password_hash(adm_row.apass, password):
                    login_user(adm_row, remember=True)
                    session["name"] = "admin"
                    print("\n\n\n\nadm Login\n\n\n\n\n")
                    return redirect("/admin-home")
                else:
                    flash('Wrong Password!!!', 'error')
            else:
                flash("The User Doesn't Exist!!!", "error")
    return render_template('admin_login.html', user=user)


# @auth.route('/student-register', methods=['GET', 'POST'])
# def studentreg():
#     if request.method == 'POST':
#         sfname = request.form['sfname']
#         slname = request.form['slname']
#         sbranch = request.form['sbranch']
#         syear = request.form['syear']
#         sdob = request.form['sdob'].split('-')
#         print(f'{sfname}<-->{slname}<-->{sbranch}<-->{syear}<-->{sdob}')
#     return render_template('student-register.html')


@auth.route('/student_registration', methods=['GET', 'POST'])
def studentreg():
    form1=ClassForm()
    form1.year.choices=[(yr.year,yr.year) for yr in Years.query.all()]
    if request.method == 'POST':
        sfname = request.form['sfname']
        slname = request.form['slname']
        syear = form1.year.data
        sbranch = form1.course.data

        sdob = request.form['sdob']
        dob = sdob.split('-')

        crs=Courses.query.filter_by(id=sbranch).first()
        students=Student.query.filter_by(syear=syear,sbranch=sbranch).all()
        sroll=len(students)+1

        semail=f'{crs.course}{syear}{sroll:03d}@std.clg.com'

        spass=f'{dob[2]}{dob[1]}{dob[0]}'

        n_std = Student(sfname=sfname, slname=slname, sbranch=sbranch, sroll=sroll, semail=semail,syear=syear, spass=generate_password_hash(spass, method='sha256'), sdob=sdob)
        db.session.add(n_std)
        db.session.commit()

        # print(f'{sfname}<-->{slname}<-->{sbranch}<-->{syear}<-->{sdob}')
    return render_template('student_registration.html',form1=form1)


@auth.route('/teacher_registration', methods=['GET', 'POST'])
def teacherreg():
    if request.method == 'POST':
        tfname = request.form['tfname']
        tlname = request.form['tlname']
        tsub = request.form['tsub']
        tdob = request.form['tdob'].split('-')
        print(f'{tfname}<-->{tlname}<-->{tsub}<-->{tdob}')
    return render_template('teacher_registration.html')


@auth.route("/logout")
@login_required
def logout():
    session["name"] = None
    logout_user()
    return redirect(url_for('auth.homepage'))


@auth.route("/addsems/<int:year>/<course>/<subject>/<sems>")
def addsems(year,course,subject,sems):
    print(f'\n\n\nY={year} C={course} S={subject} sem={sems}\n\n\n')
    y=Years.query.filter_by(year=year).first()
    if not y:
        y=Years(year=year)
        db.session.add(y)
        db.session.commit()
    
    c=Courses.query.filter_by(yer=year,course=course).first()
    if not c:
        c=Courses(yer=year,course=course)
        db.session.add(c)
        db.session.commit()

    s=Subjects.query.filter_by(crs=c.id,subject=subject).first()
    if not s:
        s=Subjects(crs=c.id,subject=subject)
        db.session.add(s)
        db.session.commit()

    for sem in sems.split(','):
        se=Sems.query.filter_by(subject=s.id,sem=int(sem)).first()
        if not se:
            se=Sems(subject=s.id,sem=int(sem))
            db.session.add(se)
            db.session.commit()
    return redirect(url_for('auth.homepage'))

