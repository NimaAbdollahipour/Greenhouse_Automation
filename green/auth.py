from flask import *
import flask
from .models import Greenhouse, User
from . import db
from datetime import *
from functools import wraps
auth = Blueprint("auth",__name__)

def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if not session.get('id'):
            return redirect(url_for('auth.login'))
        current_user = User.query.get(session.get('id'))
        return f(*args,**kwargs)
    return decorated

@auth.route('/login', methods= ["POST", "GET"])
def login():
    if request.method == 'POST':
        db_res = User.query.filter_by(username = request.form['username']).first()
        if db_res:
            if db_res.password == request.form['password']:
                session['username'] = request.form['username']
                session['id'] = db_res.id
                return redirect(url_for('green.monitor'))
            else:
                flash("Wrong Password")
                return redirect(url_for('auth.login'))
        else:
            flash("Wrong Username")
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')




@auth.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == 'POST':
        db_res = User.query.filter_by(username = request.form['username']).all()
        if len(db_res)>0:
            flash("Username Exists!")
            return redirect(url_for('auth.signup'))
        elif request.form['password'] != request.form['password2']:
            flash("Passwords didn't match!")
            return redirect(url_for('auth.signup'))
        else:
            db.session.add(User(
                request.form['name'],
                request.form['email'],
                request.form['username'],
                request.form['password']
            ))
            db.session.commit()
            db.session.add(
                Greenhouse(
                    User.query.filter_by(username = request.form['username']).first().id,
                    '',
                    '',
                    1,
                    True,
                    1,
                    True,
                    datetime.now().time(),
                    datetime.now().time()
                )
            )
            db.session.commit()
            return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')



@auth.route('/logout', methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))