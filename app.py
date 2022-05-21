from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from datetime import datetime, date
import smtplib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xjvveyyjgezcck:84c3e618727d5f5e0ad89308dbd5f83a046166957391467f2c249df67c94aedf@ec2-44-194-117-205.compute-1.amazonaws.com:5432/dbsn7qc9gjc7k1'
app.config['SECRET_KEY'] = "my super secret key yo"


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ironhart.db'

db = SQLAlchemy(app)

class Ironhart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255))
    email = db.Column(db.String(255))
    message = db.Column(db.Text())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

class InquiryForm(FlaskForm):
    name = StringField("", validators=[DataRequired(), Length(max=30)])
    subject = StringField("", validators=[DataRequired(), Length(max=30)])
    email = EmailField("", validators=[DataRequired(), Email(), Length(max=100)])
    message = TextAreaField("" ,validators=[DataRequired(message="A message is required!"), Length(max=400)])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/music')
def music():
    return render_template("music.html")

@app.route('/bio')
def bio():
    return render_template("bio.html")

@app.route('/media')
def media():
    return render_template("media.html")

@app.route('/tour')
def tour():
    return render_template("tour.html")

@app.route('/live')
def live():
    return render_template("live.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    name = None
    form = InquiryForm()

    if form.validate_on_submit():
        
        try:

            name = form.name.data
            subject = form.subject.data
            email = form.email.data
            message = form.message.data

            msg = Message(subject=f"Message from {name}", sender=email, recipients=[''])
            msg.body = f"Name: {name}\nSubject: {subject}\nEmail: {email}\n\nMessage: \t{message}"
            mail.send(msg)

            new_message = Ironhart(name=name, subject=subject, email=email, message=message)

            db.session.add(new_message)
            
            db.session.commit()

            form.name.data = ''
            form.subject.data = ''
            form.email.data = ''
            form.message.data = ''
            
            names = Ironhart.query.order_by(Ironhart.date_posted)
            return render_template('inquiry.html', name=name, names=names)
        
        except:
            flash("There was an error processing your inquiry.")


    return render_template('contact.html',
        form=form)
    

if __name__ == "__main__":
    app.run(debug=True)