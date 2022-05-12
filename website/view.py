from flask import Blueprint, redirect, render_template , request,flash, url_for
from .models import Marks,db

view=Blueprint('view',__name__)

@view.route('/')
def homepage():
    return render_template('home.html')

@view.route('/sheet',methods=['GET','POST'])
def sheet():
    asss=['assi1','assi2','assi3','assi4','assi5']
    names=['name1','name2','name3','name4','name5']
    markdict={}
    total={}
    for name in names:
        t=0
        for ass in asss:
            mid=f'{ass}-{name}'
            old_mark=Marks.query.filter_by(mid=mid).first()
            if old_mark:
                markdict[mid]=int(old_mark.mark)
                t=t+markdict[mid]
            else:
                markdict[mid]=0
                new_marks=Marks(mid=mid,mark=0)
                db.session.add(new_marks)
                db.session.commit()
        total[name]=t
    print(markdict)
    if request.method=='POST':
        for name in names:  
            for ass in asss:
                mid=f'{ass}-{name}'
                marks=request.form[mid]
                if not marks:
                    marks=0
                old_mark=Marks.query.filter_by(mid=mid).first()

                total[name]=total[name]-int(old_mark.mark)

                old_mark.mark=marks

                total[name]=total[name]+int(marks)
                markdict[mid]=marks
                db.session.commit()
                print(f'{ass}-{name}-{marks}')
        redirect('/sheet')

    return render_template('sheet.html',asss=asss,names=names,markdict=markdict,total=total)