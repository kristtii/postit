from postit_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Employee:
    db_name="postitdb"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.about = data['about']
        self.is_verified = data['is_verified']
        self.verification_code = data['verification_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_employee_by_email(cls, data):
        query = 'SELECT * FROM employees WHERE email= %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    @classmethod
    def get_employee_by_id(cls, data):
        query = 'SELECT * FROM employees WHERE id= %(employee_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def create_employee(cls, data):
        query = "INSERT INTO employees (first_name, last_name, email, about, password, verification_code) VALUES ( %(first_name)s, %(last_name)s,%(email)s,%(about)s,%(password)s, %(verification_code)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_employee(cls, data):
        query = "UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, email= %(email)s, about=,%(about)s WHERE id = %(employee_id)s ;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE employees SET verification_code = %(verification_code)s WHERE employees.id = %(employee_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE employees set is_verified = 1 WHERE employees.id = %(employee_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    @classmethod
    def delete_employee(cls, data):
        query = "DELETE FROM employees WHERE id = %(employee_id)s;"
        
    
    @staticmethod
    def validate_employee(employee):
        is_valid = True
        if not EMAIL_REGEX.match(employee['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(employee['first_name'])< 2:
            flash('First name must be more than 2 characters', 'first_name')
            is_valid = False
        if len(employee['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'last_name')
            is_valid = False
        if len(employee['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if 'confirmpassword' in employee and employee['confirmpassword'] != employee['password']:
            flash('The passwords do not match',  'passwordConfirm')
            is_valid = False
        if len(employee['about'])< 8:
            flash('About must be more or equal to 8 characters', 'about')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_employee_update(employee):
        is_valid = True
        if not EMAIL_REGEX.match(employee['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(employee['first_name'])< 2:
            flash('First name must be more than 2 characters', 'first_name')
            is_valid = False
        if len(employee['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'last_name')
            is_valid = False
        if len(employee['about'])< 8:
            flash('About must be more or equal to 8 characters', 'about')
            is_valid = False
        return is_valid