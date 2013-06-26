from flask import Flask
from flask import render_template, request, url_for, redirect, g, session
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data2.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.String)
    message = db.Column(db.String)
        
db.create_all()
@app.route('/')
def homepage():
    if not session.get('username', None):
        return redirect(url_for('loginview'))
        
    print session.get('username', None)
    messages = Message.query.all()
    messages.reverse()
    return render_template('home.html', messages =messages )

@app.before_request
def setup():
    g.username = session.get('username', None)

@app.route('/login', methods=('GET','POST'))
def loginview():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/logout')
def logoutview():
    session['username'] = None
    return redirect(url_for('loginview'))

@app.route('/add', methods=["POST"])
def add():
    if request.method == 'POST':
        new_message = Message(message=request.form['message'], timestamp = datetime.now(), \
                              username = session.get('username', None))
        db.session.add(new_message)
        db.session.commit()
        print 'added'
    return redirect(url_for('homepage'))

@app.route('/profile/<username>')
def profile(username):
    if not session.get('username', None):
        return redirect(url_for('loginview'))
    if username == None:
        return redirect(url_for('homepage'))
    else:
        messages = Message.query.filter_by(username=username).all()
        return render_template('home.html', messages = messages)
    
app.run()