from postit_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Hr:
    db_name = 'postitdb'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.company = data['company']
        self.email = data['email']
        self.about = data['about']
        self.is_verified = data['is_verified']
        self.verification_code = data['verification_code']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_hr_by_email(cls, data):
        query = 'SELECT * FROM hrs WHERE email= %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    @classmethod
    def get_hr_by_id(cls, data):
        query = 'SELECT * FROM hrs WHERE id= %(hr_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
        
    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE hrs SET verification_code = %(verification_code)s WHERE hrs.id = %(hr_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE hrs set is_verified = 1 WHERE hrs.id = %(hr_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    @classmethod
    def create_hr(cls, data):
        query = "INSERT INTO hrs (first_name, last_name, company, email, password, about, verification_code) VALUES ( %(first_name)s, %(last_name)s, %(company)s,%(email)s,%(password)s,%(about)s, %(verification_code)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_hr(cls, data):
        query = "UPDATE hrs SET first_name = %(first_name)s, last_name = %(last_name)s, company=%(company)s, email= %(email)s, about=,%(about)s WHERE id = %(hr_id)s ;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_hr(cls, data):
        query = "DELETE FROM hrs WHERE id = %(hr_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_hr(hr):
        is_valid = True
        if not EMAIL_REGEX.match(hr['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(hr['first_name'])< 2:
            flash('First name must be more than 2 characters', 'first_name')
            is_valid = False
        if len(hr['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'last_name')
            is_valid = False
        if len(hr['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if 'confirmpassword' in hr and hr['confirmpassword'] != hr['password']:
            flash('The passwords do not match',  'passwordConfirm')
            is_valid = False
        if len(hr['about'])< 8:
            flash('About must be more or equal to 8 characters', 'about')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_hr_update(hr):
        is_valid = True
        if not EMAIL_REGEX.match(hr['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(hr['first_name'])< 2:
            flash('First name must be more than 2 characters', 'first_name')
            is_valid = False
        if len(hr['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'last_name')
            is_valid = False
        if len(hr['about'])< 8:
            flash('About must be more or equal to 8 characters', 'about')
            is_valid = False
        return is_valid