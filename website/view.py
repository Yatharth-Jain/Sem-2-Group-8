from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for
from flask_login import current_user
from .models import Assignments, ClassForm, Courses, Student, Subjects, Teacher, Admin, Marks, Years, Sems, ClassForm, db
from werkzeug.security import generate_password_hash, check_password_hash
from .loginfunction import loginchecker

view = Blueprint('view', __name__)


@view.route('/student-home')
@loginchecker(role='student')
def stdhome():
    current_user
    br = Courses.query.filter_by(id=current_user.sbranch).first()
    br = br.course
    return render_template('Student_Home.html', cu=current_user, br=br)


@view.route('/admin-home')
@loginchecker(role='admin')
def admhome():
    return render_template('admin_home.html')


@view.route('/teacher-home')
@loginchecker(role='teacher')
def tchhome():
    return redirect(url_for("view.classselect"))


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


@view.route("/sheet-create", methods=['GET', 'POST'])
def classselect():
    form1 = ClassForm()
    form1.year.choices = [(yr.year, yr.year) for yr in Years.query.all()]
    if request.method == 'POST':
        crs = Courses.query.filter_by(id=form1.course.data).first()
        sub = Subjects.query.filter_by(id=form1.subject.data).first()
        sem = Sems.query.filter_by(id=form1.sem.data).first()
        # return f"<h1>Year:{form1.year.data} Course:{crs.course} Subject:{sub.subject} Sem:{sem.sem}<h1>"
        return redirect(f'/sheet/{form1.year.data}/{crs.id}/{sub.id}/{sem.id}')
    return render_template("teacher_input.html", form1=form1)


@view.route('/form/<method>/<int:val>')
def year(method, val):
    crs = []
    if method == 'year':
        for cr in Courses.query.filter_by(yer=val).all():
            c = {}
            c['id'] = cr.id
            c['course'] = cr.course
            crs.append(c)
        return jsonify({'courses': crs})
    elif method == 'course':
        for sb in Subjects.query.filter_by(crs=val).all():
            c = {}
            c['id'] = sb.id
            c['subject'] = sb.subject
            crs.append(c)
        return jsonify({'subjects': crs})
    elif method == 'subject':
        for sm in Sems.query.filter_by(subject=val).all():
            c = {}
            c['id'] = sm.id
            c['sem'] = sm.sem
            crs.append(c)
        return jsonify({'sems': crs})


@view.route('/sheet/<year>/<crs>/<sub>/<sem>', methods=['GET', 'POST'])
def sheet(year, crs, sub, sem):
    curl = f'{year}/{crs}/{sub}/{sem}'
    asss = [ass for ass in Assignments.query.filter_by(sem=sem).all()]
    # print(asss)
    students = [std for std in Student.query.filter_by(sbranch=crs).all()]
    total = {}
    marksdict = {}
    for student in students:
        t = 0
        for ass in asss:
            mark = Marks.query.filter_by(
                student=student.sid, subject=sub, sem=sem, assi=ass.id).first()
            if mark:
                if mark.mark!=-1:
                    t += mark.mark
                    marksdict[f'{ass.assi}-{student.sroll}'] = mark.mark
                else:
                    marksdict[f'{ass.assi}-{student.sroll}']='A'
            else:
                mark = Marks(student=student.sid, subject=sub, sem=sem,
                             assi=ass.id, mark=0, mid=f'{ass.assi}-{student.sroll}')
                db.session.add(mark)
                db.session.commit()
                marksdict[f'{ass.assi}-{student.sroll}'] = 0
        total[student.sroll] = t

    if request.method == 'POST':
        subtpye = request.form['subtype']
        if subtpye == 'addassi':
            new_ass = request.form['newassi']
            maxnum = request.form['maxnum']
            o_ass = Assignments.query.filter_by(
                sem=sem, assi=new_ass.capitalize()).first()
            if o_ass or new_ass == '':
                pass
            else:
                n_ass = Assignments(
                    assi=new_ass.capitalize(), maxnum=maxnum, sem=sem)
                db.session.add(n_ass)
                db.session.commit()
            return redirect(url_for(f'view.sheet', year=year, crs=crs, sub=sub, sem=sem))

        else:
            for student in students:
                for ass in asss:
                    mark = Marks.query.filter_by(
                        student=student.sid, subject=sub, sem=sem, assi=ass.id).first()
                    if mark.mark!=-1:
                        total[student.sroll] = total[student.sroll]-mark.mark
                    m = request.form[f'{ass.assi}-{student.sroll}']
                    if m!="A":
                        total[student.sroll] += int(m)
                        marksdict[mark.mid] = int(m)
                        mark.mark = m
                    else:
                        marksdict[mark.mid]='A'
                        mark.mark=-1
                    db.session.commit()
            if 'removeassi' in subtpye:
                return redirect(subtpye)

    return render_template('sheet.html', asss=asss, students=students, total=total, marksdict=marksdict, curl=curl)


@view.route('/removeassi/<year>/<crs>/<sub>/<sem>/<int:aid>')
def delassi(year, crs, sub, sem, aid):
    curl = f'{year}/{crs}/{sub}/{sem}'
    marks = Marks.query.filter_by(assi=aid).all()
    for mark in marks:
        db.session.delete(mark)
        db.session.commit()
    assi = Assignments.query.filter_by(id=aid).first()
    db.session.delete(assi)
    db.session.commit()
    return redirect(url_for(f'view.sheet', year=year, crs=crs, sub=sub, sem=sem))
