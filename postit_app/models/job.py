from postit_app.config.mysqlconnection import connectToMySQL

class Jobs:
    db_name = 'postitdb'
    def __init__(self , data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.salary = data['salary']
        self.date = data['date']
        
        
    @classmethod
    def delete_job(cls, data):
        query = "DELETE FROM Jobs WHERE id = %(job_id)s;"
