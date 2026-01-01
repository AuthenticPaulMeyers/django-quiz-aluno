# Aluno
Fullstack Quiz app - ALUNO - with Django

# Users
- Students
- Teachers
- Admin

# Database Design
## Entities
- User
- Student
- Teacher
- Class
- Subject
- Quiz
- Question
- Choice

# Entities Relationship Design

## Database type

- **Database system:** PostgreSQL

## ERD Diagram Sketch
![](/screenshots/IMG_20251021_182005_266.jpg)

## Relationships

- **teacher to user**: many_to_one
- **student to user**: many_to_one
- **student to class**: one_to_one
- **student_subject to student**: many_to_one
- **subject_class to class**: many_to_one
- **teacher to subject_teacher**: one_to_many
- **subject to subject_teacher**: one_to_many
- **subject_teacher to teacher_subject_class**: one_to_many
- **quiz to question**: one_to_many
- **teacher_subject_class to quiz**: one_to_many
- **subject to subject_class**: one_to_many
- **question to multiple_choice**: one_to_many
- **multiple_choice to attempt_answer**: one_to_many
- **question to attempt_answer**: one_to_many
- **attempt to attempt_answer**: one_to_many
- **student to attempt**: one_to_many
- **quiz to attempt**: one_to_many

## Tools used
- Python 3.14
- Django 6.0 (Updated)
- SQLite3 (Migrated to PostGreSQL using Supabase in production)
- HTML, Tailwind CSS, & JavaScript
- DrawDB.app (https://www.drawdb.app/) for ERD Design
`
## Security
1. Role based access
- Teachers, Students, and admin have different views to access the system according to their role.

2. Password Hashing
- All stored passwords are hashed using Django Authentication system.

3. Quiz expiration time and permission to take quiz
- Active quizzes have expiration time set by the teacher and students can not take expired quizzes if their due dates have passed. A timer is set on the duration of the quiz when the student is taking the active quiz, once the allowed time has elapsed, the platform warns the student that time has expired and submits the answers and grades the student. Students are allowed to take quiz only once.

# Students View
1. Landing Page
![Screenshot of the landing page](./screenshots/Screenshot%202025-11-02%20154607.png)

2. Login Page
![Screenshot of the login page](./screenshots/Screenshot%202025-11-02%20154622.png)

3. Student Dashboard Page
![Screenshot of the student dashboard page](./screenshots/Screenshot%202025-11-02%20145615.png)

4. All quizzes Page
![Screenshot of the all quizzes page](./screenshots/Screenshot%202025-11-02%20145634.png)

5. Student reports Page
![Screenshot of the reports page](./screenshots/Screenshot%202025-11-02%20145738.png)

6. Quiz details Page
![Screenshot of the quiz details page](./screenshots/Screenshot%202025-11-02%20145721.png)

7. Student profile Page
![Screenshot of the student profile page](./screenshots/Screenshot%202025-11-02%20145756.png)

7. Student change password Page
![Screenshot of the student profile page](./screenshots/Screenshot%202025-11-02%20145825.png)

# Teacher's view
1. Teacher dashboard Page
![Screenshot of the teacher dashboard page](./screenshots/Screenshot%202025-11-02%20145909.png)

2. Student reports Page
![Screenshot of the student reports page](./screenshots/Screenshot%202025-11-02%20145929.png)

3. Create quiz page
![Screenshot of the create quiz page](./screenshots/Screenshot%202025-11-02%20145950.png)
![Screenshot of the create quiz page](./screenshots/Screenshot%202025-11-02%20150003.png)

4. View Students Page
![Screenshot of the student page](./screenshots/Screenshot%202025-11-02%20150602.png)

5. Edit quiz Page
![Screenshot of the edit quiz page](./screenshots/Screenshot%202025-11-02%20150037.png)
![Screenshot of the edit quiz page](./screenshots/Screenshot%202025-11-02%20150049.png)

