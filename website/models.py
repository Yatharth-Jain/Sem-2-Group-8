from . import db


class Student(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    sfname = db.Column(db.String[50], nullable=False)
    slname = db.Column(db.String[50], nullable=False)
    sbranch = db.Column(db.String[50], nullable=False)              # {sbranch}-{syear}-{sroll}
    sroll = db.Column(db.String[100], nullable=False)               # {sroll}@clg.com
    semail = db.Column(db.String[100], nullable=False)
    syear = db.Column(db.Integer, nullable=False)
    ssem = db.Column(db.Integer, nullable=False)
    spass = db.Column(db.String, nullable=False)                    # DDMMYYYY
    sdob = db.Column(db.String, nullable=False)                     # YYYY-MM-DD


class Teacher(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String[100], nullable=False)
    temail = db.Column(db.String[100], primary_key=False)
    tsubject = db.Column(db.String[100], primary_key=False)
    tpass = db.Column(db.String[100], nullable=False)


class Admin(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    aname = db.Column(db.String[100], nullable=False)                # {name}@admin.clg.com
    aemail = db.Column(db.String[100], primary_key=False)
    apass = db.Column(db.String[100], nullable=False)


class Marks(db.Model):
    mid = db.Column(db.String[100], primary_key=True)
    mark = db.Column(db.Integer, nullable=False)

    def __init__(self, mid,mark):
        self.mid = mid
        self.mark=mark
    def __repr__(self):
        return f'{self.mid}--{self.mark}'