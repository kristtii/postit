from flask import render_template, redirect,session,request,flash
from postit_app import app

from postit_app.models.employee import Employee

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/employee')
def index():
    if 'employee_id' in session:
        return redirect('/dashboard')
    return redirect('/logout')

@app.route('/loginPage')
def loginPage():
    if 'employee_id' in session:
        return redirect('/')
    return render_template('loginEmployee.html')

@app.route('/registerPage')
def registerPage():
    if 'employee_id' in session:
        return redirect('/')
    return render_template('loginEmployee.html')

@app.route('/login', methods = ['POST'])
def login():
    if 'employee_id' in session:
        return redirect('/')
    employee = Employee.get_employee_by_email(request.form)
    if not employee:
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(employee['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    session['employee_id'] = employee['id']
    return redirect('/')
    
@app.route('/register', methods= ['POST'])
def register():
    if 'employee_id' in session:
        return redirect('/')
    
    if Employee.get_employee_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'confirmpassword': request.form['confirmpassword'],
        'about': request.form['about'],
    }
    Employee.create_employee(data)
    flash('Employee succefully created', 'employeeRegister')
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect('/')
    loggedEmployeeData = {
        'employee_id': session['employee_id']
    } 
    loggedEmployee = Employee.get_employee_by_id(loggedEmployeeData)
    if not loggedEmployee:
        return redirect('/logout')
    return render_template('dashboardEmployee.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')