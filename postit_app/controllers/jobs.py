
from postit_app import app

from flask import render_template, redirect, session, request, flash

from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
from postit_app.models.job import Job



@app.route('/jobs')
def jobs_index():
    return render_template('results.html')


@app.route('/postajob')
def postajob():
    if 'hr_id' not in session:
        return redirect('/')
    loggedHrData = {
        'hr_id': session['hr_id']
    }
    return render_template('postajob.html',loggedUser = Hr.get_hr_by_id(loggedHrData))


@app.route('/createjob', methods = ['POST'])
def createPost():
    if 'hr_id' not in session:
        return redirect('/')
    if not Job.validate_job(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'salary': request.form['salary'],
        'responsibilities': request.form['responsibilities'],
        'education_experience': request.form['education_experience'],
        'benefits': request.form['benefits'],
        'employement_status': request.form['employement_status'],
        'experience': request.form['experience'],
        'deadline': request.form['deadline'],
        'job_post_image': request.form['job_post_image'],
        'company_logo': request.form['company_logo'],
    }   
    Job.create_job(data)
    return redirect('/')


@app.route('/job/<int:id>')
def viewjob(id):
    # if 'hr_id'or 'employee_id' not in session:
    #     return redirect('/')
    data = {
        'hr_id': session['hr_id'],
        'employee_id': session['employee_id'],
        'tvshow_id': id
    }
    loggedHr = Hr.get_hr_by_id(data)
    loggedUser = Employee.get_employee_by_id(data)
    
    job = Job.get_job_by_id(data)
    jobcreator=Job.get_job_creator(data)
    return render_template('jobdisplay.html', job = job, loggedHr = loggedHr, jobcreator=jobcreator, loggedUser =loggedUser )
