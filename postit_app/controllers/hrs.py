from postit_app import app
from flask import render_template, redirect, session, request, flash
from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
from flask_bcrypt import Bcrypt

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
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'about': request.form['about'],
    }
    Hr.create_hr(data)
    flash('HR successfully created', 'hrRegister')
    return redirect('/dashboardHr')

@app.route('/dashboardHr')
def dashboardHr():
    if 'hr_id' not in session:
        return redirect('/loginPageHr')
    loggedHrData = {
        'hr_id': session['hr_id']
    } 
    loggedHr = Hr.get_hr_by_id(loggedHrData)
    if not loggedHr:
        return redirect('/logoutHr')
    return render_template('dashboardHr.html')

@app.route('/logoutHr')
def logoutHr():
    session.clear()
    return redirect('/')
