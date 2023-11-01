from postit_app.config.mysqlconnection import connectToMySQL
from flask import flash  

class Job:
    db_name = 'postitdb'
    def __init__(self , data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.salary = data['salary']
        self.responsibilities = data['responsibilities']
        self.education_experience = data['education_experience']
        self.benefits = data['benefits']
        self.employment_status = data['employment_status']
        self.experience = data['experience']
        self.deadline = data['deadline']
        self.job_post_image = data['job_post_image']
        self.company_logo = data['company_logo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
        
    @classmethod
    def delete_job(cls, data):
        query = "DELETE FROM Jobs WHERE id = %(job_id)s;"
      
    @classmethod
    def count_jobs(cls):
        query = 'SELECT COUNT(*) FROM jobs;'
        results = connectToMySQL(cls.db_name).query_db(query)
        return results[0]['COUNT(*)']
    
    @classmethod
    def get_job_by_id(cls, data):
        query = 'SELECT * FROM jobs WHERE id= %(job_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    @classmethod
    def get_all_jobs(cls):
        query = 'SELECT * FROM jobs;'
        results = connectToMySQL(cls.db_name).query_db(query)
        jobs = []
        if results:
            for job in results:
                job = Job(job)
                jobs.append(job)
            return jobs
        return jobs
    
    @classmethod
    def search(cls, search_query):

        query = f"""
            SELECT * FROM jobs where jobs.title LIKE '{search_query}%'
        """

        try:
            results = connectToMySQL(cls.db_name).query_db(query)

            jobs = []
            if results:
                for job in results:
                    jobs.append(job)
            return jobs
        except Exception as e:
            print("An error occurred:", str(e))
            return []
    
    @classmethod
    def get_hr_jobs_by_id(cls, data):
        query = 'SELECT * FROM jobs WHERE hr_id= %(hr_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results 
    
    @classmethod
    def get_job_creator(cls, data):
        query="SELECT jobs.id AS job_id, jobs.hr_id, hrs.id AS hr_id, hrs.first_name as first_name, hrs.last_name as last_name, company,email FROM jobs LEFT JOIN hrs ON jobs.hr_id = hrs.id WHERE jobs.id= %(job_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def create_job(cls, data):
        query = "INSERT INTO jobs (title, description, salary, responsibilities, education_experience, benefits, employment_status, experience, deadline, job_post_image, company_logo, hr_id) VALUES ( %(title)s, %(description)s, %(salary)s, %(responsibilities)s, %(education_experience)s, %(benefits)s, %(employment_status)s, %(experience)s, %(deadline)s, %(job_post_image)s, %(company_logo)s , %(hr_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validateImage(data):
        is_valid = True
        if len(data) < 1:
            flash('Please select at least one image', 'job_post_image')
            is_valid = False 
        return is_valid
    
    @staticmethod
    def validateImageLogo(data):
        is_valid = True
        if len(data) < 1:
            flash('Please select at least one image', 'company_logo')
            is_valid = False 
        return is_valid
    
    @staticmethod
    def validate_job(hr):
        is_valid = True
        if len(hr['title'])< 3:
            flash('Title must be more than 2 characters', 'title')
            is_valid = False
        if len(hr['description'])< 3:
            flash('Description must be more than 2 characters', 'description')
            is_valid = False
        if  len(hr['salary'])< 3:
            flash('Salary must be more or equal to 8 characters', 'salary')
            is_valid = False
        if len(hr['responsibilities'])< 4:
            flash('Responsibilities must be more or equal to 4 characters', 'responsibilities')
            is_valid = False
        if len(hr['education_experience'])< 4:
            flash('Education and Experience must be more or equal to 4 characters', 'education_experience')
            is_valid = False
        if len(hr['benefits'])< 4:
            flash('Benefits must be more or equal to 4 characters', 'benefits')
            is_valid = False
        if not (hr['employement_status']):
            flash('Choose Employement status', 'employement_status')
            is_valid = False
        if len(hr['experience'])> 3:
            flash(' Enter a valid experience', 'experience')
            is_valid = False
        return is_valid
    