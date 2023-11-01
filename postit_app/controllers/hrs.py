from postit_app import app
from flask import render_template, redirect, session, request, flash
from postit_app.models.hr import Hr
from postit_app.models.job import Job
from flask_bcrypt import Bcrypt
import random
import math
import smtplib
from .env import ADMINEMAIL
from .env import PASSWORD

bcrypt = Bcrypt(app)

# HR Routes


@app.route('/loginPageHr')
def loginPageHr():
    if 'hr_id' in session:
        return redirect('/dashboardHr')
    return render_template('loginHr.html')

@app.route('/loginHr', methods=['POST'])
def loginHr():
    if 'hr_id' in session:
        return redirect('/dashboardHr')
    hr = Hr.get_hr_by_email(request.form)
    if not hr:
        flash('This email does not exist.', 'emailLogin')
        return redirect('/loginPageHr')
    if not bcrypt.check_password_hash(hr['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect('/loginPageHr')
    session['hr_id'] = hr['id']
    return redirect('/dashboardHr')

@app.route('/registerHr', methods=['POST'])
def registerHr():
    if 'hr_id' in session:
        return redirect('/dashboardHr')
    
    if Hr.get_hr_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect('/registerPageHr')
    
    if not Hr.validate_hr(request.form):
        return redirect('/registerPageHr')
    string = '0123456789'
    vCode = ""
    length = len(string)
    for i in range(8) :
        vCode += string[math.floor(random.random() * length)]
    verificationCode = vCode

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'company': request.form['company'],
        'email': request.form['email'],
        'about': request.form['about'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'verification_code': verificationCode,
    }
    Hr.create_hr(data)

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
    
    hr = Hr.get_hr_by_email(data)
    session['hr_id'] = hr['id']

    return redirect('/verify/email/hr')

@app.route('/verify/email/hr')
def verifyEmailHr():
    if 'hr_id' not in session:
        return redirect('/')
    data = {
        'hr_id': session['hr_id']
    }
    hr = Hr.get_hr_by_id(data)

    if hr['is_verified'] == 1:
        return redirect('/dashboard')
    return render_template('verifyHr.html', loggedHr = hr)


@app.route('/activate/account/hr', methods=['POST'])
def activateAccountHr():
    if 'hr_id' not in session:
        return redirect('/')
    data = {
        'hr_id': session['hr_id']
    }
    hr = Hr.get_hr_by_id(data)
    if hr['is_verified'] == 1:
        return redirect('/dashboard')
    
    if not request.form['verification_code']:
        flash('Verification Code is required', 'wrongCode')
        return redirect(request.referrer)
    
    if int(request.form['verification_code']) != int(hr['verification_code']):
        string = '0123456789'
        vCode = ""
        length = len(string)
        for i in range(8) :
            vCode += string[math.floor(random.random() * length)]
        verificationCode = vCode
        dataUpdate = {
            'verification_code': verificationCode,
            'hr_id': session['hr_id']
        }
        Hr.updateVerificationCode(dataUpdate)
        LOGIN = ADMINEMAIL
        TOADDRS  = hr['email']
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
    
    Hr.activateAccount(data)
    return redirect('/dashboardHr')


@app.route('/dashboardHr')
def dashboardHr():
    if 'hr_id' not in session:
        return redirect('/loginPageHr')
    
    if 'employee_id' in session:
        return redirect('/logout')
    loggedHrData = {
        'hr_id': session['hr_id']
    } 
    loggedHr = Hr.get_hr_by_id(loggedHrData)
    jobs=Job.get_hr_jobs_by_id(loggedHrData)
    if not loggedHr:
        return redirect('/logoutHr')
    return render_template('dashboardHr.html', jobs=jobs)

@app.route('/logoutHr')
def logoutHr():
    session.clear()
    return redirect('/')
