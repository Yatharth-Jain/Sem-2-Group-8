from flask import Blueprint, jsonify, redirect, render_template, request, flash, send_file, url_for,session
from flask_login import current_user
from .models import Assignments, ClassForm, Courses, Student, Subjects, Teacher, Admin, Marks, Years, Sems, ClassForm, db
from werkzeug.security import generate_password_hash, check_password_hash
from .loginfunction import loginchecker
import os
import json
import pandas as pd
from collections import OrderedDict

view = Blueprint('view', __name__)


@view.route('/student-home')
@loginchecker(role='student')
def stdhome():
    current_user
    br = Courses.query.filter_by(id=current_user.sbranch).first()
    br = br.course
    return render_template('Student_Home.html', cu=current_user, br=br)

@view.route('/std-marks',methods=['POST','GET'])
@loginchecker(role='student')
def stdresult():
    std=current_user
    crs=Courses.query.filter_by(id=std.sbranch).first()
    sem=Sems.query.order_by(Sems.sem.desc()).all()
    for ss in sem:
        s=Subjects.query.filter_by(id=ss.subject,crs=crs.id).first()
        if s:
            se=ss
            break
    sub=Subjects.query.filter_by(crs=crs.id).all()
    print(sub)
    sems=[]
    for s in sub:
        ss=Sems.query.filter_by(subject=s.id,sem=se.sem)
        if ss:
            sems.append(ss)
        else:
            sub.remove(s)
    sublist=dict([(s.id,s.subject) for s in sub])
    if request.method=='POST':
        session['marksub']=request.form['subselect']
        
    if 'marksub' not in session:
        session['marksub']=sub[0].id
    f=0
    print([s.id for s in sub])
    for s in sub:
        if int(session['marksub'])==s.id:
            print("Found")
            f=1
            break
    if f==0:
        session['marksub']=sub[0].id
    
    print(session['marksub'],se.sem)
    sem=Sems.query.filter_by(subject=session['marksub'],sem=se.sem).first()
    print(sem)
    ass=Assignments.query.filter_by(sem=sem.id).all()
    sub=Subjects.query.filter_by(id=int(session['marksub'])).first()
    
    marks=[]
    assiwise={}
    maxmark=0
    for a in ass:
        maxmark+=a.maxnum
        m=Marks.query.filter_by(student=std.sid,assi=a.id).first()
        if m.mark==-1:
            marks.append(0)
            assiwise[a.assi]=['A',a.maxnum]
        else:
            marks.append(m.mark)
            assiwise[a.assi]=[m.mark,a.maxnum]
    markgot=sum(marks)
    assiwise = OrderedDict(sorted(assiwise.items()))
    gradegot='N/A'
    if sub.graderange:
        graderange=json.loads(sub.graderange)
        for grade,range in graderange.items():
            if(grade=='total'):
                continue
            elif markgot>=int(range):
                gradegot=grade.replace('u','')
                break
    
    

    return render_template('studentMarks.html',  cu=current_user,sublist=sublist,maxmark=maxmark,markgot=markgot,assiwise=assiwise,gradegot=gradegot,sub=sub.subject)

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
    # n_std = Student(sfname='stu', slname='1', sbranch=1, sroll=1, semail='csai2021001@std.clg.com',
    #                 syear=2021, spass=generate_password_hash('01012003', method='sha256'), sdob='2003-01-01')
    # db.session.add(n_std)
    # db.session.commit()

    # n_tch = Teacher(tname='teach1', temail='teach1@tchr.clg.com', tsubject='Maths',
    #                 tpass=generate_password_hash('teach1pass', method='sha256'))
    # db.session.add(n_tch)
    # db.session.commit()

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
        return redirect(f'/sheet/{form1.year.data}/{crs.id}/{sub.id}/{sem.id}/0')
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


@view.route('/sheet/<year>/<crs>/<sub>/<sem>/<int:part>', methods=['GET', 'POST'])
def sheet(year, crs, sub, sem,part):
    curl = f'{year}/{crs}/{sub}/{sem}'
    if part ==1 or part==2:
        print("\n\n\n\n\n")
        asss = [ass for ass in Assignments.query.filter_by(sem=sem,part=part).all()]
    else:
        asss = [ass for ass in Assignments.query.filter_by(sem=sem).all()]
    print(asss)
    students = [std for std in Student.query.filter_by(sbranch=crs).all()]
    total = {}
    marksdict = {}
    cgpa={}

    s=Subjects.query.filter_by(id=sub).first()
    graderange=s.graderange
    print(graderange)
    if graderange==None:
        return redirect(url_for(f'view.graderange', year=year, crs=crs, sub=sub, sem=sem))
    graderange=json.loads(graderange)
    maxm=0
    for student in students:
        t = 0
        for ass in asss:
            mark = Marks.query.filter_by(
                student=student.sid, subject=sub, sem=sem, assi=ass.id).first()
            if mark:
                if mark.mark != -1:
                    t += mark.mark
                    marksdict[f'{ass.assi}-{student.sroll}'] = mark.mark
                else:
                    marksdict[f'{ass.assi}-{student.sroll}'] = 'A'
            else:
                mark = Marks(student=student.sid, subject=sub, sem=sem,
                             assi=ass.id, mark=0)
                db.session.add(mark)
                db.session.commit()
                marksdict[f'{ass.assi}-{student.sroll}'] = 0
        total[student.sroll] = t
        if maxm<t:
            maxm=t
    for student in students:
        for grade,range in graderange.items():
            if(total[student.sroll]>=int(range)):
                cgpa[student.sroll]=grade.replace('u','')
                break

    if request.method == 'POST':
        subtype = request.form['subtype']
        if subtype == 'addassi':
            new_ass = request.form['newassi']
            maxnum = request.form['maxnum']
            if part==0:
                part=1
            o_ass = Assignments.query.filter_by(
                sem=sem,part=part, assi=new_ass.capitalize()).first()
            if o_ass or new_ass == '':
                pass
            else:
                n_ass = Assignments(
                    assi=new_ass.capitalize(), maxnum=maxnum, sem=sem,part=part)
                db.session.add(n_ass)
                db.session.commit()
        else:
            for student in students:
                for ass in asss:
                    mark = Marks.query.filter_by(
                        student=student.sid, subject=sub, sem=sem, assi=ass.id).first()
                    if mark.mark != -1:
                        total[student.sroll] = total[student.sroll]-mark.mark
                    m = request.form[f'{ass.assi}-{student.sroll}']
                    if m != "A":
                        if m == '':
                            m = 0
                        if not m.isnumeric():
                            m=0
                        total[student.sroll] += int(m)
                        marksdict[f'{ass.assi}-{student.sroll}'] = int(m)
                        mark.mark = m
                    else:
                        marksdict[f'{ass.assi}-{student.sroll}'] = 'A'
                        mark.mark = -1
                    db.session.commit()

            if 'removeassi' in subtype:
                subtype=subtype.replace("removeassi/","")
                marks = Marks.query.filter_by(assi=int(subtype)).all()
                for mark in marks:
                    db.session.delete(mark)
                    db.session.commit()
                assi = Assignments.query.filter_by(id=int(subtype)).first()
                db.session.delete(assi)
                db.session.commit()

            if 'editassi' in subtype:
                subtype=subtype.replace("editassi/","")
                assi = Assignments.query.filter_by(id=int(subtype)).first()
                assi.name=request.form['assiname']
                assi.maxnum=request.form['maxnum']
                db.session.commit()


        
                
        return redirect(url_for(f'view.sheet', year=year, crs=crs, sub=sub, sem=sem,part=0))
    return render_template('sheet.html', asss=asss, students=students, total=total, marksdict=marksdict, curl=curl,cgpa=cgpa)

@view.route('/sheet/<year>/<crs>/<sub>/<sem>/range', methods=['GET', 'POST'])
def graderange(year,crs,sub,sem):
    total=0
    for ass in Assignments.query.filter_by(sem=sem):
        total+=ass.maxnum
    names=['A+u','Au','B+u','Bu','Cu','Du','Eu','Fu']
    s=Subjects.query.filter_by(id=sub).first()
    if(request.method=='POST'):
        ranges={}
        ranges['total']=total
        for name in names:
            ranges[name]=request.form[name]
            if not ranges[name]:
                ranges[name]=0
        s.graderange=json.dumps(ranges)
        db.session.commit()
    return render_template('GradeRange.html',total=total)

@view.route('/sheet/<year>/<crs>/<sub>/<sem>/download',methods=['GET'])
def downloadsheet(year,crs,sub,sem):
    students=[s for s in Student.query.filter_by(sbranch=crs).all()]
    assign=[a for a in Assignments.query.filter_by(sem=sem).all()]
    print(len(students))
    details=pd.DataFrame({
        "Sl.No.":[s.sroll for s in students],
        "Enroll. No.":[(s.semail).split('@')[0] for s in students],
        "Student Name":[f"{s.sfname} {s.slname}" for s in students]
    })
    # assignments=pd.DataFrame()
    for ass in assign:
        # a=pd.DataFrame({ass.assi:[Marks.query.filter_by(assi=ass.id,student=s.sid).first().mark for s in students]})
        # assignments=assignments.merge(a,how='right')
        a= []
        for s in students:
            m=Marks.query.filter_by(assi=ass.id,student=s.sid).first().mark
            a.append('A' if m==-1 else m)
        print()
        details.loc[:,ass.assi]=a
    details.set_index('Sl.No.',inplace=True)
    total=[sum(int(i) if i!='A' else 0 for i in (details.loc[s.sroll,[a.assi for a in assign]])) for s in students]
    details.loc[:,'Total']=total
    name=f'{crs}-{sub}-{sem}.xlsx'
    writer = pd.ExcelWriter(f'website/static/Number-Sheets/{name}')
    # final=details.merge(assignments,how='right')
    details.to_excel(writer)
    writer.save()
    return send_file(f'static/Number-Sheets/{name}',as_attachment=True)


@view.route('/sheet/<year>/<crs>/<sub>/<sem>/upload',methods=['POST'])
def uploadsheet(year,crs,sub,sem):
    if request.method=='POST':
        f=request.files['marksheet']
        name=f.filename
        ext=name.split('.')[1]
        if ext=='xlsx':
            name=f'{crs}-{sub}-{sem}.{ext}'
            f.save(f'website/static/Number-Sheets/{name}')
        return redirect(url_for('view.confirmsheet',year=year,crs=crs,sub=sub,sem=sem))

@view.route('/sheet/<year>/<crs>/<sub>/<sem>/confirm',methods=['POST','GET'])
def confirmsheet(year,crs,sub,sem):
    students = [std for std in Student.query.filter_by(sbranch=crs).all()]
    total={}
    sheet=pd.read_excel(f'website/static/Number-Sheets/{crs}-{sub}-{sem}.xlsx')
    sheet=sheet.drop(['Enroll. No.','Total'],axis=1)
    sheet.set_index('Sl.No.',inplace=True)
    ass=list(sheet.columns)
    ass.remove('Student Name')
    asss=[i for i in Sems.query.filter_by(id=sem).first().assis if i.assi in ass]
    marksdict = {}
    for s in students:
        for a in asss:
            marksdict[f'{a.assi}-{s.sroll}']=sheet.loc[s.sroll][a.assi]

    if request.method=='POST':
        os.remove(f'website/static/Number-Sheets/{crs}-{sub}-{sem}.xlsx')

        for student in students:
            for ass in asss:
                mark = Marks.query.filter_by(
                    student=student.sid, subject=sub, sem=sem, assi=ass.id).first()
                m = request.form[f'{ass.assi}-{student.sroll}']
                if m != "A":
                    if m == '':
                        m = 0
                    mark.mark = m
                else:
                    mark.mark = -1
                db.session.commit()
        return redirect(url_for(f'view.sheet', year=year, crs=crs, sub=sub, sem=sem,part=0))

    return render_template('Confirm-Sheet.html',students=students,asss=asss,marksdict=marksdict)
