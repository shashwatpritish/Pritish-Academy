from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class Contact(db.Model):
    name = db.Column(db.String(40),nullable=False,primary_key=False)
    email = db.Column(db.String(100),nullable=False,primary_key=True)
    feedback = db.Column(db.String(5000))

    def __repr__(self) -> str:
        return f"{self.name} - {self.email} - {self.feedback}"


with app.app_context():
    db.create_all()


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/videos')
def videos():
	return render_template('videos.html')


@app.route('/contact', methods=['GET','POST'])
def contact():
	if request.method == "POST":
		name=request.form['name']
		email=request.form['email']
		feedback=request.form['feedback']
		form = Contact(name=name, email=email, feedback=feedback)
		db.session.add(form)
		db.session.commit()
	data = Contact.query.all()
	return render_template('contact.html', data=data)


app.run(host='0.0.0.0', port=81)
