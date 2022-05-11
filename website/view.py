from flask import Blueprint, redirect, render_template , request,flash, url_for
from .models import Marks,db

view=Blueprint('view',__name__)

@view.route('/')
def homepage():
    return render_template('home.html')

@view.route('/sheet',methods=['GET','POST'])
def sheet():
    asss=['ass1','ass2','ass3','ass4']
    names=['name1','name2','name3','name4','name5']
    if request.method=='POST':
        for ass in asss:
            for name in names:
                mid=f'{ass}-{name}'
                marks=request.form[mid]
                new_marks=Marks(mid=mid,mark=marks)
                db.session.add(new_marks)
                db.session.commit()
                
                print(f'{ass}-{name}-{marks}')

    return render_template('sheet.html',asss=asss,names=names)