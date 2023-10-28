from flask import Flask, render_template, request, session, redirect
from postit_app.models.employee import Employee
from postit_app.models.hr import Hr
from postit_app.models.job import Job

app = Flask(__name__)

app.secret_key = "t+hj86bjskx1udslvg@=g%9mor!pcd#*95c-es1m(46xk-q4$)"