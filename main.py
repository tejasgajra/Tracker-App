from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

app = Flask(__name__)

app = Flask(__name__) #creates a Flask instance and name is the name of current file

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3' #loading configurations in the app and assigning a path for the database

db = SQLAlchemy() # creates an object with the class type 'sqlalchemy'
db.init_app(app)
app.app_context().push()


class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column( db.Integer, autoincrement = True , primary_key = True)
    user_name= db.Column(db.String)
    trackers = db.relationship('Tracker',secondary = 'Trackerlog')

class Tracker(db.Model):
    __tablename__ = 'Trackers'
    Tracker_id = db.Column(db.Integer, autoincrement = True , primary_key = True)
    Tracker_name = db.Column(db.String )
    Description= db.Column(db.String)
    Tracker_type = db.Column(db.String)
    users= db.relationship('User',secondary = 'Trackerlog')

class Trackerlogs(db.Model):
    __tablename__ ='Trackerlog'
    Log_id = db.Column(db.Integer,autoincrement = True , primary_key = True)
    Ltracker_id = db.Column(db.Integer, db.ForeignKey('Trackers.Tracker_id') , primary_key = True , nullable = False)
    LUser_id = db.Column(db.Integer, db.ForeignKey('Users.user_id') , primary_key = True , nullable = False)
    when = db.Column(db.String )
    values = db.Column(db.String )
    notes = db.Column(db.String)


@app.route('/',methods = ['GET','POST'])

def Index():
    us = User.query.all()
    if request.method =='GET':
        if us == []:
            return render_template('Add_user.html')
        else:
            return render_template('Login_page.html')
   
    
        
    
@app.route('/add',methods = ['GET','POST'])


def Add_user():
    if request.method == 'GET':
        return render_template('newuser_form.html')
    if request.method == 'POST':
        new_user = User.query.filter_by(user_name = request.form['user_name']).first()
        if new_user is None:
            n_user = User(user_name = request.form['user_name'] )
            db.session.add(n_user)
            db.session.commit()
            return redirect(url_for('Index'))
        else:


            return render_template('user_exists.html')


@app.route('/login',methods = ['GET','POST'])

def No_tracker():
    if request.method == 'POST':
        check_user = User.query.filter_by(user_name =request.form['user_name']).first()
        if check_user == []:
            return render_template('no_user.html')
        
        


































if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = True,
        port = 8080)
