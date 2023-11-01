from postit_app import app
from flask import render_template, redirect, session, request, flash
import random
import math
import smtplib
from .env import ADMINEMAIL
from .env import PASSWORD
from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
from postit_app.models.job import Job
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Employee Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/loginPage')
def loginPage():
    if 'employee_id' in session:
        return redirect('/dashboard')
    return render_template('loginEmployee.html')

@app.route('/login', methods=['POST'])
def login():
    if 'employee_id' in session:
        return redirect('/dashboard')
    employee = Employee.get_employee_by_email(request.form)
    if not employee:
        flash('This email does not exist.', 'emailLogin')
        return redirect('/loginPage')
    if not bcrypt.check_password_hash(employee['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect('/loginPage')
    session['employee_id'] = employee['id']
    return redirect('/dashboard')

@app.route('/register', methods=['POST'])
def register():
    if 'employee_id' in session:
        return redirect('/dashboard')
    
    if Employee.get_employee_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect('/loginPage')
    string = '0123456789'
    vCode = ""
    length = len(string)
    for i in range(8) :
        vCode += string[math.floor(random.random() * length)]
    verificationCode = vCode

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'about': request.form['about'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'verification_code': verificationCode,
    }
    
    Employee.create_employee(data)
    
    LOGIN = ADMINEMAIL
    TOADDRS  = request.form['email']
    SENDER = ADMINEMAIL
    SUBJECT = 'Verify Your Email'
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
        % ((SENDER), "".join(TOADDRS), SUBJECT) )
    msg += f'Use this verification code to activate your account: {verificationCode}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()
    
    employee = Employee.get_employee_by_email(data)
    
    session['employee_id'] = employee['id']

    return redirect('/verify/email')

@app.route('/verify/email')
def verifyEmail():
    if 'employee_id' not in session:
        return redirect('/')
    data = {
        'employee_id': session['employee_id']
    }
    employee = Employee.get_employee_by_id(data)
    if employee['is_verified'] == 1:
        return redirect('/dashboard')
    return render_template('verify.html', loggedEmployee = employee)


@app.route('/activate/account', methods=['POST'])
def activateAccount():
    if 'employee_id' not in session:
        return redirect('/')
    data = {
        'employee_id': session['employee_id']
    }
    employee = Employee.get_employee_by_id(data)
    if employee['is_verified'] == 1:
        return redirect('/dashboard')
    
    if not request.form['verification_code']:
        flash('Verification Code is required', 'wrongCode')
        return redirect(request.referrer)
    
    if int(request.form['verification_code']) != int(employee['verification_code']):
        string = '0123456789'
        vCode = ""
        length = len(string)
        for i in range(8) :
            vCode += string[math.floor(random.random() * length)]
        verificationCode = vCode
        dataUpdate = {
            'verification_code': verificationCode,
            'employee_id': session['employee_id']
        }
        Employee.updateVerificationCode(dataUpdate)
        LOGIN = ADMINEMAIL
        TOADDRS  = employee['email']
        SENDER = ADMINEMAIL
        SUBJECT = 'Verify Your Email'
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
            % ((SENDER), "".join(TOADDRS), SUBJECT) )
        msg += f'Use this verification code to activate your account: {verificationCode}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()

        flash('Verification Code is wrong. We just sent you a new one', 'wrongCode')
        return redirect(request.referrer)
    
    Employee.activateAccount(data)
    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect('/loginPage')
    if 'hr_id' in session:
        return redirect('/logout')
    loggedEmployeeData = {
        'employee_id': session['employee_id']
    } 
    loggedEmployee = Employee.get_employee_by_id(loggedEmployeeData)
    job = Job.get_all_jobs()
    jobposted=Job.count_jobs()
    
    if not loggedEmployee:
        return redirect('/logout')
  
    return render_template('dashboard.html',job=job, jobposted=jobposted)

@app.route('/results', methods=['GET', 'POST'])
def search():
    if 'employee_id' not in session:
        return redirect('/')

    search_query = request.args.get('searchfield', default='')

    jobs = []

    if search_query:
        jobs = Job.search(search_query)
    return render_template('results.html', jobs=jobs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

