from . import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import SelectField

# Testing email student--> sid=1, sfname=stu, slname=1, sbranch=csai, sroll=1, semail=csai-2021-001@std.clg.com ,syear=2021, ssem=2, spass=01012003, sdob=2003-01-01

# Teacher--> tname='teach1', temail='teach1@tchr.clg.com', tsubject='Maths', tpass='teach1pass'

# Admin--> aname='admin1', aemail='admin1@admin.clg.com', apass='admin1pass'



class Student(db.Model, UserMixin):
    sid = db.Column(db.Integer, primary_key=True)
    sfname = db.Column(db.String[50], nullable=False)
    slname = db.Column(db.String[50], nullable=False)
    sbranch = db.Column(db.String[50], nullable=False)
    sroll = db.Column(db.Integer, nullable=False)
    # {sbranch}-{syear}-{sroll}@std.clg.com
    semail = db.Column(db.String[100], nullable=False)
    syear = db.Column(db.Integer, nullable=False)
    ssem = db.Column(db.Integer, nullable=False)
    # DDMMYYYY
    spass = db.Column(db.String[100], nullable=False)
    # YYYY-MM-DD
    sdob = db.Column(db.String[100], nullable=False)
    role = db.Column(db.String[100], default='student')
    # crs=db.Column(db.Integer, db.ForeignKey('courses.id'))
    # smarks=db.relationship('Marks')

    def __init__(self, sfname, slname, sbranch, sroll, semail, syear, ssem, spass, sdob):
        self.sfname = sfname
        self.slname = slname
        self.sbranch = sbranch
        self.sroll = sroll
        self.semail = semail
        self.syear = syear
        self.ssem = ssem
        self.spass = spass
        self.sdob = sdob

    def printdetails(self):
        print(self.sfname+self.slname+self.sbranch +
              self.sroll+self.sdob+self.role)

    def get_id(self):
        return self.sid


class Teacher(db.Model, UserMixin):
    tid = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String[100], nullable=False)
    # {name}@tchr.clg.com
    temail = db.Column(db.String[100], primary_key=False)
    tsubject = db.Column(db.String[100], primary_key=False)
    tpass = db.Column(db.String[100], nullable=False)
    role = db.Column(db.String, default='teacher')

    def get_id(self):
        return self.tid

    def printdetails(self):
        print(self.tname+self.temail+self.role)


class Admin(db.Model, UserMixin):
    aid = db.Column(db.Integer, primary_key=True)
    # {name}@admin.clg.com
    aname = db.Column(db.String[100], nullable=False)
    aemail = db.Column(db.String[100], primary_key=False)
    apass = db.Column(db.String[100], nullable=False)
    role = db.Column(db.String, default='admin')

    def get_id(self):
        return self.aid

    def printdetails(self):
        print(self.aname+self.aemail+self.role)


class Marks(db.Model):
    mid = db.Column(db.String[100], primary_key=True)
    mark = db.Column(db.Integer, nullable=False)
    # stu_id=db.Column(db.String[100],db.ForeignKey('student.sroll'))

    def __init__(self, mid, mark):
        self.mid = mid
        self.mark = mark

    def __repr__(self):
        return f'{self.mid}--{self.mark}'


class Years(db.Model):
    year = db.Column(db.Integer, primary_key=True)
    courses = db.relationship("Courses")


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yer = db.Column(db.Integer, db.ForeignKey('years.year'))
    course = db.Column(db.String[100], nullable=False)
    subs = db.relationship("Subjects")


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crs = db.Column(db.Integer, db.ForeignKey('courses.id'))
    subject = db.Column(db.String[100], nullable=False)
    sems = db.relationship("Sems")
    # students=db.relationship("Student")


class Sems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    sem = db.Column(db.Integer)
    assis = db.relationship("Assignments")


class Assignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assi = db.Column(db.String[100], nullable=False)
    sem = db.Column(db.Integer, db.ForeignKey('sems.id'))


class ClassForm(FlaskForm):
    year = SelectField('year', choices=[])
    course=SelectField('course',choices=[])
    subject=SelectField('subject',choices=[])
    sem=SelectField('sem',choices=[])
