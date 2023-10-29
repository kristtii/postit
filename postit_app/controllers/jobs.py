from postit_app import app

from flask import render_template, redirect, session, request, flash

from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
# from postit_app.models.job import Jobs


@app.route('/jobs')
def index():
    return render_template('results.html')