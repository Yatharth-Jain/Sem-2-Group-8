from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for
from flask_login import current_user
from .models import Assignments, ClassForm, Courses, Student, Subjects, Teacher, Admin, Marks, Years,Sems,ClassForm, db
from werkzeug.security import generate_password_hash, check_password_hash
from .loginfunction import loginchecker

view = Blueprint('view', __name__)


@view.route('/student-home')
@loginchecker(role='student')
def stdhome():
    current_user
    br=Courses.query.filter_by(id=current_user.sbranch).first()
    br=br.course
    return render_template('Student_Home.html',cu=current_user,br=br)


@view.route('/admin-home')
@loginchecker(role='admin')
def admhome():
    return render_template('admin_home.html')


@view.route('/teacher-home')
@loginchecker(role='teacher')
def tchhome():
    return "<h1 style='font-size:100px;'>Teacher Home</h1>"


@view.route('/testprofilesadd')
def addtest():
    n_std = Student(sfname='stu', slname='1', sbranch=1, sroll=1, semail='csai2021001@std.clg.com',
                    syear=2021, spass=generate_password_hash('01012003', method='sha256'), sdob='2003-01-01')
    db.session.add(n_std)
    db.session.commit()

    n_tch = Teacher(tname='teach1', temail='teach1@tchr.clg.com', tsubject='Maths',
                    tpass=generate_password_hash('teach1pass', method='sha256'))
    db.session.add(n_tch)
    db.session.commit()

    n_adm = Admin(aname='admin1', aemail='admin1@admin.clg.com',
                  apass=generate_password_hash('admin1pass', method='sha256'))
    db.session.add(n_adm)
    db.session.commit()
    return redirect('/')


# @view.route('/sheet', methods=['GET', 'POST'])
# def sheet():
#     asss = ['assi1', 'assi2', 'assi3', 'assi4', 'assi5','assi6']
#     names = ['name1', 'name2', 'name3', 'name4', 'name5']
#     markdict = {}
#     total = {}
#     for name in names:
#         t = 0
#         for ass in asss:
#             mid = f'{ass}-{name}'
#             old_mark = Marks.query.filter_by(mid=mid).first()
#             if old_mark:
#                 markdict[mid] = int(old_mark.mark)
#                 t = t+markdict[mid]
#             else:
#                 markdict[mid] = 0
#                 new_marks = Marks(mid=mid, mark=0)
#                 db.session.add(new_marks)
#                 db.session.commit()
#         total[name] = t
#     print(markdict)
#     if request.method == 'POST':
#         for name in names:
#             for ass in asss:
#                 mid = f'{ass}-{name}'
#                 marks = request.form[mid]
#                 if not marks:
#                     marks = 0
#                 old_mark = Marks.query.filter_by(mid=mid).first()

#                 total[name] = total[name]-int(old_mark.mark)

#                 old_mark.mark = marks

#                 total[name] = total[name]+int(marks)
#                 markdict[mid] = marks
#                 db.session.commit()
#         redirect('/sheet')

#     return render_template('sheet.html', asss=asss, names=names, markdict=markdict, total=total)


@view.route("/sheet-create",methods=['GET','POST'])
def testform():
    form1=ClassForm()
    form1.year.choices=[(yr.year,yr.year) for yr in Years.query.all()]
    if request.method=='POST':
        crs=Courses.query.filter_by(id=form1.course.data).first()
        sub=Subjects.query.filter_by(id=form1.subject.data).first()
        sem=Sems.query.filter_by(id=form1.sem.data).first()
        assi=request.form['assignment']
        o_ass=Assignments.query.filter_by(sem=sem.id,assi=assi.capitalize()).first()
        if o_ass or assi=='':
            pass
        else:
            n_ass=Assignments(assi=assi.capitalize(),sem=sem.id)
            db.session.add(n_ass)
            db.session.commit()
        # return f"<h1>Year:{form1.year.data} Course:{crs.course} Subject:{sub.subject} Sem:{sem.sem}<h1>"
        return redirect(f'/sheet/{form1.year.data}/{crs.id}/{sub.id}/{sem.id}')
    return render_template("teacher_input.html",form1=form1)

@view.route('/form/<method>/<int:val>')
def year(method,val):
    crs=[]
    if method=='year':
        for cr in Courses.query.filter_by(yer=val).all():
            c={}
            c['id']=cr.id
            c['course']=cr.course
            crs.append(c)
        return jsonify({'courses':crs})
    elif method=='course':
        for sb in Subjects.query.filter_by(crs=val).all():
            c={}
            c['id']=sb.id
            c['subject']=sb.subject
            crs.append(c)
        return jsonify({'subjects':crs})
    elif method=='subject':
        for sm in Sems.query.filter_by(subject=val).all():
            c={}
            c['id']=sm.id
            c['sem']=sm.sem
            crs.append(c)
        return jsonify({'sems':crs})

@view.route('/sheet/<year>/<crs>/<sub>/<sem>', methods=['GET', 'POST'])
def sheet(year,crs,sub,sem):
    asss=[ass for ass in Assignments.query.filter_by(sem=sem).all()]
    # print(asss)
    students=[std for std in Student.query.filter_by(sbranch=crs).all()]
    total={}
    marksdict={}
    for student in students:
        t=0
        for ass in asss:
            mark=Marks.query.filter_by(student=student.sid,subject=sub,sem=sem,assi=ass.id).first()
            if mark:
                t+=mark.mark
                marksdict[f'{ass.assi}-{student.sroll}']=mark.mark
            else:
                mark=Marks(student=student.sid,subject=sub,sem=sem,assi=ass.id,mark=0,mid=f'{ass.assi}-{student.sroll}')
                db.session.add(mark)
                db.session.commit()
                marksdict[f'{ass.assi}-{student.sroll}']=0
        total[student.sroll]=t

    if request.method=='POST':
        for student in students:
            for ass in asss:
                mark=Marks.query.filter_by(student=student.sid,subject=sub,sem=sem,assi=ass.id).first()
                total[student.sroll]=total[student.sroll]-mark.mark
                m=request.form[f'{ass.assi}-{student.sroll}']
                total[student.sroll]+=int(m)
                marksdict[mark.mid]=int(m)
                mark.mark=m
                db.session.commit()
                
    return render_template('sheet.html',asss=asss,students=students,total=total,marksdict=marksdict)