from flask import Blueprint, redirect, render_template , request,flash, url_for

view=Blueprint('view',__name__)

@view.route('/')
def homepage():
    return render_template('home.html')