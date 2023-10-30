from postit_app import app
from flask import render_template, redirect, session, request, flash
from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Employee Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loginPage')
def loginPage():
    if 'employee_id' in session:
        return redirect('/dashboard')
    return render_template('loginEmployee.html')

@app.route('/registerPage')
def registerPage():
    if 'employee_id' in session:
        return redirect('/dashboard')
    return render_template('registerEmployee.html')

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
        return redirect('/registerPage')
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'about': request.form['about'],
    }
    Employee.create_employee(data)
    flash('Employee successfully created', 'employeeRegister')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect('/loginPage')
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

