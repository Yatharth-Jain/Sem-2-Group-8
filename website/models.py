from . import db

# Testing email student--> sid=1, sfname=stu, slname=1, sbranch=csai, sroll=1, semail=csai-2021-001@std.clg.com ,syear=2021, ssem=2, spass=01012003, sdob=2003-01-01

# Teacher--> tname='teach1', temail='teach1@tchr.clg.com', tsubject='Maths', tpass='teach1pass'

# Admin--> aname='admin1', aemail='admin1@admin.clg.com', apass='admin1pass'

class Student(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    sfname = db.Column(db.String[50], nullable=False)
    slname = db.Column(db.String[50], nullable=False)
    sbranch = db.Column(db.String[50], nullable=False)              
    sroll = db.Column(db.Integer, nullable=False)   
    semail=db.Column(db.String[100],nullable=False)                 # {sbranch}-{syear}-{sroll}@std.clg.com
    syear = db.Column(db.Integer, nullable=False)
    ssem = db.Column(db.Integer, nullable=False)
    spass = db.Column(db.String[100], nullable=False)                    # DDMMYYYY
    sdob = db.Column(db.String[100], nullable=False)                     # YYYY-MM-DD
    srole=db.Column(db.String[100],default='student')
    # smarks=db.relationship('Marks')


class Teacher(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String[100], nullable=False)
    temail = db.Column(db.String[100], primary_key=False)            #{name}@tchr.clg.com
    tsubject = db.Column(db.String[100], primary_key=False)
    tpass = db.Column(db.String[100], nullable=False)
    trole=db.Column(db.String,default='teacher')



class Admin(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    aname = db.Column(db.String[100], nullable=False)                # {name}@admin.clg.com
    aemail = db.Column(db.String[100], primary_key=False)
    apass = db.Column(db.String[100], nullable=False)
    arole=db.Column(db.String,default='admin')


class Marks(db.Model):
    mid = db.Column(db.String[100], primary_key=True)
    mark = db.Column(db.Integer, nullable=False)
    # stu_id=db.Column(db.String[100],db.ForeignKey('student.sroll'))

    def __init__(self, mid,mark):
        self.mid = mid
        self.mark=mark
    def __repr__(self):
        return f'{self.mid}--{self.mark}'

if __name__=='__main__':
    n_std=Student(sfname='stu', slname='1', sbranch='csai', sroll=1, semail='csai-2021-001@std.clg.com' ,syear=2021, ssem=2, spass='01012003', sdob='2003-01-01',srole='student')
    db.session.add(n_std)
    db.session.commit()

    n_tch=Teacher(tname='teach1', temail='teach1@tchr.clg.com', tsubject='Maths', tpass='teach1pass')
    db.session.add(n_tch)
    db.session.commit()

    n_adm=Admin(aname='admin1', aemail='admin1@admin.clg.com', apass='admin1pass')
    db.session.add(n_adm)
    db.session.commit()