from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from threading import Thread
from app import mail
from .models import Alert, Student
from . import db
import africastalking
import os
import smtplib


main = Blueprint('main', __name__)

username = os.getenv('user_name', 'sandbox')
api_key = os.getenv('api_key', 'key')
phone = os.getenv('phone', 'phone')

africastalking.initialize(username, api_key)
sms = africastalking.SMS

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# def send_email(to, subject, template, **kwargs):
#     msg = Message(subject, recipients=[to], html=template)
#     Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


@main.route('/')
@login_required
def index():
    alerts = Alert.query.all()
    return render_template('index.html', alerts=alerts)


@main.route('/alert')
@login_required
def alert():
    return render_template('alert.html')


@main.route('/alert', methods=['POST'])
@login_required
def add_alert():
    title = request.form.get('title')
    body = request.form.get('body')

    new_alert = Alert(title=title, body=body)

    db.session.add(new_alert)
    db.session.commit()

    # message = f"Dear {new_alert.name} your alert, ID: 00{new_alert.id} has been logged into our storage"

    # msg = Message("alert Added",
    #             sender=os.getenv("email"),
    #             recipients=[new_alert.email],
    #             body=message)

    # mail.send(msg)

    # sms.send(f"Dear {new_alert.name} your alert ID: 00{new_alert.id} has been logged into our storage", [f"{phone}"], callback=on_finish)
    return redirect(url_for('main.index'))


def on_finish(error, response):
    if error is not None:
        raise error
    print(response)

@main.route('/student')
@login_required
def student():
    students = Student.query.all()
    return render_template('student.html', students=students)

@main.route('/student', methods=['POST'])
@login_required
def add_student():
    name = request.form.get('name')
    reg = request.form.get('reg')
    email = request.form.get('email')
    phone = request.form.get('phone')
    school = request.form.get('school')

    new_student = Student(name=name, reg=reg, email=email, phone=phone, school=school)

    db.session.add(new_student)
    db.session.commit()

    message = f"Dear {new_student.name} you have been subscribed to university email alerts"

    msg = Message("University News Subscription",
                sender=os.getenv("email"),
                recipients=[new_student.email],
                body=message)

    mail.send(msg)


    # send_email(new_student.email, "University News Subscription", message)

    return redirect(url_for('main.student'))


@main.route('/alert/<id>')
@login_required
def view_alert(id):
    alert = Alert.query.filter_by(id=id).first_or_404()
    data = f"Post Code: {alert.id}\n Title: {alert.title}\n Body: {alert.body}"
    return render_template('show_alert.html', alert=alert, data=data)


@main.route('/logout/<id>')
@login_required
def logout(id):
    alert = Alert.query.filter_by(id=id).first_or_404()

    db.session.delete(alert)
    db.session.commit()
    flash("alert logged out")

    return redirect(url_for('main.index'))



