from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
os.environ['FLASK_ENV'] = 'development'


load_dotenv()

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Path to the SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
db = SQLAlchemy(app)

# User Profile Model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True)

# Job Application Model
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default='Applied')

# Course Progress Model
class CourseProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False)
    progress = db.Column(db.Float, default=0.0)  # Progress in percentage (0-100)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/add_sample_data')
def add_sample_data():
    sample_user = UserProfile(username='johndoe', email='john@example.com')
    sample_job = JobApplication(job_title='Software Engineer', company_name='Tech Corp')
    sample_course = CourseProgress(course_name='Python for Beginners', progress=50.0)

    db.session.add(sample_user)
    db.session.add(sample_job)
    db.session.add(sample_course)
    db.session.commit()

    return "Sample data added!"

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/users')
def get_users():
    users = UserProfile.query.all()  # Get all users
    return '<br>'.join([f"{user.username} - {user.email}" for user in users])

@app.route('/jobs')
def get_jobs():
    jobs = JobApplication.query.all()  # Get all job applications
    return '<br>'.join([f"{job.job_title} at {job.company_name}" for job in jobs])

@app.route('/courses')
def get_courses():
    courses = CourseProgress.query.all()  # Get all courses
    return '<br>'.join([f"{course.course_name} - {course.progress}%" for course in courses])
