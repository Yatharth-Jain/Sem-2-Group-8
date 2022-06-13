from flask_login import current_user
from flask import flash, redirect

def loginchecker(role="None"):
    def inner(f):
        def wrapper(*args,**kwargs):
            if current_user.is_authenticated:
                if(role==current_user.role):
                    return f(*args,**kwargs)
                else:
                    return redirect(f'/{current_user.role}-home')
            else:
                flash("You Are Not Logged In!",'error')
                return redirect('/')
                
        wrapper.__name__=f.__name__
        return wrapper
    return inner
