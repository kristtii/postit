
from postit_app import app

from flask import render_template, redirect, session, request, flash

from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
from postit_app.models.job import Job

from .env import UPLOAD_FOLDER
from .env import UPLOAD_FOLDER_LOGOS
from .env import ALLOWED_EXTENSIONS
app.config['job_images'] = UPLOAD_FOLDER
app.config['job_images_logo'] = UPLOAD_FOLDER_LOGOS
from flask_cors import CORS
CORS(app)
import os
from werkzeug.utils import secure_filename
from datetime import datetime

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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


@app.route('/createjob', methods=['POST'])
def create_job():
    if 'hr_id' not in session:
        return redirect('/')

    images = request.files.getlist('job_post_image')
    image_filenames = []

    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename
            filename = time
            image.save(os.path.join(app.config['job_images'], filename))
            image_filenames.append(filename)

    # Get the company logo image and save it
    logos = request.files.getlist('company_logo')
    logo_filenames = []

    for logo in logos:
        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename
            filename = time
            logo.save(os.path.join(app.config['job_images_logo'], filename))
            logo_filenames.append(filename)

    # Construct the data dictionary for creating the job
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'salary': request.form['salary'],
        'responsibilities': request.form['responsibilities'],
        'education_experience': request.form['education_experience'],
        'benefits': request.form['benefits'],
        'employment_status': request.form.get('employment_status'),
        'experience': request.form['experience'],
        'deadline': request.form['deadline'],
        'job_post_image': ','.join(image_filenames),
        'company_logo': ','.join(logo_filenames),
        'hr_id': session['hr_id']
    }
    
    # Create the job using your Job class
    Job.create_job(data)

    return redirect('/dashboardHr')


@app.route('/job/<int:id>')
def viewjob(id):
    if 'hr_id' in session:
        data = {
            'hr_id': session.get('hr_id'),
            'job_id': id
        }
        loggedHr = Hr.get_hr_by_id(data)
        job = Job.get_job_by_id(data)
        jobcreator = Job.get_job_creator(data)
        return render_template('jobdisplay.html', job=job, loggedHr=loggedHr, jobcreator=jobcreator)

    elif 'employee_id' in session:
        data = {
            'employee_id': session.get('employee_id'),
            'job_id': id
        }
        loggedUser = Employee.get_employee_by_id(data)
        job = Job.get_job_by_id(data)
        jobcreator = Job.get_job_creator(data)
        return render_template('jobdisplay.html', job=job, loggedUser=loggedUser, jobcreator=jobcreator)

    else:
        return redirect('/')